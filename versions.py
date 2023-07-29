from os import path
from subprocess import run
from platform import system
from gettext import gettext as _
from gettext import ngettext as _N
import json
import httpx
import gui
import vars
LATEST_VER = False
VERSION_LIST = None
def get_version_list():
    global VERSION_LIST
    if VERSION_LIST is None:
        try:
            version_remote = httpx.get(vars.SOURCE_URL + 'versions.json')
            VERSION_LIST = json.loads(version_remote.text)
        except httpx.RequestError:
            gui.message_end(_("Could not get version list. If your internet connection is fine, "
                              "the servers could be having technical issues."), 1)
    return VERSION_LIST



def update_version_file():
    """
    The previous launcher/updater leaves behind a .revision file with the old revision
    number.
    We just write a .adastral file with the next revision number. We'll deal with semver later.
    """

    try:
        if path.exists(vars.INSTALL_PATH + vars.DATA_DIR + '.adastral'):
            get_installed_version()
            return True
        old_version_file = open(vars.INSTALL_PATH + vars.DATA_DIR + '.revision', 'r')
        old_version = old_version_file.read()
        if not old_version.strip().isdigit():
            raise FileNotFoundError
        old_version_file.close()
        new_version_file = open(vars.INSTALL_PATH + vars.DATA_DIR + '.adastral', 'w')
        json.dump({"version":old_version.strip()},new_version_file)
        new_version_file.close()
        return True
    except FileNotFoundError:
        if gui.message_yes_no(_("We can't read the version of your installation. It could be corrupted. Do you want to reinstall the game?"), False):
            return False
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)


def get_latest_version():
    return str(sorted([int(x) for x in get_version_list()["versions"].keys()], reverse=True)[0])

def get_installed_version():
    local_version_file = open(vars.INSTALL_PATH + vars.DATA_DIR + '.adastral', 'r')
    local_version = json.load(local_version_file)["version"]
    return local_version

def check_for_updates():
    """
    This function checks the local version against the list of remote versions and deems firstly, if an update is necessary, and secondarily, whether it's more efficient to update or reinstall.
    """

    # This probably was already communicated to the user in update_version_file(), but if version.txt doesn't exist, skip updating.
    if not path.exists(vars.INSTALL_PATH + vars.DATA_DIR + '.adastral'):
        if gui.message_yes_no(_("No game installation detected at given sourcemods path. Do you want to install the game?")):
            return False
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)

    try:
        local_version_file = open(vars.INSTALL_PATH + vars.DATA_DIR + '.adastral', 'r')
        local_version = json.loads(local_version_file.read())["version"]
    except ValueError:
        if gui.message_yes_no(_("We can't read the version of your installation. It could be corrupted. Do you want to reinstall the game?"), False):
            return False
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)
    # End of checking, we definitely have a valid installation at this point
    # Now we have to see if there's a remote patch matching our local version


    # First, as a basic sanity check, do we know about this version at all?
    # We don't want to try to patch from 746 or some other nonexistent version.
    version_json = get_version_list()["versions"]
    found = False
    for ver in version_json:
        if ver == local_version:
            found = True
            break

    if not found:
        if gui.message_yes_no(_("The version of your installation is unknown. It could be corrupted. Do you want to reinstall the game?"), False):
            return False
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)

    # Now we're checking the latest version, to see if we're already up-to-date.
    latest_version = get_latest_version()
    if local_version == latest_version:
        if gui.message_yes_no(_("We think we've found an existing up-to-date installation of the game. Do you want to reinstall it?"), False):
            return False
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)

    # Finally, we ensure our local version has a patch available before continuing.
    patches = get_version_list()["patches"]
    if local_version in patches:
        if gui.message_yes_no(_("An update is available for the game. Do you want to install it?"), None, True):
            if gui.message_yes_no(_("If running, please close your game client and/or game launcher. Confirm once they're closed."), None, True):
                return True
            else:
                gui.message_end(_("Exiting..."), 0)
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)
    else:
        gui.message_end(_("An update is available, but no patch could be found for your game version. Try reinstalling?"), 0)