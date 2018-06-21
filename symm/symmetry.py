import numpy as np
import scipy as sc

import scipy.interpolate
import scipy.optimize
import scipy.signal


def unzip(data_xy):
    x, y = zip(*data_xy)
    return np.array(list(x)), np.array(list(y))


class FunctionGenerator(object):
    def __init__(self):
        pass

    def to_function(self, data_xy: list):
        x, y = unzip(data_xy)
        f = sc.interpolate.UnivariateSpline(x, y, k=3, ext=1, s=0)
        return f

class SymmetryNorm(object):
    def __init__(self, interpolated_function: sc.interpolate.UnivariateSpline, evaluation_points):
        self._f = interpolated_function
        self._p = evaluation_points

    def norm(self, axis_position):
        if not (self._p[0] <= axis_position <= self._p[-1]):
            return np.inf



        # Usually, we would check self._f(axis_position + p) - self._f(axis_position - p)
        # Since, they might not be centered around zero, we shift the points such that they
        # are centered around zero (by subtracting axis_position), hence you have
        # f(axis_position + (p-axis_position)) - f(axis_position - (p - axis_position)) and
        # you arrive at the equation below :)
        evaluation = np.array([self._f(p) - self._f(2*axis_position - p) for p in self._p])

        norm = self._f.integral(self._p[0], self._p[-1])

        if norm > 0:
            return np.sum(np.square(evaluation / norm))
        else:
            return np.inf

    def __call__(self, x):
        return self.norm(x)


class SymmetryProblem(object):
    def __init__(self):
        pass

    def find_symmetry_axis(self, func: SymmetryNorm, x0):
        return sc.optimize.minimize(func, x0, method='Nelder-Mead')

    def find_peaks(self, data_xy):
        x, y = unzip(data_xy)
        return sc.signal.find_peaks_cwt(y, np.arange(1, len(data_xy)))


class Symmetry(object):
    def __init__(self, data_xy):
        self._data = data_xy
        self._x, self._y = unzip(data_xy)
        self._prob = SymmetryProblem()
        self._func = FunctionGenerator().to_function(data_xy)
        self._symNorm = SymmetryNorm(self._func, self._x)

    def find_peaks(self):
        x_index = self._prob.find_peaks(self._data)

        x = self._x[x_index]
        y = self._y[x_index]

        return list(zip(x, y))

    def optimize_symmetry(self, x0=None):
        if x0 is None:
            x0 = self._x[self._y.argmax()]

        return self._prob.find_symmetry_axis(self._symNorm, x0)

    def make_symmetric(self, symm_axis=None):
        if symm_axis is None:
            symm_axis = self.optimize_symmetry().x

        x, y = [], []
        x_bigger = self._x[self._x > symm_axis]
        x_lesser = self._x[self._x < symm_axis]
        diff = len(x_bigger) - len(x_lesser)
        # print("removing %s entries" % diff)
        if diff > 0:
            x = self._x[:-diff]
            y = self._y[:-diff]
        elif diff < 0:
            x = self._x[-diff:]
            y = self._y[-diff:]

        if len(x) > 0:
            # print(list(zip(x,y)))
            return Symmetry(list(zip(x, y)))
        else:
            return self

    def symmetry(self, x0):
        return self._symNorm.norm(x0)

    def get_function(self):
        return self._func

    def get_symmetry_function(self):
        return self._symNorm
