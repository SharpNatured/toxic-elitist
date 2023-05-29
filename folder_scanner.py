import os

class FolderScanner:
    def __init__(self):
        self.found_files = []

    def scan(self, folder_path):
        self._scan_folder(folder_path)
        return self.found_files

    def _scan_folder(self, folder_path):
        for root, _, files in os.walk(folder_path):
            if "index.json" in files:
                index_file_path = os.path.join(root, "index.json")
                self.found_files.append(index_file_path)
            else:
                self._handle_missing_file(root)

    def _handle_missing_file(self, folder_path):
        # Call another class here with the folder as input and retrieve the path to "index.json"
        # Assuming the other class is called "IndexJsonFinder" and has a method called "find_index_json"
        index_json_finder = IndexJsonFinder()
        index_file_path = index_json_finder.find_index_json(folder_path)
        if index_file_path:
            self.found_files.append(index_file_path)

class IndexJsonFinder:
    def find_index_json(self, folder_path):
        # Custom logic to find "index.json" file in the folder
        # This is just a placeholder, you should implement your own logic here
        for file_name in os.listdir(folder_path):
            if file_name == "index.json":
                return os.path.join(folder_path, file_name)

        return None
