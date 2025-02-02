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
Operators
"""

# Unary
SELECT = 'select'
PROJECT = 'project'

# Binary
PRODUCT = 'product'
NJOIN = 'njoin'
INTERSECT = 'intersect'
DIFFERENCE = 'difference'
UNION = 'union'

UOPERATORS = (SELECT, PROJECT)
BOPERATORS = (PRODUCT, NJOIN, INTERSECT, DIFFERENCE, UNION)

OPERATORS = {
    'select': SELECT,
    'project': PROJECT,
    'njoin': NJOIN,
    'product': PRODUCT,
    'intersect': INTERSECT,
    'difference': DIFFERENCE,
    'union': UNION
}
