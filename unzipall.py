import os
import zipfile

# Specify the directory path you want to list files from
folder_paths = ['/media/monlamai/Monlam SSD/Tsepak-2023-100', '/media/monlamai/Monlam SSD/BDRC etexts']

id = 0
catalog = []
for folder_path in folder_paths:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.zip'):
                # Full path of the zip file
                zip_path = os.path.join(root, file)

                # Directory to extract to (same name as the zip file without the extension)
                extract_path = os.path.join(root, os.path.splitext(file)[0])

                # Create the directory if it does not exist
                if not os.path.exists(extract_path):
                    os.makedirs(extract_path)

                # Open the zip file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # Extract all the contents into the directory
                    zip_ref.extractall(extract_path)

                print(f"Extracted '{zip_path}' to '{extract_path}'")