# -*- coding: utf-8 -*-
#
# Copyright 2015 - Gabriel Acosta <acostadariogabriel@gmail.com>
#
# This file is part of Pireal.
#
# Pireal is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# Pireal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pireal; If not, see <http://www.gnu.org/licenses/>.

"""
Pireal settings
"""

import sys
from PyQt4.QtGui import QFont


# Operating System
LINUX, WINDOWS = False, False
if sys.platform.startswith('linux'):
    LINUX = True
else:
    WINDOWS = True


# Font
if LINUX:
    FONT = QFont('Monospace', 12)
else:
    FONT = QFont('Courier', 10)

# Supported relation files
#RFILES = "(*.csv *.prf)"

# Supported files
RFILES = "Pireal Data Base File (*.pdb);; Pireal Query File (*.pqf)"
