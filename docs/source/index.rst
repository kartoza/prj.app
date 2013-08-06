
Visual Change Logger
====================

A simple app to allow community edited visual changelogs for software releases.

Some notes:
-----------

User authentication is via userena. I copied the userena templates into
accounts/templates and then used django-widget-tweaks to add extrac
bootstrap css to them so that the forms look nice.

To install do::

    virtualenv venv
    source venv/bin/activate
    pip install -r REQUIREMENTS-dev.txt
    cd django-project
    python manage.py syncdb
    python manage.py migrate

I'm only using the sqlite backend so there should be no need to configure a
database.


PIL Issues
----------

You need to manually build PIL into your virtual environment and you should
avoid using the installed python-imaging (the debian pil package) on your
system that is needed by tilecache.

If you get an error like this when trying to view jpg thumbs::

  decoder jpeg not available


or if thumbnails produced are being corrupted,

Your PIL is missing jpg (and probably png support). To fix it do::

  ../python/bin/activate
  pip uninstall pil
  sudo apt-get install libjpeg-dev libfreetype6 libfreetype6-dev
  wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz
  tar xfz Imaging-1.1.7.tar.gz
  cd Imaging-1.1.7

Now edit setup.py to set these (for 32 bit)::

   TCL_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"
   JPEG_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"
   ZLIB_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"
   TIFF_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"
   FREETYPE_ROOT = "/usr/lib/i386-linux-gnu/", "/usr/include"

Or for 64 bit::

  TCL_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"
  JPEG_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"
  ZLIB_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"
  TIFF_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"
  FREETYPE_ROOT = "/usr/lib/x86_64-linux-gnu/", "/usr/include"

Test if your configs work::

  python setup.py build_ext -i

The build report should show::

  *** TKINTER support not available (Tcl/Tk 8.5 libraries needed)
  --- JPEG support available
  --- ZLIB (PNG/ZIP) support available
  --- FREETYPE2 support available
  *** LITTLECMS support not available


Now build pil:

``python setup.py install``


Tim Sutton, August 2013
