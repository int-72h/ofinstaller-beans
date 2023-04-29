# Adastral.
## Downloading to the stars.
To end-users, this tool... you shouldn't be using. use the official TF2Cdownloader and whatever OF is currently using.

To programmers, this is a thin and rough script which is/will be backend agnostic for STVN vs Butler testing. Functionally similar to OFToast I (but functional).

To other Sourcemods, this is a tool you can use for your project with only minor work, as the mechanism here is extremely agnostic and flexible. Get in touch with cco or intcoms on Discord if you're interested!

----

Requires Rich, PyZstd, TQDM, and HTTPX to build.

PyInstaller is used to build this into a single-file binary. A spec file is included.

For convenience in building, the Binaries folder of the repository contains prebuilt and static versions of Aria2 and Butler for Windows and Linux. Aria2 is extracted from here: https://github.com/q3aql/aria2-static-builds (aria2-1.36.0-win-64bit-build2.7z)

The official build of Butler, as supplied by itch.io, is used.

----

Translations currently aren't up to scratch due to string changes. Don't use them.
