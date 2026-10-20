[app]

# (str) Title of your application
title = CodeQuest

# (str) Package name / domain -> org.codequest.codequest
package.name = codequest
package.domain = org.codequest

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,json,html,css,js,svg,png,h

# (list) Directories to exclude. Lesson/problem *sources* aren't needed at
# runtime: the app loads the pre-built codequest/data/*.json.
source.exclude_dirs = tests, tools, termux, assets, bin, .github, .buildozer, codequest/content

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# python3 + the scientific stack used by the "Math & Data" problems.
# sympy is pure Python and needs mpmath; numpy has a python-for-android recipe.
requirements = python3,numpy,sympy,mpmath

# (str) Presplash / icon of the application
presplash.filename = %(source.dir)s/assets/presplash.png
icon.filename = %(source.dir)s/assets/icon.png
android.presplash_color = #0f1222

# (list) Supported orientations
orientation = portrait

fullscreen = 0

#
# Android specific
#

# (list) Permissions. INTERNET is needed for the WebView to talk to the
# embedded server on 127.0.0.1 (and, optionally, to a Termux judge for C++).
android.permissions = INTERNET

# (int) Target Android API (Google Play requires a recent one)
android.api = 34
# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (bool) Automatically accept SDK license agreements (needed for CI)
android.accept_sdk_license = True

# (list) The Android archs to build for. arm64-v8a covers practically every
# phone from the last ~8 years; add armeabi-v7a for very old devices
# (doubles build time because NumPy is compiled per arch).
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

#
# Python for android (p4a) specific
#

# (str) Bootstrap to use. "webview" runs main.py (our HTTP server) and shows
# http://127.0.0.1:<p4a.port>/ in a full-screen Android WebView.
p4a.bootstrap = webview

# (int) port number to specify an explicit --port= p4a argument
p4a.port = 5000

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
