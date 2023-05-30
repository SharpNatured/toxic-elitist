import os
import requests
import json
import re

class ReportConverter:
    def convert_links(self, directory):
        links_file = os.path.join(directory, "links.txt")
        date_time_pattern = r"\d{8}-\d{6}"

        with open(links_file, 'r') as f:
            links = f.read().splitlines()

        for link in links:
            match = re.search(date_time_pattern, link)
            if match:
                date_time = match.group()
                file_name = f"{date_time}.zevtc"
                file_path = os.path.join(directory, file_name)

                if os.path.exists(file_path):
                    json_data = self.get_upload_metadata(link)
                    json_file_name = f"{date_time}.zevtc.json"
                    json_file_path = os.path.join(directory, json_file_name)

                    with open(json_file_path, 'w') as json_file:
                        json.dump(json_data, json_file, indent=4)
                else:
                    print(f"Warning: .zevtc file '{file_name}' does not exist.")
            else:
                print(f"Warning: Invalid date-time pattern in link '{link}'.")

    @staticmethod
    def get_upload_metadata(link):
        url = "https://dps.report/getUploadMetadata"
        params = {"permalink": link}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Failed to fetch metadata for '{link}'")
            return None
