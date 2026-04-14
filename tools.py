from config import CATEGORY_FOLDERS
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shutil
import os
import datetime

def duplicate_file_rename(dest_file):
    """
    Changes the destination filename to avoid overrwritting duplicate files
    
    Returns:
        new_file_name: the new filename that increments in number 
        dest_file: the original filename if no duplicate was found
    """
    if os.path.exists(dest_file):
        # split filename 
        file_name, extension = os.path.splitext(dest_file)

        i = 1
        # check if other filename versions exists and increment for new filename
        while os.path.exists(f"{file_name}_{i}{extension}"):
            i += 1
        new_file_name = f"{file_name}_{i}{extension}"
        return new_file_name
    else:
        return dest_file

def select_root_folder():
    """ 
    Get the selected root folder from the user

    Returns:
        root_path: the root folder that the user selected
    """
    print('Please select the root folder containing downloads/category folders (current directory for testing):')
    print('Opening directory...')

    # get root directory
    try:
        # create folder GUI window                 
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root_path = filedialog.askdirectory(title = "Select a folder")
        print('Selected folder: ', root_path)

        return root_path
    except Exception as e:
        print(f'Failed to select a folder: {e}')

def reset_folders_testing():
    """
    Resets the downloaded client files back to the downloads folder from their destination (For testing)
    """
    print('Please select the client folder directory (select the current directory to use the dummy data for testing):')
    print('Opening directory...')

    # get root directory
    try:
        # create folder GUI window
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root_path = filedialog.askdirectory(title = "Select a folder")
        print('Selected folder: ', root_path)

        downloads_path = Path(root_path) / 'Downloads'
        for folder_name, subfolders, file_names in os.walk(root_path):
            # remove full path from current folder
            subfolder_category = Path(folder_name).name
            # only get client folders within the category folders
            if subfolder_category in CATEGORY_FOLDERS:
                # iterate through each client folder
                for dest_client_folder in subfolders:
                    dest_client_folder_path = Path(root_path) / Path(subfolder_category) / Path(dest_client_folder)
                    # iterate through each client destination folder
                    for folder_name_L2, subfolders_L2, dest_client_folder in os.walk(dest_client_folder_path):
                        for dest_client_file in dest_client_folder:
                            if dest_client_file.endswith('.gitkeep') or dest_client_file.endswith('.md') or dest_client_file.startswith('Wrong Person'):
                                continue
                            dest_client_file_path = Path(dest_client_folder_path) / Path(dest_client_file)
                            dwn_folder_path = downloads_path / Path(dest_client_file)
                            dwn_folder_path = duplicate_file_rename(dwn_folder_path)
                            shutil.move(dest_client_file_path,dwn_folder_path)
    except Exception as e:
        print(f'Failed to reset folders: {e}')
    
def move_folder():
    """
    Moves the first selected folder to the second selected folder
    """
    try:
        print("Select the folder you want to move!")
        print("Opening directory...\n")

        # create folder GUI window
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_to_move = filedialog.askdirectory(title = "Select the folder you want to move")

        print("Select the destination for the first folder")
        print("Opening directory...\n")
    
        dest_folder = filedialog.askdirectory(title = "Select the destination for the first folder")
        dest_folder = Path(dest_folder) / Path(folder_to_move).name
        dest_folder = duplicate_file_rename(dest_folder)
        shutil.move(folder_to_move,dest_folder)
    except Exception as e:
        print(f'Failed to move folders: {e}\n')

def separate_client_files():
    """
    Separates the chosen clients files from existing folder to new folder
    """
    try:
        print("\nSelect the client folder you want to separate files in!")
        print("Opening directory...\n")

        # create folder GUI window
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        separate_folder = filedialog.askdirectory(title = "Select the folder you want to separate")

        # check if chosen folder is inside the cateogry folders
        if separate_folder.split("/")[-2] not in CATEGORY_FOLDERS:
            print(f"Chosen folder is not inside the category folders: returning to main menu...\n")
        
            return
        
        # get names from chosen folder
        names = Path(separate_folder).name.split()
        client_names = []
        count = 0
        full_name = ''
        for name in names:
            if name == 'n':
                continue

            if count == 0:
                full_name += name
                count += 1
            elif count == 1:
                full_name += ' ' + name
                client_names.append(full_name)
                full_name = ''
                count = 0

        if len(client_names) == 1:
            print('Only one client in this folder: returning to main menu...')
            return

        # ask user which client they would like to separate
        for i in range (1,len(client_names) + 1):
            print(f'[{i}]: ' + client_names[i-1])
        remove_client = client_names[int(input(f'Choose the client [1-{len(client_names)}] you would like to separate from the folder: ')) - 1]

        # create new folder for separated client
        new_folder = Path(separate_folder).parent / remove_client
        new_folder = duplicate_file_rename(new_folder)
        new_folder.mkdir(exist_ok = True)       

        # go inside the chosen folder
        file_count = 0
        for folder_name, subfolders, file_names in os.walk(separate_folder):
            # find files with the client name
            for file_name in file_names:
                if file_name.startswith(remove_client):
                    # move that file to new folder
                    file_to_move = Path(separate_folder) / file_name
                    shutil.move(file_to_move,duplicate_file_rename(Path(new_folder) / file_name))
                    file_count += 1

        # rename the separate folder to remove the clients name
        client_names.remove(remove_client)
        new_file_name = ' n '.join(client_names)
        Path(separate_folder).rename(Path(separate_folder).parent / Path(new_file_name))

        print(f'Separated {file_count} file/s of {remove_client} from {separate_folder}\n')        
    except Exception as e:
        print(f'Failed to separate files: {e}\n')

def merge_download_files(dest_merge,dwn_folder):
    """
    Merge client files in Downloads to other client's folder
    """
    try:
        # get client name from user
        client_name = input('\nEnter the full name of the client you would like to merge (e.g Joe Bloggs): ')
        client_name_formatted = ''

        # redefine for format
        for name in client_name.split():
            client_name_formatted += name[0].upper() + name[1:].lower() + " "
        client_name_formatted = client_name_formatted[:-1]

        # get client files in downloads folder
        for folder_names, subfolders, client_files in os.walk(Path(dwn_folder)):
            for client_file in client_files:
                # get client full name from filename
                dwn_client_name = client_file.split(' ')[0] + ' ' + client_file.split(' ')[1]
                # merge file to other client's folder
                if client_file.startswith(client_name_formatted):
                    shutil.move(Path(dwn_folder) / client_file, duplicate_file_rename(Path(dest_merge) / client_file))

        # get names from chosen folder
        names = Path(dest_merge).name.split()
        client_names = []
        count = 0
        full_name = ''
        for name in names:
            if name == 'n':
                continue

            if count == 0:
                full_name += name
                count += 1
            elif count == 1:
                full_name += ' ' + name
                client_names.append(full_name)
                full_name = ''
                count = 0

        # check if client files were merged to their own folder
        if client_name_formatted not in client_names:
            # rename merged folder to include new client
            new_path = Path(dest_merge).parent / (Path(dest_merge).name + ' n ' + client_name_formatted)
            Path(dest_merge).rename(new_path)
        
    except Exception as e:
        print(f'Failed to merge files from Downloads folder: {e}\n')

def merge_two_folders(dest_merge,src_merge):
    """
    Merge two client folders together
    """
    try:
        # route files to merged folder
        for folder_names,subfolders,file_names in os.walk(src_merge):
            for file_name in file_names:
                shutil.move(Path(src_merge) / file_name, duplicate_file_rename(Path(dest_merge) / filename))
        
        # delete empty folder
        Path(src_merge).rmdir()

        # get names from chosen folder
        names = Path(src_merge).name.split()
        client_names = []
        count = 0
        full_name = ''
        for name in names:
            if name == 'n':
                continue

            if count == 0:
                full_name += name
                count += 1
            elif count == 1:
                full_name += ' ' + name
                client_names.append(full_name)
                full_name = ''
                count = 0

        for name in client_names:
            if name in dest_merge:
                client_names.remove(name)

        new_folder_name = ' n '.join(client_names)

        # rename merged folder to include new client/s
        new_path = Path(dest_merge).parent / (Path(dest_merge).name + ' n ' + new_folder_name)
        Path(dest_merge).rename(new_path)
    except Exception as e:
        print(f'Failed to merge two tolders together: {e}\n')

def merge_client_files():
    """
    Merge client files into one folder from existing client folders or downloaded client files
    """
    try:
        # get first merge source
        print('Select the source folder you want to merge from (Downloads folder or other existing client folder):')
        # create folder GUI window
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        src_merge = filedialog.askdirectory(title = "Select the folder to merge into")

        # get second merge source
        print('Select the client folder to merge into:\n')
        # create folder GUI window
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        dest_merge = filedialog.askdirectory(title = "Select the client folder to merge into")

        src_path = Path(src_merge)
        # route files on download folder
        if src_path.name == 'Downloads':
            merge_download_files(dest_merge,src_path)
        elif str(src_path.parent).split('/')[-1] in CATEGORY_FOLDERS:
            # route files on client folder
            merge_two_folders(dest_merge,src_path)
        else:
            print("User did not choose Downlaods folder or client folder: returning...")
            exit()
    except Exception as e:
        print(f'Failed to merge files: {e}\n')

def rename_folder():
    """
    Renames the chosen folder using user input
    """
    try:
        print('Select the source folder you want to rename:')
        # create folder GUI window
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        src_rename = filedialog.askdirectory(title = "Select the folder to merge into")

        new_name = input('Enter new folder name: ')

        Path(src_rename).rename(Path(src_rename).parent / new_name)
    except Exception as e:
        print(f'Failed to rename folder: {e}\n')