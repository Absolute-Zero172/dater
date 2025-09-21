import os
import datetime
import glob


def get_modified_date(filepath: str) -> datetime.datetime:
    unix_timestamp = os.path.getmtime(filepath)
    modified_date = datetime.datetime.fromtimestamp(unix_timestamp)
    return modified_date


def get_files(search_pattern="*.*", recursive=False) -> list[str]:
    return glob.glob(search_pattern, recursive=recursive)


def rename_file(old_name: str, new_name: str) -> None:
    try:
        # Rename the file
        os.rename(old_name, new_name)
    except FileNotFoundError:
        print(f"Error: The file '{old_name}' was not found.")
    except FileExistsError:
        print(f"Error: A file named '{new_name}' already exists.")
    except OSError as e:
        print(f"An operating system error occurred: {e}")
