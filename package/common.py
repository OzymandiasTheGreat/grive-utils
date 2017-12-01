#!/usr/bin/env python3

import re
from shutil import which
from subprocess import run, PIPE
from distutils.version import LooseVersion
from pathlib import Path
from configparser import ConfigParser
from gi.repository import GLib

def supported_grive_version():

	process = run([GRIVE, '--version'], stdout=PIPE, universal_newlines=True)
	string = _VERSION.search(process.stdout).group('version')
	return LooseVersion(string) >= LooseVersion('0.5.1')

def save_config():

	with CONFIG_FILE.open('w') as fd:
		CONFIG.write(fd)

VERSION = '0.1'
GRIVE = which('grive')
_VERSION = re.compile(r'(?P<version>\d+\.\d+(?:\.\d+)?)')
SUPPORTED = supported_grive_version()
FILENAME = re.compile(r'(?P<type>f(?:ile|older)) \"(?:\.\/)?(?P<path>.+)\"'
	+ r'|sync \"(?:\.\/)?(?P<local>.+)\"')
#~ OUTPUT = re.compile(r'sync \"(?:\.\/)?(?P<path>.+)\" (?P<status>.+)')
STATUS = {
	'already in sync': None,
	"doesn't exist in server, uploading": 'Created',
	'created in remote. creating local': 'Created',
	'changed in local. uploading': 'Modified',
	'changed in remote. downloading': 'Modified',
	'deleted in remote. deleting local': 'Deleted',
	'deleted in local. deleting remote': 'Deleted'}
CONFIG_FILE = Path(GLib.get_user_config_dir()) / 'grive-utils'
CONFIG = ConfigParser(empty_lines_in_values=False, interpolation=None)
CONFIG.optionxform = lambda option: option
CONFIG['DEFAULT']['init'] = 'false'
CONFIG['DEFAULT']['Pause'] = 'false'
CONFIG['DEFAULT']['Path'] = str(Path.home() / 'Google Drive')
CONFIG['DEFAULT']['Interval'] = '60'
CONFIG['DEFAULT']['UpRate'] = '0'
CONFIG['DEFAULT']['DownRate'] = '0'
CONFIG['DEFAULT']['Notify'] = 'true'
CONFIG['DEFAULT']['LightPanel'] = 'false'
try:
	with CONFIG_FILE.open() as fd:
		CONFIG.read_file(fd)
except FileNotFoundError:
	pass
