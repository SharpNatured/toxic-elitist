import os
import re
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

        # Extract the date-time from each log name using regular expressions
        date_time_pattern = r"\d{8}-\d{6}"
        log_date_times = []
        for log in logs:
            match = re.search(date_time_pattern, log)
            if match:
                log_date_times.append((match.group(), log))

        # Sort the logs based on the date-time
        sorted_logs = sorted(log_date_times, key=lambda x: x[0])

        # Upload the logs and get the response objects
        responses = self.upload_logs([log for _, log in sorted_logs])

        # Create the output file path
        output_file = os.path.join(dir_path, "index.txt")

        # Write the sorted links to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            first_log = sorted_logs[0][0]
            first_date = first_log[:8]
            file.write(f"**{first_date[6:8]}/{first_date[4:6]}/{first_date[2:4]}**\n")

            emoji_success = "✅ "
            emoji_failure = "🤡 "
            for response, (date_time, _) in zip(responses, sorted_logs):
                if response.status_code == 200:
                    data = response.json()
                    encounter_success = data.get("encounter", {}).get("success")
                    link = data.get("permalink", "")
                    if encounter_success:
                        file.write(emoji_success + link + "\n")
                    else:
                        file.write(emoji_failure + link + "\n")
                else:
                    file.write(emoji_failure + "\n")
                file.flush()

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
