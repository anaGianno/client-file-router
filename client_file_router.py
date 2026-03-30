import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shutil
import os

CATEGORY_FOLDERS = ['New Purchase','Refinance','Refinance & New Purchase','Refinance & Restructure','Refinance & Top-up','Refix & Refinance','Refix & Restructure']

def select_root_folder():
    """
    Get the selected root folder from the user

    Returns:
        root_path: the root folder that the user selected
    """
    print('Please select the root folder; containing the category folders and download folder (select the current directory to use the dummy data for testing):')
    # get root directory
    try:
        # create folder GUI window
        root = tk.Tk()
        root.withdraw()
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
        dwn_client_files (dict): names of all clients in the downloads folder aswell as their file names
        dest_folders (dict): names of the category folders and the names of the client destination folders inside
    """
    try:
        # check all categories
        for category in dest_folders.keys():
            dest_client_folders = dest_folders.get(category,None)
            # check all client folders in each category
            for dest_client_folder in dest_client_folders:
                dest_path = Path('')
                if len(dest_client_folders) > 1:
                    client_folder_names = ' n '.join(dest_client_folder)
                else:
                    client_folder_names = dest_client_folder

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
    # get root directory
    try:
        # create folder GUI window
        root = tk.Tk()
        root.withdraw()
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
    # get client name from user
    client_name = input('\nEnter client name the full name of the client you would like to create a new folder for (e.g John Public): ')
    client_name_formatted = ''

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
    dest_folders.setdefault(chosen_category_formatted,[client_name_formatted])
    route_client(root_path,client_name_formatted,dwn_client_files,dest_folders)
    print('Created new folder!\n')


# fix casing for client names
    

def main():
    # greet user and prompt for destination directory
    print('Welcome to Client File Router!\n')
    while True:
        print('[1]: Route downloaded client files')
        print('[2]: Create new client folder and transfer files')
        print('[3]: Reset client files to Downloads folder (FOR TESTING)')
        print('[x]: Exit')
        user_input = input('Please enter a number (1-3) or (x) to exit: ')

        if user_input == "1":
            root_path = select_root_folder()
            dest_folders = get_destination_folders(root_path)
            dwn_client_files = get_downloaded_files(root_path)
            route_all_clients(root_path,dwn_client_files,dest_folders)
        elif user_input == "2":
            create_client_folder()
        elif user_input == "3":
            reset_folders_testing()
        elif user_input == "x":
            exit()
        
# run code if file was executed directly
if __name__ == "__main__":
    main()