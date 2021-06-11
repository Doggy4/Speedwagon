import os
from configparser import ConfigParser

def get_section_params(section, filename=fr'{os.getcwd()}/speedwagon.ini'):
	parser = ConfigParser()
	parser.read(filename)
	params = {}
	if parser.has_section(section):
		items = parser.items(section)
		for item in items:
			params[item[0]] = item[1]
	else:
		raise Exception(f'Section <{section}> not found in the <{filename}> file')

	return params
