from gettext import gettext as _
import vars
import gui
import urllib.request

def apply_blacklist():
    gui.message(_("Applying safety blacklist..."))
    try:
        urllib.request.urlretrieve(vars.BLACKLIST_URL, vars.INSTALL_PATH + vars.BLACKLIST_PATH)
    except:
        gui.message(_("WARNING: could not apply safety blacklist."))
