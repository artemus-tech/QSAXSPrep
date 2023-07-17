from dependency_injector import containers, providers
import logging.config
import services
from BL.SaxsGear import SaxsGear
from MPL.MplEditCanvas import MplEditCanvas
from MPL.MplCanvas import MplCanvas
from MPL.MplRepository import MplRepository
from MPL.CustomNavigationToolbar2QT import CustomNavigationToolbar2QT


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    # Gateways
    plot_client = providers.Factory(
        MplCanvas

    )

    edit_plot_client = providers.Factory(
        MplEditCanvas
    )

    math_lib = providers.Singleton(
        SaxsGear
    )

    # services
    input_service = providers.Factory(
        services.DataPreprocessingService,
        engine=math_lib
    )
    toolbar = providers.Factory(
        CustomNavigationToolbar2QT
    )
    """
    plot_service_factory = providers.Factory(
        PlotRepository,
        plot_factory=plot_client.provider,
        toolbar=toolbar.provider
    )

    edit_plot_service_factory = providers.Factory(
        EditPlotRepository,
        edit_plot_factory=edit_plot_client.provider,
        toolbar=toolbar.provider

    )
    """
    mpl_service_factory = providers.Factory(
        MplRepository,
        edit_plot_factory=edit_plot_client.provider,
        plot_factory=plot_client.provider,
        toolbar=toolbar.provider
    )

