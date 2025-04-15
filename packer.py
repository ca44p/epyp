import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile #Import the zipfile library

# ... (rest of your PS2 environment configuration) ...

def process_directory_or_zip(input_path, output_elf_path, output_ee_path):
    """Handles both directories and zip files."""
    if input_path.lower().endswith(".zip"):
        # Handle zip file
        try:
            with zipfile.ZipFile(input_path, 'r') as zip_ref:
                temp_dir = "temp_extracted" # temp directory for extraction
                os.makedirs(temp_dir, exist_ok=True)
                zip_ref.extractall(temp_dir)
                compile_elf(temp_dir, output_elf_path)
                create_ee(output_elf_path, output_ee_path)
                #cleanup
                for filename in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))

                os.rmdir(temp_dir) #remove empty directory
        except zipfile.BadZipFile:
            messagebox.showerror("Error", "Invalid zip file.")
            return

    else:
        # Handle directory
        compile_elf(input_path, output_elf_path)
        create_ee(output_elf_path, output_ee_path)

# ... (rest of your GUI functions) ...

def select_input_path():
    """Allows selecting a directory or a zip file."""
    input_path = filedialog.askopenfilename(filetypes=[("C Source (Directory or Zip)", "*"), ("ZIP files", "*.zip")])
    if input_path:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, input_path)

# ... (rest of your GUI setup) ...

#Modify the compile button:
def compile_and_create_ee():
    input_path = directory_entry.get()
    elf_output_path = elf_output_entry.get()
    ee_output_path = ee_output_entry.get()

    if not input_path or not elf_output_path or not ee_output_path:
        messagebox.showerror("Error", "Please select all required paths.")
        return

    process_directory_or_zip(input_path, elf_output_path, ee_output_path)

#Modify GUI setup:
directory_button = tk.Button(root, text="Browse", command=select_input_path) #change browse to select input path.
