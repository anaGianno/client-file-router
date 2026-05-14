from routing import (
    get_destination_folders,
    get_downloaded_files,
    route_all_clients,
    create_client_folder,
)

from tools import (
    merge_client_files,
    separate_client_files,
    move_folder,
    rename_folder,
    reset_folders_testing,
    select_root_folder
)

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