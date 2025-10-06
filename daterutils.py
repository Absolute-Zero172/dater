import os
import datetime
import glob
from rich import print
import re


def get_modified_date(filepath: str) -> datetime.datetime:
    """
    gets the date modified of a filepath
    :param filepath: relative or absolute filepath
    :return: datetime object
    """
    unix_timestamp = os.path.getmtime(filepath)
    modified_date = datetime.datetime.fromtimestamp(unix_timestamp)
    return modified_date


def get_files(search_pattern="*.*", recursive=False) -> list[str]:
    """
    gets list of string paths for files with a given glob search pattern
    :param search_pattern: the pattern to search
    :param recursive: recursive in directories
    :return: list of paths
    """
    return glob.glob(search_pattern, recursive=recursive)


def rename_file(old_name: str, new_name: str) -> None:
    """
    renames a file
    :param old_name: old name/filepath
    :param new_name: new name/filepath
    :return: None
    """
    try:
        # Rename the file
        os.rename(old_name, new_name)
    except FileNotFoundError:
        print(f"Error: The file '{old_name}' was not found.")
    except FileExistsError:
        print(f"Error: A file named '{new_name}' already exists.")
    except OSError as e:
        print(f"An operating system error occurred: {e}")


def get_dated_name(file_name: str, format_string="%Y.%m.%d", delimiter='--', pad_delimiter=True, titleize=True,
                   check_prenamed=True) -> tuple[str, bool]:
    """
    takes an input name and returns the formatted name with the date appended to the beginning
    :param file_name: input file name (with optional path)
    :param format_string: the format for the date (default: yyyy.mm.dd)
    :param delimiter: how to separate the date and title (default: --)
    :param pad_delimiter: pad delimiter with spaces on both sides
    :param titleize: call .title() on the title (w/o file extension)
    :param check_prenamed: guess if the file has been named before; if so, remove and update the date
    :return: tuple, first item is the modified name and second is a boolean flag whether the date was a prename update
    """

    name_update_flag = False

    # decide to pad delimiter
    if pad_delimiter:
        delimiter = f' {delimiter} '

    # get path and name
    path = '\\'.join(file_name.split('\\')[:-1])
    path += '' if path == '' else '\\'
    name = file_name.split('\\')[-1]
    file_extension = '.' + name.split('.')[-1]
    name = '.'.join(name.split('.')[:-1])

    # check for prenames
    if check_prenamed:
        # determine match with regex
        match = re.fullmatch(r"[0-9]*\.[0-9]*\.[0-9]* *[-=:_]+ *.*$", name) is not None

        # if match, update name and flag
        if match:
            guessed_name = re.split(r" *[-=:_]+ *", name)[-1]
            name = guessed_name
            name_update_flag = True

    # titleize name
    if titleize:
        name = name.title()

    # get dates
    modified_date = get_modified_date(file_name)
    formatted_date = modified_date.strftime(format_string)

    # format name
    formatted_name = formatted_date + delimiter + name

    # add path and extension
    completed_path = path + formatted_name + file_extension

    return completed_path, name_update_flag


def date_files(files: list[str], format_string="%Y.%m.%d", delimiter='--', pad_delimiter=True, titleize=True,
               ask=True) -> None:
    """
    renames files with the date, a delimiter, and its original title
    :param files: list of file paths to rename
    :param format_string: the format for the date (default: yyyy.mm.dd)
    :param delimiter: how to separate the date and title (default: --)
    :param pad_delimiter: pad delimiter with spaces on both sides
    :param titleize: call .title() on the title (w/o file extension)
    :param ask: confirm rename
    :return: None
    """
    name_changes = []

    for old_name in files:
        # get new name
        new_name, prename_flag = get_dated_name(old_name, format_string=format_string, delimiter=delimiter,
                                                pad_delimiter=pad_delimiter, titleize=titleize)

        # add name change
        name_changes.append((old_name, new_name, prename_flag))

    # print files

    # get maximum size
    max_old = max([len(name[0]) for name in name_changes]) + 1
    max_new = max([len(name[1]) for name in name_changes]) + 1

    # print names
    for index, (old_name, new_name, prename_flag) in enumerate(name_changes):
        print(
            f'''{index}: [deep_pink4]"{old_name + '"':<{max_old}}[/deep_pink4] ([light_blue]\
{'-' if not prename_flag else '*'}[/light_blue]) -> [green]"{new_name + '"':<{max_new}}[/green]''')

    # ask
    confirmation = True
    if ask:
        print("\nConfirm? [[green]y[/green]/[red]n[/red]]: ", end="")
        confirmation = input().lower() == 'y'

    # rename files
    if confirmation:
        print("[green]CONFIRMED[/green] -- Renaming files...")
        for old_name, new_name, _ in name_changes:
            rename_file(old_name, new_name)
    else:
        print("[red]CANCELLED[/red] -- Nothing will be renamed")


if __name__ == '__main__':
    date_files(get_files("test\\*.*"))
