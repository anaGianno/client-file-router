from config import CATEGORY_FOLDERS
from pathlib import Path
from tools import duplicate_file_rename
import shutil
import os
import datetime

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
                    names = subfolder.split()
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
                parts = client_file.split(' ')
                if len(parts) < 2:
                    print(f"Skipping invalid filename: {client_file}")
                    continue
                # get client full name from filename
                dwn_client_name = parts[0] + ' ' + parts[1]
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
        return {}

def route_client(root_path,dwn_client_name,dwn_client_files,dest_folders):
    """
    Route downloaded client files for given client to its destination folder

    Args:
        root_path (str): User selected path to the root directory 
        dwn_client_name (str): given client name from route_all_clients function
        dwn_client_folders (dict): names of all clients in the downloads folder aswell as their file names
        dest_folders (dict): names of the category folders and the names of the client destination folders inside
    """
    # keep track of files moved
    file_record = [0,0]
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
                        try:
                            file_path = Path(root_path) / 'Downloads' / file
                            dest_path = Path(root_path) / category / client_folder_names
                            dest_path.mkdir(exist_ok=True)

                            dest_file = dest_path / file
                            dest_file = duplicate_file_rename(dest_file)

                            shutil.move(file_path, dest_file)
                            file_record[0] += 1

                        except Exception as move_error:
                            print(f"Failed to move {file}: {move_error}")
                            file_record[1] += 1
                    return file_record
        return file_record
    except Exception as e:
        print(f'Failed to get route client files for client {dwn_client_name}: {e}')
        return file_record

def route_all_clients(root_path,dwn_client_files,dest_folders):
    """
    Route downloaded client files for all clients to their destination folders

    Args:
        root_path (str): User selected path to the root directory 
        dwn_client_files (dict): names of all clients in the downloads folder aswell as their file names
        dest_folders (dict): names of the category folders and the names of the client destination folders inside
    """
    total_file_record = [0,0]
    # attempt to route each client's files in the downloaded files dictionary
    for dwn_client_name in dwn_client_files.keys():
        file_record = route_client(root_path,dwn_client_name,dwn_client_files,dest_folders)
        total_file_record[0] += file_record[0]
        total_file_record[1] += file_record[1]

    print(f"Total files moved: {total_file_record[0]}")
    print(f"Total files failed: {total_file_record[1]}")