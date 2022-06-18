from random import choice

import sys

from Messages.ControlSystemMessage import ControlSystemCommands, ControlSystemMessageParams, createControlSystemMessage
sys.path.append('..')
from Components.Constants import CuratorType
from Services.DataBaseService import *
from Services.SocketService import *
from Messages.SenderInfo import *
from Messages.CuratorMessage import *

class CuratorSystemComponent():

    def __init__(self, dbService, socketService):
        self.log = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        self.dbService : DataBaseService = dbService
        self.socketService : SocketService = socketService
        self.type = 'Component'
        self.id = None
    
    def __exit__(self):
        self.dbService.__exit__()
        self.socketService.__exit__()

    def getSenderInfo(self):
        return SenderInfo(self.type, self.id, self.socketService.hostIp, self.socketService.port)

    def getEventGenerator(self):
        generators = self.dbService.select(self.dbService.SELECT_CURATORS_WITH_TYPE, (CuratorType.generator,))
        if len(generators) > 0:
            return generators[0]
        else: 
            return None
    
    def sendToRandomCurator(self, fact):
        ids = self.dbService.select(self.dbService.SELECT_CURATOR_IDS_WITH_FUNCTION, (fact.__class__.__name__,))
        if len(ids) == 0:
            self.log.error('Curator with such functions does not exist')
            return False, None
        id = choice(ids)['curator_id']
        curator = self.dbService.select(self.dbService.SELECT_CURATOR_WITH_ID, (id,))[0]
        msg = createCuratorMessage(self.getSenderInfo(), fact)
        self.socketService.send(curator['host'], curator['port'], msg)
        return True, id

    def sendToCurator(self, id, fact):
        res = self.dbService.select(self.dbService.SELECT_CURATOR_WITH_ID, (id,))
        if len(res) == 0:
            self.log.error('Curator with id=' + str(id) + ' does not exist')
            return False
        curator = res[0]
        msg = createCuratorMessage(self.getSenderInfo(), fact)
        self.socketService.send(curator['host'], curator['port'], msg)
        return True

    def sendToOtherCurators(self, fact):
        curators = self.dbService.select(self.dbService.SELECT_OTHER_CURATORS, (self.id,))
        msg = createCuratorMessage(self.getSenderInfo(), fact)
        for curator in curators:
            self.socketService.send(curator['host'], curator['port'], msg)

    def sendToEventGenerator(self, fact):
        generator = self.getEventGenerator()
        if generator is None:
            self.log.error('EventGenerator does not exist')
            return
        msg = createCuratorMessage(self.getSenderInfo(), fact)
        self.socketService.send(generator['host'], generator['port'], msg)

    def sendToAllCurators(self, msg):
        curators = self.dbService.select(self.dbService.SELECT_ALL_CURATORS, None)
        for curator in curators:
            self.socketService.send(curator['host'], curator['port'], msg)
