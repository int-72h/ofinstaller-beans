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
def get_version_list(beta=False):
    global VERSION_LIST
    if VERSION_LIST is None:
        try:
            version_remote = httpx.get(vars.SOURCE_URL + ('versions_beta.json'if beta else
                                                          'versions.json'))
            VERSION_LIST = json.loads(version_remote.text)
        except httpx.RequestError:
            gui.message_end(_("Could not get version list. If your internet connection is fine, the servers could be having technical issues."), 1)
    return VERSION_LIST



def update_version_file():
    """
    The previous launcher/updater leaves behind a .revision file with the old revision
    number.
    To avoid file bloat, we reuse this, but replace it with the game's semantic version number.
    To obtain the game's semantic version number, we simply format it as 0.rev.0.
    """
    try:
        old_version_file = open(vars.INSTALL_PATH + vars.DATA_DIR + '.revision', 'r')
        old_version = old_version_file.read()
        new_version_file = open(vars.INSTALL_PATH + vars.DATA_DIR + '.adastral', 'w')
        # We unconditionally overwrite .revision since .adastral is the canonical file.
        new_version_file.write('0.' + old_version + '.0')
        new_version_file.close()
        old_version_file.close()
        return True
    except FileNotFoundError:
        if gui.message_yes_no(_("We can't read the version of your installation. It could be corrupted. Do you want to reinstall the game?"), False):
            return False
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)


def get_latest_version(beta=False):
    return sorted(get_version_list(beta)["versions"].keys(), reverse=True)[0]

def get_installed_version():
    local_version_file = open(vars.INSTALL_PATH + vars.DATA_DIR + '.revision', 'r')
    local_version = local_version_file.read().rstrip('\n')
    return local_version

def check_for_updates(beta_ver=False):
    """
    This function checks the local version against the list of remote versions and deems firstly, if an update is necessary, and secondarily, whether it's more efficient to update or reinstall.
    """
    # This probably was already communicated to the user in update_version_file(), but if version.txt doesn't exist, skip updating.
    if not path.exists(vars.INSTALL_PATH + vars.DATA_DIR + 'version.txt'):
        if gui.message_yes_no(_("No game installation detected at given sourcemods path. Do you want to install the game?")):
            return False
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)

    try:
        local_version_file = open(vars.INSTALL_PATH + vars.DATA_DIR + 'rev.txt', 'r')
        local_version = local_version_file.read().rstrip('\n')
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
    beta_json = get_version_list(True)["versions"]
    found = False
    beta = False
    latest_version = sorted(version_json.keys(), reverse=True)[0]
    for ver in version_json:
        if ver == local_version:
            found = True
            break
    for ver in beta_json:
        if ver == local_version:
            beta = True
            break
    if not found and not beta:
        if gui.message_yes_no(
                _("The version of your installation is unknown. It could be corrupted. Do you "
                  "want to reinstall the game (to stable)?"),
                False):
            return False
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)

    if not beta_ver:
        if not found and beta:
            if not gui.message_yes_no(_("You're on a beta version! would you like to go back to "
                                        "the "
                                    "stable version?"), False):
                gui.message_end(_("We have nothing to do. Goodbye!"), 0)

        # Now we're checking the latest version, to see if we're already up-to-date.
        if local_version == latest_version:
            if gui.message_yes_no(_("We think we've found an existing up-to-date installation of the game. Do you want to reinstall it?"), False):
                return False
            else:
                gui.message_end(_("We have nothing to do. Goodbye!"), 0)
        # Finally, we ensure our local version has a patch available before continuing.
        patches = get_version_list()["patches"]
    else:
        latest_beta_version = sorted(beta_json.keys(), reverse=True)[0]
        if local_version == latest_beta_version:
            if gui.message_yes_no(_("We think we've found an existing up-to-date beta installation "
                                    "of the game. Do you want to reinstall it?"), False):
                return False
            else:
                gui.message_end(_("We have nothing to do. Goodbye!"), 0)
        patches = get_version_list(True)["patches"]
    if local_version in patches:
        if gui.message_yes_no(_("An update is available for the game. Do you want to install it?"),
                              None, True):
            if gui.message_yes_no(
                    _("If running, please close your game client. Confirm once they're closed."),
                    None, True):
                return True
            else:
                gui.message_end(_("Exiting..."), 0)
        else:
            gui.message_end(_("We have nothing to do. Goodbye!"), 0)
    else:
        gui.message_end(_("An update is available, but no patch could be found for your game "
                          "version. This probably means it's better to reinstall. reinstall?"), 0)


isbeta = lambda : True if 'b' in get_installed_version() else False