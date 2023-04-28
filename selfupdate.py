"""
Hashes the running binary with SHA-512.
Compares against remote hash which should always correspond with the latest stable release.
If it doesn't match, prompt to update the game.
"""

from sys import argv
from subprocess import run
from platform import system
from gettext import gettext as _
import hashlib
import httpx
import os
import sys
import gui
import vars

def hash_script():
    h = hashlib.sha512()
    with open(argv[0], 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()

def check_downloader_update():
    try:
        if system() == 'Windows':
            remote_hash = httpx.get(vars.UPDATE_HASH_URL_WINDOWS)
        else:
            remote_hash = httpx.get(vars.UPDATE_HASH_URL_LINUX)
    except httpx.RequestError:
        gui.message(_("WARNING: downloader failed to check itself for updates, potentially out-of-date."))
        return

    remote_hash_string = remote_hash.text
    remote_hash_string = remote_hash_string.rstrip('\n')

    if remote_hash_string == hash_script():
        gui.message(_("Adastral appears to be up-to-date."))
    elif gui.message_yes_no(_("Adastral has an update available. Your current version may not work properly. Do you want to install it?")) and not vars.SCRIPT_MODE:
        gui.message_end(_('Delete Adastral, then redownload and relaunch it from %s') % vars.UPDATE_DOWNLOAD_URL, 0)
    elif vars.SCRIPT_MODE:
        gui.message(_("Adastral out-of-date."))
    else:
        gui.message(_("User chose to skip update. Things may be broken."))
