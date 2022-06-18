from experta import Rule, AS, MATCH, AND, W
from .CuratorFacts.GeneralFacts import *
from .CuratorFacts.SecurityCuratorFacts import *
from .CuratorEngine import CuratorEngine

class SecurityCuratorEngine(CuratorEngine):
    curatorStateFact = SecurityCuratorState()
    delayedCalls = list()

    def decide(self, fact):
        super().decide(fact)

    @Rule(AS.environmentState << EnvironmentState())
    def current_env_state(self, environmentState):
        self.debug('current EnvironmentState: accident = ' + str(environmentState['accident']))
    
    @Rule(AS.curatorState << SecurityCuratorState())
    def current_agent_state(self, curatorState):
        self.debug('current SecurityCuratorState: alert_system = ' + str(curatorState['alert_system']))

    @Rule(AND(EnvironmentState(accident='nothing'),
              Fire(True, fromCurator=MATCH.fromCurator)))
    def fire_started(self, fromCurator):
        self.environmentStateFact = self.modify(self.environmentStateFact, accident='fire')
        self.info('the fire breaks out')
        self.curatorStateFact = self.modify(self.curatorStateFact, alert_system=True)
        self.info('alert system is on')
        if not fromCurator:
            self.declare(Call("firefighters"))
            self.info('a notice about the fire has been sent to all curators')
            self.curator.sendToOtherCurators(Fire(True, fromCurator=True))

    @Rule(AND(EnvironmentState(accident='fire'),
              Fire(False, fromCurator=MATCH.fromCurator)))
    def fire_ended(self, fromCurator):
        self.environmentStateFact = self.modify(self.environmentStateFact, accident='nothing')
        self.info('the fire extinguished')
        self.curatorStateFact = self.modify(self.curatorStateFact, alert_system=False)
        self.info('alert system is off')
        if not fromCurator:
            self.info('a notice about the end of the fire has been sent to all curators')
            self.curator.sendToOtherCurators(Fire(False, fromCurator=True))
        while len(self.delayedCalls) > 0:
            fact = self.delayedCalls.pop(0)
            self.call_repairer(fact)        

    @Rule(Call("firefighters"))
    def call_firefighters(self):
        self.info('call to the firefighters')

    @Rule(Call("security"))
    def call_police(self):
        self.info('call to the security')

    @Rule(AND(EnvironmentState(accident='nothing'),
              'fact' << Call("repairer", id=W())))
    def call_repairer(self, fact):
        self.info('call to the repairer')
        self.curator.sendToEventGenerator(fact)

    @Rule(AND(EnvironmentState(accident='fire'),
              'fact' << Call("repairer", id=W())))
    def delay_call_repairer(self, fact):
        self.info('delay the call to the repairer')
        self.delayedCalls.append(fact)