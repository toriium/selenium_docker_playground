import os
from pathlib import Path
import os
import time
from datetime import datetime
def create_file_path(file_path: str):
    path_obj = Path(file_path)
    is_dir = path_obj.suffix == ""

    if is_dir:
        os.makedirs(file_path, exist_ok=True)
    else:
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w'):
                ...


def newest_file_in_dir(dir_path: str):
    newest_file = None
    newest_file_path = None
    for path_obj in Path(dir_path).iterdir():
        file_date_timestamp = path_obj.stat().st_ctime
        file_date = datetime.fromtimestamp(file_date_timestamp)
        if not newest_file:
            newest_file = file_date
            newest_file_path = path_obj.absolute()
        if file_date > newest_file:
            newest_file = file_date
            newest_file_path = path_obj.absolute()

    return str(newest_file_path)
