import os

from utils import config_parser

class EnvironPaths(object):
	def __init__(self):
		self.chrome_driver_path = os.environ.get('CHROMEDRIVER_PATH')
		self.chrome_bin_path = os.environ.get('GOOGLE_CHROME_BIN')
		if self.chrome_driver_path is None:
			self.chrome_driver_path = config_parser.get_section_params('parser').get('chrome_driver_path')
		if self.chrome_bin_path is None:
			self.chrome_bin_path = config_parser.get_section_params('parser').get('chrome_bin_path')
