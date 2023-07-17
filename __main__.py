import sys
from dependency_injector.wiring import Provide, inject
from MVC.app import App
from services import DataPreprocessingService
from containers import Container


@inject
def main(
        saxs_input_service: DataPreprocessingService = Provide[Container.input_service],
        mpl_service = Provide[Container.mpl_service_factory]
) -> None:
    app = App(sys.argv, saxs_input_service, mpl_service)

    sys.exit(app.exec_())


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    main()
