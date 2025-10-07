from check import keybox_check
from helpers import SAVE_DIR

for file_path in SAVE_DIR.glob("*.xml"):
    file_content = file_path.read_bytes()  # Read file content as bytes
    # Run CheckValid to determine if the file is still valid
    if not keybox_check(file_content):
        # Prompt user for deletion
        print(f"File '{file_path.name}' is no longer valid. Deleting it...")
        try:
            file_path.unlink()  # Delete the file
            print(f"Deleted file: {file_path.name}")
        except OSError as e:
            print(f"Error deleting file {file_path.name}: {e}")