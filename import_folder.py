from pathlib import Path
from typing import Iterator

from check import keybox_check
from helpers import FILE_DIR, SAVE_DIR, hash_xml_file


def get_path_iterator(path: Path, exclude_dir: Path = SAVE_DIR) -> Iterator[Path]:
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()

    if not path.exists():
        print(f"Error: The path '{path}' does not exist.")
        return iter([])

    if path.is_dir():
        # Returns an iterator over the directory contents.
        for dirpath, dirnames, filenames in path.walk():
            if dirpath == exclude_dir:
                continue
            for name in filenames:
                yield dirpath / name
    else:
        # For a file, return an iterator with just the file.
        yield path


for item in get_path_iterator(FILE_DIR / "manual"):
    if item.suffix != ".xml":
        continue
    content = item.read_bytes()
    valid = keybox_check(content)
    if valid:
        # Save the valid file to the export directory.
        new_path = SAVE_DIR / hash_xml_file(content)
        try:
            new_path.hardlink_to(item)
        except FileExistsError:
            continue
        print(f"Saved valid file: {item.name}")
    else:
        print(f"Invalid file: {item.name}")
