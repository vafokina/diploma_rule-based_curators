import threading, _thread
from time import sleep
from io import StringIO

import sys
sys.path.append('..')
from Components.CuratorKnowledgeEngines.CuratorEngine import *
from Components.CuratorSystemComponent import CuratorSystemComponent

class BaseCurator(CuratorSystemComponent):
    def __init__(self, type, engine, functions, controlSystemHost, controlSystemPort, dbService, socketService, countTime = False):
        super().__init__(dbService, socketService)
        self.log = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        self.controlSystemHost = controlSystemHost
        self.controlSystemPort = controlSystemPort
        self.queue = [] 
        self._continue = True
        self.countTime = countTime
        self.type = type
        self.functions = functions
        self.engine: CuratorEngine = engine

        self.id = self.__register()
        
        if not self.engine is None: 
            self.engine.bindWithCurator(self)
            self.curatorLog = getCuratorEngineLogger(self.__getName())
            if self.countTime:
                self.timeRecords = StringIO()
                self.timeRecords.write('declare time, millis\trun time, millis\tfact name\tfact params\tcurator type\n')

        self.log.debug('create ' + self.__getName())
        print('\n\ncreate ' + self.__getName() + "\n\n")
        self.sendLogToControlSystem('curator is active')
    
    def start(self):
        self.listenMessages()

    def listenMessages(self):
        self.thread1 = threading.Thread(target=self.socketService.listen, args=(self.queue,)) 
        self.thread2 = threading.Thread(target=self.processMessages) 
        self.thread1.start()
        self.thread2.start()

    def processMessages(self):
        while self._continue:
            if len(self.queue) > 0:
                item: str = self.queue.pop(0)
                if item.__contains__('command'):
                    msg : ControlSystemMessage = parseControlSystemMessage(item)
                    self.processMessagesFromControlSystem(msg)
                else:
                    msg : CuratorMessage = parseCuratorMessage(item)
                    self.processMessagesFromCurator(msg)
            else:
                sleep(0.2)
    
    def processMessagesFromCurator(self, msg: CuratorMessage):
        fact = resolveFact(msg.factName, msg.fact)
        self.log.debug('resolve a fact ' + str(fact))
        self.engine.decide(fact)

    def processMessagesFromControlSystem(self, msg: ControlSystemMessage):
        if msg.command == ControlSystemCommands.close:
            _thread.interrupt_main()

    def sendLogToControlSystem(self, logMsg):
        curatorState, environmentState = self.getStates()
        msg = createControlSystemMessage(self.getSenderInfo(), ControlSystemCommands.info, {ControlSystemMessageParams.logMsg: logMsg, ControlSystemMessageParams.environmentState: environmentState, ControlSystemMessageParams.curatorState: curatorState})
        self.socketService.send(self.controlSystemHost, self.controlSystemPort, msg)

    def getStates(self):
        curatorState = None
        environmentState = None
        if not self.engine is None:
            if not self.engine.curatorStateFact is None:
                curatorState = self.engine.curatorStateFact.as_dict()
            if not self.engine.environmentStateFact is None:
                environmentState = self.engine.environmentStateFact.as_dict()
        return curatorState, environmentState

    def noteTime(self, fact: Fact, time1, time2):
        if self.countTime:
            self.timeRecords.write('%(time1)s\t%(time2)s\t%(factName)s\t%(factDict)s\t%(curatorType)s\n'%{'time1':time1, 'time2':time2, 'factName':str(fact.__class__.__name__), 'factDict':json.dumps(fact, default=lambda o: o.__dict__).replace(', "__factid__": 3','').replace('"__factid__": 3',''), 'curatorType':self.type})

    def __getName(self):
        return self.type + '_' + str(self.id)

    def __register(self):
        self.log.debug('register with the control system (host: ' + self.controlSystemHost + ', port: ' + str(self.controlSystemPort) + ')')
        curatorState, environmentState = self.getStates()
        msg = createControlSystemMessage(self.getSenderInfo(), ControlSystemCommands.register, {ControlSystemMessageParams.functions: self.functions, ControlSystemMessageParams.environmentState: environmentState, ControlSystemMessageParams.curatorState: curatorState})
        ans = self.socketService.sendAndReceive(self.controlSystemHost, self.controlSystemPort, msg)
        ans = parseControlSystemMessage(ans)
        id = ans.params[ControlSystemMessageParams.id]
        if id is None:
            raise Exception('curator is already registered')
        self.log.debug('registered with id = ' + str(id))
        return id

    def __signOut(self):
        self.log.debug('sign out with the control system (host: ' + self.controlSystemHost + ', port: ' + str(self.controlSystemPort) + ')')
        msg = createControlSystemMessage(self.getSenderInfo(), ControlSystemCommands.signOut)
        ans = self.socketService.sendAndReceive(self.controlSystemHost, self.controlSystemPort, msg)
        if (ans == 'OK'):
            self.log.debug('unregistered successfully')
        else:
            self.log.error('failed to unregister')
        self.sendLogToControlSystem('curator is closed')

    def __exit__(self):
        self.log.debug('close ' + self.__getName())
        self._continue = False
        self.__signOut()
        super().__exit__()
        self.thread1.join()
        self.thread2.join()

        if self.countTime:
            rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logsDir = os.path.join(rootDir, 'Resources', 'time')
            fileName = os.path.join(logsDir, self.__getName() + '.csv')
            with open(fileName, 'w') as fd:
                fd.write(self.timeRecords.getvalue())
                self.timeRecords.close()
                self.log.debug('save time record file: ' + fileName)
