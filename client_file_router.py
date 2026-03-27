import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shutil
import os

# greet user and prompt for destination directory
print('Welcome to Client File Router!\n')
print('Please select the client folder directory (select the current directory to use the dummy data for testing):')

# get root directory
try:
    # create folder GUI window
    root = tk.Tk()
    root.withdraw()

    root_path = filedialog.askdirectory(title = "Select a folder")
    print('Selected folder: ', root_path)
except Exception as e:
    print(f'Failed to select a folder: {e}')

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
                if dest_folders.get(short_folder_name,None) == None:
                    dest_folders.setdefault(short_folder_name,[subfolder])    
                else:
                    dest_folders.get(short_folder_name,None).append(subfolder)

        # print destination folders
        print('Existing client destination folders:')
        for dest_folder in dest_folders.keys():
            print(dest_folder + ':')
            dest_client_folders = dest_folders.get(dest_folder,None)
            for dest_client_folder in dest_client_folders:
                print(dest_client_folder)
            print()
except Exception as e:
    print(f'Failed to get destination folders: {e}')

# dictionary for client data in downloads with client name as key and files as list stored in values
client_files = {}
client_folders = []
try:
    # iterate through each file/subfolder in download folder
    downloads_folder = root_path + '/Downloads'
    for folder_names, subfolders, file_names in os.walk(downloads_folder):
        for subfolder in subfolders:
            client_folders.append(subfolder)

        for file_name in file_names:
            # get client full name from filename
            client_name = file_name.split(' ')[0] + ' ' + file_name.split(' ')[1]
            # group all files from current client
            if client_files.get(client_name,None) == None:
                client_files.setdefault(client_name,[file_name])
            else:
                client_files.get(client_name,None).append(file_name)

    # print destination folders
    print('Downloaded client files:')
    for client_name in client_files.keys():
        print(client_name + ':')
        client_file_list = client_files.get(client_name,None)
        for client_file in client_file_list:
            print(client_file)
        print()

    print('Client folders in Downloads:')
    for client_folder in client_folders:
        print(client_folder)
except Exception as e:
    print(f'Failed to get downloaded client files/folders: {e}')

# check if client exists in directory 
# for dest_folder 

# transfer client files if found

