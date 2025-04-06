import os
import zipfile

def decompress_zips(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.zip'):
                zip_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(root)
                    print(f"Successfully extracted: {zip_path}")
                    
                    # Optional: Remove the original ZIP file after extraction
                    # os.remove(zip_path)
                    # print(f"Removed original ZIP: {zip_path}")
                    
                except zipfile.BadZipFile:
                    print(f"Error: {zip_path} is not a valid ZIP file or is corrupted")
                except Exception as e:
                    print(f"Failed to extract {zip_path}: {str(e)}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    decompress_zips(current_directory)