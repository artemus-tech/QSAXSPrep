from typing import Tuple

from PyQt5.QtCore import QObject, pyqtSignal
from numpy import ndarray


class Model(QObject):
    load_file_path_changed = pyqtSignal(str)
    plot_scale_index_changed = pyqtSignal(int)
    options_scale_index_changed = pyqtSignal(int)
    result_scale_index_changed = pyqtSignal(int)
    structure_factor_scale_index_changed = pyqtSignal(int)

    has_error_occurs = pyqtSignal(bool)

    data_uploaded = pyqtSignal(ndarray)
    data2_uploaded = pyqtSignal(ndarray)
    data3_uploaded = pyqtSignal(ndarray)
    data4_uploaded = pyqtSignal(ndarray)
    data5_uploaded = pyqtSignal(ndarray)

    enable_plot_changed = pyqtSignal(bool)
    arg_changed = pyqtSignal(int)

    @property
    def filepath(self):
        return self._filepath

    @property
    def arg(self):
        return self._arg

    @arg.setter
    def arg(self, value):
        self._arg = value
        self.arg_changed.emit(value)

    @property
    def enable_plot(self):
        return self._enable_plot

    @property
    def plot_scale_index(self):
        return self._plot_scale_index

    @plot_scale_index.setter
    def plot_scale_index(self, index):
        self._plot_scale_index = index
        self.plot_scale_index_changed.emit(index)

    @property
    def options_scale_index(self):
        return self._options_scale_index

    @options_scale_index.setter
    def options_scale_index(self, index):
        self._options_scale_index = index
        self.options_scale_index_changed.emit(index)

    @property
    def structure_factor_scale_index(self):
        return self._structure_factor_scale_index

    @structure_factor_scale_index.setter
    def structure_factor_scale_index(self, index):
        self._structure_factor_scale_index = index
        self.structure_factor_scale_index_changed.emit(index)



    @property
    def has_error(self):
        return self._has_error

    @has_error.setter
    def has_error(self, flag):
        self._has_error = flag
        self.has_error_occurs.emit(flag)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, text):
        self._message = text

    @property
    def result_scale_index(self):
        return self._result_scale_index

    @result_scale_index.setter
    def result_scale_index(self, index):
        self._result_scale_index = index
        self.result_scale_index_changed.emit(index)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
        self.data_uploaded.emit(data)

    @property
    def data2(self):
        return self._data2

    @data2.setter
    def data2(self, data2):
        self._data2 = data2
        self.data2_uploaded.emit(data2)

    @property
    def data3(self):
        return self._data3

    @data3.setter
    def data3(self, data3):
        self._data3 = data3
        self.data3_uploaded.emit(data3)


    @property
    def data4(self):
        return self._data4

    @data4.setter
    def data4(self, data4):
        self._data4 = data4
        self.data4_uploaded.emit(data4)


    @filepath.setter
    def filepath(self, value):
        self._filepath = value
        self.load_file_path_changed.emit(value)

    @enable_plot.setter
    def enable_plot(self, value):
        self._enable_plot = value
        self.enable_plot_changed.emit(value)

    def __init__(self):
        super().__init__()

        self._data4 = None
        self._message = ""
        self._has_error = False

        self._arg = False
        self._enable_plot = False

        self._data = None
        self._data2 = None
        self._data3 = None

        self._filepath = ''
        self._enable_reset = False

        self._plot_scale_index = 0
        self._options_scale_index = 0
        self._result_scale_index = 0
        self._structure_factor_scale_index = 0

    def reset(self) -> None:
        if '_data' in self.l__dict__:
            del self._data
        if '_data2' in self.__dict__:
            del self._data2
        if '_data3' in self.__dict__:
            del self._data3
        if '_filepath' in self.__dict__:
            del self._filepath
        if '_message' in self.__dict__:
            del self._message
        if '_has_error' in self.__dict__:
            del self._has_error
        if '_enable_plot' in self.__dict__:
            del self._enable_plot
        if '_options_scale_index' in self.__dict__:
            del self._options_scale_index
        if '_plot_scale_index' in self.__dict__:
            del self._plot_scale_index
        if '_arg_changed' in self.__dict__:
            del self.arg_changed
        if '_enable_reset' in self.__dict__:
            del self._enable_reset
