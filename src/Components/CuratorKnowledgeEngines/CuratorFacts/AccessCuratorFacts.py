from experta import Fact, Field

class AccessCuratorState(Fact):
    """Info about agent state"""
    access = Field(int, default=1) # 0 - access denied, 1 - access restricted, 2 - access unlimited
    emergency_exits = Field(bool, default=False) # True - are open, False - are close 

    def as_dict(self):
        defaults = {
            'access': 1,
            'emergency_exits': False,
        }
        values = super().as_dict()
        return {**defaults, **values}
    pass

class Access(Fact):
    """Info about person who want to pass"""
    admission = Field(bool, mandatory=True) # True - the person has a access card and can pass 

    def fromDict(dict: dict):
        return Access(admission=dict.pop('admission'))
    pass

class Violation(Fact):
    """Info on violation and trespassing"""
    # the person has entered the territory illegally 
    
    def fromDict(dict: dict):
        return Violation()
    pass
