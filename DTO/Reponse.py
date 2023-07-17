from dataclasses import dataclass

import numpy as np

import Common.cast as ct


@dataclass
class Response:
    """Class for Data transfer"""
    Status : bool = True
    Message: str = "Success"
    data : np.ndarray = ct.init_zero_length_array()

