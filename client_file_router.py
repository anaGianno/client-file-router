import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shutil
import os

def select_root_folder():
    """
    Get the selected root folder from the user

    Returns:
        root_path: the root folder that the user selected
    """
    print('Please select the client folder directory (select the current directory to use the dummy data for testing):')
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
    category_folders = ['New Purchase','Refinance','Refinance & NewPurchase','Refinance & Restructure','Refinance & Top-up','Refix & Refinance','Refix & Restructure']
    try:
        # read in all existing client destination folders in given directory
        for folder_name, subfolders, file_names in os.walk(root_path):
            # remove full path from current folder
            short_folder_name = Path(folder_name).name
            # only get client folders within the category folders
            if short_folder_name in category_folders:
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
                            
                    if dest_folders.get(short_folder_name,None) == None:
                        dest_folders.setdefault(short_folder_name,[dest_client_names])    
                    else:
                        dest_folders.get(short_folder_name,None).append(dest_client_names)

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
        downloads_folder = Path(root_path) / 'Downloads'
        for folder_names, subfolders, file_names in os.walk(downloads_folder):
            for file_name in file_names:
                # get client full name from filename
                dwn_client_name = file_name.split(' ')[0] + ' ' + file_name.split(' ')[1]
                # group all files from current client
                if dwn_client_files.get(dwn_client_name,None) == None:
                    dwn_client_files.setdefault(dwn_client_name,[file_name])
                else:
                    dwn_client_files.get(dwn_client_name,None).append(file_name)

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
    category_folders = ['New Purchase','Refinance','Refinance & NewPurchase','Refinance & Restructure','Refinance & Top-up','Refix & Refinance','Refix & Restructure']
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
            short_folder_name = Path(folder_name).name
            # only get client folders within the category folders
            if short_folder_name in category_folders:
                # iterate through each category
                for subfolder in subfolders:
                    dest_client_folder_path = Path(root_path) / Path(short_folder_name) / Path(subfolder)
                    # iterate through each client destination folder
                    for folder_name_L2, subfolders_L2, file_names_L2 in os.walk(dest_client_folder_path):
                        # for subfolder_L2 in subfolders_L2:
                        #     dest_client_folder_path = Path(dest_client_folder_path) / Path(subfolder_L2)
                        # transfer each client file back to the downloads folder
                        for file_name_L2 in file_names_L2:
                            if file_name_L2.endswith('.gitkeep') or file_name_L2.endswith('.md') or file_name_L2.startswith('Wrong Person'):
                                continue
                            dest_client_file_path = Path(dest_client_folder_path) / Path(file_name_L2)
                            shutil.move(dest_client_file_path,downloads_path)
                            
    except Exception as e:
        print(f'Failed to reset folders: {e}')


def main():
    # greet user and prompt for destination directory
    print('Welcome to Client File Router!\n')
    print('What would you like to do?')
    while True:
        user_input = input('Enter [1] to select your client folder directory, Enter [2] to reset the client files back the the downloads folder after routing (TESTING ONLY), Enter [3] to exit: ')

        if user_input == "1":
            root_path = select_root_folder()
            dest_folders = get_destination_folders(root_path)
            dwn_client_files = get_downloaded_files(root_path)
            route_all_clients(root_path,dwn_client_files,dest_folders)
        elif user_input == "2":
            reset_folders_testing()
        elif user_input == "3":
            exit()
        
# run code if file was executed directly
if __name__ == "__main__":
    main()

    




