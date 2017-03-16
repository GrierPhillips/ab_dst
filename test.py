'''
test.py: File containing tests that relate to the development of the ab_dst
    gui.
'''
import unittest

from collections import OrderedDict

from property_generator import PropGen

# pylint: disable=W0212, C0301


class PropGenTest(unittest.TestCase):
    '''
    Suite of tests for methods contained in BasePropGen class.
    '''
    # def __init__(self, *args, **kwargs):
    #     super(PropGenTest, self).__init__(*args, methodName='runTest')

    def setUp(self):
        '''
        Setup the BasePropGen class befor each test.
        '''
        super(PropGenTest, self).setUp()
        self.template = 'test_template.properties'
        self.params = {
            'basepath': '/Users/grr/ab_dst/',
            'max.h.id': 200000}
        self.prop_gen = PropGen(self.template, self.params)

    def teardown(self):
        '''
        Teardown the BasePropGen class after each test.
        '''
        self.params = {}
        self.prop_gen = None

    def test_read_temp(self):
        '''
        The _read_temp method should return all of the lines in a template file.'''  # noqa
        lines = self.prop_gen._read_temp()
        expected = [
            'schedule.adjustment.parameters.file = BASEPATHFile.xls\n',
            'max.hh.id = 150000\n',
            'simulated.vehicle.dat.file = BASEPATHLOOP_PAIR/file_#.dat\n',
            'adjusted.schedules.output.file = BASEPATHLOOP_PAIR/file.csv\n',
            'special.purpose.models.trip.file = BASEPATHtruck/TRK_EXT\n']
        self.assertEqual(
            lines,
            expected,
            msg='Expected {}, but found {}'.format(expected, lines))

    def test_get_params(self):
        '''
        The _get_params method should collect a dictionary of all the key, value pairs present in the template file.'''  # noqa
        params = self.prop_gen._get_params()
        tuples = [
            ('schedule.adjustment.parameters.file ', 'BASEPATHFile.xls'),
            ('max.hh.id ', '150000'),
            ('simulated.vehicle.dat.file ', 'BASEPATHLOOP_PAIR/file_#.dat'),
            ('adjusted.schedules.output.file ', 'BASEPATHLOOP_PAIR/file.csv'),
            ('special.purpose.models.trip.file ', 'BASEPATHtruck/TRK_EXT')]
        expected = OrderedDict((key, value) for (key, value) in tuples)
        self.assertEqual(
            params,
            expected,
            msg='Expected {}, but found {}'.format(expected, params))

    def test_get_path_keys(self):
        '''
        The _get_path_keys method should set self.loop_path_keys and self.root_path_keys to lists of the keys in the template that require the root path or a loop path to be set.'''  # noqa
        roots = self.prop_gen.root_path_keys
        loops = self.prop_gen.loop_path_keys
        expected_roots = [
            'schedule.adjustment.parameters.file ',
            'special.purpose.models.trip.file ']
        expected_loops = [
            'simulated.vehicle.dat.file ',
            'adjusted.schedules.output.file ']
        self.assertEqual(
            expected_roots,
            roots,
            msg='Expected {}, but found {}.'.format(expected_roots, roots))
        self.assertEqual(
            expected_loops,
            loops,
            msg='Expected {}, but found {}.'.format(expected_loops, loops))
