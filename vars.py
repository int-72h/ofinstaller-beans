"""
Tiny module that currently just establishes
the temp paths and some variables for other
modules to use.
"""
from platform import system
import sys
import tempfile

if system() == 'Windows':
    TEMP_PATH = tempfile.gettempdir()
else:
    TEMP_PATH = '/var/tmp/'

# For determining whether we're installing or updating/repairing the game
INSTALLED = False

ARIA2C_BINARY = None
BUTLER_BINARY = None
INSTALL_PATH = None
TF2C_PATH = None
VCREDIST = None

SCRIPT_MODE = len(sys.argv) > 1
DATA_DIR = "/open_fortress/"
SOURCE_URL = 'https://beans.adastral.net/'

UPDATE_HASH_URL_WINDOWS = SOURCE_URL + 'beans_sha512sum_windows'
UPDATE_HASH_URL_LINUX = SOURCE_URL + 'beans_sha512sum_linux'

UPDATE_DOWNLOAD_URL = 'https://openfortress.fun/download'

# Only on Linux
TO_SYMLINK = [
    ["bin/server.so", "bin/server_srv.so"]
]
