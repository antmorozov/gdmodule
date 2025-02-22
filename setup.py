# Setup for gdmodule 0.50 and later

from distutils.core import setup, Extension
import os, glob, sys, string, commands

# version of this gdmodule package
this_version = "0.59"

# directory existence tester

def dirtest(lst):
    rlst = []
    for d in lst:
        try:
            if os.listdir(d):
                rlst.append(d)
        except:
            pass
    return rlst

def filetest(path, names):
    rlst = []
    for d in path:
        for i in range(len(names)):
            found = glob.glob(os.path.join(d, "lib%s.*" % names[i]))
            if found:
                rlst.append(names[i])
                names[i] = None
        names = filter(None, names)
    return rlst

def remove(itm, lst):
    r = range(len(lst))
    r.reverse()
    for i in r:
        if lst[i] == itm:
            del lst[i]

# library_dirs option is rather non-portable, but since I am targetting
# Unixoid OS's I will just look for the usual suspects.

libdirs = dirtest([
    "/usr/local/lib", "/sw/lib", "/usr/lib",
    "/usr/lib/i386-linux-gnu", "/usr/lib/x86_64-linux-gnu",
    "/usr/lib/aarch64-linux-gnu",
    "/usr/lib/X11", "/usr/X11R6/lib",
    "/opt/gnome/lib",
])

try:
    exotic_libdir = commands.getoutput("gdlib-config --libdir"),
    libdirs += exotic_libdir
except:
    pass

# include_dirs are also non-portable; same trick here.

incdirs = dirtest([
    "/usr/local/include", "/sw/include", "/usr/include",
    "/usr/include/X11", "/usr/X11R6/include",
    "/opt/gnome/include",
])

try:
    exotic_incdir = commands.getoutput("gdlib-config --includedir"),
    incdirs += exotic_incdir
except:
    pass

# Try to identify our libraries

want_libs = [
    "gd",
    "jpeg", "png", "gif",
    "X11", "Xpm",
    "z", "ttf", "freetype",
]

libs = filetest(libdirs, want_libs)

missing = []

for l in want_libs:
    if l and l not in libs:
        missing.append(l)

if "ttf" in missing and "freetype" not in missing:
    remove("ttf", missing)

if missing:
    print "WARNING:  Missing", string.join(missing, ", "), "Libraries"

# hand-clean the libs

if "gd" not in libs:
    print "Can't find GD library."
    sys.exit(0)

if "ttf" in libs and "freetype" in libs:
    remove("ttf", libs)

if "Xpm" in libs and "X11" not in libs:
    remove("Xpm", libs)

if "png" in libs and "z" not in libs:
    remove("png", libs)

if "z" in libs and "png" not in libs:
    remove("png", libs)

# build the macro list

macros = []

for l in libs:
    macros.append(( "HAVE_LIB%s" % l.upper(), None ))

# OK, now do it!

setup(name="gdmodule", version=this_version,

    description="GD Package",
    long_description="GD Package",
    author="Chris Gonnerman",
    author_email="chris.gonnerman@newcenturycomputers.net",

    url="http://newcenturycomputers.net/projects/gdmodule.html",
    py_modules=["gd"],
    ext_modules=[
        Extension("_gd", ["_gdmodule.c"], 
            include_dirs=incdirs, library_dirs=libdirs,
            libraries=libs, define_macros=macros)],
)

# end of file.
