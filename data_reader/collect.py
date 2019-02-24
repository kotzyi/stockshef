import os
import logging
import csv

class Collect:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def save_realtime(self, code, item):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/real/{}.csv'.format(code))
        self._create_dir(path)
        with open(path, "a+") as csv_file:
            writer = csv.writer(csv_file, delimiter=',',lineterminator='\n')
            writer.writerow(item)
        self.logger.info("SAVE FILES: {}".format(path))

    def save_chart(self, chart, code):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/chart/{}.csv'.format(code))
        self._create_dir(path)
        chart.to_csv(path, mode='w+', index=False)
        self.logger.info("SAVE FILES: {}".format(path))

    def append_dataframe(self, chart, new_chart):
        if chart is None:
            return new_chart

        return chart.append(new_chart)

    def _create_dir(self, path):
        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
            self.logger.info("MAKE DIRECTORIES: {}".format(basedir))
