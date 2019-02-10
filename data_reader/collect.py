import os
import logging


class Collect:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

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
