import re

__author__ = 'Bacon'
class Movie(object):
    # (W8329834)   (My Fair Lady)     (102) (0)
    pattern = re.compile("^([A-Z0-9]+)\s+(.+?)\s+([0-9]+)\s+([0-9]+)$")
    def __init__(self, text):
        (self.criterion_id, self.title, self.runtime, self.year) = self.pattern.search(text).groups()
        pass

    def __unicode__(self):
        return "\t".join([self.criterion_id, self.title, self.runtime, self.year]) + "\r\n"