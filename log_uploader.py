import json
import os
import requests
import time
from tqdm import tqdm

UPLOAD_LIMIT = 25
UPLOAD_SLEEP_TIME = 60
MAX_RETRY_COUNT = 3

class LogUploader:
    def upload(self, dir_path):
        if not os.path.isdir(dir_path):
            print("Invalid directory path.")
            return

        # Get all files with the .zevtc extension in the directory
        logs = [os.path.join(dir_path, log) for log in os.listdir(dir_path) if log.endswith('.zevtc')]

        # Upload the logs and get the response objects
        return self.upload_logs(logs)

    def upload_logs(self, logs):
        json_files = []  # List to store the names of the JSON files
        filtered_logs = [log for log in logs if not os.path.exists(log + ".json")]
        if (len(filtered_logs) == 0):
            return json_files

        progress_bar = tqdm(total=len(filtered_logs), desc="Uploading logs", unit="log")

        for log in filtered_logs:
            retry_count = 0
            response = self.upload_file(log)

            while response.status_code == 429 and retry_count < MAX_RETRY_COUNT:
                print("Upload limit reached. Sleeping for 60 seconds before retrying...")
                time.sleep(UPLOAD_SLEEP_TIME)
                retry_count += 1
                response = self.upload_file(log)

            if response.status_code == 200:
                json_data = response.json()
                json_file_path = log + ".json"
                with open(json_file_path, 'w') as json_file:
                    json.dump(json_data, json_file, indent=4)
                json_files.append(json_file_path)
            else:
                print(f"Upload failed for file: {log}")

            progress_bar.update(1)

        progress_bar.close()
        return json_files

    def upload_file(self, file_path):
        with open(file_path, 'rb') as file:
            payload = {'json': '1', 'generator': 'ei'}
            response = requests.post('https://dps.report/uploadContent', files={'file': file}, params=payload)
        return response
