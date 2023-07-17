from PyQt5.QtWidgets import QApplication, QWizard
from MVC.model import Model
from MVC.main_controller import MainController
from MVC.main_view import MainView


class App(QApplication):
    def __init__(self, sys_argv, saxs_input_service, mpl_service):
        super(App, self).__init__(sys_argv)

        self.model = Model()

        self.main_controller = MainController(self.model, saxs_input_service)

        self.main_view = MainView(self.model, self.main_controller, mpl_service)

        self.main_view.show()
