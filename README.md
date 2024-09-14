# Configuration-Management-and-automation-2-tasks---Tier-3-Ansible-and-Python

# Ansible =============

### Task: Ansible Playbook for Web Server Environment Setup

#### Description:
Write an Ansible playbook to automate the setup of a web server environment using Nginx and PHP on multiple CentOS servers. The playbook should install and configure Nginx as the web server and PHP for dynamic content processing. Additionally, configure a basic PHP info page for testing purposes. Test the playbook on a test environment to verify its functionality.

# Python ==============

# Task: Python Script for Automated File Backup

Here is the Python script with detailed explanations for each step to ensure it meets all the criteria for automating backups on a CentOS server. I will go over each section of the script, explaining how it handles the various requirements like recursive directory traversal, error handling, and the creation of compressed .tar.gz archives.

# Python Script for Automated File Backup with Detailed Explanations

Make the directories for the data and for backup 

<img width="384" alt="s2" src="https://github.com/user-attachments/assets/f3374ebd-6c8d-4f72-b237-3242f9aec8d0">

Detailed Step-by-Step Explanation

# Step 1: Define Files and Directories to Back Up
In the files_to_backup list, we specify both files and directories that need to be backed up. This can include paths to any files and folders. For example: Pic is shown after step 2

This will enable the script to traverse directories recursively and back up all files within those directories.

# Step 2: Define the Backup Location

The backup_location variable defines where the backup will be stored. It is a directory where the script will create timestamped subdirectories for each backup. You can set this path based on your CentOS server’s directory structure:

<img width="450" alt="211" src="https://github.com/user-attachments/assets/90be2ae6-dc54-4ba2-a2c9-07f04eaa430b">

# Step 3: Generate a Timestamped Folder for Backups
The script uses the datetime module to generate a unique timestamp for each backup:


<img width="447" alt="124" src="https://github.com/user-attachments/assets/022a99a0-5b46-4e42-b9da-31d966601966">

This ensures that each backup is stored in its own folder, and no backups overwrite previous ones.

# Step 4: Create a .tar.gz Archive
To compress files and directories, the script uses the tarfile module. It creates a .tar.gz archive with the following:

with tarfile.open(backup_file, 'w:gz') as tar:
    tar.add(item, arcname=os.path.basename(item))
This creates a tar archive and adds each file or directory to it while preserving the original directory structure. The compression saves space on the backup disk.

Step 5: Error Handling for Robustness
The script includes several error handling mechanisms:

PermissionError: This handles issues where the script doesn’t have permission to access certain files or directories.
OSError: This captures operating system-level errors such as missing directories, disk space issues, etc.

General Exceptions: Any other unforeseen errors are caught and reported.
For example:

<img width="451" alt="512" src="https://github.com/user-attachments/assets/ba583289-7f93-49cd-ac7e-febe3bde4eaa">

This ensures the script can gracefully handle any errors and continue functioning, either by skipping problematic files or alerting the user to fix the issue.

# Step 6: Check and Create Backup Location
Before creating the backup, the script checks if the specified backup_location exists. If it doesn’t, the script tries to create it:

if not os.path.exists(backup_location):
    os.makedirs(backup_location)

    If this operation fails due to permissions or other reasons, an error is reported, and the backup process stops.

# Step 7: Main Function to Trigger Backup
The main() function orchestrates the backup by first checking the backup location and then calling the create_backup() function to perform the actual backup.

# Additional Considerations

Recursive Traversal: The tar.add() method is inherently recursive when adding directories, so all files within the specified directories will be included.

Testing: Before deployment, ensure the script has access to all the files, directories, and the backup location. Run tests on your CentOS server using the command:

<img width="397" alt="122" src="https://github.com/user-attachments/assets/77f37d99-4501-4e18-aff6-2a0bf376a570">

How to Automate the Backup (Optional)
To automate this backup script, you can set up a cron job on your CentOS server. For example:

Open the cron table for the root user

sudo crontab -e
Add the following line to schedule the script to run daily at 2 AM:
0 2 * * * /usr/bin/python3 /path/to/backup_script.py

This cron job will run the script daily, ensuring your backups are performed automatically.

Let me know if you'd like further customization or clarification!clear

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






