import json
from experta import * 

import sys, os
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
from Messages.SenderInfo import SenderInfo
from Components.CuratorKnowledgeEngines.CuratorFacts.AccessCuratorFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.SecurityCuratorFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.ResourceManagementCuratorFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.GeneralFacts import *

class CuratorMessage():
    def __init__(self, sender, factName, fact):
        self.sender: SenderInfo = sender
        self.factName = factName
        self.fact = fact

def createCuratorMessage(sender: SenderInfo, fact, factName = None):
    if factName is None:
        msg = CuratorMessage(sender, fact.__class__.__name__, fact)
    else:
        msg = CuratorMessage(sender, factName, fact)
    jsonMsg = json.dumps(msg, default=lambda o: o.__dict__)
    return jsonMsg

def parseCuratorMessage(str):
    msg = CuratorMessage(**json.loads(str))
    sender = SenderInfo(msg.sender['type'], msg.sender['id'], msg.sender['ip'], msg.sender['port'])
    return CuratorMessage(sender, msg.factName, msg.fact)

def resolveFact(factName, fact):
    if factName == Fire.__name__:
        return Fire.fromDict(fact)
    elif factName == Access.__name__:
        return Access.fromDict(fact)
    elif factName == Violation.__name__:
        return Violation.fromDict(fact)
    elif factName == Motion.__name__:
        return Motion.fromDict(fact)
    elif factName == BrokenBulb.__name__:
        return BrokenBulb.fromDict(fact)
    elif factName == RepairedBulb.__name__:
        return RepairedBulb.fromDict(fact)
    elif factName == BrokenEnergySupply.__name__:
        return BrokenEnergySupply.fromDict(fact)
    elif factName == RepairedEnergySupply.__name__:
        return RepairedEnergySupply.fromDict(fact)
    elif factName == Call.__name__:
        return Call.fromDict(fact)
    else: 
        raise Exception("Fact cannot be resolved") 
