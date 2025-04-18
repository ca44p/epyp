import os
import subprocess
import sys
import shutil  # Import the shutil module

# --- PS2 Environment Configuration (Adjust these paths!) ---
# These should be the full paths to your tools.  Using shutil.which() is a robust way to find them.
PS2_GCC = shutil.which("ps2-gcc")
PS2_LD = shutil.which("ps2-ld")
PS2_OBJCOPY = shutil.which("ps2-objcopy")
PS2_EE_MAKER = shutil.which("ee-maker")
# --- End of PS2 Environment Configuration ---

def compile_elf(c_files_dir, output_elf_path):
    """Compiles C files in a directory into an ELF file for PS2."""
    try:
        c_files = [os.path.join(c_files_dir, f) for f in os.listdir(c_files_dir) if f.endswith('.c')]

        if not c_files:
            print("Error: No C files found in the selected directory.")
            return  # Important: Exit the function if no C files are found

        object_files = []
        for c_file in c_files:
            object_file = os.path.splitext(c_file)[0] + ".o"
            compile_command = [PS2_GCC, "-O2", "-G0", "-c", c_file, "-o", object_file]
            # Use subprocess.run with explicit error checking
            result = subprocess.run(compile_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Compiled {c_file} -> {object_file}") # Add some feedback
            object_files.append(object_file)

        link_command = [PS2_LD, "-Ttext=0x00100000", "-o", output_elf_path] + object_files
        # Use subprocess.run with explicit error checking
        result = subprocess.run(link_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Linked ELF: {output_elf_path}")
        for obj_file in object_files:
            os.remove(obj_file)  # Clean up object files

        print(f"ELF file created: {output_elf_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error: Compilation failed: {e}")
        print(f"Command: {e.cmd}")  # Print the command that failed
        print(f"Return Code: {e.returncode}")
        print(f"Output (stdout): {e.stdout.decode()}")  # Decode bytes to string
        print(f"Error (stderr): {e.stderr.decode()}")  # Decode bytes to string

    except FileNotFoundError as e:
        print(f"Error: Compiler or linker not found: {e}")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        print(f"Details: {e}")

def create_ee(elf_path, ee_path):
    """Converts the ELF file to an EE file."""
    try:
        # Use a more descriptive temporary file name
        temp_bin_path = os.path.splitext(elf_path)[0] + ".bin"
        objcopy_command = [PS2_OBJCOPY, "-O", "binary", elf_path, temp_bin_path]
        result = subprocess.run(objcopy_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Converted ELF to binary: {temp_bin_path}")

        ee_maker_command = [PS2_EE_MAKER, temp_bin_path, ee_path]
        result = subprocess.run(ee_maker_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Created EE file: {ee_path}")

        os.remove(temp_bin_path)  # Use the defined variable

        print(f"EE file created: {ee_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error: EE creation failed: {e}")
        print(f"Command: {e.cmd}")
        print(f"Return Code: {e.returncode}")
        print(f"Output (stdout): {e.stdout.decode()}")
        print(f"Error (stderr): {e.stderr.decode()}")
    except FileNotFoundError as e:
        print(f"Error: objcopy or ee-maker not found: {e}")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred during EE creation: {e}")
        print(f"Details: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: Drag and drop a folder onto this script.")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print("Error: Invalid folder path.")
        sys.exit(1)

    elf_output_path = os.path.join(folder_path, "output.elf")
    ee_output_path = os.path.join(folder_path, "output.ee")

    compile_elf(folder_path, elf_output_path)
    create_ee(elf_output_path, ee_output_path)
