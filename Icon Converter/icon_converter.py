import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog

class IconConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Icon Converter")
        self.geometry("420x420")
        self.resizable(False, False)
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.frames = {}
        for F in (MainMenu, ConvertPNG, ConvertFolder):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainMenu)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Icon Converter", font=("Arial", 18))
        label.pack(pady=30)
        btn_png = ttk.Button(self, text="Convert PNG", width=20,
                             command=lambda: controller.show_frame(ConvertPNG))
        btn_png.pack(pady=10)
        btn_folder = ttk.Button(self, text="Convert Folder", width=20,
                                command=lambda: controller.show_frame(ConvertFolder))
        btn_folder.pack(pady=10)

class ConvertPNG(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_png = tk.StringVar(value="")
        self.save_location = tk.StringVar()
        # Default to Downloads folder
        self.save_location.set(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.selected_size = tk.IntVar(value=256)

        back_btn = ttk.Button(self, text="← Back", command=lambda: controller.show_frame(MainMenu))
        back_btn.place(x=10, y=10)

        label = ttk.Label(self, text="Convert PNG", font=("Arial", 14))
        label.pack(pady=(40, 15))

        # Choose PNG button
        choose_png_btn = ttk.Button(self, text="Choose PNG", command=self.choose_png)
        choose_png_btn.pack(pady=8)

        # Label for selected PNG path (hidden by default)
        self.png_path_label = ttk.Label(self, textvariable=self.selected_png, font=("Arial", 10), foreground="gray")
        self.png_path_label.pack(pady=4)
        self.png_path_label.pack_forget()

        # Image preview (hidden by default)
        self.image_preview_label = ttk.Label(self)
        self.image_preview_label.pack(pady=6)
        self.image_preview_label.pack_forget()
        self.preview_image = None  # To keep a reference

        # Size options
        size_frame = ttk.Frame(self)
        size_frame.pack(pady=15)
        sizes = [16, 32, 64, 128, 256]
        for s in sizes:
            rb = ttk.Radiobutton(size_frame, text=f"({s},{s})", variable=self.selected_size, value=s)
            rb.pack(side="left", padx=7)

        # Choose location to save button
        choose_loc_btn = ttk.Button(self, text="Choose location to save", command=self.choose_location)
        choose_loc_btn.pack(pady=12)

        # Label for save location
        self.location_label = ttk.Label(self, textvariable=self.save_location, font=("Arial", 10), foreground="gray")
        self.location_label.pack(pady=4)

        # Convert button at the bottom
        convert_btn = ttk.Button(self, text="Convert", command=self.convert_png_to_ico)
        convert_btn.pack(side="bottom", pady=25)

    def choose_png(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PNG files", "*.png")],
            title="Select a PNG file"
        )
        if file_path:
            self.selected_png.set(file_path)
            self.png_path_label.pack(pady=4)
            self.show_image_preview(file_path)
        else:
            self.selected_png.set("")
            self.png_path_label.pack_forget()
            self.image_preview_label.pack_forget()

    def show_image_preview(self, file_path):
        from PIL import Image, ImageTk
        try:
            img = Image.open(file_path)
            img.thumbnail((52,52))
            self.preview_image = ImageTk.PhotoImage(img)
            self.image_preview_label.configure(image=self.preview_image)
            self.image_preview_label.pack(pady=6)
        except Exception:
            self.image_preview_label.pack_forget()

    def choose_location(self):
        folder_selected = filedialog.askdirectory(title="Select folder to save")
        if folder_selected:
            self.save_location.set(folder_selected)

    def convert_png_to_ico(self):
        from PIL import Image
        import os
        from tkinter import messagebox
        image_path = self.selected_png.get()
        save_folder = self.save_location.get()
        size = self.selected_size.get()
        if not image_path:
            messagebox.showerror("Error", "Please select a PNG image.")
            return
        if not os.path.isfile(image_path):
            messagebox.showerror("Error", "Selected PNG file does not exist.")
            return
        if not os.path.isdir(save_folder):
            messagebox.showerror("Error", "Selected save location does not exist.")
            return
        # Save with the same base name as the PNG
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        save_path = os.path.join(save_folder, f"{base_name}.ico")
        try:
            img = Image.open(image_path)
            img.save(save_path, format='ICO', sizes=[(size, size)])
            messagebox.showinfo("Success", f"Icon saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert image:\n{e}")

class ConvertFolder(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        import os
        from tkinter import filedialog
        self.controller = controller
        self.selected_folder = tk.StringVar(value="")
        self.save_location = tk.StringVar(value="")
        self.selected_size = tk.IntVar(value=256)

        back_btn = ttk.Button(self, text="← Back", command=lambda: controller.show_frame(MainMenu))
        back_btn.place(x=10, y=10)

        label = ttk.Label(self, text="Convert Folder", font=("Arial", 14))
        label.pack(pady=(40, 15))

        # Choose folder button
        choose_folder_btn = ttk.Button(self, text="Choose Folder", command=self.choose_folder)
        choose_folder_btn.pack(pady=8)

        # Label for selected folder path (hidden by default)
        self.folder_path_label = ttk.Label(self, textvariable=self.selected_folder, font=("Arial", 10), foreground="gray")
        self.folder_path_label.pack(pady=4)
        self.folder_path_label.pack_forget()

        # Choose location button
        choose_loc_btn = ttk.Button(self, text="Choose location to save", command=self.choose_location)
        choose_loc_btn.pack(pady=8)

        # Label for save location (hidden by default)
        self.location_label = ttk.Label(self, textvariable=self.save_location, font=("Arial", 10), foreground="gray")
        self.location_label.pack(pady=4)
        self.location_label.pack_forget()

        # Size options
        size_frame = ttk.Frame(self)
        size_frame.pack(pady=15)
        sizes = [16, 32, 64, 128, 256]
        for s in sizes:
            rb = ttk.Radiobutton(size_frame, text=f"({s},{s})", variable=self.selected_size, value=s)
            rb.pack(side="left", padx=7)

        # Convert button at the bottom
        convert_btn = ttk.Button(self, text="Convert", command=self.convert_folder_to_ico)
        convert_btn.pack(side="bottom", pady=25)

    def choose_folder(self):
        import os
        from tkinter import filedialog
        folder_path = filedialog.askdirectory(title="Select folder containing PNGs")
        if folder_path:
            self.selected_folder.set(folder_path)
            self.folder_path_label.pack(pady=4)
            # Set default save location as Downloads\<folder_name>_icons
            downloads = os.path.join(os.path.expanduser("~"), "Downloads")
            folder_name = os.path.basename(folder_path)
            default_save = os.path.join(downloads, f"{folder_name}_icons")
            self.save_location.set(default_save)
            self.location_label.pack(pady=4)
        else:
            self.selected_folder.set("")
            self.folder_path_label.pack_forget()
            self.save_location.set("")
            self.location_label.pack_forget()

    def choose_location(self):
        from tkinter import filedialog
        folder_selected = filedialog.askdirectory(title="Select folder to save icons")
        if folder_selected:
            self.save_location.set(folder_selected)
            self.location_label.pack(pady=4)

    def convert_folder_to_ico(self):
        from PIL import Image
        import os
        from tkinter import messagebox
        folder_path = self.selected_folder.get()
        save_folder = self.save_location.get()
        size = self.selected_size.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder containing PNG images.")
            return
        if not save_folder or not os.path.isdir(os.path.dirname(save_folder)):
            messagebox.showerror("Error", "Please select a valid save location.")
            return
        # Create save folder if it doesn't exist
        if not os.path.exists(save_folder):
            try:
                os.makedirs(save_folder)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create save folder:\n{e}")
                return
        png_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.png')]
        if not png_files:
            messagebox.showerror("Error", "No PNG files found in the selected folder.")
            return
        errors = []
        converted_count = 0
        for png_file in png_files:
            png_path = os.path.join(folder_path, png_file)
            base_name = os.path.splitext(png_file)[0]
            save_path = os.path.join(save_folder, f"{base_name}.ico")
            try:
                img = Image.open(png_path)
                img.save(save_path, format='ICO', sizes=[(size, size)])
                converted_count += 1
            except Exception as e:
                errors.append(f"{png_file}: {e}")
        total = len(png_files)
        if errors:
            messagebox.showerror(
                "Done with Errors",
                f"Some files could not be converted:\n" + "\n".join(errors) + f"\n\nTotal images converted: {converted_count} out of {total}"
            )
        else:
            messagebox.showinfo(
                "Success",
                f"All PNGs converted to ICOs in:\n{save_folder}\nTotal images converted: {converted_count}"
            )

if __name__ == "__main__":
    app = IconConverterApp()
    app.mainloop()
