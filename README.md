# py-checkers

## An obligatory Chinese Checkers implementation ##

### written in Python and Kivy ###

It's the famous board game presented in a cross-platform app. Tested on Android and Windows and can be packaged to iOS as well.

#### Purpose ####

The app was completely written on a smartphone (LG G4) as a challenge. No desktop computer was used whatsoever except for packaging. Nevertheless it runs not only on smartphones but desktops as well like Linux, Windows or Mac, wherever Python is available.

As an IDE, the great [QPython](http://www.qpython.com/) was used.

A screenshot of the app running on Linux:

![Linux screenshot](https://raw.githubusercontent.com/auxiliaire/py-checkers/master/PyCheckers%202018-03-06%2020-52-34.png)

#### Requires ####

* Python 2.7 (3 may be an option)
* Kivy 1.10.0 (`pip install kivy`)

#### How to run ####

`python main.py`

#### How to build ####

`buildozer.spec` file contains the specification to build - adjustable to one's needs. (Currently set to Android API 24 arm64-v8a.)

Package: `buildozer -v android debug`

Deploy/run/debug: `buildozer -v android debug deploy run logcat` provided that `adb logcat` is already running and phone is connected.
