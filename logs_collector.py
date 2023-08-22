from datetime import datetime
import os
import shutil

from logger import log_error, log_info

class LogsCollector:
    def __init__(self, source_folder, target_folder):
        self.source_folder = source_folder
        self.target_folder = target_folder

    def parse_datetime(self, datetime_str):
        datetime_formats = [
            '%d%m%y-%H%M%S',  # ddMMyy-HHmmss
            '%d%m%y-%H%M',    # ddMMyy-HHmm
            '%d%m%y-%H',      # ddMMyy-HH
            '%d%m%y'          # ddMMyy
        ]

        datetime_value = None

        for datetime_format in datetime_formats:
            try:
                datetime_value = datetime.strptime(datetime_str, datetime_format)
                break
            except ValueError:
                pass

        if datetime_value is None:
            raise ValueError(f"Invalid datetime format.")

        return datetime_value

    def copy_files_by_datetime(self, datetime_str):
        try:
            datetime_value = self.parse_datetime(datetime_str)
        except ValueError as error:
            log_error(str(error))
            return

        new_folder_name = datetime_value.strftime('%y-%m-%d')
        new_folder_path = os.path.join(self.target_folder, new_folder_name)

        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        for root, _, files in os.walk(self.source_folder):
            for file in files:
                file_datetime_str = file[:15]  # Extract yyyyMMdd-HHmmss from filename
                file_datetime = datetime.strptime(file_datetime_str, '%Y%m%d-%H%M%S')
                if file_datetime >= datetime_value:
                    source_file_path = os.path.join(root, file)
                    target_file_path = os.path.join(new_folder_path, file)
                    shutil.copy2(source_file_path, target_file_path)
                    log_info(f"Copied '{file}' to '{new_folder_name}' folder.")