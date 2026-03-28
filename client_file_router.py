import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shutil
import os

# greet user and prompt for destination directory
print('Welcome to Client File Router!\n')
print('Please select the client folder directory (select the current directory to use the dummy data for testing):')

def select_root_folder():
    """
    Get the selected root folder from the user

    Returns:
        root_path: the root folder that the user selected
    """
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
            short_folder_name = folder_name.split('/')[-1]
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
        downloads_folder = root_path + '/Downloads'
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

def get_downloaded_folders(root_path):
    """
    Get all client folder names from the Downloads folder

    Args:
        root_path (str): User selected path to the root directory 

    Returns:
        dwn_client_folders (dict): All client folders names in Downloads
    """
    dwn_client_folders = []
    try:
        # iterate through each subfolder in download folder
        downloads_folder = root_path + '/Downloads'
        for folder_names, subfolders, file_names in os.walk(downloads_folder):
            for subfolder in subfolders:
                dwn_client_folders.append(subfolder)

        # print folders in downloads
        print('Client folders in Downloads:')
        for client_folder in dwn_client_folders:
            print(client_folder)

        return dwn_client_folders
    except Exception as e:
        print(f'Failed to get downloaded client files: {e}')


# def route_clients(dwn_client_files,dwn_client_folders,dest_folders):
#     # check if client exists in directory for files
#     for dwn_client_name in dwn_client_files.keys():
#             for category in dest_folders.keys():
#                 dest_client_names = dest_folders.get(category,None)
#                 for dest_client_name in dest_client_names:
#                     for dest_client_name in dest_client_names:
#                         if dest_client_name == dest_client_name:
#                             # transfer client files if found

def main():
    root_path = select_root_folder()
    dest_folders = get_destination_folders(root_path)
    dwn_client_files = get_downloaded_files(root_path)
    dwn_client_folders = get_downloaded_folders(root_path)
    # route_clients(dwn_client_files,dwn_client_folders,dest_folders)

# run code if file was executed directly
if __name__ == "__main__":
    main()

    




