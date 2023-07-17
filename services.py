"""Services module."""

import logging
import numpy as np
from BL.SaxsGear import SaxsGear
from DTO.Reponse import Response
from consts import *
import cast as ct


class BaseService:

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )


class DataPreprocessingService(BaseService):
    """todo:
    specify custom status codes  depends on data
    Handle different exception types
    """

    def __init__(self, engine: SaxsGear) -> None:
        self.engine = engine
        super().__init__()

    def subtract_const(self, indicatrix_matrix: np.ndarray, q1: float, q2: float):
        # CUT OF MAIN CURVE
        """


        :param indicatrix_matrix:
        :param q1:
        :param q2:
        :return: q, I(q) - CONST
        """
        response = Response()
        try:
            response = self.engine.get_indicatrix_without_slope(indicatrix_matrix, q1, q2)

        except Exception as e:
            logging.debug(str(e))
            response.Status = False
            response.Message = e.args[0]

        return response

    def load_data(self, location: str) -> Response:
        """

        :param location: path to file with data
        :return: 2d ndarray
        """
        self.logger.debug("load_data was called")
        response = Response()

        try:
            response.data = self.engine.load_indicatrix(location)
        except Exception as e:
            self.logger.debug(e)
            response.Status = False
            response.Message = e.args[0]

        return response

    def convert_to_guinier(self, data) -> Response:
        """

        :param data: indicatrix matrix
        :return: the same but in log(I) of q^2
        """
        self.logger.debug("Convert to log(I) of q^2")
        response = Response()

        try:
            response = self.engine.to_guinier(data)
        except Exception as e:
            self.logger.debug(e)
            response.Status = False
            response.Message = e.args[0]

        return response

    def convert_to_q(self, data) -> Response:
        """

        """
        self.logger.debug("Convert to log(I) of q^2")
        response = Response()

        try:

            response.data = self.engine.convert_arg_to_q(data)
        except Exception as e:
            self.logger.debug(e)
            response.Status = False
            response.Message = e.args[0]

        return response

    def calculate_params(self, data, q3q4q5) -> Response:
        """


        :param data:
        :param q3q4q5:
        :return: Response object, with data-matrix represented by
        [
            S(q)|I(q)|I(q)/S(q)| coef * S(q)
        ],
        coef = EXP(a3_optimal+b3_optimal*q^2)


        """
        self.logger.debug("calculate_params")

        response = Response()

        try:
            # bounds
            q3 = q3q4q5[0]
            q4 = q3q4q5[2]
            # upper bound for linear regression
            q5 = q3q4q5[1]

            print(q3q4q5)

            # file format: |q^2 | lOG(I - CONST) | q^2 | lOG(i) | Q |i
            M3 = self.engine.extract_a_b_range(q3, q4, data, 0)
            np.savetxt("./tmp/M4.txt", np.c_[M3, ct.wize_log(M3[:,5])])

            b3 = self.engine.get_b(M3, q5)

            # we're assuming Indicatrix without constant
            q = M3[:, 4]
            I = M3[:, 5]

            SF = self.engine.get_structure_factor(q, start_D, start_KSI, start_r0)

            MN = I[0] / SF[0]

            a3 = np.log(MN)

            DELTA = self.engine.get_delta_for_min([a3, b3, start_D, start_KSI, start_r0], I, q)

            start = np.c_[q, MN * SF, q, I, q, I / (MN * SF)]

            print(DELTA, a3, b3, start_D, start_KSI, start_r0)

            print(q3q4q5)
            print(np.sqrt(q3))
            print(np.sqrt(q4))
            np.savetxt("./tmp/iq.txt", np.c_[q,I])

            mm = self.engine.get_min_by_delta(I, q, [a3, b3, start_D, start_KSI, start_r0])
            print(mm)

            if mm.success:
                opt_a3, opt_b3, opt_D, opt_KSI, opt_r0 = mm.x

                structure_factor = self.engine.get_structure_factor(q, opt_D, opt_KSI, opt_r0)

                response.data = np.c_[
                    q, structure_factor, q, I, q, I / structure_factor, q,
                    np.exp(opt_a3 + opt_b3 * np.power(q,2)) * structure_factor
                ]
            else:
                response.data = start
                response.Message = mm.message

        except Exception as e:
            self.logger.debug(e)
            response.Status = False
            response.Message = e.args[0]

        return response
