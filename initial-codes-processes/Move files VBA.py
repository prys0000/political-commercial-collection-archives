import os
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilenames

def move_files():
    Tk().withdraw()

    # Select the file names
    file_names = askopenfilenames(title="Please select the file names")

    if not file_names:
        return

    # Select the original folder
    original_folder = askdirectory(title="Please select the original folder")
    if not original_folder:
        return

    # Select the destination folder
    destination_folder = askdirectory(title="Please select the destination folder")
    if not destination_folder:
        return

    for file_name in file_names:
        file_path = os.path.join(original_folder, file_name)

        if os.path.isfile(file_path):
            new_file_path = os.path.join(destination_folder, file_name)

            # Move the file
            os.rename(file_path, new_file_path)

move_files()
