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
        responses = self.upload_logs(logs)

        for response, log in zip(responses, logs):
            if response.status_code == 200:
                data = response.json()
                # Write response body to a .zevtc.json file if it doesn't already exist
                json_file = log + ".json"
                if not os.path.exists(json_file):
                    self.write_response_body(json_file, data)

    def write_response_body(self, json_file, data):
        with open(json_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data))

    def upload_logs(self, logs):
        responses = []
        progress_bar = tqdm(total=len(logs), desc="Uploading logs", unit="log")

        for log in logs:
            retry_count = 0
            response = self.upload_file(log)

            while response.status_code == 429 and retry_count < MAX_RETRY_COUNT:
                print("Upload limit reached. Sleeping for 60 seconds before retrying...")
                time.sleep(UPLOAD_SLEEP_TIME)
                retry_count += 1
                response = self.upload_file(log)

            if response.status_code == 429:
                print(f"Upload failed for file: {log}")
            else:
                responses.append(response)

            progress_bar.update(1)

        progress_bar.close()
        return responses

    def upload_file(self, file_path):
        with open(file_path, 'rb') as file:
            payload = {'json': '1', 'generator': 'ei'}
            response = requests.post('https://dps.report/uploadContent', files={'file': file}, params=payload)
        return response
