# -*- coding: utf-8 -*-
#
# Copyright © 2009- The Spyder Development Team
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""
Utilities to define configuration values
"""

import os
import os.path as osp
import sys

from spyderlib.config.base import _
from spyderlib.utils import iofuncs


#==============================================================================
# File extensions supported by Spyder
#==============================================================================
EDIT_FILETYPES = (
    (_("Python files"), ('.py', '.pyw', '.ipy')),
    (_("Cython/Pyrex files"), ('.pyx', '.pxd', '.pxi')),
    (_("C files"), ('.c', '.h')),
    (_("C++ files"), ('.cc', '.cpp', '.cxx', '.h', '.hh', '.hpp', '.hxx')),
    (_("OpenCL files"), ('.cl', )),
    (_("Fortran files"), ('.f', '.for', '.f77', '.f90', '.f95', '.f2k')),
    (_("IDL files"), ('.pro', )),
    (_("MATLAB files"), ('.m', )),
    (_("Julia files"), ('.jl',)),
    (_("Yaml files"), ('.yaml','.yml',)),
    (_("Patch and diff files"), ('.patch', '.diff', '.rej')),
    (_("Batch files"), ('.bat', '.cmd')),
    (_("Text files"), ('.txt',)),
    (_("reStructuredText files"), ('.txt', '.rst')),
    (_("gettext files"), ('.po', '.pot')),
    (_("NSIS files"), ('.nsi', '.nsh')),
    (_("Web page files"), ('.scss', '.css', '.htm', '.html',)),
    (_("XML files"), ('.xml',)),
    (_("Javascript files"), ('.js',)),
    (_("Json files"), ('.json',)),
    (_("IPython notebooks"), ('.ipynb',)),
    (_("Enaml files"), ('.enaml',)),
    (_("Configuration files"), ('.properties', '.session', '.ini', '.inf',
                                '.reg', '.cfg', '.desktop')),
)


def _create_filter(title, ftypes):
    return "%s (*%s)" % (title, " *".join(ftypes))


ALL_FILTER = "%s (*)" % _("All files")


def _get_filters(filetypes):
    filters = []
    for title, ftypes in filetypes:
        filters.append(_create_filter(title, ftypes))
    filters.append(ALL_FILTER)
    return ";;".join(filters)


def _get_extensions(filetypes):
    ftype_list = []
    for _title, ftypes in filetypes:
        ftype_list += list(ftypes)
    return ftype_list


def get_pygments_extensions():
    """Return all file type extensions supported by Pygments"""
    # NOTE: Leave this import here to keep startup process fast!
    import pygments.lexers as lexers
    extensions = []
    all_lexers = lexers.get_all_lexers()
    for lx in all_lexers:
        lexer_exts = lx[2]
        if lexer_exts:
            extensions = extensions + list(lexer_exts)
    return tuple(extensions)


def get_filter(filetypes, ext):
    """Return filter associated to file extension"""
    if not ext:
        return ALL_FILTER
    for title, ftypes in filetypes:
        if ext in ftypes:
            return _create_filter(title, ftypes)
    else:
        return ''


EDIT_FILTERS = _get_filters(EDIT_FILETYPES)
EDIT_EXT = _get_extensions(EDIT_FILETYPES)+['']

# Extensions supported by Spyder's Variable explorer
IMPORT_EXT = list(iofuncs.iofunctions.load_extensions.values())


# Extensions that should be visible in Spyder's file/project explorers
SHOW_EXT = ['.png', '.ico', '.svg']


# Extensions supported by Spyder (Editor or Variable explorer)
VALID_EXT = EDIT_EXT+IMPORT_EXT


#==============================================================================
# Detection of OSes specific versions
#==============================================================================
def is_ubuntu():
    "Detect if we are running in an Ubuntu-based distribution"
    if sys.platform.startswith('linux') and osp.isfile('/etc/lsb-release'):
        release_info = open('/etc/lsb-release').read()
        if 'Ubuntu' in release_info:
            return True
        else:
            return False
    else:
        return False


def is_gtk_desktop():
    "Detect if we are running in a Gtk-based desktop"
    if sys.platform.startswith('linux'):
        xdg_desktop = os.environ.get('XDG_CURRENT_DESKTOP', '')
        if xdg_desktop:
            gtk_desktops = ['Unity', 'GNOME', 'XFCE']
            if any([xdg_desktop.startswith(d) for d in gtk_desktops]):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
