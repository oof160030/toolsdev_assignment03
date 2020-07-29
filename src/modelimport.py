import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from pymel.core.system import Path

import maya.cmds as cmds

import filereader

def maya_main_window():
    """Return maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class modelimport(QtWidgets.QDialog):
    """This class creates a ser interface that enables file viewing and importing"""
    def __init__(self):
        '''Constructor'''
        #Makes constructor compatible with both python 2 and 3
        super(modelimport, self).__init__(parent=maya_main_window())
        '''Setup connection to filereader'''
        self.manager = filereader.SceneFile()
        self.validExtensions = ["ma", "obj", "fbx"]
        self.myPath = Path.splitpath(Path(__file__))[0]

        '''Setup new python window'''
        self.setWindowTitle("3D Model Import")
        self.resize(1000,800)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create Widgets for UI"""
        self.title_lbl = QtWidgets.QLabel("File Import")
        self.title_lbl.setStyleSheet("font: bold 50px")

        self.dir_le = QtWidgets.QLineEdit()
        self.dir_le.setPlaceholderText("No search directory entered")
        self.browse_btn = QtWidgets.QPushButton("Browse")

        self.files_lbl = QtWidgets.QLabel("Available Models to Import")
        self.files_list = QtWidgets.QListWidget()
        self.files_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection);

        self.search_le = QtWidgets.QLineEdit()
        self.search_le.setPlaceholderText("Enter search term...")

        self.filter_btn = QtWidgets.QPushButton("Filter")
        self.clear_btn = QtWidgets.QPushButton("Clear")
        self.ext_dropList = QtWidgets.QComboBox()
        self.ext_dropList.addItems(["All ext."])
        for ext in self.validExtensions:
            self.ext_dropList.addItem("." + ext)

        self.import_btn = QtWidgets.QPushButton("Import File")

        self.m_import_spinbox = QtWidgets.QSpinBox()
        self.m_import_spinbox.setRange(2,10)
        self.m_import_spinbox.setValue(2)
        self.m_import_btn = QtWidgets.QPushButton("Import " + str(self.m_import_spinbox.value()) + " Copies of File")

    def create_layout(self):
        """Create Layout for UI Window"""
        self.UI_layout = QtWidgets.QVBoxLayout()

        self.directory_lay = QtWidgets.QHBoxLayout()
        self.directory_lay.addWidget(self.dir_le)
        self.directory_lay.addWidget(self.browse_btn)

        self.files_lay = QtWidgets.QVBoxLayout()
        self.files_lay.addWidget(self.files_lbl)
        self.files_lay.addWidget(self.files_list)

        self.search_lay = QtWidgets.QHBoxLayout()
        self.search_lay.addWidget(self.filter_btn)
        self.search_lay.addWidget(self.clear_btn)
        self.search_lay.addWidget(self.ext_dropList)

        self.m_search_lay = QtWidgets.QHBoxLayout()
        self.m_search_lay.addWidget(self.m_import_spinbox)
        self.m_search_lay.addWidget(self.m_import_btn)

        self.UI_layout.addWidget(self.title_lbl)
        self.UI_layout.addLayout(self.directory_lay)
        self.UI_layout.addLayout(self.files_lay)
        self.UI_layout.addWidget(self.search_le)
        self.UI_layout.addLayout(self.search_lay)
        self.UI_layout.addWidget(self.import_btn)
        self.UI_layout.addLayout(self.m_search_lay)

        self.setLayout(self.UI_layout)

    def create_connections(self):
        """Creates connections between widgets and methods"""
        self.browse_btn.clicked.connect(self.browse)
        self.import_btn.clicked.connect(self._import_file)
        self.filter_btn.clicked.connect(self._refreshFiles)
        self.clear_btn.clicked.connect(self._clearFilter)
        self.m_import_btn.clicked.connect(self._import_file_multiple)

        self.m_import_spinbox.valueChanged.connect(self.spinbox_edit)
        self.ext_dropList.currentIndexChanged.connect(self._refreshFiles)

    @QtCore.Slot()
    def browse(self):
        """Opens file browser to select folder to fetch files from"""
        folderDirectory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder",
                                                                     self.dir_le.text(),
                                                                     QtWidgets.QFileDialog.ShowDirsOnly)
        if folderDirectory != '':
            self.dir_le.setText(folderDirectory)
            self.manager.setTargetFolder(folderDirectory)
            listOfFiles = self.manager.getFileList()
            self.files_list.clear()
            for file in listOfFiles:
                self._addListItem(file)

    def _refreshFiles(self):
        """Refreshes the list of files, applying filters for extension and name"""
        if(self.manager.validateDir()):
            self.files_list.clear()
            listOfFiles = self.manager.getFileList()

            for file in listOfFiles:
                fileSplit = file.split(".")
                validExtension = self.ext_dropList.currentIndex() is 0 or str("." + fileSplit[1]) == self.ext_dropList.currentText()
                validFileName = self.search_le.text() is "" or self.search_le.text() in fileSplit[0]
                if validExtension and validFileName:
                    self._addListItem(file)

    def _addListItem(self, fileName):
        """Adds a list element to our current file list (including assigning a specific icon)"""
        fileExt = fileName.split(".")[1]
        if(fileExt == 'ma'):
            QtWidgets.QListWidgetItem(QtGui.QIcon(str(self.myPath + "\ma_icon.png")),fileName, self.files_list)
        elif(fileExt == 'obj'):
            QtWidgets.QListWidgetItem(QtGui.QIcon(str(self.myPath + "\obj_icon.png")),fileName, self.files_list)
        elif (fileExt == 'fbx'):
            QtWidgets.QListWidgetItem(QtGui.QIcon(str(self.myPath + "\\fbx_icon.png")), fileName, self.files_list)

    @QtCore.Slot()
    def _import_file(self):
        """Imports the selected file to the scene"""
        currentItem = self.files_list.currentItem()
        if(isinstance(currentItem,QtWidgets.QListWidgetItem)):
            stringToFile = self.manager.getDir() + "\\" + currentItem.text()
            """print(stringToFile)"""
            cmds.file(stringToFile, i=True, gr=True, gn=currentItem.text().split(".")[0] + "_ImportGroup",
                                 mnc=True, pr=False, rdn=False, rnn=True)

    @QtCore.Slot()
    def _import_file_multiple(self):
        """Repeats a file import up to 10 times for faster use"""
        currentItem = self.files_list.currentItem()
        if (isinstance(currentItem, QtWidgets.QListWidgetItem)):
            xLoop = 0
            while xLoop < self.m_import_spinbox.value():
                stringToFile = self.manager.getDir() + "\\" + currentItem.text()
                groupName = currentItem.text().split(".")[0] + "_ImportGroup"
                newNodes = cmds.file(stringToFile, i=True, gr=True, gn=groupName + str(xLoop+1),
                                     pr=False, rdn=False, rnn=True)
                for node in newNodes:
                    nodePath = cmds.ls(node, sn=True)[0]
                    nodeName = nodePath.split("|")[-1]
                    if groupName in nodeName:
                        cmds.xform(node,t=(0,0,2*xLoop))
                xLoop += 1

    @QtCore.Slot()
    def _clearFilter(self):
        """Resets the text filter for files"""
        self.search_le.setText("")
        self._refreshFiles()

    def spinbox_edit(self):
        """Updates the multi-import button label based on number to import"""
        self.m_import_btn.setText("Import " + str(self.m_import_spinbox.value()) + " Copies of File")
