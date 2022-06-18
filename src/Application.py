import logging.config
from dependency_injector import containers, providers
from Services.DataBaseService import DataBaseService
from Services.SocketService import SocketService
from Services.CuratorService import CuratorService
from Components.ControlSystem import ControlSystem
from Web.WebApp import WebApp

class Core(containers.DeclarativeContainer):

    config = providers.Configuration()

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )


class Curator(containers.DeclarativeContainer):

    config = providers.Configuration()
    services = providers.DependenciesContainer()

    curatorService = providers.Factory(
        CuratorService,
        config=config,
        dbService=services.dbService,
        socketService=services.socketService
    )

class ControlSystemServices(containers.DeclarativeContainer):

    config = providers.Configuration()
    controlSystemConfig = providers.Configuration()

    dbService = providers.Factory(
        DataBaseService,
        name=config.database.name, 
        user=config.database.user, 
        password=config.database.password, 
        host=config.database.host, 
        port=config.database.port
    )

    socketService = providers.Factory(
        SocketService,
        host=controlSystemConfig.host,
        port=controlSystemConfig.port,
    )

class Services(containers.DeclarativeContainer):

    config = providers.Configuration()

    dbService = providers.Factory(
        DataBaseService,
        name=config.database.name, 
        user=config.database.user, 
        password=config.database.password, 
        host=config.database.host, 
        port=config.database.port
    )

    socketService = providers.Factory(
        SocketService,
        excludePorts=config.socket.excludePorts
    )

class CuratorApplication(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    core = providers.Container(
        Core,
        config=config.core,
    )

    services = providers.Container(
        Services,
        config=config.services,
    )

    curator = providers.Container(
        Curator,
        config=config.curator,
        services=services,
    )

class ControlSystemApplication(containers.DeclarativeContainer):

    config = providers.Configuration(yaml_files=["config.yml"])

    core = providers.Container(
        Core,
        config=config.core,
    )

    dbService = providers.Factory(
        DataBaseService,
        name=config.services.database.name, 
        user=config.services.database.user, 
        password=config.services.database.password, 
        host=config.services.database.host, 
        port=config.services.database.port
    )

    socketService = providers.Factory(
        SocketService,
        host=config.curator.controlSystem.host,
        port=config.curator.controlSystem.port,
    )

    controlSystem = providers.Factory(
        ControlSystem,
        dbService=dbService,
        socketService=socketService
    )

    webApp = providers.Factory(
        WebApp,
        controlSystem=controlSystem,
    )