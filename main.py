from cleanup import cleanup_invalid_keyboxes
from helpers import print_section, print_summary
from import_folder import import_manual_keyboxes
from keyboxer import scrape_keyboxes


def main() -> None:
    print_section("Importing manual keyboxes")
    import_stats = import_manual_keyboxes(verbose=False)
    print_summary(
        "Import Summary",
        [
            ("Inspected", str(import_stats.inspected)),
            ("Linked", str(import_stats.linked)),
            ("Invalid", str(import_stats.invalid)),
            ("Duplicates", str(import_stats.duplicates)),
        ],
    )

    print_section("Searching GitHub for new keyboxes")
    scrape_stats = scrape_keyboxes(verbose=False)
    print_summary(
        "GitHub Search Summary",
        [
            ("Examined", str(scrape_stats.searched)),
            ("Too Many Requests", str(scrape_stats.too_many_requests)),
            ("Added", str(scrape_stats.added)),
            ("Malformed", str(scrape_stats.malformed)),
            ("Duplicates", str(scrape_stats.duplicates)),
            ("Cached Hits", str(scrape_stats.cached)),
        ],
    )

    print_section("Cleaning up stored keyboxes")
    cleanup_stats = cleanup_invalid_keyboxes(verbose=False)
    print_summary(
        "Cleanup Summary",
        [
            ("Inspected", str(cleanup_stats.inspected)),
            ("Removed", str(cleanup_stats.removed)),
            ("Errors", str(cleanup_stats.errors)),
        ],
    )


if __name__ == "__main__":
    main()
