import logging

from Components.CuratorKnowledgeEngines.AccessCuratorEngine import AccessCuratorEngine
from Components.CuratorKnowledgeEngines.ResourceManagementCuratorEngine import ResourceManagementCuratorEngine
from Components.CuratorKnowledgeEngines.SecurityCuratorEngine import SecurityCuratorEngine
from Components.EventGenerator import EventGenerator
from Components.CuratorKnowledgeEngines.CuratorFacts.GeneralFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.SecurityCuratorFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.AccessCuratorFacts import *
from Components.CuratorKnowledgeEngines.CuratorFacts.ResourceManagementCuratorFacts import *
from Components.Constants import CuratorType
from Components.Curator import BaseCurator

class CuratorService():

    def __init__(self, config, dbService, socketService):
        self.log = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )
        type = config['type']
        controlSystemHost = config['controlSystem']['host']
        controlSystemPort = config['controlSystem']['port']
        
        if type == "generator":
            generatorConfig = config['generator']
            self.curator = EventGenerator(controlSystemHost, controlSystemPort, dbService, socketService, generatorConfig['speed'], generatorConfig['generate'], generatorConfig['logging']['enable'], generatorConfig['logging']['provideRecipient'])
        else:
            engine = None
            functions = []
            if type == "access":
                fullTypeName = CuratorType.access
                engine = AccessCuratorEngine()
                functions = [Access.__name__, Violation.__name__]
            elif type == "security":
                fullTypeName = CuratorType.security
                engine = SecurityCuratorEngine()
                functions = [Fire.__name__, Call.__name__]
            elif type == "resource":
                fullTypeName = CuratorType.resource
                engine = ResourceManagementCuratorEngine(config['resource']['bulbCount'])
                functions = [Motion.__name__, BrokenBulb.__name__, RepairedBulb.__name__, BrokenEnergySupply.__name__, RepairedEnergySupply.__name__]
            else: 
                raise Exception("Curator type " + type + " cannot be resolved")
            self.curator = BaseCurator(fullTypeName, engine, functions, controlSystemHost, controlSystemPort, dbService, socketService, config['countTime'])

    def start(self):
        self.curator.start()

    def __exit__(self):
        self.curator.__exit__()