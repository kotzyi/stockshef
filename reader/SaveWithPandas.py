from reader import SaveProcess
import pandas as pd
import os
import csv


class SaveWtihPandas(SaveProcess):
    def __init__(self):
        self.save_path = 'data/chart/{}.csv'

    def save_history(self, chart, code):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.save_path.format(code))
        self._create_dir(path)
        chart.to_csv(path, mode='w+', index=False)

    def save_realtime(self, code, item):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.save_path.format(code))
        self._create_dir(path)

        with open(path, "a+") as csv_file:
            writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
            writer.writerow(item)
        self.logger.info("SAVE FILES: {}".format(path))


