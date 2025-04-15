import os
import subprocess
import sys
import shutil

# --- PS2 Environment Configuration (Adjust these paths!) ---
PS2_GCC = "ps2-gcc"
PS2_LD = "ps2-ld"
PS2_OBJCOPY = "ps2-objcopy"
PS2_EE_MAKER = "ee-maker"
# --- End of PS2 Environment Configuration ---

def compile_elf(c_files_dir, output_elf_path):
    """Compiles C files in a directory into an ELF file for PS2."""
    try:
        c_files = [os.path.join(c_files_dir, f) for f in os.listdir(c_files_dir) if f.endswith('.c')]

        if not c_files:
            print("Error: No C files found in the selected directory.")
            return

        object_files = []
        for c_file in c_files:
            object_file = os.path.splitext(c_file)[0] + ".o"
            compile_command = [PS2_GCC, "-O2", "-G0", "-c", c_file, "-o", object_file]
            subprocess.run(compile_command, check=True)
            object_files.append(object_file)

        link_command = [PS2_LD, "-Ttext=0x00100000", "-o", output_elf_path] + object_files
        subprocess.run(link_command, check=True)

        for obj_file in object_files:
            os.remove(obj_file)

        print(f"ELF file created: {output_elf_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error: Compilation failed: {e}")
    except FileNotFoundError as e:
        print(f"Error: Compiler or linker not found: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

def create_ee(elf_path, ee_path):
    """Converts the ELF file to an EE file."""
    try:
        objcopy_command = [PS2_OBJCOPY, "-O", "binary", elf_path, "temp.bin"]
        subprocess.run(objcopy_command, check=True)

        ee_maker_command = [PS2_EE_MAKER, "temp.bin", ee_path]
        subprocess.run(ee_maker_command, check=True)

        os.remove("temp.bin")

        print(f"EE file created: {ee_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error: EE creation failed: {e}")
    except FileNotFoundError as e:
        print(f"Error: objcopy or ee-maker not found: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred during EE creation: {e}")

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
