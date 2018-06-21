import numpy as np

import pylab as pl
from uxdconverter.raw.converter import MeasurementsConverter
from uxdconverter.raw.parser import RawParser

from symm.symmetry import Symmetry, unzip

class Plot(object):
    def plot(self, data_xy, color='b'):
        symm = Symmetry(data_xy)

        peaks = symm.find_peaks()
        symm_axis = symm.optimize_symmetry()

        func = symm.get_symmetry_function()

        x, y = unzip(data_xy)
        func = symm.get_function()


        print("Peaks at (x,y):")
        print(peaks)

        for peak in peaks:
            pl.axvline(peak[0], linestyle='--', color=color)

        pl.plot(x, y)

        x_space = np.linspace(x[0], x[-1], num=200)
        pl.plot(x_space, func(x_space))

        print("Found axis at %s with symmetry %s" % (symm_axis.x, symm_axis.fun))

        pl.axvline(symm_axis.x, color=color)



        symm_opt = symm.make_symmetric(symm_axis.x)
        symm_axis = symm_opt.optimize_symmetry()

        print("Found new axis at %s with symmetry %s" % (symm_axis.x, symm_axis.fun))
        pl.axvline(symm_axis.x, linestyle='--', color=color)
        print()
        print()

        # pl.show()
        # mirror to the right
        # right_space = np.linspace(0, x[-1] - symm_axis.x, num=100)
        # pl.plot(right_space + symm_axis.x, func(-right_space+symm_axis.x))
        # mirror to the left
        # left_space = np.linspace(x[0] - symm_axis.x, 0, num=100)
        # pl.plot(left_space +symm_axis.x, func(-left_space+symm_axis.x))


class Loader(object):
    def __init__(self):
        self._plotter = Plot()
        self._parser = MeasurementsConverter()

    def load(self, file, color):

        try:
            rawms = RawParser().parse_from_file(file)
            print("Loaded file %s" % file)
        except BaseException as e:
            print("Cannot parse file %s" % file)

            print(e)
            return

        measurement = rawms.get_measurements()[0]
        stepsize = measurement.get_header().get_step_size()
        steptime = measurement.get_header().get_step_time()
        start = measurement.get_header().get_start_two_theta()

        # Convert to counts per second
        data_y = np.array(measurement.get_data().get_data_points()) / steptime
        data_x = np.array(range(0, measurement.get_data().get_number_of_data_points())) * stepsize + start
        data_xy = list(zip(data_x, data_y))

        self._plotter.plot(data_xy, color=color)


loader = Loader()


# file = '/mnt/hektor/measure/Dünnschicht/XRD/Alex/Alignment_2018_March/12_alignment_source_slit_0d2/262_SS0d2_'
# rawms = RawParser().parse_from_file(file)
# loader.load(file + 'DS.raw', 'b')
# loader.load(file + 'BS.raw', 'r')

def load(number, slit='0d1'):
    pl.cla()

    print(len(slit))
    if not slit  == '':
        file = '/mnt/hektor/measure/Dünnschicht/XRD/Alex/03_Alignment/Alignment_2018_June/09_ReAlign_Exit_Slit/' + str(number) + '_' + slit + '_'
    else:
        file = '/mnt/hektor/measure/Dünnschicht/XRD/Alex/03_Alignment/Alignment_2018_June/09_ReAlign_Exit_Slit/' + str(number) + '_'

    loader.load(file + 'DS.raw', 'b')
    loader.load(file + 'BS.raw', 'r')

load('23', '')