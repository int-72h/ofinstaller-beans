"""
Master module. Runs basic checks and then offloads all
of the real work to functions defined in other files.
"""
import os
import traceback
import ctypes
from platform import system
from shutil import which
from subprocess import run
import sys
from sys import argv, exit, stdin
import gettext
from gettext import gettext as _
from rich import print
import gui
import downloads
import setup
import vars
import versions
import selfupdate

# PyInstaller offers no native way to select which application you use for the console.
# Instead, it uses the system default, which is cmd.exe at time of writing.
# This hack checks if Windows Terminal is installed. If it is, and if the application
# is launched with cmd.exe instead, it relaunches the application in WT instead.
if not vars.SCRIPT_MODE and system() == 'Windows':
    if which('wt') is not None and os.environ.get("WT_SESSION") is None:
        run(['wt', argv[0]], check=True)
        exit()

# Disable QuickEdit so the process doesn't pause when clicked
if not vars.SCRIPT_MODE and system() == 'Windows':
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100))

def sanity_check():
    """
    This is mainly for Linux, because it's easy to launch it by double-clicking it, which would
    run it in the background and not show any output. PyInstaller has no way to force a terminal
    open for this on Linux. We could implement something similar to what we do to force using WT,
    but it's not a priority right now since Linux users can figure out how to use the terminal.
    """
    if not stdin or not stdin.isatty():
        print(_("Looks like we're running in the background. We don't want that, so we're exiting."))
        exit(1)
    if system() == 'Windows':
        print(_("We need to download vcredist, give us a moment..."))
        run([vars.ARIA2C_BINARY, "https://aka.ms/vs/17/release/vc_redist.x86.exe","--check-certificate=false","-d",vars.TEMP_PATH])
        print(_("now installing..."))
        run([os.path.join(vars.TEMP_PATH, "VC_redist.x86.exe"),'/install','/passive','/norestart'])
        print(_("Done!"))


if sys.stdout.encoding == 'ascii':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding == 'ascii':
    sys.stderr.reconfigure(encoding='utf-8')

if os.getenv('LANG') is None:
    import locale
    lang, enc = locale.getlocale()
    if lang is not None:
        os.environ['LANG'] = lang

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    gettext.bindtextdomain('beans', os.path.abspath(os.path.join(os.path.dirname(__file__), 'locale')))
else:
    gettext.bindtextdomain('beans', 'locale')
gettext.textdomain('beans')

def wizard():
    try:
        setup.setup_binaries()
        sanity_check()
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            selfupdate.check_downloader_update()
        setup.setup_path(False)
        versions.get_version_list()

        # Check if the game is already installed, for the purposes of running update_version_file() safely
        if os.path.exists(vars.INSTALL_PATH + vars.DATA_DIR + '.adastral'):
            vars.INSTALLED = True
        elif os.path.exists(vars.INSTALL_PATH + vars.DATA_DIR + '.revision') or os.path.exists(
                vars.INSTALL_PATH + vars.DATA_DIR + 'gameinfo.txt'):
            vars.INSTALLED = True
            versions.update_version_file()


        # All of the choice logic is handled in this function directly.
        gui.main_menu()

    except Exception as ex:
        if ex is not SystemExit:
            traceback.print_exc()
            print(_("[italic magenta]----- Exception details above this line -----"))
            print(_("[bold red]:warning: The program has failed. Post a screenshot in the respective troubleshooting channels on the Open Fortress "
                    "Discord. :warning:[/bold red]"))
            if os.environ.get("WT_SESSION"):
                print(_("[bold]You are safe to close this window."))
            else:
                input(_("Press Enter to exit."))
            exit(1)

def manual_script():
    try:
        if sys.argv[1] == "--help":
            print(_(
            '''Usage: beans [COMMAND] [PATH]
Installation utility for Open Fortress.

If no arguments are provided, the downloader will be ran in setup mode, in
which a series of questions will be asked to install the game for a regular
user. This is what's used when opening the downloader from the desktop.

Valid commands:
  --install           installs OF into a new folder inside PATH
  --update            updates the pre-existing OF installation in its
                      folder inside PATH
  --help              shows this

PATH is the folder containing the game's folder. This is usually the
sourcemods folder for clients, or the Source dedicated server folder for
servers.

If PATH isn't provided, then it'll be replaced with the detected path to the
sourcemods folder in the Steam directory. If it couldn't be detected, then the
path will be the current work directory.'''
            ))
            exit(0)

        if sys.argv[1] == "--install":
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                selfupdate.check_downloader_update()
            setup.setup_path_script()
            setup.setup_binaries()

            if os.path.exists(vars.INSTALL_PATH + vars.DATA_DIR + 'gameinfo.txt'):
                vars.INSTALLED = True

            if vars.INSTALLED:
                gui.message(_("Open Fortress is already installed. Assuming a reinstallation."))
            downloads.install()
            print(_("The installation has successfully completed. Remember to restart Steam!"))
            exit(0)
        elif sys.argv[1] == "--update":
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                selfupdate.check_downloader_update()
            setup.setup_path_script()
            setup.setup_binaries()
            if os.path.exists(vars.INSTALL_PATH + vars.DATA_DIR + 'gameinfo.txt'):
                vars.INSTALLED = True

            if not vars.INSTALLED:
                print(_("OF isn't installed, cannot do an update. Consider using "
                        "--install instead."))
                exit(1)
            else:
                vars.INSTALLED = versions.update_version_file()
                if versions.check_for_updates() == 'reinstall':
                    downloads.install()
                else:
                    downloads.update()
                print(_("The update has successfully completed."))
                exit(0)
        else:
            print(_("Unrecognised command. Try --help"))
            exit(1)

    except Exception as ex:
        if ex is not SystemExit:
            traceback.print_exc()
            print(_("[italic magenta]----- Exception details above this line -----"))
            print(_("[bold red]:warning: The beans have failed. Post a screenshot in "
                    "#beans-troubleshooting on the Discord. :warning:[/bold red]"))
            exit(1)

if vars.SCRIPT_MODE:
    manual_script()
else:
    wizard()
