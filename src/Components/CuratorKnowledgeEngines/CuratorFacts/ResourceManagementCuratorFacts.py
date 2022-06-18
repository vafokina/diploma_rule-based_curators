from experta import Fact, Field

class ResourceManagementCuratorState(Fact):
    """Info about agent state"""
    energy_supply = Field(int, default=1) #  0 - power supply is switched off, 1 - is switched on, 2 - is damaged 
    light = Field(bool, default=False) # True - light is on, False - is off
    all_bulbs_are_broken = Field(bool, default=False) # or True
    bulb_count = Field(int, mandatory=True)
    broken_bulb_count = Field(int, default=0)
    emergency_lights = Field(bool, default=False) # True - emergency lights are switched on, False - are off 

    def as_dict(self):
        defaults = {
            'energy_supply': 1,
            'light': False,
            'all_bulbs_are_broken': False,
            'broken_bulb_count': 0,
            'emergency_lights': False,
        }
        values = super().as_dict()
        return {**defaults, **values}
    pass

class Motion(Fact):
    """Info about motion"""
    # True - motion, False - silence 
    
    def fromDict(dict: dict):
        return Motion(list(dict.values())[0])
    pass

class BrokenBulb(Fact):
    """Info about broken bulb"""
    # the bulb is broken
    
    def fromDict(dict: dict):
        return BrokenBulb()
    pass

class RepairedBulb(Fact):
    """Info about repaired bulb"""
    # the bulb has been repaired
    
    def fromDict(dict: dict):
        return RepairedBulb()
    pass

class BrokenEnergySupply(Fact):
    """Info about broken energy supply"""
    # power supply fails to work
    
    def fromDict(dict: dict):
        return BrokenEnergySupply()
    pass

class RepairedEnergySupply(Fact):
    """Info about repaired energy supply"""
    # power supply has been repaired
    
    def fromDict(dict: dict):
        return RepairedEnergySupply()
    pass
