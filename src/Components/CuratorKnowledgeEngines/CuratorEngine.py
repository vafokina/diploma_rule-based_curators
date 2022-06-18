from timeit import default_timer as timer
from time import sleep
from experta import KnowledgeEngine

import sys, os
BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_PATH)
from Components.CuratorKnowledgeEngines.CuratorFacts.GeneralFacts import *
from Config.LoggingConfig import *
from Services.DataBaseService import *
from Services.SocketService import *
from Messages.CuratorMessage import *
from Messages.ControlSystemMessage import *
from Messages.SenderInfo import *

class CuratorEngine(KnowledgeEngine):
    curatorStateFact = None
    environmentStateFact = EnvironmentState()

    def bindWithCurator(self, curator):
        self.curator = curator

    def decide(self, fact):
        self.reset()
        if self.curatorStateFact is None:
            raise Exception("Set initial state of curator")
        else:
            self.curatorStateFact = self.declare(self.curatorStateFact)
        if self.environmentStateFact is None:
            self.environmentStateFact = self.declare(EnvironmentState())
        else:
            self.environmentStateFact = self.declare(self.environmentStateFact)

        start1 = timer()
        self.declare(fact)
        end1 = timer()

        self.debug("\n" + str(self.facts))
        self.debug("\n" + str(self.agenda))

        start2 = timer()
        self.run()
        end2 = timer()

        time1 = (end1 - start1) * 1000
        time2 = (end2 - start2) * 1000
        self.debug('execution time = ' + str(time1) + ' and ' + str(time2)  + ' millis')
        try:
            self.curator.noteTime(fact, time1, time2)
        except:
            pass
    
    def info(self, str):
        try:
            self.curator.curatorLog.info(str)
            self.curator.sendLogToControlSystem(str)
        except:
            print(str)

    def debug(self, str):
        try:
            self.curator.curatorLog.debug(str)
        except:
            print(str)
    
    def error(self, str):
        try:
            self.curator.curatorLog.error(str)
        except:
            print(str)
