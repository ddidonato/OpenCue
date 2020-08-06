from PySide2 import QtWidgets

from .file_sequence_proxy_model import FileSequenceProxyModel

class DDFileBrowser(QtWidgets.QFileDialog):
    def __init__(self, parent=None, selectFolders=False, fileTypes=[], detectFileSequences=True, multiSelect=True):
        super(DDFileBrowser,self).__init__(parent)
        self._detectFileSequences = detectFileSequences
        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        self.setContentsMargins(8, 8, 2, 0)
        if selectFolders:
            self.setFileMode(QtWidgets.QFileDialog.Directory)
        else:
            fileType = 'All Files (*.*)'
            if len(fileTypes) > 0:
                file_string_list = ["*.{0}".format(file_type) for file_type in fileTypes]
                fileType = "Custom ({})".format(' '.join(file_string_list))
            self.setNameFilter(fileType)
            if detectFileSequences:
                proxy_model = FileSequenceProxyModel(self)
                self.setProxyModel(proxy_model)
                proxy_model.connectSignals()
            if multiSelect:
                self.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
            else:
                self.setFileMode(QtWidgets.QFileDialog.ExistingFile)

    def selectedFiles(self):
        selected_files = super(DDFileBrowser,self).selectedFiles()
        if self._detectFileSequences:
            selected_files_with_sequences = []
            for selected_file in selected_files:
                file_seq = self.proxyModel().getSequenceForPath(selected_file)
                if file_seq:
                    selected_files_with_sequences += list(file_seq)
                else:
                    selected_files_with_sequences.append(selected_file)
            return selected_files_with_sequences
        return selected_files