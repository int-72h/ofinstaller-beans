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

SCRIPT_MODE = len(sys.argv) > 1
DATA_DIR = "/tf2classic/"
SOURCE_URL = 'https://wiki.tf2classic.com/kachemak/'

BLACKLIST_URL = 'https://tf2classic.org/serverlist/blacklist.php'
BLACKLIST_PATH = '/tf2classic/cfg/server_blacklist.txt'

UPDATE_HASH_URL_WINDOWS = SOURCE_URL + 'https://wiki.tf2classic.com/kachemak/tf2cd_sha512sum_windows'
UPDATE_HASH_URL_LINUX = SOURCE_URL + 'https://wiki.tf2classic.com/kachemak/tf2cd_sha512sum_linux'

UPDATE_DOWNLOAD_URL = 'https://tf2classic.com/download'

# Only on Linux
TO_SYMLINK = [
    ["/tf2classic/bin/server.so", "/tf2classic/bin/server_srv.so"]
]
