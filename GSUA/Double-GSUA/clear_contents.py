import os
import shutil
import tkinter as tk
from tkinter import messagebox
import naming_function

inputs = naming_function.mec_input_names()
outputs = naming_function.mec_output_names()
models = naming_function.model_names()
gen_path, indiv_path, structure_path = naming_function.path_names()


def erase_files_in_folder(folder_path):
    try:
        if not os.path.exists(folder_path):
            messagebox.showinfo("Folder Not Found", f"The folder '{folder_path}' does not exist.")
            return
        
        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to erase all files within '{folder_path}'?")
        
        if confirmation:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

            messagebox.showinfo("Deletion Complete", f"All files within '{folder_path}' have been erased.")
        else:
            messagebox.showinfo("Deletion Cancelled", "Deletion process cancelled.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def confirm_and_erase(folder_path):
    erase_files_in_folder(folder_path)
