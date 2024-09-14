
import os
import tarfile
import shutil
from datetime import datetime

# 1. Define files and directories to back up
# This list includes both files and directories you wish to back up.
files_to_backup = [
    '/path/to/directory1',  # Example directory to back up
    '/path/to/directory2',  # Another directory to back up
    '/path/to/file1.txt'    # An individual file to back up
]

# 2. Define the backup location
# This is the directory where the backup archives will be stored.
backup_location = '/path/to/backup_location'

def create_backup(backup_items, backup_dir):
    """
    This function handles the creation of a backup by compressing the 
    specified files and directories into a timestamped .tar.gz archive.
    
    Parameters:
    backup_items: list of paths (files and directories) to be backed up
    backup_dir: the location where the backup will be stored
    
    """
    try:
        # 3. Generate a timestamped folder to store the backup
        # The datetime module is used to generate a unique timestamp for each backup.
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_folder = os.path.join(backup_dir, f'backup_{timestamp}')
        
        # Create the backup folder if it doesn't already exist
        os.makedirs(backup_folder, exist_ok=True)
        
        # 4. Define the name of the compressed archive (tar.gz)
        # The backup will be compressed into a .tar.gz archive file.
        backup_file = os.path.join(backup_folder, f'backup_{timestamp}.tar.gz')

        # 5. Create the .tar.gz archive and add files/directories to it
        # The 'w:gz' mode is used to create a compressed tar.gz archive.
        with tarfile.open(backup_file, 'w:gz') as tar:
            for item in backup_items:
                # Check if the file or directory exists before adding to the backup
                if os.path.exists(item):
                    # Add the file/directory to the tar archive, preserving its structure
                    tar.add(item, arcname=os.path.basename(item))
                else:
                    print(f'Warning: {item} does not exist and will be skipped.')
        
        print(f'Backup created successfully: {backup_file}')
    except PermissionError:
        # Handle permission errors, which may occur if the script does not have access to the file
        print("Error: Permission denied. Please check your file and directory permissions.")
    except OSError as e:
        # Catch and display any other OS-related errors (like missing directories or disk issues)
        print(f"Error: OS error occurred: {e}")
    except Exception as e:
        # Catch any other general errors to ensure robustness
        print(f"Error: An unexpected error occurred: {e}")

def main():
    """
    This is the main function that triggers the backup process. It checks the 
    backup location, ensures it exists, and then calls the create_backup function.
    """
    # 6. Check if the backup location exists and create it if necessary
    if not os.path.exists(backup_location):
        try:
            os.makedirs(backup_location)
        except PermissionError:
            print("Error: Could not create backup location due to permission issues.")
            return
        except Exception as e:
            print(f"Error: Could not create backup location: {e}")
            return
    
    # 7. Start the backup process
    create_backup(files_to_backup, backup_location)

if __name__ == "__main__":
    main()
