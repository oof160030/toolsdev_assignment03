import maya.cmds as cmds
from pymel.core.system import Path
import pymel.core.system as System
import pymel.core as pmc
from os import listdir

class SceneFile(object):
    """This class handles file retrieval and parsing It stores a list of
    files in the folder provided

    Attributes:
        _dir - the directory to the file
        targetFolder - the Path object representing _dir
        fileList[] - list of all valid files in the folder
    """

    def __init__(self, dir=''):
        """Defines target directory and creates list of files"""
        self._dir = dir
        self.setTargetFolder(self._dir)
        self.fileList = []

    def setTargetFolder(self, dir):
        """Saves a given file path and directory for later use"""
        self.targetFolder = self.path(dir)
        self._dir = dir

    def getFileList(self):
        """Retrieve a list of all files in the target folder"""
        self.fileList = listdir(self._dir)
        return self.fileList

    def path(self, directory):
        """returns path to provided directory"""
        return Path(directory)

    def getDir(self):
        return self._dir

    def validateDir(self):
        """Checks if the current target directory exists"""
        return Path.exists(self.path(self._dir))

    def importFile(self, fileName):
        """Receives filename as a string, imports file"""
        filePath = self._dir + "/" + fileName
        """print(filePath)"""
        return System.importFile(filePath)