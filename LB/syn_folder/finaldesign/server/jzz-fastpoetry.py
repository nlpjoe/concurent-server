# -*- coding: UTF-8 -*-.

# tac(Twisted Application Configuration)


port = 10000
from twisted.internet import gtkreactor # for gtk-1.2
gtkreactor.install()

from twisted.internet import reactor
