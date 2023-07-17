import os
from typing import Tuple

from PyQt5.QtWidgets import QMainWindow, QWizard, QFileDialog, QVBoxLayout, QTabWidget, QWidget
from PyQt5.QtCore import pyqtSlot
from numpy import ndarray

import consts
from MVC.main_view_ui import Ui_MainWindow
from PyQt5 import QtCore

from QtAssets import show_dialog


class MainView(QWizard):
    def __init__(self, model, main_controller, mpl_service):
        # def __init__(self, model, main_controller, saxs_plot_service, saxs_edit_plot_service):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        # ----------------------------------------------------------------------------------------------
        # self._ui = Ui_MainWindow(saxs_plot_service,saxs_edit_plot_service)
        self._ui = Ui_MainWindow(mpl_service)

        self._ui.setupUi(self)
        # ----------------------------------------------------------------------------------------------

        # connect widgets to controller
        self._ui.browse_button.clicked.connect(self.load_file)
        self._ui.plot_page_scale_cmb.currentIndexChanged.connect(self._main_controller.change_plot_scale)
        self._ui.options_page_scale_cmb.currentIndexChanged.connect(self._main_controller.change_options_scale)
        self._ui.result_page_scale_cmb.currentIndexChanged.connect(self._main_controller.change_result_scale)
        self._ui.guinier_page_scale_cmb.currentIndexChanged.connect(self._main_controller.change_structure_factor_scale)
        # self._ui.is_scattering_vector_module_chb.stateChanged.connect(self._main_controller.change_arg)
        self._ui.next_btn.clicked.connect(self.go_to_next_step)

        # listen for model event signals
        self._model.load_file_path_changed.connect(self.on_load_file_path_changed)
        self._model.enable_plot_changed.connect(self.on_plot_changed)
        self._model.data_uploaded.connect(self.on_data_load)
        self._model.data2_uploaded.connect(self.on_data2_load)
        self._model.data3_uploaded.connect(self.on_data3_load)
        self._model.data4_uploaded.connect(self.on_data4_load)

        self._model.plot_scale_index_changed.connect(self.on_plot_scale_changed)
        self._model.options_scale_index_changed.connect(self.on_options_scale_changed)
        self._model.result_scale_index_changed.connect(self.on_result_scale_changed)
        self._model.structure_factor_scale_index_changed.connect(self.on_structure_factor_scale_changed)
        self._model.arg_changed.connect(self.on_arg_changed)
        self._model.has_error_occurs.connect(self.alert)
        # set default scale for user time economy
        self._ui.plot_page_scale_cmb.setCurrentIndex(3)
        self._ui.options_page_scale_cmb.setCurrentIndex(0)

    @pyqtSlot(bool)
    def go_to_next_step(self):
        try:
            self._main_controller.next_step(self.currentId())
        except Exception as e:
            show_dialog("Error", e.args[0])

    @pyqtSlot(bool)
    def alert(self, flag):
        show_dialog(str(flag), self._model.message)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*.*')

        if os.path.isfile(file_name):
            try:
                self._main_controller.load_file(file_name)
            except Exception as e:
                show_dialog(e.args)

    @pyqtSlot(str)
    def on_load_file_path_changed(self, value):
        self._ui.filepath_txb.setText(value)

    @pyqtSlot(int)
    def on_arg_changed(self, value):
        print(value)

    @pyqtSlot(int)
    def on_structure_factor_scale_changed(self, index):
        selected = self._ui.get_cmb_options_by_index(index)
        self._ui.plot3.set_scale(selected)
        self._ui.edit_plot3.set_scale(selected)

    @pyqtSlot(ndarray)
    def on_data_load(self, value):
        self._ui.plot1.get_plot(value)
        self._ui.edit_plot1.bind_datastorage(value, os.path.join(consts.DS, "./q1q2.txt"),
                                             label_list=["$q, nm^{-1}$", "I, arb. units"])

    @pyqtSlot(ndarray)
    def on_data2_load(self, value):
        self._ui.plot2.get_plot(value,
                                label_list=["$q, nm^{-1}$", "I, arb. units", ],
                                legend=["I(q)-CONST", "I(q)"])

    @pyqtSlot(ndarray)
    def on_data3_load(self, value):
        self._ui.plot3.get_plot(value,
                                label_list=["$q^2, nm^{-1}$", "Ln(I)"],
                                legend=["I(q)-CONST","I(q)"])

        self._ui.edit_plot3.bind_datastorage(value,
                                             os.path.join(consts.DS, "./q3q4.txt"),
                                             label_list=["$q^2, nm^{-1}$", "Ln(I), arb. units"])

    @pyqtSlot(ndarray)
    def on_data4_load(self, value):
        # S(q)|I(q)|I(q)/S(q)| coef * S(q)
        self._ui.plot4.get_plot(value,
                                legend=["S(q)", "I(q)", "I(q)/S(q)", "$e^{a3+b3 \cdot q^2} \cdot S(q)$"])

    @pyqtSlot(int)
    def on_plot_scale_changed(self, index):
        selected = self._ui.get_cmb_options_by_index(index)
        self._ui.plot1.set_scale(selected)
        self._ui.edit_plot1.set_scale(selected)

    @pyqtSlot(int)
    def on_options_scale_changed(self, index):
        selected = self._ui.get_cmb_options_by_index(index)
        self._ui.plot2.set_scale(selected)
        self._ui.edit_plot2.set_scale(selected)

    @pyqtSlot(int)
    def on_result_scale_changed(self, index):
        selected = self._ui.get_cmb_options_by_index(index)
        self._ui.plot4.set_scale(selected)

    @pyqtSlot(bool)
    def on_plot_changed(self, value):
        self._ui.plot_widget_panel.setEnabled(value)

    @pyqtSlot()
    def validateCurrentPage(self):
        if self.currentId() == 0:
            if not self.field("file-path"):
                self.button(QWizard.NextButton).setEnabled(False)
            else:
                self.button(QWizard.NextButton).setEnabled(True)

        return True
