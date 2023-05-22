# ofinstaller-beans
## Sappho said we needed something in the interim. so here's beans
To end-users, this tool is what you use to install/update OF whilst adastral's cooking in the oven.

To programmers, this is a version of TF2Downloader genericized for use for OF with some spec changes to kachemak (beta branch mainly)

Requires Rich, PyZstd, TQDM, and HTTPX to build.

PyInstaller is used to build this into a single-file binary. A spec file is included.

For convenience in building, the Binaries folder of the repository contains prebuilt and static versions of Aria2 and Butler for Windows and Linux. Aria2 is extracted from here: https://github.com/q3aql/aria2-static-builds (aria2-1.36.0-win-64bit-build2.7z)

The official build of Butler, as supplied by itch.io, is used.

----

Translations currently aren't up to scratch due to string changes. Don't use them.
