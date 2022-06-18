import logging, threading
from time import sleep

import sys

sys.path.append('..')
from Messages.ControlSystemMessage import *
from Components.Constants import CuratorState, CuratorType
from Components.CuratorSystemComponent import CuratorSystemComponent
from Components.CuratorView import CuratorsHolder

class ControlSystem(CuratorSystemComponent):

    def __init__(self, dbService, socketService):
        super().__init__(dbService, socketService)
        self.log = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        self.logHolder = CuratorsHolder()
        self.dbService.clear()
        self.type = 'ControlSystem'
    
    def start(self):
        self.thread1 = threading.Thread(target=self.socketService.listenAndSend, args=(self.__processMessage,)) 
        self.thread1.start()

    def getCurators(self):
        curators = []
        for id in self.logHolder.curators.keys():
            # if self.logHolder.curators[id].type != CuratorType.generator:
                curators.append({
                    'id': id, 
                    'type': self.logHolder.curators[id].type
                })
        return curators

    def getFullCuratorState(self, id):
        curatorState, environmentState = self.logHolder.getState(id)
        return {
            'state': None,
            'curatorState': curatorState,
            'environmentState': environmentState,
        }
    
    def getCuratorLog(self, id):
        return self.logHolder.getLog(id)

    def getGeneralCuratorLog(self):
        return self.logHolder.getGeneralLog()

    def sendGenerateCommand(self, generateValue: bool):
        generator = self.getEventGenerator()
        if not generator is None:
            self.socketService.send(generator['host'], generator['port'], createControlSystemMessage(self.getSenderInfo(), ControlSystemCommands.generate, {ControlSystemMessageParams.generate: generateValue}))
            return True
        else:
            return False
    
    def sendEvent(self, factName, fact):
        msg = createControlSystemMessage(self.getSenderInfo(), ControlSystemCommands.addEvent, {ControlSystemMessageParams.factName: factName, ControlSystemMessageParams.fact: fact})
        generator = self.getEventGenerator()
        if not generator is None:
            self.socketService.send(generator['host'], generator['port'], msg)
            return True
        else:
            return False

    def sendCloseCommand(self):
        self.sendToAllCurators(createControlSystemMessage(self.getSenderInfo(), ControlSystemCommands.close, None))

    def __processMessage(self, msg):
        msg : ControlSystemMessage = parseControlSystemMessage(msg)
        
        sender = msg.sender
        if msg.command == ControlSystemCommands.info:
            return self.__processLogMessage(sender, msg.params)
        elif msg.command == ControlSystemCommands.register:
            return self.__processRegisterMessage(sender, msg.params)
        elif msg.command == ControlSystemCommands.signOut:
            return self.__processSignOutMessage(sender)
        else:
            self.log.error('Unexpected message command: ' + str(msg.command))

    def __processRegisterMessage(self, sender: SenderInfo, params: dict):
        type = sender.type
        ip = sender.ip
        port = sender.port
        functions = params[ControlSystemMessageParams.functions]
        environmentState = params[ControlSystemMessageParams.environmentState]
        curatorState = params[ControlSystemMessageParams.curatorState]

        if type == CuratorType.generator:
            if not self.getEventGenerator() is None:
                return createControlSystemMessage(self.getSenderInfo(), ControlSystemCommands.register, {ControlSystemMessageParams.id:None})

        id = self.dbService.insert(self.dbService.INSERT_CURATOR, (type, CuratorState.active, ip, port))
        self.log.debug('write to DB curator ' + type + '_' + str(id))
        for f in functions:
            self.log.debug('write to DB function ' + f + ' for ' + type + '_' + str(id))
            self.dbService.insert(self.dbService.INSERT_CURATOR_FUNCTION, (id, f))

        self.logHolder.register(id, type, curatorState, environmentState)
        return createControlSystemMessage(self.getSenderInfo(), ControlSystemCommands.register, {ControlSystemMessageParams.id:id})

    def __processSignOutMessage(self, sender: SenderInfo):
        type = sender.type
        id = sender.id
        ip = sender.ip
        port = sender.port
        self.log.debug('delete from DB curator ' + type + '_' + str(id))
        self.dbService.delete(self.dbService.DELETE_CURATOR_FUNCTION, (id,))
        self.dbService.delete(self.dbService.DELETE_CURATOR, (id,))
        return "OK"

    def __processLogMessage(self, sender: SenderInfo, params: dict):
        type = sender.type
        id = sender.id
        ip = sender.ip
        port = sender.port
        logMsg = params[ControlSystemMessageParams.logMsg]
        environmentState = params[ControlSystemMessageParams.environmentState]
        curatorState = params[ControlSystemMessageParams.curatorState]
        self.logHolder.info(id, type, logMsg, curatorState, environmentState)
        return "OK"

    def __setState(self, id, state):
        # change in db
        pass

    def __getState(self, id, state):
        # change in db
        pass

    def __exit__(self):
        self.log.debug('close all curators')
        self.sendCloseCommand()
        self.log.debug('wait for the process to be completed')
        sleep(5)
        self.log.debug('close ControlSystem')
        self.logHolder.__exit__()
        super().__exit__()
        self.thread1.join()