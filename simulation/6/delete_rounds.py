import os
import shutil

def delete_round_folders(start_path, ask_confirmation=True):
    """
    Recursively searches for and deletes all subdirectories starting with 'round_' within the specified directory,
    with an option to ask for user confirmation before deletion.

    Parameters:
    - start_path (str): The path of the directory from which the search and deletion process starts.
    - ask_confirmation (bool): If True, the function will prompt the user for confirmation before deleting any directories.
    
    Description:
    The function walks through the directory tree starting from 'start_path'. It collects all directories that start with 'round_'.
    If ask_confirmation is True, it then lists all found directories and asks the user to confirm the deletion. Upon confirmation,
    it deletes the directories. The traversal is done in a bottom-up manner.

    Warnings:
    - The function performs deletions without any confirmation if ask_confirmation is set to False. Use with caution.
    - Ensure that the script has appropriate permissions to delete the directories, or it may raise a PermissionError.
    
    Example Usage:
    ```
    current_directory = os.getcwd()
    delete_round_folders(current_directory)
    ```

    Output:
    - The function prints the path of each directory marked for deletion and, based on user input, may delete them.
    """
    # Collect all directories to be deleted
    dirs_to_delete = []
    for root, dirs, files in os.walk(start_path, topdown=False):
        for dir_name in dirs:
            if dir_name.startswith('round_'):
                full_dir_path = os.path.join(root, dir_name)
                dirs_to_delete.append(full_dir_path)
    
    if not dirs_to_delete:
        print("No directories found matching the criteria.")
        return
    
    # Ask for confirmation if required
    if ask_confirmation:
        print("The following directories will be deleted:")
        for dir_path in dirs_to_delete:
            print(dir_path)
        confirmation = input("Do you want to proceed with the deletion? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Deletion cancelled by user.")
            return

    # Delete directories
    for dir_path in dirs_to_delete:
        shutil.rmtree(dir_path)
        print(f"Deleted folder: {dir_path}")

if __name__ == "__main__":
    # Get the current directory where the script is running
    current_directory = os.getcwd()
    # Call the function with the current directory
    delete_round_folders(current_directory)
