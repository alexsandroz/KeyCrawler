# KeyCrawler 🔑

## Overview
**KeyCrawler** is a Python project designed to fetch, validate, and manage `keybox.xml` files from GitHub. This project is specifically intended to work with [TrickyStore](https://github.com/5ec1cff/TrickyStore) / [TrickyStoreOSS](https://github.com/beakthoven/TrickyStoreOSS), tools for modifying certificate chains in Android Key Attestation to pass integrity checks.

The scraper uses the GitHub API to locate `keybox.xml` files, validating their content with the Google public key.

Hacked together really quick - any contributions to improve the code quality are welcome!

## Features
- Scrapes `keybox.xml` files from GitHub repositories using the GitHub API.
- Validates `keybox.xml` files using a custom validation function (`keybox_check` from `check.py`).
- Stores validated files in a hashed format to prevent duplicates.
- Provides an interactive interface to manage invalid files.

## Requirements
- Python 3.10+
- [Uv](https://github.com/astral-sh/uv) (recommended) or your preferred Python environment manager.
- A GitHub personal access token with permissions to search code repositories.

## Setup

1. Clone the repository and navigate to the project directory:
   ```sh
   git clone KeyCrawler
   cd KeyCrawler
   ```

2. Install the required Python libraries using uv:
   ```sh
   uv venv
   uv sync
   ```
   (Or use your preferred method to install dependencies from `pyproject.toml`.)

3. Create a `.env` file in the project directory and add your GitHub personal access token:
   ```env
   GITHUB_TOKEN=your_personal_access_token
   ```

> [!NOTE]
> Visit [GitHub's tokens panel](https://github.com/settings/tokens) to create a token.


## Usage

Run the main script to 
   1. Import any custom keyboxes from the `manual` directory,
   2. Scrape `keybox.xml` files from GitHub, validate them, and save them.
   3. Clean up old and invalid files from the `keys` directory.
   ```sh
   uv run python3 ./main.py
   ```

Use the keys with [TrickyStore](https://github.com/5ec1cff/TrickyStore) or [TrickyStoreOSS](https://github.com/beakthoven/TrickyStoreOSS) to achieve strong integrity.

> [!IMPORTANT]
> The project uses the GitHub API and requires a valid token in the `.env` file. Make sure the token has the necessary permissions ( the `public_repo` permission) to search code repositories.


## Limitations
- The script only processes fully valid XML files.

## License
This project is licensed under the GPLv3 License.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

> [!TIP]
> To install development dependencies (type hints for now), run:
> ```sh
> uv sync --dev
> ```

## Acknowledgments
- [KimmyXYC's KeyboxChecker](https://github.com/KimmyXYC/KeyboxChecker)
- [TrickyStore](https://github.com/5ec1cff/TrickyStore) / [TrickyStoreOSS](https://github.com/beakthoven/TrickyStoreOSS)
