import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pathlib import Path
import shutil

class DesignRenamerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Design File Renamer")
        
        # Setup directories using relative paths
        self.base_dir = Path("designs")
        self.incoming_dir = self.base_dir / "incoming"
        self.finished_dir = self.base_dir / "finished"
        
        # Ensure directories exist
        self.incoming_dir.mkdir(parents=True, exist_ok=True)
        self.finished_dir.mkdir(parents=True, exist_ok=True)
        
        # Categories and design types
        self.categories = {
            "WVB": "Women's Volleyball",
            "WBV": "Women's Beach Volleyball",
            "BVB": "Boys Volleyball",
            "GEN": "Generic"
        }
        
        self.design_types = {
            "LOGO": "Logo Design",
            "SLOGAN": "Text/Slogan",
            "MASCOT": "Mascot Design",
            "PLAYER": "Player/Action"
        }
        
        self.setup_ui()
        self.current_file = None
        self.files_to_process = []
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Waiting for files...")
        self.status_label.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Image preview
        self.preview_label = ttk.Label(main_frame)
        self.preview_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        # File info
        self.file_label = ttk.Label(main_frame, text="Current file: ")
        self.file_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # Category selection
        ttk.Label(main_frame, text="Category:").grid(row=3, column=0, pady=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(main_frame, textvariable=self.category_var)
        category_combo['values'] = list(self.categories.keys())
        category_combo.grid(row=3, column=1, pady=5)
        
        # Design type selection
        ttk.Label(main_frame, text="Design Type:").grid(row=4, column=0, pady=5)
        self.design_type_var = tk.StringVar()
        design_type_combo = ttk.Combobox(main_frame, textvariable=self.design_type_var)
        design_type_combo['values'] = list(self.design_types.keys())
        design_type_combo.grid(row=4, column=1, pady=5)
        
        # Description entry
        ttk.Label(main_frame, text="Description:").grid(row=5, column=0, pady=5)
        self.description_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.description_var).grid(row=5, column=1, pady=5)
        
        # Preview new name
        self.new_name_label = ttk.Label(main_frame, text="New filename: ")
        self.new_name_label.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Preview", command=self.preview_rename).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Rename & Move", command=self.rename_and_move_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Skip", command=self.next_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh Files", command=self.refresh_files).pack(side=tk.LEFT, padx=5)
        
    def refresh_files(self):
        """Refresh the list of files to process"""
        self.load_files()
        
    def load_files(self):
        """Load all PNG files from the incoming directory"""
        self.files_to_process = list(self.incoming_dir.glob("*.png"))
        if self.files_to_process:
            self.status_label.config(text=f"Found {len(self.files_to_process)} files to process")
            self.load_next_file()
        else:
            self.status_label.config(text="No files found in incoming directory")
            self.clear_preview()
            
    def clear_preview(self):
        """Clear the preview area"""
        self.preview_label.config(image="")
        self.file_label.config(text="Current file: None")
        self.category_var.set("")
        self.design_type_var.set("")
        self.description_var.set("")
        self.new_name_label.config(text="New filename: ")
            
    def load_next_file(self):
        """Load the next file for processing"""
        if self.files_to_process:
            self.current_file = self.files_to_process.pop(0)
            self.file_label.config(text=f"Current file: {self.current_file.name}")
            
            # Load and display image preview
            img = Image.open(self.current_file)
            # Resize image to fit display
            img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)
            self.preview_label.config(image=photo)
            self.preview_label.image = photo  # Keep a reference
            
            # Clear previous entries
            self.category_var.set("")
            self.design_type_var.set("")
            self.description_var.set("")
            self.new_name_label.config(text="New filename: ")
            
            self.status_label.config(text=f"{len(self.files_to_process)} files remaining")
        else:
            self.status_label.config(text="All files processed")
            self.clear_preview()
            
    def preview_rename(self):
        """Preview the new filename"""
        if not all([self.category_var.get(), self.design_type_var.get(), self.description_var.get()]):
            tk.messagebox.showwarning("Input Required", "Please fill in all fields")
            return
            
        new_name = f"{self.category_var.get()}_{self.design_type_var.get()}_{self.description_var.get()}.png"
        self.new_name_label.config(text=f"New filename: {new_name}")
        
    def rename_and_move_file(self):
        """Rename the current file and move it to the finished directory"""
        if not all([self.category_var.get(), self.design_type_var.get(), self.description_var.get()]):
            tk.messagebox.showwarning("Input Required", "Please fill in all fields")
            return
            
        new_name = f"{self.category_var.get()}_{self.design_type_var.get()}_{self.description_var.get()}.png"
        new_path = self.finished_dir / new_name
        
        try:
            # Check if file already exists in finished directory
            if new_path.exists():
                if not tk.messagebox.askyesno("File Exists", 
                    f"A file named {new_name} already exists in the finished directory. Overwrite?"):
                    return
            
            # Move and rename the file
            shutil.move(str(self.current_file), str(new_path))
            self.next_file()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error processing file: {str(e)}")
            
    def next_file(self):
        """Skip to the next file"""
        self.load_next_file()

def main():
    root = tk.Tk()
    app = DesignRenamerGUI(root)
    
    # Load initial files
    app.load_files()
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()