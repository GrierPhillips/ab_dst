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
            'max.hh.id ': '200000',
            'special.purpose.models.trip.file ': 'ARC_TRK-EXT_dep_second.csv'}
        self.prop_gen = PropGen(self.template, self.params)
        self.expected_in = [
            ('schedule.adjustment.parameters.file ',
             'BASEPATHSchedule_Adjustment_LP_Parameters_Revised_test.xls'),
            ('max.hh.id ', '150000'),
            ('simulated.vehicle.dat.file ',
             'BASEPATHLOOP_PAIR/output_vehicle_#.dat'),
            ('adjusted.schedules.output.file ',
             'BASEPATHLOOP_PAIR/adjusted_schedules_#.csv'),
            ('inner.loop.abm.data.folder ', 'BASEPATHOUTER/abmData'),
            ('special.purpose.models.trip.file ', 'BASEPATHtruck/TRK_EXT')]

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
            'schedule.adjustment.parameters.file = BASEPATHSchedule_Adjustment_LP_Parameters_Revised_test.xls\n',  # noqa
            'max.hh.id = 150000\n',
            'simulated.vehicle.dat.file = BASEPATHLOOP_PAIR/output_vehicle_#.dat\n',  # noqa
            'adjusted.schedules.output.file = BASEPATHLOOP_PAIR/adjusted_schedules_#.csv\n',  # noqa
            'inner.loop.abm.data.folder = BASEPATHOUTER/abmData\n',
            'special.purpose.models.trip.file = BASEPATHtruck/TRK_EXT\n']
        self.assertEqual(
            lines,
            expected,
            msg='Expected {}, but found {}'.format(expected, lines)
        )

    def test_get_params(self):
        '''
        The _get_params method should collect a dictionary of all the key, value pairs present in the template file.'''  # noqa
        params = self.prop_gen._get_params()
        expected = OrderedDict(
            (key, value) for (key, value) in self.expected_in
        )
        self.assertEqual(
            params,
            expected,
            msg='Expected {}, but found {}'.format(expected, params)
        )

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
            'adjusted.schedules.output.file ',
            'inner.loop.abm.data.folder ']
        self.assertEqual(
            expected_roots,
            roots,
            msg='Expected {}, but found {}.'.format(expected_roots, roots))
        self.assertEqual(
            expected_loops,
            loops,
            msg='Expected {}, but found {}.'.format(expected_loops, loops))

    def test_set_root_paths(self):
        '''
        The _set_root_paths method should set the value of BASEPATH in the template values to the value of 'basepath' provided in the user parameter dictionary.'''  # noqa
        for key in self.prop_gen.params.keys():
            self.prop_gen.set_root_paths(key, self.params['basepath'])
        expected_tuples = [
            ('schedule.adjustment.parameters.file ',
             '/Users/grr/ab_dst/Schedule_Adjustment_LP_Parameters_Revised_test.xls'),  # noqa
            ('max.hh.id ', '150000'),
            ('simulated.vehicle.dat.file ',
             '/Users/grr/ab_dst/LOOP_PAIR/output_vehicle_#.dat'),
            ('adjusted.schedules.output.file ',
             '/Users/grr/ab_dst/LOOP_PAIR/adjusted_schedules_#.csv'),
            ('inner.loop.abm.data.folder ',
             '/Users/grr/ab_dst/OUTER/abmData'),
            ('special.purpose.models.trip.file ',
             '/Users/grr/ab_dst/truck/TRK_EXT')]
        expected = OrderedDict(
            (key, value) for (key, value) in expected_tuples
        )
        self.assertEqual(
            expected,
            self.prop_gen.params,
            msg='Expected {}, but found {}.'.format(
                expected, self.prop_gen.params)
        )

    def test_set_loop_paths_inner_not_0(self):
        '''
        The _set_loop_paths method should set the value of LOOP_PAIR or OUTER in the template values with the values for the current loop.'''  # noqa
        for key in self.prop_gen.params.keys():
            self.prop_gen.set_loop_paths(key, '0', '1')
        expected_tuples = [
            ('schedule.adjustment.parameters.file ',
             'BASEPATHSchedule_Adjustment_LP_Parameters_Revised_test.xls'),
            ('max.hh.id ', '150000'),
            ('simulated.vehicle.dat.file ',
             '/Users/grr/ab_dst/outer0/inner0/output_vehicle_0.dat'),
            ('adjusted.schedules.output.file ',
             'BASEPATHouter0/inner1/adjusted_schedules_1.csv'),
            ('inner.loop.abm.data.folder ',
             'BASEPATHouter0/abmData'),
            ('special.purpose.models.trip.file ',
             'BASEPATHtruck/TRK_EXT')]
        expected = OrderedDict(
            (key, value) for (key, value) in expected_tuples
        )
        self.assertEqual(
            expected,
            self.prop_gen.params,
            msg='Expected {}, but found {}.'.format(
                expected, self.prop_gen.params)
        )

    def test_set_loop_paths_inner0(self):
        '''
        If inner is 0 the _set_loop_paths method should set the values for keys in the self.offset_keys list to an empty string.'''  # noqa
        for key in self.prop_gen.params.keys():
            self.prop_gen.set_loop_paths(key, '0', '0')
        expected_tuples = [
            ('schedule.adjustment.parameters.file ',
             'BASEPATHSchedule_Adjustment_LP_Parameters_Revised_test.xls'),
            ('max.hh.id ', '150000'),
            ('simulated.vehicle.dat.file ',
             ''),
            ('adjusted.schedules.output.file ',
             'BASEPATHouter0/inner0/adjusted_schedules_0.csv'),
            ('inner.loop.abm.data.folder ',
             'BASEPATHouter0/abmData'),
            ('special.purpose.models.trip.file ',
             'BASEPATHtruck/TRK_EXT')]
        expected = OrderedDict(
            (key, value) for (key, value) in expected_tuples
        )
        self.assertEqual(
            expected,
            self.prop_gen.params,
            msg='Expected {}, but found {}.'.format(
                expected, self.prop_gen.params)
        )

    def test_set_path(self):
        '''
        The _set_path method should set the proper paths for parameters containing paths. This includes the current iteration number.'''  # noqa
        for key in self.prop_gen.params.keys():
            self.prop_gen._set_path(key, '0', '0', '/Users/grr/ab_dst/')
        expected_tuples = [
            ('schedule.adjustment.parameters.file ',
             '/Users/grr/ab_dst/Schedule_Adjustment_LP_Parameters_Revised_test.xls'),  # noqa
            ('max.hh.id ', '150000'),
            ('simulated.vehicle.dat.file ',
             ''),
            ('adjusted.schedules.output.file ',
             '/Users/grr/ab_dst/outer0/inner0/adjusted_schedules_0.csv'),
            ('inner.loop.abm.data.folder ',
             '/Users/grr/ab_dst/outer0/abmData'),
            ('special.purpose.models.trip.file ',
             '/Users/grr/ab_dst/truck/TRK_EXT')]
        expected = OrderedDict(
            (key, value) for (key, value) in expected_tuples
        )
        self.assertEqual(
            expected,
            self.prop_gen.params,
            msg='Expeced {}, but found {}.'.format(
                expected, self.prop_gen.params)
        )

    def test_set_values0(self):
        '''
        The _set_values method should set the parameter value for each parameter key in the user supplied parameters dictionary.'''  # noqa
        self.prop_gen._set_values('0', '0')
        expected_tuples = [
            ('schedule.adjustment.parameters.file ',
             '/Users/grr/ab_dst/Schedule_Adjustment_LP_Parameters_Revised_test.xls'),  # noqa
            ('max.hh.id ', '200000'),
            ('simulated.vehicle.dat.file ',
             ''),
            ('adjusted.schedules.output.file ',
             '/Users/grr/ab_dst/outer0/inner0/adjusted_schedules_0.csv'),
            ('inner.loop.abm.data.folder ',
             '/Users/grr/ab_dst/outer0/abmData'),
            ('special.purpose.models.trip.file ',
             '/Users/grr/ab_dst/truck/ARC_TRK-EXT_dep_second.csv')]
        expected = OrderedDict(
            (key, value) for (key, value) in expected_tuples
        )
        self.assertEqual(
            expected,
            self.prop_gen.params,
            msg='Expected {}, but found {}.'.format(
                expected, self.prop_gen.params)
        )

    def test_set_values_not_0(self):
        '''
        If inner is not 0, the _set_values method should set loop value appropriately, esp note simulated.vehicle.dat.file and an empty string for special.purpose.models.trip.file.'''  # noqa
        self.prop_gen._set_values('0', '1')
        expected_tuples = [
            ('schedule.adjustment.parameters.file ',
             '/Users/grr/ab_dst/Schedule_Adjustment_LP_Parameters_Revised_test.xls'),  # noqa
            ('max.hh.id ', '200000'),
            ('simulated.vehicle.dat.file ',
             '/Users/grr/ab_dst/outer0/inner0/output_vehicle_0.dat'),
            ('adjusted.schedules.output.file ',
             '/Users/grr/ab_dst/outer0/inner1/adjusted_schedules_1.csv'),
            ('inner.loop.abm.data.folder ',
             '/Users/grr/ab_dst/outer0/abmData'),
            ('special.purpose.models.trip.file ',
             '')]
        expected = OrderedDict(
            (key, value) for (key, value) in expected_tuples
        )
        self.assertEqual(
            expected,
            self.prop_gen.params,
            msg='Expected {}, but found {}.'.format(
                expected, self.prop_gen.params)
        )

    def test_create(self):
        '''
        The create method should properly set all values and create a properties file.'''  # noqa
        self.prop_gen.create('test_output', '0', '0')
        with open('test_output', 'r') as file_obj:
            lines = file_obj.readlines()
        expected = [
            'schedule.adjustment.parameters.file = /Users/grr/ab_dst/Schedule_Adjustment_LP_Parameters_Revised_test.xls\n',  # noqa
            'max.hh.id = 200000\n',
            'simulated.vehicle.dat.file = \n',
            "adjusted.schedules.output.file = /Users/grr/ab_dst/outer0/inner0/adjusted_schedules_0.csv\n",  # noqa
            'inner.loop.abm.data.folder = /Users/grr/ab_dst/outer0/abmData\n',
            'special.purpose.models.trip.file = /Users/grr/ab_dst/truck/ARC_TRK-EXT_dep_second.csv\n'  # noqa
        ]
        self.assertEqual(
            expected,
            lines,
            msg='Expected {}, but found {}.'.format(expected, lines)
        )
