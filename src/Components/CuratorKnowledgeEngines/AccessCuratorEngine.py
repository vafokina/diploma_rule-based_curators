from experta import Rule, AND, W, L, AS
from .CuratorFacts.GeneralFacts import *
from .CuratorFacts.AccessCuratorFacts import *
from .CuratorFacts.SecurityCuratorFacts import *
from .CuratorEngine import CuratorEngine

class AccessCuratorEngine(CuratorEngine):
    curatorStateFact = AccessCuratorState()
    
    def decide(self, fact):
        super().decide(fact)

    @Rule(AS.environmentState << EnvironmentState())
    def current_env_state(self, environmentState):
        self.debug('current EnvironmentState: accident = ' + str(environmentState['accident']))
    
    @Rule(AS.curatorState << AccessCuratorState())
    def current_agent_state(self, curatorState):
        self.debug('current AccessCuratorState: access = ' + str(curatorState['access']) + ', emergency_exits = ' + str(curatorState['emergency_exits']))

    @Rule(AND(EnvironmentState(accident='nothing'),
              Fire(True)))
    def fire_started(self):
        self.environmentStateFact = self.modify(self.environmentStateFact, accident='fire')
        self.info('the fire breaks out')
        self.curatorStateFact = self.modify(self.curatorStateFact, access=0, emergency_exits=True)
        self.info('the entry is blocked to everyone, emergency exits are open')
        
    @Rule(AND(EnvironmentState(accident='fire'),
              Fire(False)))
    def fire_ended(self):
        self.environmentStateFact = self.modify(self.environmentStateFact, accident='nothing')
        self.info('the fire extinguished')
        self.curatorStateFact = self.modify(self.curatorStateFact, access=1, emergency_exits=False)
        self.info('the entry is restricted, emergency exits are close')

    @Rule(AND(EnvironmentState(accident='nothing'),
              AccessCuratorState(access=1),
              Access(admission=True)))
    def person_came_with_access_card(self):
        self.info('the person with the access card have passed')

    @Rule(AND(EnvironmentState(accident='nothing'),
              AccessCuratorState(access=1),
              Access(admission=False)))
    def person_came_without_access_card(self):
        self.info('the person without the access card cannot pass')

    @Rule(AND(EnvironmentState(accident='nothing'),
              AccessCuratorState(access=L(0) | L(1)),
              Violation()))
    def person_entered_illegally(self):
        self.info('the person has entered the territory illegally')
        self.info('a request has been sent to the curator to call security')
        self.curator.sendToRandomCurator(Call('security'))

    @Rule(AND(EnvironmentState(accident=W()),
              AccessCuratorState(access=0),
              Access(admission=W())))
    def person_came_when_access_denied(self):
        self.info('nobody can pass, access denied')

    @Rule(AND(EnvironmentState(accident='fire'),
              AccessCuratorState(access=W()),
              Violation()))
    def person_entered_illegally_in_fire(self):
        self.info('the person trespassing has been ignored')
       
    
