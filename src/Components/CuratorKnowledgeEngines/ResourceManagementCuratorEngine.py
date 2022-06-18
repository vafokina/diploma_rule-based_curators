from experta import Rule, AND, OR, NOT, W, L, AS

from Components.CuratorKnowledgeEngines.CuratorFacts.SecurityCuratorFacts import Call
from .CuratorFacts.GeneralFacts import *
from .CuratorFacts.ResourceManagementCuratorFacts import *
from .CuratorEngine import CuratorEngine

class ResourceManagementCuratorEngine(CuratorEngine):

    def __init__(self, bulbCount):
        self.curatorStateFact = ResourceManagementCuratorState(bulb_count=bulbCount)
        super().__init__()

    def decide(self, fact):
        super().decide(fact)

    @Rule(AS.environmentState << EnvironmentState(), salience=-999)
    def current_env_state(self, environmentState):
        self.debug('current EnvironmentState: accident = ' + str(environmentState['accident']))
    
    @Rule(AS.curatorState << ResourceManagementCuratorState(), salience=-999)
    def current_agent_state(self, curatorState):
        self.debug('current ResourceManagementCuratorState: energy_supply = ' + str(curatorState['energy_supply']) + ', light = ' + str(curatorState['light']) + ', all_bulbs_are_broken = ' + str(curatorState['all_bulbs_are_broken']) + ', bulb_count = ' + str(curatorState['bulb_count']) + ', broken_bulb_count = ' + str(curatorState['broken_bulb_count']) + ', emergency_lights = ' + str(curatorState['emergency_lights']))

    @Rule(AND(EnvironmentState(accident='nothing'),
              Fire(True)))
    def fire_started(self):
        self.environmentStateFact = self.modify(self.environmentStateFact, accident='fire')
        self.info('the fire breaks out')
        
    @Rule(AND(EnvironmentState(accident='nothing'),
              Fire(True),
              NOT(ResourceManagementCuratorState(energy_supply=2))), salience=1)
    def fire_started_when_energy_supply_is_not_damaged(self):
        self.curatorStateFact = self.modify(self.curatorStateFact, energy_supply=0)
        self.info('energy supply is off')

    @Rule(AND(EnvironmentState(accident='fire'),
              Fire(False)))
    def fire_ended(self):
        self.environmentStateFact = self.modify(self.environmentStateFact, accident='nothing')
        self.info('the fire extinguished')

    @Rule(AND(EnvironmentState(accident='fire'),
              Fire(False),
              NOT(ResourceManagementCuratorState(energy_supply=2))), salience=1)
    def fire_ended_when_energy_supply_is_not_damaged(self):
        self.curatorStateFact = self.modify(self.curatorStateFact, energy_supply=1)
        self.info('energy supply is switched on')       

    @Rule(AND(OR(AND(EnvironmentState(accident='nothing'),
                     Fire(True)), 
                 AND(EnvironmentState(accident='fire'),
                     Fire(False)),),
              ResourceManagementCuratorState(energy_supply=2)), salience=1)
    def fire_when_energy_supply_is_damaged(self):
        self.info('energy supply has been damaged before')

    @Rule(BrokenEnergySupply())
    def energy_supply_is_damaged(self):
        self.curatorStateFact = self.modify(self.curatorStateFact, energy_supply=2)
        self.info('power supply fails to work')
        self.info('a request has been sent to the curator to call repairer')
        self.curator.sendToRandomCurator(Call('repairer', id=self.curator.id, target='energy_supply'))

    @Rule(AND(EnvironmentState(accident='nothing'),
              RepairedEnergySupply()))
    def energy_supply_is_repaired(self):
        self.curatorStateFact = self.modify(self.curatorStateFact, energy_supply=1)
        self.info('power supply has been repaired')

    @Rule(AND(EnvironmentState(accident='fire'),
              RepairedEnergySupply()))
    def energy_supply_is_repaired(self):
        self.curatorStateFact = self.modify(self.curatorStateFact, energy_supply=0)
        self.info('power supply has been repaired')

    @Rule(AND(EnvironmentState(accident='nothing'),
              ResourceManagementCuratorState(energy_supply=1, light=False, all_bulbs_are_broken=False),
              Motion(True)))
    def light_on(self):
        self.curatorStateFact = self.modify(self.curatorStateFact, light=True)
        self.info('turn on the light')

    @Rule(OR(AND(EnvironmentState(accident='nothing'),
                 ResourceManagementCuratorState(energy_supply=1, light=True, all_bulbs_are_broken=False),
                 Motion(False)), 
             ResourceManagementCuratorState(energy_supply=L(0) | L(2), light=True),
             ResourceManagementCuratorState(all_bulbs_are_broken=True, light=True)))
    def light_off(self):
        self.curatorStateFact = self.modify(self.curatorStateFact, light=False)
        self.info('turn off the light')

    @Rule(OR(ResourceManagementCuratorState(energy_supply=L(0) | L(2), emergency_lights=False),
             ResourceManagementCuratorState(all_bulbs_are_broken=True, emergency_lights=False)))
    def emergency_light_on(self):
        self.curatorStateFact = self.modify(self.curatorStateFact, emergency_lights=True)
        self.info('emergency lights are switched on')

    @Rule(ResourceManagementCuratorState(energy_supply=1, all_bulbs_are_broken=False, emergency_lights=True))
    def emergency_light_off(self):
        self.curatorStateFact = self.modify(self.curatorStateFact, emergency_lights=False)
        self.info('emergency lights are off')

    @Rule(AS.brokenBulb << BrokenBulb())
    def bulb_is_broken(self, brokenBulb):
        bulbCount = self.curatorStateFact['bulb_count']
        brokenBulbCount = self.curatorStateFact['broken_bulb_count'] + 1
        if brokenBulbCount > bulbCount: 
            return
        if brokenBulbCount == bulbCount:
            self.curatorStateFact = self.modify(self.curatorStateFact, all_bulbs_are_broken=True, broken_bulb_count=brokenBulbCount)
            self.info('all bulbs are broken')
        else:
            self.curatorStateFact = self.modify(self.curatorStateFact, broken_bulb_count=brokenBulbCount)
            self.info('the bulb is broken')
        self.info('a request has been sent to the curator to call repairer')
        self.curator.sendToRandomCurator(Call('repairer', id=self.curator.id, target='bulb'))

    @Rule(AS.repairedBulb << RepairedBulb())
    def bulb_is_repaired(self, repairedBulb):
        brokenBulbCount = self.curatorStateFact['broken_bulb_count'] - 1
        if brokenBulbCount < 0:
            return
        all_bulbs_are_broken = self.curatorStateFact['all_bulbs_are_broken']
        if all_bulbs_are_broken:
            self.curatorStateFact = self.modify(self.curatorStateFact, all_bulbs_are_broken=False, broken_bulb_count=brokenBulbCount)
            self.info('the bulb is repaired, one bulb works')
        else:
            self.curatorStateFact = self.modify(self.curatorStateFact, broken_bulb_count=brokenBulbCount)
            self.info('the bulb is repaired')
        
       
    