import logging
import os.path

import numpy as np
from PyQt5.QtCore import QObject, pyqtSlot

import consts


class MainController(QObject):
    def __init__(self, model, saxs_input_service):
        super().__init__()

        self._model = model
        self._saxs_input_service = saxs_input_service

    @pyqtSlot(str)
    def next_step(self, i):
        # First step
        np.savetxt("./tmp/M0.txt",self._model.data)
        if i == 1:
            # load q1/q2
            q1q2 = np.loadtxt(os.path.join(consts.DS, "q1q2.txt"))
            q1 = q1q2[0]
            q2 = q1q2[1]

            subtract = self._saxs_input_service.subtract_const(self._model.data, q1, q2)

            if subtract.Status:
                self._model.data2 = np.c_[subtract.data, self._model.data]


            else:
                self._model.message = subtract.Message
                self._model.has_error = subtract.Status
            np.savetxt("./tmp/M1.txt", self._model.data2)

        if i == 2:
            guiner_convert_result = self._saxs_input_service.convert_to_guinier(self._model.data2)

            if not guiner_convert_result.Status:
                self._model.message = guiner_convert_result.Message
                self._model.has_error = guiner_convert_result.Status

            guiner_src_convert_result = self._saxs_input_service.convert_to_guinier(self._model.data)

            if not guiner_src_convert_result.Status:
                self._model.message = guiner_convert_result.Message
                self._model.has_error = guiner_convert_result.Status

            if guiner_src_convert_result.Status and guiner_convert_result.Status:
                self._model.data3 = np.c_[guiner_convert_result.data, guiner_src_convert_result.data]

            np.savetxt("./tmp/M2.txt", self._model.data3)

        if i == 3:
            # loading q1,q2,q3,q4
            q3q4 = np.loadtxt(os.path.join(consts.DS, "q3q4.txt"))

            optimize_result = self._saxs_input_service.calculate_params(
                np.c_[self._model.data3, self._model.data2],
                q3q4
            )

            if optimize_result.Status:
                self._model.data4 = optimize_result.data
            else:
                self._model.message = optimize_result.Message
                self._model.has_error = optimize_result.Status

    @pyqtSlot(int)
    def change_plot_scale(self, index):
        # set proper index for scale
        self._model.plot_scale_index = index
        # recalculation has been  started

    @pyqtSlot(int)
    def change_arg(self, value):
        """
        # set proper index for scale
        self._model.arg = value
        # recalculation has been  started
        if value == 2:
            result = self._saxs_input_service.convert_to_q(self._model.data)
            self._model.data = result.data
        if value == 0:
            result = self._saxs_input_service.convert_to_ang(self._model.data)
            self._model.data = result.data
        """

    @pyqtSlot(int)
    def change_options_scale(self, index):
        # set proper index for scale
        self._model.options_scale_index = index

    @pyqtSlot(int)
    def change_result_scale(self, index):
        # set proper index for scale
        self._model.result_scale_index = index

    @pyqtSlot(int)
    def change_structure_factor_scale(self, index):
        # set proper index for scale
        self._model.structure_factor_scale_index = index

    @pyqtSlot(str)
    def load_file(self, value):
        try:

            result = self._saxs_input_service.load_data(value)
            if result.Status:
                self._model.filepath = value
                self._model.data = result.data

        except Exception as e:
            raise Exception(e)
