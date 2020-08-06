from PySide2 import QtCore
from .file_utils import getFileSequencesFromPaths, formatFileSequenceAsRangePath, sizeof_fmt
import os

class FileSequenceProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self,parent=None):
        super(FileSequenceProxyModel,self).__init__(parent)
        self._detectFileSequences = True
        self.fileSequences = []
        self._directoryLoaded = False

    def detectFileSequences(self,input_value):
        self._detectFileSequences = input_value

    def handleRootPathChanged(self):
        self._directoryLoaded = False
        self.fileSequences = []
        if self.sourceModel().rootPath() == '/':
            self.handleDirectoryLoaded()

    def handleDirectoryLoaded(self):
        model = self.sourceModel()
        root_idx = model.index(model.rootPath(),0)
        num_rows = model.rowCount(root_idx)
        paths = [model.filePath(model.index(row, 0, root_idx)) for row in range(0, num_rows)]
        file_sequences = getFileSequencesFromPaths(paths)
        self.fileSequences = []
        for file_sequence in file_sequences:
            if len(file_sequence) > 1 and os.path.isfile(file_sequence[0]):
                self.fileSequences.append(file_sequence)
        for file_seq in self.fileSequences:
            file_seq.dataSize = 0
            for path in list(file_seq):
                file_seq.dataSize += model.size(model.index(path,0))
        self._directoryLoaded = True
        self.invalidate()

    def connectSignals(self):
        self.sourceModel().rootPathChanged.connect(self.handleRootPathChanged)
        self.sourceModel().directoryLoaded.connect(self.handleDirectoryLoaded)

    def filterAcceptsRow(self, source_row, parent):
        model = self.sourceModel()
        if model.filePath(parent) == model.rootPath():
            if not self._directoryLoaded:
                return False
            index0 = model.index(source_row, 0, parent)
            path = model.filePath(index0)
            for file_seq in self.fileSequences:
                paths = list(file_seq)
                if path in paths and path != paths[0]:
                    return False
        return True

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole and len(self.fileSequences) > 0:
            if not index.isValid():
                return None
            source_index = self.mapToSource(index)
            col_number = source_index.column()
            if col_number in [0,1]:
                model = self.sourceModel()
                path = model.filePath(source_index)
                file_seq = self.getSequenceForPath(path)
                if file_seq:
                    if col_number == 0:
                        return formatFileSequenceAsRangePath(file_seq)
                    if col_number == 1:
                        return sizeof_fmt(file_seq.dataSize)
        return super(FileSequenceProxyModel,self).data(index,role)

    def getSequenceForPath(self,path):
        for file_seq in self.fileSequences:
            if path in list(file_seq):
                return file_seq
        return None