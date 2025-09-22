import os
import datetime
import glob
from rich import print


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


def date_files(files: list[str], format_string="%Y.%m.%d", delimiter='--', pad_delimiter=True, titleize=True,
               ask=True) -> None:
    name_changes = []

    if pad_delimiter:
        delimiter = f' {delimiter} '

    for old_name in files:
        # get date
        modified_date = get_modified_date(old_name)
        formatted_date = modified_date.strftime(format_string)

        # get original name
        original_name = old_name.split("\\")[-1]

        # titleize
        if titleize:
            original_name = ('.'.join(original_name.split(".")[:-1])).title() + '.' + original_name.split(".")[-1]

        # modify original name
        modified_name = formatted_date + delimiter + original_name

        # append path
        path = "\\".join(old_name.split("\\")[:-1])
        new_name = path + ("\\" if path != '' else '') + modified_name

        # add name change
        name_changes.append((old_name, new_name))

    # print files
    for index, (old_name, new_name) in enumerate(name_changes):
        print(f'''{index}:\t[deep_pink4]"{old_name}"[/deep_pink4]\t->\t[green]"{new_name}"[/green]''')

    # ask
    confirmation = True
    if ask:
        print("\nConfirm? [[green]y[/green]/[red]n[/red]]: ", end="")
        confirmation = input().lower() == 'y'

    # rename files
    if confirmation:
        for old_name, new_name in name_changes:
            rename_file(old_name, new_name)
