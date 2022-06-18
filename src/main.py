import sys, time, os

from dependency_injector.wiring import Provide, inject

from Services.CuratorService import CuratorService
from Application import CuratorApplication

@inject
def main(
        curator: CuratorService = Provide[CuratorApplication.curator.curatorService],
) -> None:
    try:
        curator.start()
        while True: time.sleep(1)
    except KeyboardInterrupt:
        curator.__exit__()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except Exception as ex:
        curator.__exit__()
        print(str(type(ex)) + " : " + str(ex))

if __name__ == "__main__":
    application = CuratorApplication()
    application.core.init_resources()
    if len(sys.argv) > 1:
        application.config.set(selector='curator.type', value=sys.argv[1]) 
    if len(sys.argv) > 2:
        application.config.set(selector='curator.controlSystem.host', value=sys.argv[2]) 
    application.wire(modules=[__name__])
    
    print('Application is running. To exit press CTRL+C')
    main()
    print('Application is closed')