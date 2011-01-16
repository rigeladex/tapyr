# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.Trie
#
# Purpose
#    Trie (prefix tree)
#
# Revision Dates
#    15-Jan-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import       TFL
import _TFL._Meta.Object

import itertools

class Node (object) :
    """Node of a trie."""

    __slots__     = ("children", "parent", "value")

    def __init__ (self, parent, value = None) :
        self.children = {}
        self.parent   = parent
        self.value    = value
    # end def __init__

    def pre_order (self) :
        def gen (key, node) :
            yield key, node
            for ck, cn in sorted (node.children.iteritems ()) :
                for k, n in gen (ck, cn) :
                    yield k, n
        v = self.value
        return gen (v [-1] if v else "", self)
    # end def pre_order

    def values (self) :
        for node in self :
            if node.value :
                yield node.value
    # end def values

    def visualized (self) :
        children = self.children
        value    = self.value
        kind     = "Node" if self.parent else "Root"
        tail     = ""
        if children :
            tail = "\n  ".join \
                ( itertools.chain
                    ( * (   c.visualized ().split ("\n")
                        for c in children.itervalues ()
                        )
                    )
                ,
                )
        if value :
            if tail :
                fmt = "<Value %s\n  %s\n>"
            else :
                fmt = "<Value %s%s>"
            return fmt % (value, tail)
        elif children :
            return "<%s\n  %s\n>" % (kind, tail)
        else :
            return "<%s>" % (kind, )
    # end def visualized

    def __iter__ (self) :
        for key, node in self.pre_order () :
            yield node
    # end def __iter__

    def __repr__ (self) :
        children = self.children
        value    = self.value
        kind     = "Node" if self.parent else "Root"
        if value :
            if children :
                fmt = "<%s ...>"
            else :
                fmt = "<%s>"
            return fmt % (value, )
        else :
            return "<%s>" % (kind, )
    # end def __repr__

    if __debug__ :
        def __setattr__ (self, name, value) :
            if name == "value" :
                old = getattr (self, name, None)
                if not (value == old or value is None or old is None) :
                    raise AttributeError \
                        ("Cannot change value from %s to %s" % (old, value))
            object.__setattr__ (self, name, value)
        # end def __setattr__

# end class Node

class Word_Trie (TFL.Meta.Object) :
    """Trie (prefix tree) for words.

    >>> wt = Word_Trie (
    ...   "ada", "adam", "beta", "cab", "cabby", "cat", "cats", "cathy", "cub")
    >>> list (wt.values ())
    ['ada', 'adam', 'beta', 'cab', 'cabby', 'cat', 'cathy', 'cats', 'cub']
    >>> list (str (node) for key, node in  wt.pre_order ())
    ['<Root>', '<Node>', '<Node>', '<ada ...>', '<adam>', '<Node>', '<Node>',\
    '<Node>', '<beta>', '<Node>', '<Node>', '<cab ...>', '<Node>', '<cabby>',\
    '<cat ...>', '<Node>', '<cathy>', '<cats>', '<Node>', '<cub>']
    >>> list (repr (key) for key, node in  wt.pre_order ())
    ["''", "'a'", "'d'", "'a'", "'m'", "'b'", "'e'", "'t'", "'a'", "'c'",\
    "'a'", "'b'", "'b'", "'y'", "'t'", "'h'", "'y'", "'s'", "'u'", "'b'"]

    >>> wt.fuzzy_matches ("cat", 0)
    [('cat', 0)]
    >>> wt.fuzzy_matches ("cat", 1)
    [('cab', 1), ('cat', 0), ('cats', 1)]
    >>> wt.fuzzy_matches ("cat", 2)
    [('cab', 1), ('cat', 0), ('cathy', 2), ('cats', 1), ('cub', 2)]

    >>> wt.fuzzy_matches ("cit", 0)
    []
    >>> wt.fuzzy_matches ("cit", 1)
    [('cat', 1)]
    >>> wt.fuzzy_matches ("cit", 2)
    [('cab', 2), ('cat', 1), ('cats', 2), ('cub', 2)]

    >>> print wt
    Word_Trie ('ada', 'adam', 'beta', 'cab', 'cabby', 'cat', 'cathy',\
        'cats', 'cub')
    >>> print wt.visualized ()
    <Root
      <Node
        <Node
          <Value ada
            <Value adam>
          >
        >
      >
      <Node
        <Node
          <Value cab
            <Node
              <Value cabby>
            >
          >
          <Value cat
            <Node
              <Value cathy>
            >
            <Value cats>
          >
        >
        <Node
          <Value cub>
        >
      >
      <Node
        <Node
          <Node
            <Value beta>
          >
        >
      >
    >
    >>> print wt.find ("ca").visualized ()
    <Node
      <Value cab
        <Node
          <Value cabby>
        >
      >
      <Value cat
        <Node
          <Value cathy>
        >
        <Value cats>
      >
    >
    >>> wt.discard ("cab")
    True
    >>> print wt.find ("ca").visualized ()
    <Node
      <Node
        <Node
          <Value cabby>
        >
      >
      <Value cat
        <Node
          <Value cathy>
        >
        <Value cats>
      >
    >
    >>> wt.discard ("cabby")
    True
    >>> print wt.find ("ca").visualized ()
    <Node
      <Value cat
        <Node
          <Value cathy>
        >
        <Value cats>
      >
    >
    >>> list (wt.values ())
    ['ada', 'adam', 'beta', 'cat', 'cathy', 'cats', 'cub']
    >>> list (str (node) for key, node in wt.pre_order ())
    ['<Root>', '<Node>', '<Node>', '<ada ...>', '<adam>', '<Node>', '<Node>',\
    '<Node>', '<beta>', '<Node>', '<Node>', '<cat ...>', '<Node>', '<cathy>',\
    '<cats>', '<Node>', '<cub>']
    >>> list (repr (key) for key, node in wt.pre_order ())
    ["''", "'a'", "'d'", "'a'", "'m'", "'b'", "'e'",\
    "'t'", "'a'", "'c'", "'a'", "'t'", "'h'", "'y'",\
    "'s'", "'u'", "'b'"]

from _TFL.Trie import *
wt = Word_Trie ("ada", "adam", "beta", "cab", "cabby", "cat", "cats", "cathy", "cub")
    """

    def __init__ (self, * words) :
        self.root = Node (None)
        for w in words :
            self.add (w)
    # end def __init__

    def add (self, word) :
        return self._add (word, self.root)
    # end def add

    def closest (self, word) :
        if word :
            result = self.root
            for c in word :
                try :
                    result = result.children [c]
                except KeyError :
                    return result, None
            return result, True
    # end def closest

    def discard (self, word) :
        node, found = self.closest (word)
        if found :
            node.value = None
            for c in reversed (word) :
                parent = node.parent
                if node.children or not parent :
                    break
                del parent.children [c]
                node.parent = None
                node        = parent
        return found
    # end def discard

    def find (self, word) :
        node, found = self.closest (word)
        return found and node
    # end def find

    def fuzzy_match_iter (self, word, max_edits) :
        """Generate all words with a Levenshtein-distance <= max_edits to word."""
        ### http://en.wikipedia.org/wiki/Levenshtein_distance
        ### http://stevehanov.ca/blog/index.php?id=114
        row_1  = range (len (word) + 1)
        for char, node in self.root.children.iteritems () :
            for m in self._match_iter (char, node, word, max_edits, row_1) :
                yield m
    # end def fuzzy_match_iter

    def fuzzy_matches (self, word, max_edits) :
        return list (self.fuzzy_match_iter (word, max_edits))
    # end def fuzzy_matches

    def longest_prefix (self, word) :
        node, found = self.closest (word)
        return node
    # end def longest_prefix

    def pre_order (self) :
        return self.root.pre_order ()
    # end def pre_order

    def remove (self, word) :
        if not self.discard (word) :
            raise KeyError (word)
    # end def remove

    def values (self) :
        return self.root.values ()
    # end def values

    def visualized (self) :
        return self.root.visualized ()
    # end def visualized

    def _add (self, word, node) :
        for c in word :
            if c not in node.children :
                node.children [c] = Node (node)
            node = node.children [c]
        node.value = word
        return node
    # end def _add

    def _match_iter (self, char, node, word, max_edits, row_p) :
        wlen  = len (word)
        row_c = [row_p [0] + 1] + [0] * wlen
        for col in range (1, wlen + 1) :
            row_c [col] = min \
                ( row_p [col]     + 1                        # a  deletion
                , row_c [col - 1] + 1                        # an insertion
                , row_p [col - 1] + (word [col - 1] != char) # a  replacement
                )
        ### row_c [-1] now contains the edit distance between
        ### `word` and `node.value`, if any
        if row_c [-1] <= max_edits and node.value is not None :
            yield (node.value, row_c [-1])
        if any (c <= max_edits for c in row_c) :
            for char, node in node.children.iteritems () :
                for m in self._match_iter (char, node, word, max_edits, row_c) :
                    yield m
    # end def _match_iter

    def __iter__ (self) :
        return iter (self.root)
    # end def __iter__

    def __str__ (self) :
        return "%s (%s)" % \
            ( self.__class__.__name__
            , ", ".join (repr (w) for w in self.values ())
            )
    # end def __str__

# end class Word_Trie

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Trie
