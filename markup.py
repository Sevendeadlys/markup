#coding=utf-8

import sys,re
from handlers import *
from util import *
from rules import *

class Parser:
    def __init__(self,handler):
        self.handler = handler
        self.rules = []
        self.filters = []

    def addRule(self,rule):
        self.rules.append(rule)

    def addFilter(self, patten, name):
        def filter(block, handler):
            return re.sub(patten, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, f):
        self.handler.start('document')
        for block in blocks(f):
            for filter in self.filters:
                block = filter(block,self.handler)

            for rule in self.rules:
                if rule.condition(block):
                    last = rule.action(block,self.handler)
                    if last: break
        self.handler.end('document')

class BasicTextParser(Parser):
    def __init__(self, handler):
        """

        :rtype : object
        """
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z0-9/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z0-9]+@[\.a-zA-Z0-9]+[a-zA-Z0-9]+)', 'mail')

if __name__ == '__main__':
    handler = HTMLRender()
    parse = BasicTextParser(handler)
    try:
        f = open(sys.argv[1], 'r')
        parse.parse(f)
        f.close()
    except IOError:
        print 'IOerror'
