print("Importing Custom Keyboxes from ./manual...")
import import_folder  # imports folder of xml files stored at ./manual
print("Searching GitHub for new keyboxes...")
import keyboxer  # downloads keyboxes from github search
print("Cleaning up old keyboxes...")
import cleanup  # removes duplicates and invalid files from ./keys
