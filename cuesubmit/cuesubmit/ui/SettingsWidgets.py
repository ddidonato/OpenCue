from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from PySide2 import QtCore, QtWidgets

from cuesubmit import Constants
from cuesubmit.ui import Command
from cuesubmit.ui import Widgets


class BaseSettingsWidget(QtWidgets.QWidget):
    """Swappable widget to provide application specific settings. """

    dataChanged = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(BaseSettingsWidget, self).__init__(parent)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

    def getCommandData(self):
        """Override this method to return a dictionary of the settings data."""
        raise NotImplementedError

    def setCommandData(self, commandData):
        """Given a settings data dictionary, set this widget's data."""
        raise NotImplementedError


class InMayaSettings(BaseSettingsWidget):
    """Settings widget to be used when launching from within Maya."""

    def __init__(self, cameras=[], filename='', project='', parent=None, *args, **kwargs):
        super(InMayaSettings, self).__init__(parent=parent)
        self._filename = filename
        self._project = project
        self.mayaFileInput = Widgets.CueLabelFileSelect(
            'Maya File:', fileTypes=['ma', 'mb']
        )
        if self._filename:
            self.mayaFileInput.fileSelect.setSelected(self._filename)
        self.mayaProjectInput = Widgets.CueLabelFileSelect(
            'Maya Project:', selectFolders=True
        )
        if self._project:
            self.mayaProjectInput.fileSelect.setSelected(self._project)
        self.cameraSelector = Widgets.CueSelectPulldown('Render Cameras', options=cameras)
        self.selectorLayout = QtWidgets.QHBoxLayout()
        super(InMayaSettings, self).__init__(parent=parent)

    def setupUi(self):
        super(InMayaSettings, self).setupUi()
        self.selectorLayout.addWidget(self.cameraSelector)
        self.mainLayout.addLayout(self.selectorLayout)

    def setCommandData(self, commandData):
        self.mayaFileInput.fileSelect.setSelected(commandData.get('mayaFile', self._filename))
        self.mayaProjectInput.fileSelect.setSelected(commandData.get('mayaProject', self._project))
        self.cameraSelector.setChecked(commandData.get('camera', '').split(','))

    def getCommandData(self):
        return {
            'mayaFile': self.mayaFileInput.fileSelect.selected(),
            'mayaProject': self.mayaProjectInput.fileSelect.selected(),
            'camera': self.cameraSelector.text(),
        }


class BaseMayaSettings(BaseSettingsWidget):
    """Standard Maya settings widget to be used from outside Maya."""

    def __init__(self, parent=None, *args, **kwargs):
        super(BaseMayaSettings, self).__init__(parent=parent)
        self.mayaFileInput = Widgets.CueLabelFileSelect('Maya File:', fileTypes=['ma', 'mb'], multiSelect=False)
        self.mayaProjectInput = Widgets.CueLabelFileSelect('Maya Project:', selectFolders=True, multiSelect=False)
        self.setupUi()
        self.setupConnections()

    def setupUi(self):
        self.mainLayout.addWidget(self.mayaFileInput)
        self.mainLayout.addWidget(self.mayaProjectInput)

    def setupConnections(self):
        self.mayaFileInput.fileSelect.selectionChanged.connect(self.dataChanged.emit)
        self.mayaProjectInput.fileSelect.selectionChanged.connect(self.dataChanged.emit)

    def setCommandData(self, commandData):
        self.mayaFileInput.fileSelect.setSelected(commandData.get('mayaFile', None))
        self.mayaProjectInput.fileSelect.setSelected(commandData.get('mayaProject', None))

    def getCommandData(self):
        return {
            'mayaFile': self.mayaFileInput.selected(),
            'mayaProject': self.mayaProjectInput.selected(),
        }


class InNukeSettings(BaseSettingsWidget):
    """Settings widget to be used when launching from within Nuke."""

    def __init__(self, writeNodes=None, filename=None, parent=None, *args, **kwargs):
        super(InNukeSettings, self).__init__(parent=parent)
        self.fileInput = Widgets.CueLabelFileSelect(
            'Nuke File:', fileTypes=['nk'], multiSelect=False, selectFolders=False
        )
        if filename:
            self.fileInput.fileSelect.setSelected(filename)
        self.writeNodeSelector = Widgets.CueSelectPulldown('Write Nodes:', emptyText='[All]',
                                                           options=writeNodes)
        self.selectorLayout = QtWidgets.QHBoxLayout()
        self.setupUi()

    def setupUi(self):
        self.mainLayout.addWidget(self.fileInput)
        self.selectorLayout.addWidget(self.writeNodeSelector)
        self.mainLayout.addLayout(self.selectorLayout)

    def setCommandData(self, commandData):
        self.fileInput.fileSelect.setSelected(commandData.get('nukeFile', None))
        self.writeNodeSelector.setChecked(commandData.get('writeNodes', '').split(','))

    def getCommandData(self):
        return {
            'nukeFile': self.fileInput.fileSelect.selected(),
            'writeNodes': self.writeNodeSelector.text()
        }


class BaseNukeSettings(BaseSettingsWidget):
    """Standard Nuke settings widget to be used from outside Nuke."""

    def __init__(self, parent=None, *args, **kwargs):
        super(BaseNukeSettings, self).__init__(parent=parent)
        self.fileInput = Widgets.CueLabelFileSelect(
            'Nuke File:', fileTypes=['nk'], multiSelect=False, selectFolders=False
        )
        self.setupUi()
        self.setupConnections()

    def setupUi(self):
        self.mainLayout.addWidget(self.fileInput)

    def setupConnections(self):
        self.fileInput.fileSelect.selectionChanged.connect(self.dataChanged.emit)

    def setCommandData(self, commandData):
        self.fileInput.fileSelect.setSelected(commandData.get('nukeFile', None))

    def getCommandData(self):
        return {
            'nukeFile': self.fileInput.fileSelect.selected(),
        }


class ShellSettings(BaseSettingsWidget):
    """Basic settings widget for submitting simple shell commands."""

    def __init__(self, parent=None, *args, **kwargs):
        super(ShellSettings, self).__init__(parent=parent)

        self.commandTextBox = Command.CueCommandWidget()

        self.setupUi()
        self.setupConnections()

    def setupUi(self):
        self.mainLayout.addWidget(self.commandTextBox)

    def setupConnections(self):
        self.commandTextBox.textChanged.connect(lambda: self.dataChanged.emit(None))

    def getCommandData(self):
        return {'commandTextBox': self.commandTextBox.text()}

    def setCommandData(self, commandData):
        self.commandTextBox.setText(commandData.get('commandTextBox', ''))


class BaseBlenderSettings(BaseSettingsWidget):
    """Standard Blender settings widget to be used from outside Blender."""

    def __init__(self, parent=None, *args, **kwargs):
        super(BaseBlenderSettings, self).__init__(parent=parent)
        self.fileInput = Widgets.CueLabelFileSelect(
            'Blender File:', fileTypes=['blend'], selectFolders=False, multiSelect=False
        )
        self.outputPath = Widgets.CueLabelFileSelect(
            'Output Path (Optional):', selectFolders=True, multiSelect=False, clearOnCancel=True
        )
        self.outputSelector = Widgets.CueSelectPulldown(
            'Output Format (Optional)', options=Constants.BLENDER_FORMATS, multiselect=False
        )
        self.outputLayout = QtWidgets.QHBoxLayout()
        self.setupUi()
        self.setupConnections()

    def setupUi(self):
        self.mainLayout.addWidget(self.fileInput)
        self.outputSelector.toolButton.setFixedWidth(120)
        self.outputLayout.addWidget(self.outputSelector)
        self.outputLayout.addStretch(1)
        self.outputLayout.setStretchFactor(self.outputSelector, 0)
        self.mainLayout.addLayout(self.outputLayout)
        self.mainLayout.addWidget(self.outputPath)

    def setupConnections(self):
        self.fileInput.fileSelect.selectionChanged.connect(self.dataChanged.emit)
        self.outputPath.fileSelect.selectionChanged.connect(self.dataChanged.emit)

    def setCommandData(self, commandData):
        self.fileInput.fileSelect.setSelected(commandData.get('nukeFile', None))
        self.outputPath.fileSelect.setSelected(commandData.get('outputPath', None))
        self.outputSelector.setChecked(commandData.get('outputFormat', ''))

    def getCommandData(self):
        return {
            'blenderFile': self.fileInput.fileSelect.selected(),
            'outputPath': self.outputPath.fileSelect.selected(),
            'outputFormat': self.outputSelector.text()
        }


class BaseArnoldSettings(BaseSettingsWidget):
    def __init__(self, parent=None,  *args, **kwargs):
        super(BaseArnoldSettings, self).__init__(parent=parent)
        self.arnoldFileInput = Widgets.CueLabelFileSelect(
            'Arnold Files:', fileTypes=['ass'], detectFileSequences=True
        )
        self.renderFolderInput = Widgets.CueLabelFileSelect(
            'Render Folder (Optional):', selectFolders=True, clearOnCancel=True
        )
        self.renderFileInput = Widgets.CueLabelLineEdit('Render Filename (Optional):')
        self.renderFileInput.setVisible(False)
        self.fileTypeSelector = Widgets.CueSelectPulldown(
            'Render Filetype (Optional):', options=['','exr','jpg','png','tif'], multiselect=False
        )
        self.selectorLayout = QtWidgets.QHBoxLayout()
        self.setupUi()
        self.setupConnections()

    def setupUi(self):
        self.mainLayout.addWidget(self.arnoldFileInput)
        self.mainLayout.addWidget(self.renderFolderInput)
        self.mainLayout.addWidget(self.renderFileInput)
        self.fileTypeSelector.toolButton.setFixedWidth(120)
        self.selectorLayout.addWidget(self.fileTypeSelector)
        self.selectorLayout.addStretch(1)
        self.selectorLayout.setStretchFactor(self.fileTypeSelector, 0)
        self.mainLayout.addLayout(self.selectorLayout)
        self.renderFolderInput.setEnabled(False)
        self.fileTypeSelector.setEnabled(False)
        self.renderFileInput.setVisible(False)

    def setupConnections(self):
        self.arnoldFileInput.fileSelect.selectionChanged.connect(self.dataChanged.emit)
        self.arnoldFileInput.fileSelect.selectionChanged.connect(self.handleArnoldFileChange)
        self.renderFolderInput.fileSelect.selectionChanged.connect(self.dataChanged.emit)
        self.renderFolderInput.fileSelect.selectionChanged.connect(self.handleRenderFolderChange)
        self.renderFileInput.lineEdit.textChanged.connect(self.dataChanged.emit)
        self.fileTypeSelector.optionsMenu.triggered.connect(self.dataChanged.emit)
        self.fileTypeSelector.optionsMenu.triggered.connect(self.setRenderFileName)

    def handleRenderFolderChange(self):
        self.renderFileInput.setVisible(bool(self.renderFolderInput.fileSelect.selected()))
        self.setRenderFileName()

    def setRenderFileName(self):
        if self.arnoldFileInput.fileSelect.selected() and self.renderFolderInput.fileSelect.selected():
            file_sequence = self.arnoldFileInput.fileSelect.selected()
            file_sequence.setPadding('%0{}d'.format(file_sequence.zfill()))
            if not self.fileTypeSelector.text():
                self.fileTypeSelector.setChecked(['exr'])
            path_template = '{{basename}}{{padding}}.{0}'.format(self.fileTypeSelector.text())
            formatted_file_name = file_sequence.format(template=path_template)
            self.renderFileInput.setText(formatted_file_name)

    def handleArnoldFileChange(self):
        if self.arnoldFileInput.fileSelect.selected():
            self.renderFolderInput.setEnabled(True)
            self.fileTypeSelector.setEnabled(True)
            file_sequence = self.arnoldFileInput.fileSelect.selected()
            self.parent().parent().parent().parent().frameBox.frameSpecInput.setText(
                "{0}-{1}".format(file_sequence.start(), file_sequence.end())
            )
        else:
            self.parent().parent().parent().parent().frameBox.frameSpecInput.setText("")
            self.renderFolderInput.setEnabled(False)
            self.fileTypeSelector.setEnabled(False)
            self.renderFileInput.setVisible(False)
        self.setRenderFileName()

    def setCommandData(self, commandData):
        self.arnoldFileInput.fileSelect.setSelected(commandData.get('arnoldFile', None))
        self.renderFolderInput.fileSelect.setSelected(commandData.get('renderFolder', None))
        self.renderFileInput.setText(commandData.get('renderFile', ''))
        self.fileTypeSelector.setChecked(commandData.get('renderFileType', ''))

    def getCommandData(self):
        return_dict = {
            'arnoldFile': self.arnoldFileInput.fileSelect.selected(),
            'renderFolder': self.renderFolderInput.fileSelect.selected(),
            'renderFile': self.renderFileInput.text(),
            'renderFileType': self.fileTypeSelector.text(),
        }
        return return_dict
