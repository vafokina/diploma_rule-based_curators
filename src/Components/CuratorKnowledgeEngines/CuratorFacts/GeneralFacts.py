from experta import Fact, Field

class EnvironmentState(Fact):
    """Info about agent state"""
    accident = Field(str, default='nothing') # or fire

    def as_dict(self):
        defaults = {
            'accident': 'nothing',
        }
        values = super().as_dict()
        return {**defaults, **values}
    pass

class Fire(Fact):
    """Info on violation and trespassing"""
    # True - the fire breaks out, False - the fire extinguished

    fromCurator = Field(bool, default=False) # if from curator, security curator does not forward the message to other curators. if from environment, the curator does

    def fromDict(dict: dict):
        if dict.get('fromCurator') is None:
            return Fire(dict["0"])
        else:
            return Fire(dict["0"], fromCurator=dict["fromCurator"])
    pass

