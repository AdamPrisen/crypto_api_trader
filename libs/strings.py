"""
libs.string

By default en-gb.json file inside the strings top level folder

If language changes, set libs.string.default_locale and run  libs.strings.refresh()
"""
import json

default_locale = "en-gb"
cached_strings = {}

def refresh():
    global cached_strings
    with open (f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)

def gettext(name):
    return cached_strings[name]

def set_default_locale(locale):
    global default_locale
    default_locale = locale

refresh()