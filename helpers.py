import hashlib
from pathlib import Path

from lxml import etree

FILE_DIR = Path(__file__).resolve().parent

SAVE_DIR = FILE_DIR / "keys"
if not SAVE_DIR.exists():
    SAVE_DIR.mkdir(exist_ok=True)

CACHE_FILE = FILE_DIR / "cache.txt"
if not CACHE_FILE.exists():
    CACHE_FILE.touch()


def hash_xml_file(file_content: bytes) -> str:
    """Hashes the contents of an XML file."""
    root = etree.fromstring(file_content)
    canonical_xml = etree.tostring(root, method="c14n")
    hash_value = hashlib.sha256(canonical_xml).hexdigest()
    file_name = hash_value + ".xml"
    return file_name
