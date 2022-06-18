from experta import Fact, Field

class SecurityCuratorState(Fact):
    """Info about agent state"""
    alert_system = Field(bool, default=False) # True - alert system is on, False - is off

    def as_dict(self):
        defaults = {
            'alert_system': False,
        }
        values = super().as_dict()
        return {**defaults, **values}
    pass

class Call(Fact):
    """Info about call"""
    # security - call to the security
    # repairer - call to the repairer
    # firefighters - call to the firefighters

    id = Field(int) # id of curator who needs a repairer
    target = Field(str) # item that has broken

    def fromDict(dict: dict):
        if dict.get('id') is None:
            return Call(dict["0"])
        else:
            return Call(dict["0"], id=dict["id"], target=dict["target"])
    pass