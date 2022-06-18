from time import sleep
from experta import *
from random import choice
from Components.CuratorKnowledgeEngines import AccessCuratorEngine
from Components.CuratorKnowledgeEngines.CuratorFacts.GeneralFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.AccessCuratorFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.SecurityCuratorFacts import *
from Components.CuratorKnowledgeEngines.SecurityCuratorEngine import SecurityCuratorEngine
from Messages.ControlSystemMessage import ControlSystemCommands, createControlSystemMessage, parseControlSystemMessage
from Messages.CuratorMessage import createCuratorMessage, parseCuratorMessage
from Messages.SenderInfo import SenderInfo

fact = Fire(True)
v = fact.get(0)

engine = SecurityCuratorEngine()
engine.decide(Call("repairer", id=268))
engine.declare(fact)

engine = AccessCuratorEngine.AccessCuratorEngine(1, None, None)
"""
engine.decide(Fire(True))
sleep(5)"""


engine.decide(Fire(True))
sleep(5)

engine.decide(Access(admission = False))
sleep(15)
engine.decide(Access(admission = True))
sleep(15)
engine.decide(Violation())
sleep(15)

engine.decide(Fire(False))
sleep(5)

engine.decide(Access(admission = False))
sleep(15)
engine.decide(Access(admission = True))
sleep(15)
engine.decide(Violation())
sleep(15)

