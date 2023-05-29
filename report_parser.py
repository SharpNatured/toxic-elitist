import os
import json

class ReportParser:
    def parse_report(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        success = data['encounter']['success']
        encounter_time = data['encounterTime']
        duration = data['encounter']['duration']
        permalink = data['permalink']
        boss = data['encounter']['boss']

        return {
            'success': success,
            'timestamp': encounter_time,
            'duration': duration,
            'permalink': permalink,
            'encounter': boss
        }

    def parse_reports(self, directory):
        reports = []
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                report = self.parse_report(file_path)
                reports.append(report)
        return reports
