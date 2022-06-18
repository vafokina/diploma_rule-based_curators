import sys, time, os

from dependency_injector.wiring import Provide, inject

from Components.ControlSystem import ControlSystem
from Application import ControlSystemApplication
from Web.WebApp import WebApp


@inject
def main(
        app: WebApp = Provide[ControlSystemApplication.webApp],
) -> None:
    try:
        app.controlSystem.start()
        app.runServerInAnotherThread()
        while True: time.sleep(1)
    except KeyboardInterrupt:
        app.controlSystem.__exit__()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    application = ControlSystemApplication()
    application.core.init_resources()
    application.wire(modules=[__name__])
    
    print('Application is running. To exit press CTRL+C')
    main()
    print('Application is closed')