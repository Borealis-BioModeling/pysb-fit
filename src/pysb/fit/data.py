import pysb
import numpy as np
import pandas as pd



class Tabular(pysb.Annotation):
    _datatype = 'tabular'

    def __init__(self, observable, filepath, x_col, y_col):
        self._data = None
        super(Tabular, self).__init__(observable, (filepath, x_col, y_col), 'fit-data')
    
    @staticmethod
    def _read_file(*args):
        return None

    @property
    def get_data(self):
        return self._data
    
    def load_data(self):
        if self._data is None:
            self._data = self._read_file(self.object[0], [self.object[1], self.object[2]])
        return

class CSVMixin():
    _filetype = 'csv'
    _extensions = ['csv']

    @staticmethod
    def _read_file(filepath, usecols):
        return pd.read_csv(filepath, usecols=usecols)


class ExcelMixin():
    _filetype = 'excel'
    _extensions = ['xls', 'xlsx']

    @staticmethod
    def _read_file(filepath, usecols):
        return pd.read_excel(filepath, usecols=usecols)

class ExcelData(Tabular, ExcelMixin):
    def __init__(self, observable, filepath, x_col, y_col):
        super(ExcelData, self).__init__(observable, filepath, x_col, y_col)

class CsvData(Tabular, CSVMixin):
    def __init__(self, observable, filepath, x_col, y_col):
        super(CsvData, self).__init__(observable, filepath, x_col, y_col)

class TimeSeries():
    _eee = 'eee'