#!/bin/sh
## This caused GLib2 applications to convert filenames from 
## locale encoding to UTF-8. If the locale encoding is already
## UTF-8 then it makes no difference.

G_FILENAME_ENCODING="@locale"
export G_FILENAME_ENCODING
