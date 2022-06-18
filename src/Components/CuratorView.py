import logging, os
from io import StringIO
from typing import Dict
from datetime import datetime

class CuratorView:

    def __init__(self, id, type, curatorState, environmentState):
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        self.type = type
        self.name = type + '_' + str(id)
        self.curatorState = curatorState # data from fact as ResourceManagementCuratorState etc.
        self.environmentState = environmentState # data from fact EnvironmentState
        self.logStream = StringIO()

    def info(self, logMsg, curatorState, environmentState):
        self.logStream.write(logMsg)
        self.curatorState = curatorState # data from fact as ResourceManagementCuratorState etc.
        self.environmentState = environmentState # data from fact EnvironmentState

    def saveInFile(self, fileName):
        with open(fileName, 'w') as fd:
            fd.write(self.logStream.getvalue())
            self.log.debug('save log file: ' + fileName)

    def __exit__(self):
        self.logStream.close()

class CuratorsHolder:
    curators = {}
    generalLog = StringIO()
    curatorLogFmt = '%(asctime)s - %(curator)s : %(message)s\n'

    def __init__(self):
        logger = logging.getLogger("curatorEventLogger",)
        logger.setLevel(logging.DEBUG)

        fmt = '%(asctime)s - CURATOR EVENT - %(message)s'
        formatter = logging.Formatter(fmt)

        mainHandler = logging.StreamHandler()
        mainHandler.setFormatter(formatter)
        
        logger.addHandler(mainHandler)
        logger.propagate = False
        self.log = logger

    def register(self, id, type, curatorState, environmentState):
        self.curators[id] = CuratorView(id, type, curatorState, environmentState)

    def getLog(self, id):
        return self.curators[id].logStream.getvalue()

    def getGeneralLog(self):
        return self.generalLog.getvalue()
    
    def getState(self, id):
        return self.curators[id].curatorState, self.curators[id].environmentState

    def info(self, id, type, logMsg, curatorState, environmentState):
        curatorName = '%s_%s'%(type, id)
        self.log.info('%s : %s', curatorName, logMsg)
        record = self.__createRecord(curatorName, logMsg)

        self.curators[id].info(record, curatorState, environmentState)
        self.generalLog.write(record)

    def __createRecord(self, curatorName, msg):
        return self.curatorLogFmt%{'asctime':datetime.now(), 'curator':curatorName, 'message':msg}

    def __exit__(self):
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}",)
        rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logsDir = os.path.join(rootDir, 'Resources', 'logs')
        files = os.listdir(logsDir)
        for file in files:
            os.remove(os.path.join(logsDir, file))
            self.log.debug('delete file: ' + logsDir + '\\' + file)
            pass

        for curator in self.curators.values():
            fileName = os.path.join(logsDir, curator.name + '.txt')
            curator.saveInFile(fileName)
            curator.__exit__()

        fileName = os.path.join(logsDir, 'general_log.txt')
        with open(fileName, 'w') as fd:
            fd.write(self.generalLog.getvalue())
            self.generalLog.close()
            self.log.debug('save log file: ' + fileName)
