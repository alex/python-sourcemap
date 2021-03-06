"""
sourcemap.objects
=================
"""
from bisect import bisect_right
from collections import namedtuple

class Token(object):
    def __init__(self, dst_line, dst_col, src, src_line, src_col, name):
        self.dst_line = dst_line
        self.dst_col = dst_col
        self.src = src
        self.src_line = src_line
        self.src_col = src_col
        self.name = name

    def __str__(self):
        return str(self.name)

    def __unicode__(self):
        return unicode(self.name)

    def __eq__(self, other):
        keys = ('dst_line', 'dst_col', 'src', 'src_line', 'src_col', 'name')
        for key in keys:
            if getattr(self, key) != getattr(other, key):
                return False
        return True

    def __repr__(self):
        args = self.dst_line, self.dst_col, self.src, self.src_line, self.src_col, self.name
        return '<Token: dst_line=%d dst_col=%d src=%r src_line=%d src_col=%d name=%r>' % args


class SourceMapIndex(object):
    def __init__(self, tokens, line_index, index, sources):
        self.tokens = tokens
        self.line_index = line_index
        self.index = index
        self.sources = sources

    def lookup(self, line, column):
        try:
            # Let's hope for a direct match first
            return self.index[(line, column)]
        except KeyError:
            pass

        # Figure out which line to search through
        line_index = self.line_index[line]
        # Find the closest column token
        i = bisect_right(line_index, column)
        if not i:
            # You're gonna have a bad time
            raise IndexError
        # We actually want the one less than current
        column = line_index[i - 1]
        # Return from the main index, based on the (line, column) tuple
        return self.index[(line, column)]

    def __getitem__(self, item):
        return self.tokens[item]

    def __iter__(self):
        return iter(self.tokens)

    def __repr__(self):
        return '<SourceMapIndex: %s>' % ', '.join(map(str, self.sources))

