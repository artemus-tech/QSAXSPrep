import logging
import os
from typing import Union

from scipy.optimize import minimize
from scipy.special import gamma
from scipy.stats import linregress
from var_dump import var_dump

import Common.cast as ct
import numpy as np
from DTO.Reponse import Response


class SaxsGear:
    q_convert = 2 * np.pi / 0.1542 * 0.001

    q_index = 0
    I_index = 1

    def get_indicatrix_without_slope(self, indicatrix_matrix, q1, q2, ):
        """
        :param q1: lower bound
        :param q2:  upper bound
        :param indicatrix_matrix: target matrix of indicatrix
        :return: q,I(q)-CONST
        """
        resp = Response()

        try:
            if ct.matrix_is_valid(indicatrix_matrix):
                # get data between q1,q2
                iq_matrix_limited = self.extract_a_b_range(q1, q2, indicatrix_matrix, self.q_index)

                if iq_matrix_limited.size > 0:
                    # I^4
                    iq_matrix_limited[:, self.q_index] = np.power(iq_matrix_limited[:, self.q_index], 4)

                    # power up 4
                    q1_power4 = np.power(q1, 4)
                    q2_power4 = np.power(q2, 4)

                    # result extract by q^4
                    matrix_result = self.extract_a_b_range(q1_power4, q2_power4, iq_matrix_limited, self.q_index)

                    if matrix_result.size > 0:
                        # I= I * q
                        matrix_result[:, self.I_index] *= matrix_result[:, self.q_index]
                        # slope calculation
                        lr = linregress(matrix_result[:, self.q_index], matrix_result[:, self.I_index])
                        # slope subtraction
                        resp.data = np.c_[
                            indicatrix_matrix[:, self.q_index], indicatrix_matrix[:, self.I_index] - lr.slope]
                else:
                    resp.Status = False
                    resp.Message = "Zero sized range"
            else:
                resp.Status = False
                resp.Message = "Invalid matrix"
        except Exception as e:
            resp.Status = False
            resp.Message = e.args

        return resp

    def load_indicatrix(self, data: Union[str, np.ndarray], mrad_to_nm=False):
        """


        :param data: matrix or path to file with matrix
        :param mrad_to_nm: true if source file contains mrad specified argument
        :return: indicatrix matrix - 2d ndarray [q,I]
        """
        indicatrix_matrix = None

        if isinstance(data, str):
            try:
                indicatrix_matrix = ct.load_data(data)
            except Exception as e:
                raise Exception(e.args[0])

        elif isinstance(data, np.ndarray):
            if ct.matrix_is_valid(data):
                indicatrix_matrix = data
            else:
                logging.error(f'Input data invalid')
        if indicatrix_matrix is not None:
            if mrad_to_nm:
                indicatrix_matrix[:, self.q_index] *= self.q_convert

        return indicatrix_matrix

    def extract_a_b_range(self, a: float, b: float, data: np.array, column_index: int):
        """
        :param a: start argument range border
        :param b: end argument range border
        :param data:
        :return: extracted matrix by first column range
        """
        if a < b:
            return data[(data[:, column_index] >= a) & (data[:, column_index] <= b)]
        else:
            raise Exception("Upper bound should be greater than lower")

    def convert_arg_to_q(self, data):
        """
        Convert function to guiner
        :param data: matrix:[q,I ...]
        :return: matrix [q^2 log(I) ...]
        """
        if ct.matrix_is_valid(data):
            data[:, self.q_index] *= self.q_convert
            return data
        else:
            logging.error(f'Attempt to convert to guiner Invalid matrix')

    def to_guinier(self, data):
        resp = Response()
        """
        Convert function to guiner
        :param data: matrix:[q,I ...]
        :return: matrix [q^2 log(I) ...]
        """
        try:
            if ct.matrix_is_valid(data):
                if np.any(data[:, self.I_index] < 0):
                    resp.Message = "Intensity contains negative values"
                    resp.Status = False
                else:
                    resp.data = np.c_[np.power(data[:, self.q_index], 2), np.log(data[:, self.I_index])]
            else:
                resp.Message = "Attempt to convert to guiner coordinates Invalid matrix"
                resp.Status = False
        except Exception as e:
            resp.Message = e.args[0]
            resp.Status = False
        return resp

    def get_structure_factor(self, q_array, d, ksi, r0):

        numerator = d * gamma(d - 1.0)

        trouble = np.power(1 + np.power(q_array * ksi, -2), 0.5 * (d - 1))
        some_strange_thing = np.sin((d - 1.0) * np.arctan(q_array * ksi))

        res = 1.0 + numerator / (np.power(q_array * r0, d) * trouble) * some_strange_thing

        #if np.any(np.isnan(res)) or np.any(np.isposinf(res)) or np.any(np.isneginf(res)):
            #print(f'd={d}')
            #print(f'ksi={ksi}')
            #print(f'r0={r0}')
            #print(f'some_strange_thing = {some_strange_thing}')
            #print(f'touble = {trouble}')
            #print(f'numerator={numerator}')
        return res

    def get_fi(self, x, a, b, d, ksi, r0, clip=True):
        if clip:
            return a + b * np.power(x, 2) + ct.wize_log(self.get_structure_factor(x, d, ksi, r0))
        else:
            return a + b * np.power(x, 2) + np.log(self.get_structure_factor(x, d, ksi, r0))

    def get_delta_for_min(self, params, intensity_vector, x, clip=True):
        a, b, d, ksi, r0 = params
        if clip:
            DELTA = np.sum(
                np.power(self.get_fi(x, a, b, d, ksi, r0) - ct.wize_log(intensity_vector)
                         , 2))
        else:
            DELTA = np.sum(np.power(self.get_fi(x, a, b, d, ksi, r0) - np.log(intensity_vector), 2))
        with open("./tmp/delta_a_b_d_ksi_r0.txt", "a") as myfile:
            myfile.write(f'\n==================\n{DELTA}|{a}|{b}|{d}|{ksi}|{r0}\n')

        return DELTA

    def get_min_by_delta(self, I, q, params):
        a = params[0]
        b = params[1]

        d = params[2]
        ksi = params[3]
        r0 = params[4]
        """

        np.savetxt(f'./tmp/IQ_stat_params='
                   f'['
                   f'a={np.round(a,3)}_'
                   f'b={np,round(b,3)}_'
                   f'd={np.round(d,3)}_'
                   f'ksi={np.round(ksi,3)}_'
                   f'r0={np.round(r0,3)}'
                   f'].txt',np.c_[q,I])
        """

        res = minimize(self.get_delta_for_min,
                       np.array([a, b, d, ksi, r0]),
                       bounds=((0, 100), (-10, 0), (1.5, 6), (10, 1000), (2, 100)),
                       method='L-BFGS-B', args=(I, q), tol=1e-1,
                       #options={'disp': True}
                       options={
                           'disp': True,
                           'maxls': 20,
                           'iprint': -1,
                           'gtol': 1e-05,
                           'eps': 1e-08,
                           'maxiter': 15000,
                           'ftol': 2.220446049250313e-09,
                           'maxcor': 10,
                           'maxfun': 15000
                       })


        return res

    def get_b(self, data, cut_of_by_sqr_q=0.33):
        """

        :param data: extract range from guinier zone, it means that we are talking about sqr(q)
        :param cut_of_by_sqr_q: limit in Guinier coordinates, q^2
        :return: linear regression slope for  [q3, q4] range
        """
        # q^2
        data_extracted = data[(data[:, 0] >= cut_of_by_sqr_q)]
        np.savetxt("./tmp/data_extracted.txt", data_extracted)

        lr = linregress(data_extracted[:, 0], data_extracted[:, 1])

        return lr.slope
