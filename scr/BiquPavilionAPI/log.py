import logging


class LogConfig:
    def __init__(self, log_file_name):
        self.filemode = 'a'
        self.file_name = log_file_name
        self.logger = logging.getLogger(__name__)
        self.level = logging.DEBUG
        self.format = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'

    def init_logger(self):
        print('init logger')
        logging.basicConfig(
            format=self.format, level=self.level, filename=self.file_name, filemode=self.filemode
        )

    def del_logger(self):
        print('del logger')
        logging.basicConfig(
            format=self.format, level=self.level, filename=self.file_name, filemode="w"
        )
