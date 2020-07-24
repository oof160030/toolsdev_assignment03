import maya.cmds as cmds
from pymel.core.system import Path
import pymel.core.system as System
import pymel.core as pmc
from os import listdir

class SceneFile(object):
    """This class handles file retrieval and parsing It stores a list of
    files in the folder provided

    Attributes:
        dir - the directory to the file
        files[] - list of all valid files in the folder
    """

    def __init__(self, dir=''):
        """Defines target directory and creates list of files"""
        self._dir = dir
        self.setTargetFolder(self._dir)
        self.fileList = []

    def setTargetFolder(self, dir):
        self.targetFolder = self.path(dir)
        self._dir = dir

    def getFileList(self):
        self.fileList = listdir(self._dir)
        return self.fileList

    def path(self, directory):
        """returns path to provided directory"""
        return Path(directory)

    def validateDir(self):
        return Path.exists(self.path(self._dir))

    def importFile(self, fileName):
        """Receives filename as a string, imports file"""
        filePath = self._dir + "/" + fileName
        print(filePath)
        System.importFile(filePath)