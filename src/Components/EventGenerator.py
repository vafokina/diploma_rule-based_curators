import threading, _thread
from time import sleep
from random import choice, randint

import sys
sys.path.append('..')
from Components.CuratorKnowledgeEngines.CuratorFacts.GeneralFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.AccessCuratorFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.SecurityCuratorFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.ResourceManagementCuratorFacts import *
from Components.Curator import *
from Components.Constants import *
from Config.LoggingConfig import *
from Services.DataBaseService import *
from Services.SocketService import *
from Messages.CuratorMessage import *
from Messages.ControlSystemMessage import *
from Messages.SenderInfo import *

class EventGenerator(BaseCurator):
    factsToGenerate = [Fire.__name__, Access.__name__, Violation.__name__, Motion.__name__,  BrokenEnergySupply.__name__, BrokenBulb.__name__ ]
    fire = False
    lock = threading.Lock()

    def __init__(self, controlSystemHost, controlSystemPort, dbService, socketService, speed, generate, sendLog, provideRecipient):
        super().__init__(CuratorType.generator, None, [], controlSystemHost, controlSystemPort, dbService, socketService)
        self.speed = speed
        self.generate = generate
        self.sendLog = sendLog
        self.provideRecipient = provideRecipient
        self.events = [] 

    def start(self):
        self.listenMessages()
        if self.generate: 
            self.generateEvents()
        self.threadSendEvents = threading.Thread(target=self.__sendEvents) 
        self.threadSendEvents.start()

    def generateEvents(self):
        self.log.debug('start generation')
        self.sendLogToControlSystem('event generation has started')
        self.threadGenerateFire = threading.Thread(target=self.__generateFire, daemon=True) 
        self.threadGenerateAccess = threading.Thread(target=self.__generateAccess, daemon=True) 
        self.threadGenerateViolation = threading.Thread(target=self.__generateViolation, daemon=True) 
        self.threadGenerateMotion = threading.Thread(target=self.__generateMotion, daemon=True) 
        self.threadGenerateBrokenEnergySupply = threading.Thread(target=self.__generateBrokenEnergySupply, daemon=True) 
        self.threadGenerateBrokenBulb = threading.Thread(target=self.__generateBrokenBulb, daemon=True) 
        self.threadGenerateFire.name = 'thread_GenerateFire'
        self.threadGenerateAccess.name = 'thread_GenerateAccess' 
        self.threadGenerateViolation.name = 'thread_GenerateViolation'
        self.threadGenerateMotion.name = 'thread_GenerateMotion'
        self.threadGenerateBrokenEnergySupply.name = 'thread_GenerateBrokenEnergySupply'
        self.threadGenerateBrokenBulb.name = 'thread_GenerateBrokenBulb'
        self.threadGenerateFire.start()
        self.threadGenerateAccess.start()
        self.threadGenerateViolation.start()
        self.threadGenerateMotion.start()
        self.threadGenerateBrokenEnergySupply.start()
        self.threadGenerateBrokenBulb.start()

    def processMessagesFromCurator(self, msg: CuratorMessage):
        fact = resolveFact(msg.factName, msg.fact)
        if fact.__class__.__name__ == Call.__name__:
            curatorId = fact["id"]
            target = fact["target"]
            self.threadGenerateCall = threading.Thread(target=self.__generateCall, args=(curatorId, target), daemon=True) 
            self.threadGenerateCall.name = 'thread_GenerateCall'
            self.threadGenerateCall.start()
        elif fact.__class__.__name__ == Fire.__name__:
            with self.lock:
                curatorFireValue = fact.get(0)
                if curatorFireValue != self.fire:
                    self.log.error('the generator and curators have been desynchronised')
                    self.fire = curatorFireValue
        else:
            pass

    def processMessagesFromControlSystem(self, msg: ControlSystemMessage):
        if msg.command == ControlSystemCommands.close:
            _thread.interrupt_main()
        elif msg.command == ControlSystemCommands.generate:
            self.__setGenerate(msg.params[ControlSystemMessageParams.generate])
        elif msg.command == ControlSystemCommands.addEvent:
            fact = resolveFact(msg.params[ControlSystemMessageParams.factName], msg.params[ControlSystemMessageParams.fact])
            if fact.__class__.__name__ == Fire.__name__:
                with self.lock:
                    curatorFireValue = fact.get(0)
                    self.fire = curatorFireValue
            self.__addEvent(fact)

    def getStates(self):
        curatorState = None
        environmentState = None
        if (self.fire): 
            environmentState = EnvironmentState(accident='fire')
        else:
            environmentState = EnvironmentState(accident='nothing')
        return curatorState, environmentState

    def __setGenerate(self, generate):
        if self.generate != generate:
            self.generate = generate
            if self.generate:
                self.generateEvents()
            else:
                self.log.debug('stop generation')
                self.sendLogToControlSystem('event generation is stopped')

    def __generateFire(self):
        while self.generate:
            self.__sleep(60*randint(3,7))
            with self.lock:
                if self.generate:
                    self.fire = not self.fire
                    self.__addEvent(Fire(self.fire))
                    if choice([True, False]):
                        self.__addEvent(BrokenEnergySupply())

    def __generateAccess(self):
        while self.generate:
            self.__sleep(randint(20,180))
            if self.generate:
                self.__addEvent(Access(admission=choice([True, False])))

    def __generateViolation(self):
        while self.generate:
            self.__sleep(60*randint(1,2))
            if self.generate:
                self.__addEvent(Violation())

    def __generateMotion(self):
        while self.generate:
            self.__sleep(30)
            if self.generate:
                self.__addEvent(Motion(choice([True, False])))

    def __generateBrokenEnergySupply(self):
        pass # generate in __generateFire

    def __generateBrokenBulb(self):
        while self.generate:
            self.__sleep(10*randint(3,7))
            if self.generate:
                self.__addEvent(BrokenBulb())

    def __generateCall(self, id, target):
        self.__sleep(60*randint(1,3))
        while True:
            self.lock.acquire()
            if not self.fire:
                if target == 'bulb':
                    self.__addEvent(RepairedBulb(), id)
                elif target == 'energy_supply':
                    self.__addEvent(RepairedEnergySupply(), id)
                self.lock.release()
                break
            else:
                self.lock.release()
                self.__sleep(randint(30,90))

    def __sleep(self, seconds):
        realValue = seconds/self.speed
        self.log.debug('sleep for ' + str(realValue))
        sleep(realValue)

    def __addEvent(self, fact, id = None):
        self.log.debug('add event: ' + str(fact))
        self.events.append((id, fact))

    def __sendEvents(self):
        while self._continue:
            if len(self.events) > 0:
                pair = self.events.pop(0)
                id = pair[0]
                fact = pair[1]
                if self.sendLog:
                    self.sendLogToControlSystem("send event " + str(fact).replace('<Undeclared Fact> ',''))
                if id is None: 
                    res, id = self.sendToRandomCurator(fact)
                else:
                    res = self.sendToCurator(id, fact)
                if self.sendLog:
                    if res:
                        if self.provideRecipient:
                            self.sendLogToControlSystem("event " + str(fact).replace('<Undeclared Fact> ','') + " was sent to curator with id " + str(id))
                    else:
                        self.sendLogToControlSystem("no one to send event " + str(fact).replace('<Undeclared Fact> ',''))
            else:
                sleep(0.2)

    def __sendToControlSystem(self, command, params: dict):
        msg = createControlSystemMessage(self.getSenderInfo(), command, params)
        self.socketService.send(self.controlSystemHost, self.controlSystemPort, msg)

    def __exit__(self):
        self._continue = False
        super().__exit__()
        self.threadSendEvents.join()
