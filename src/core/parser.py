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
Parser based on Relation by ltworf http://ltworf.github.io/relational
"""


class Node(object):

    def __init__(self, expression):
        if len(expression) == 1:
            self._name = expression[0]
            return
        for i in range(len(expression) - 1, -1, -1):
            if expression[i] in ('select', 'project'):
                self._name = expression[i]
                self._attrs = expression[1 + i].strip()
                self._child = Node(expression[2 + i])

    def to_python(self):
        if self._name in ('select', 'project'):
            prop = self._attrs
            if self._name == 'project':
                prop = '\"{}"'.format(prop.replace(
                                      ' ', '').replace(',', '\", \"'))
            else:
                prop = '\"{}"'.format(prop)
            return '{0}.{1}({2})'.format(self._child.to_python(),
                                         self._name, prop)
        else:
            return self._name


def _find_end_parenthesis(text):
    count = 0
    for index in range(len(text)):
        if text[index] == '(':
            count += 1
        elif text[index] == ')':
            count -= 1
            if count == 0:
                return index


def parse(query):
    """ This function generates a list of tokens """

    tokens = []

    while query:
        if query.startswith(('select', 'project')):
            length_operator = len(query.split()[0])
            operator = query[:length_operator]
            tokens.append(operator)
            query = query[length_operator:].strip()

            par_end = query.find('(')
            tokens.append(query[:par_end].strip())
            query = query[par_end:].strip()
        elif query.startswith('('):
            par_end = _find_end_parenthesis(query)
            tokens.append(parse(query[1:par_end]))
            query = query[par_end + 1:].strip()
        else:
            tokens.append(query)
            query = ""
    return tokens


def convert_to_python(query):
    return Node(parse(query)).to_python()


if __name__ == "__main__":
    # Test
    tokens = Node(parse("project name, age (select id == 1 (people))"))
    print(tokens.to_python())