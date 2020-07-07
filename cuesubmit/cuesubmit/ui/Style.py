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


class NoMarginsStyle(QtWidgets.QProxyStyle):
    def pixelMetric(self, QStyle_PixelMetric, QStyleOption_option=None, QWidget_widget=None):
        if QStyle_PixelMetric == QtWidgets.QStyle.PM_LayoutLeftMargin:
            return 0
        if QStyle_PixelMetric == QtWidgets.QStyle.PM_LayoutRightMargin:
            return 0
        if QStyle_PixelMetric == QtWidgets.QStyle.PM_LayoutTopMargin:
            return 0
        if QStyle_PixelMetric == QtWidgets.QStyle.PM_LayoutBottomMargin:
            return 0
        else:
            return QtWidgets.QCommonStyle.pixelMetric(self, QStyle_PixelMetric, QStyleOption_option=QStyleOption_option,
                                                           QWidget_widget=QWidget_widget)

