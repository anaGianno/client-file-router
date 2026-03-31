import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shutil
import os
import time

CATEGORY_FOLDERS = ['New Purchase','Refinance','Refinance & New Purchase','Refinance & Restructure','Refinance & Top-up','Refix & Refinance','Refix & Restructure']

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

def get_destination_folders(root_path):
    """
    Get the root destination folder containing all the categories and existing client destination folders from the user

    Args:
        root_path (str): User selected path to the root directory 

    Returns:
        dest_folders (dict): All category folders names with the corresponding client names
    """
    # dictionary for client destination folders with category folder as key and client folders as values
    dest_folders = {}
    try:
        # read in all existing client destination folders in given directory
        for folder_name, subfolders, file_names in os.walk(root_path):
            # remove full path from current folder
            subfolder_category = Path(folder_name).name
            # only get client folders within the category folders
            if subfolder_category in CATEGORY_FOLDERS:
                for subfolder in subfolders:
                    names = subfolder.split(" ")
                    count = 0
                    dest_client_names = []
                    full_name = ''
                    # concatenate first and last name together and add to list
                    for name in names:
                        if name == 'n':
                            continue

                        if count == 0:
                            full_name += name
                            count += 1
                        elif count == 1:
                            full_name += ' ' + name
                            dest_client_names.append(full_name)
                            full_name = ''
                            count = 0
                            
                    if dest_folders.get(subfolder_category,None) == None:
                        dest_folders.setdefault(subfolder_category,[dest_client_names])    
                    else:
                        dest_folders.get(subfolder_category,None).append(dest_client_names)

        # print destination folders
        print('Existing client destination folders:')
        for dest_folder in dest_folders.keys():
            print(dest_folder + ':')
            dest_client_folders = dest_folders.get(dest_folder,None)
            for dest_client_names in dest_client_folders:
                all_names = ''
                for client_name in dest_client_names:
                    all_names += client_name + ' n '
                print(all_names[:-3])
            print()

        return dest_folders    
    except Exception as e:
        print(f'Failed to get destination folders: {e}')

def get_downloaded_files(root_path):
    """
    Get all downloaded client file names from the Downloads folder and categorized by client name

    Args:
        root_path (str): User selected path to the root directory 

    Returns:
        dwn_client_files (dict): All downloaded client file names categorized by client name
    """
    # dictionary for client data in downloads with client name as key and files as list stored in values
    dwn_client_files = {}
    try:
        # iterate through each file in download folder
        downloads_path = Path(root_path) / 'Downloads'
        for folder_names, subfolders, file_names in os.walk(downloads_path):
            for client_file in file_names:
                # get client full name from filename
                dwn_client_name = client_file.split(' ')[0] + ' ' + client_file.split(' ')[1]
                # group all files from current client
                if dwn_client_files.get(dwn_client_name,None) == None:
                    dwn_client_files.setdefault(dwn_client_name,[client_file])
                else:
                    dwn_client_files.get(dwn_client_name,None).append(client_file)

        # print downloaded files
        print('Downloaded client files:')
        for dwn_client_name in dwn_client_files.keys():
            print(dwn_client_name + ':')
            client_file_list = dwn_client_files.get(dwn_client_name,None)
            for client_file in client_file_list:
                print(client_file)
            print()

        return dwn_client_files
    except Exception as e:
        print(f'Failed to get downloaded client files: {e}')

def route_client(root_path,dwn_client_name,dwn_client_files,dest_folders):
    """
    Route downloaded client files for given client to its destination folder

    Args:
        root_path (str): User selected path to the root directory 
        dwn_client_name (str): given client name from route_all_clients function
        dwn_client_folders (dict): names of all clients in the downloads folder aswell as their file names
        dest_folders (dict): names of the category folders and the names of the client destination folders inside
    """
    try:
        # check all categories
        for category in dest_folders.keys():
            dest_client_folders = dest_folders.get(category,None)
            # check all client folders in each category
            for dest_client_folder in dest_client_folders:
                dest_path = Path('')
                client_folder_names = ' n '.join(dest_client_folder)

                # check if the client name exists in the folder name
                if dwn_client_name in dest_client_folder:
                    for file in dwn_client_files.get(dwn_client_name,None):
                            file_path = Path(root_path) / 'Downloads' / file
                            dest_path = Path(root_path) / category / client_folder_names 
                            dest_path.mkdir(exist_ok=True)
                            dst_file = dest_path / file
                            shutil.move(file_path,dst_file)
                    return
        return
    except Exception as e:
        print(f'Failed to get route client files for client {dwn_client_name}: {e}')

def route_all_clients(root_path,dwn_client_files,dest_folders):
    """
    Route downloaded client files for all clients to their destination folders

    Args:
        root_path (str): User selected path to the root directory 
        dwn_client_files (dict): names of all clients in the downloads folder aswell as their file names
        dest_folders (dict): names of the category folders and the names of the client destination folders inside
    """
    # attempt to route each client's files in the downloaded files dictionary
    for dwn_client_name in dwn_client_files.keys():
        route_client(root_path,dwn_client_name,dwn_client_files,dest_folders)

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
                            shutil.move(dest_client_file_path,downloads_path)
    except Exception as e:
        print(f'Failed to reset folders: {e}')

def create_client_folder():
    """
    Creates a new client folder for an unrecognized client's files in chosen category and routes files to it
    """
    try:
        # get client name from user
        client_name = input('\nEnter the full name of the client you would like to create a new folder for (e.g John Public): ')
        client_name_formatted = ''

        # redefine for format
        for name in client_name.split(" "):
            client_name_formatted += name[0].upper() + name[1:].lower() + " "
        client_name_formatted = client_name_formatted[:-1]

        # get root folder from user
        root_path = select_root_folder()

        # get category from user 
        print('CATEGORY FOLDERS:')
        while True:
            for category in CATEGORY_FOLDERS:
                print(f'[{category}]')
            chosen_category = input('\nPlease enter a category folder location for the new folder (e.g Refinance) or (x) to exit: ')

            if chosen_category == 'x':
                exit()

            chosen_category_formatted = ''
            for word in chosen_category.split(" "):
                chosen_category_formatted += word[0].upper() + word[1:].lower() + " "
            chosen_category_formatted = chosen_category_formatted[:-1]

            if chosen_category_formatted in CATEGORY_FOLDERS:
                break
            else:
                print(f'{chosen_category} is an invalid category')

        dwn_client_files = {}
        # get client files in downloads folder
        downloads_path = Path(root_path) / 'Downloads'
        for folder_names, subfolders, client_files in os.walk(downloads_path):
            for client_file in client_files:
                # get client full name from filename
                dwn_client_name = client_file.split(' ')[0] + ' ' + client_file.split(' ')[1]
                # group all files from current client
                if dwn_client_name.upper() == client_name.upper():
                    if dwn_client_files.get(dwn_client_name,None) == None:
                        dwn_client_files.setdefault(client_name_formatted,[client_file])
                    else:
                        dwn_client_files.get(client_name_formatted,None).append(client_file)

        # exit if no files found in Downloads folder
        if dwn_client_files.get(client_name_formatted,None) == None:
            print(f"Client name '{client_name}' not found in downloads folder: returning to main menu...\n")
            return

        # create new client folder in category folder
        new_folder_path = Path(root_path) / chosen_category_formatted / client_name_formatted
        new_folder_path.mkdir(exist_ok = True)

        # move client files to new folder
        dest_folders = {}
        dest_folders.setdefault(chosen_category_formatted,[[client_name_formatted]])
        route_client(root_path,client_name_formatted,dwn_client_files,dest_folders)
        print('Created new folder!\n')
    except Exception as e:
        print(f'Failed to create client folder: {e}\n')
    
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
    
        destination_folder = filedialog.askdirectory(title = "Select the destination for the first folder")
        shutil.move(folder_to_move,destination_folder)
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
        names = Path(separate_folder).name.split(" ")
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
        new_folder.mkdir(exist_ok = True)       

        # go inside the chosen folder
        file_count = 0
        for folder_name, subfolders, file_names in os.walk(separate_folder):
            # find files with the client name
            for file_name in file_names:
                if file_name.startswith(remove_client):
                    # move that file to new folder
                    file_to_move = Path(separate_folder) / file_name
                    shutil.move(file_to_move,new_folder)
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
        for name in client_name.split(" "):
            client_name_formatted += name[0].upper() + name[1:].lower() + " "
        client_name_formatted = client_name_formatted[:-1]

        # get client files in downloads folder
        for folder_names, subfolders, client_files in os.walk(Path(dwn_folder)):
            for client_file in client_files:
                # get client full name from filename
                dwn_client_name = client_file.split(' ')[0] + ' ' + client_file.split(' ')[1]
                # merge file to other client's folder
                if client_file.startswith(client_name_formatted):
                    shutil.move(Path(dwn_folder) / client_file, Path(dest_merge))

        # get names from chosen folder
        names = Path(dest_merge).name.split(" ")
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
                shutil.move(Path(src_merge) / file_name, dest_merge)
        
        # delete empty folder
        Path(src_merge).rmdir()

        # get names from chosen folder
        names = Path(src_merge).name.split(" ")
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
    print('Select the source folder you want to rename:')
    # create folder GUI window
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    src_rename = filedialog.askdirectory(title = "Select the folder to merge into")

    new_name = input('Enter new folder name: ')

    Path(src_rename).rename(Path(src_rename).parent / new_name)



def main():
    # greet user and prompt for destination directory
    print('Welcome to Client File Router!\n')
    while True:
        print('[1]: Route downloaded client files')
        print('[2]: Create new client folder and transfer files')
        print('[3]: Merge client files into one folder')
        print('[4]: Separate client files to new folder')
        print('[5]: Move existing client folder')
        print('[6]: Rename existing client folder')
        print('[7]: Reset client files to Downloads folder (FOR TESTING)')
        print('[x]: Exit')
        user_input = input('Please enter a number (1-7) or (x) to exit: ')

        if user_input == "1":
            root_path = select_root_folder()
            dest_folders = get_destination_folders(root_path)
            dwn_client_files = get_downloaded_files(root_path)
            route_all_clients(root_path,dwn_client_files,dest_folders)
        elif user_input == "2":
            create_client_folder()
        elif user_input == "3":
            merge_client_files()
        elif user_input == "4":
            separate_client_files()
        elif user_input == "5":
            move_folder()
        elif user_input == "6":
            rename_folder()
        elif user_input == "7":
            reset_folders_testing()
        elif user_input == "x":
            exit()
        
# run code if file was executed directly
if __name__ == "__main__":
    main()