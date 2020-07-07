from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from PySide2 import QtCore, QtGui, QtWidgets

DEFAULT_FONT = 'Luxi Sans'

def setFont(font):
    """sets the application font"""
    global Font
    Font = font
    QtGui.qApp.setFont(font)


def init():
    """initialize the global style settings"""
    setFont(DEFAULT_FONT)
