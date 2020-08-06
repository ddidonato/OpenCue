from PySide2 import QtCore,QtWidgets
import os
import logging
import traceback
from .file_utils import formatPathsAsFileSequences,getFileSequencesFromPaths
from .dd_file_browser import DDFileBrowser


class DDFileSelect(QtWidgets.QWidget):
    selectionChanged = QtCore.Signal(object)

    def __init__(self, defaultText='', parent=None, selectFolders=False, fileTypes=[], detectFileSequences=True,
                 multiSelect=True, clearOnCancel=False
         ):
        super(DDFileSelect,self).__init__(parent)
        self.fileBrowseButton = QtWidgets.QPushButton('...')
        self.fileBrowseButton.setFixedWidth(24)
        self._selectFolders = selectFolders
        self._fileTypes = fileTypes
        self._multiSelect = multiSelect
        self._clearOnCancel = clearOnCancel
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setText(defaultText)
        self.lineEdit.setReadOnly(True)
        self.setAcceptDrops(True)
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addWidget(self.lineEdit,0,0,1,1)
        self.mainLayout.addWidget(self.fileBrowseButton,0,1,1,1)
        self.setLayout(self.mainLayout)
        self.lineEdit.setReadOnly(True)
        self.fileBrowseButton.clicked.connect(self.handleFileButtonClick)
        self._detectFileSequences = detectFileSequences
        self._selected = []

    def selected(self, detectFileSequences=None):
        if detectFileSequences is None:
            detectFileSequences = self._detectFileSequences
        if detectFileSequences:
            return_data = getFileSequencesFromPaths(self._selected)
        else:
            return_data = self._selected
        if not self._multiSelect:
            if len(return_data) > 0:
                return return_data[0]
            return None
        return return_data

    def updateLabelText(self):
        # FIX THIS FOR ONLY 1 FILE
        paths = self._selected
        if self._detectFileSequences:
            paths = formatPathsAsFileSequences(paths)
        if len(paths) > 1:
            if not self._multiSelect:
                self.lineEdit.setText("Error")
            else:
                self.lineEdit.setText("Multiple selected")
        elif len(paths) == 1:
            self.lineEdit.setText(paths[0])
        else:
            self.lineEdit.setText("")

    def setSelected(self, paths):
        self._selected = []
        try:
            if paths:
                if not isinstance(paths, (list, tuple)):
                    paths = [paths]
                if self._selectFolders is False and len(paths) == 1 and os.path.isdir(paths[0]):
                    paths = [os.path.join(paths[0], f) for f in os.listdir(paths[0])]
                file_paths = []
                for path in paths:
                    if not os.path.basename(path).startswith('.'):
                        file_paths.append(path)
                self._selected = paths
            self.updateLabelText()
            self.selectionChanged.emit(self.selected())
        except:
            logging.error(traceback.format_exc())
            self.lineEdit.setText("Error")

    def handleFileButtonClick(self):
        file_browser = DDFileBrowser(
            self, selectFolders=self._selectFolders, fileTypes=self._fileTypes,
            detectFileSequences=self._detectFileSequences, multiSelect=self._multiSelect
        )
        result = file_browser.exec_()
        if result:
            self.setSelected(file_browser.selectedFiles())
        elif self._clearOnCancel:
            self.setSelected(None)

    def dropEvent(self, event):
        mime_data = event.mimeData()
        try:
            if mime_data.hasUrls():
                self.setSelected([url.toLocalFile() for url in mime_data.urls()])
                event.accept()
        except:
            logging.error(traceback.format_exc())
            self.lineEdit.setText("Error")

    def dragEnterEvent(self, event):
        super(DDFileSelect, self).dragEnterEvent(event)
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            event.accept()

    def dragMoveEvent(self, event):
        super(DDFileSelect, self).dragMoveEvent(event)
        event.accept()
