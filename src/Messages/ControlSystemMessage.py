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

class ControlSystemMessage():
    def __init__(self, sender, command, params):
        self.sender: SenderInfo = sender
        self.command = command
        self.params = params

def createControlSystemMessage(sender: SenderInfo, command, params: dict = None):
    msg = ControlSystemMessage(sender, command, params)
    jsonMsg = json.dumps(msg, default=lambda o: o.__dict__)
    return jsonMsg

def parseControlSystemMessage(str):
    msg = ControlSystemMessage(**json.loads(str))
    sender = SenderInfo(msg.sender['type'], msg.sender['id'], msg.sender['ip'], msg.sender['port'])
    return ControlSystemMessage(sender, msg.command, msg.params)

class ControlSystemCommands:
    register = 'register'
    signOut = 'signOut'
    info = 'info'
    generate = 'generate' # to generator
    addEvent = 'addEvent' # to generator
    close = 'close' # to all curators

class ControlSystemMessageParams:
    functions = 'functions' # to list
    curatorState = 'curatorState' # to dict (json)
    environmentState = 'environmentState' # to dict (json)
    logMsg = 'log' # to str
    id = 'id' # to int
    generate = 'generate' # to bool
    factName = 'factName' # to str
    fact = 'fact' # to dict
