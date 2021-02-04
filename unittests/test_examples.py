import json
import os
import shutil
from unittest import TestCase
from AEDTLib.Desktop import Desktop
from AEDTLib.Maxwell import Maxwell3D

import src.ElectronicTransformer.etk_callback as etk


class BaseAEDT(TestCase):
    report_path = None
    transformer = None
    desktop = None
    project = None
    tests_dir = None
    root_dir = None
    m3d = None
    input_file = None

    @classmethod
    def setUpClass(cls):
        cls.desktop = Desktop("2021.1")
        cls.project = cls.desktop._main.oDesktop.NewProject()
        cls.tests_dir = os.path.abspath(os.path.dirname(__file__))
        cls.root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        cls.report_path = os.path.join(cls.tests_dir, "report.tab")
        etk.oDesktop = cls.desktop._main.oDesktop

        with open(os.path.join(cls.root_dir, cls.input_file)) as file:
            etk.transformer_definition = json.load(file)
        etk.transformer_definition["setup_definition"]["project_path"] = cls.tests_dir

        cls.transformer = etk.TransformerClass(None)
        cls.transformer.read_material_data()
        cls.transformer.project = cls.project
        cls.transformer.setup_analysis()
        cls.transformer.design.Analyze("Setup1")
        cls.m3d = Maxwell3D()

    @classmethod
    def tearDownClass(cls):
        cls.desktop.release_desktop(close_projects=True)

        project_file = os.path.join(cls.tests_dir, cls.transformer.design_name + '.aedt')
        if os.path.isfile(project_file):
            os.remove(project_file)

        project_results = project_file + "results"
        if os.path.isdir(project_results):
            shutil.rmtree(project_results)

        json_file = os.path.join(cls.tests_dir, cls.transformer.design_name + '_parameters.json')
        if os.path.isfile(json_file):
            os.remove(json_file)

        circuit_file = os.path.join(cls.tests_dir, cls.transformer.design_name + '"_circuit.sph"')
        if os.path.isfile(circuit_file):
            os.remove(circuit_file)

        if os.path.isfile(cls.report_path):
            os.remove(cls.report_path)

    def vertex_from_edge_coord(self, coord, name, sort_key=1):
        edge = self.m3d.modeler.primitives.get_edgeid_from_position(coord, obj_name=name)
        vertices = self.m3d.modeler.primitives.get_edge_vertices(edge)
        vertex_coord = [self.m3d.modeler.primitives.get_vertex_position(vertex) for vertex in vertices]
        vertex_coord.sort(key=lambda x: x[sort_key])
        return vertex_coord

    def set_freq_units(self, plot):
        """
        Set primary frequency units for report to kHz
        """
        self.transformer.module_report.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Data Filter",
                    [
                        "NAME:PropServers",
                        plot + ":PrimarySweepDrawing"
                    ],
                    [
                        "NAME:ChangedProps",
                        [
                            "NAME:Number Format",
                            "Value:="	, "Scientific"
                        ],
                        [
                            "NAME:Units",
                            "Value:="		, "kHz"
                        ]
                    ]
                ]
            ])

    def compare_leakage(self, ref_name):
        """
        exports leakage report and compares all values for tolerance of 2%
        """
        self.set_freq_units("Leakage Inductance")
        self.transformer.module_report.ExportToFile("Leakage Inductance", self.report_path, False)

        reference_path = os.path.join(self.tests_dir, "reference_results", ref_name)
        with open(reference_path) as ref_file, open(self.report_path) as actual_file:
            next(ref_file)
            next(actual_file)

            for line1, line2 in zip(ref_file, actual_file):
                ref_result = [float(val) for val in line1.split()]
                actual_result = [float(val) for val in line2.split()]

                for actual, ref in zip(actual_result, ref_result):
                    self.assertAlmostEqual(actual, ref, delta=ref*0.02,
                                           msg="Error at frequency {}kHz".format(ref_result[0]))


class TestIEEE(BaseAEDT):
    @classmethod
    def setUpClass(cls):
        cls.input_file = r"src/ElectronicTransformer/examples/Demo_IEEE.json"
        super(TestIEEE, cls).setUpClass()

    def test_01_air_gap(self):
        """
        Check that air gap exists only on central leg
        """
        vertex_coord = self.vertex_from_edge_coord((0, 0, 1.08), "I_Core")
        self.assertListEqual(vertex_coord[0], [0.0, -2.5, 1.08])
        self.assertListEqual(vertex_coord[1], [0.0, 2.5, 1.08])

        vertex_coord = self.vertex_from_edge_coord((0, 0, 0.98), "E_Core")
        self.assertListEqual(vertex_coord[0], [0.0, -2.5, 0.98])
        self.assertListEqual(vertex_coord[1], [0.0, 2.5, 0.98])

        vertex_coord = self.vertex_from_edge_coord((-5.5, 0, 1.08), "E_Core")
        self.assertListEqual(vertex_coord[0], [-5.5, -2.5, 1.08])
        self.assertListEqual(vertex_coord[1], [-5.5, 2.5, 1.08])

    def test_02_layer_turns(self):
        """
        Check that only 7 turns are created on layer 8
        """
        # layers + terminals
        layers_list = self.m3d.modeler.get_matched_object_name("Layer8*")
        self.assertEqual(len(layers_list), 14)

        # terminals
        layers_list = self.m3d.modeler.get_matched_object_name("Layer8*Section*")
        self.assertEqual(len(layers_list), 7)

    def test_03_conductor_dimensions(self):
        """
        Test conductor cross section
        """
        # width
        vertex_coord = self.vertex_from_edge_coord((0.0, 5.0, -0.27), "Layer3_3")
        self.assertListEqual(vertex_coord[0], [0.0, 4.87, -0.27])
        self.assertListEqual(vertex_coord[1], [0.0, 5.68, -0.27])

        # height
        vertex_coord = self.vertex_from_edge_coord((0, 5.68, -0.3), "Layer3_3", sort_key=2)
        self.assertListEqual(vertex_coord[0], [0.0, 5.68, -0.34])
        self.assertListEqual(vertex_coord[1], [0.0, 5.68, -0.27])

    def test_04_board_dimensions(self):
        """
        Test board XYZ dimensions
        """
        # length X
        vertex_coord = self.vertex_from_edge_coord((-2, 6.5, 1.01), "Board_8", sort_key=0)
        self.assertListEqual(vertex_coord[0], [-5.5, 6.5, 1.01])
        self.assertListEqual(vertex_coord[1], [0.0, 6.5, 1.01])

        # height Z
        vertex_coord = self.vertex_from_edge_coord((0, 6.5, 0.9), "Board_8", sort_key=2)
        self.assertListEqual(vertex_coord[0], [0.0, 6.5, 0.81])
        self.assertListEqual(vertex_coord[1], [0.0, 6.5, 1.01])

        # width Y
        vertex_coord = self.vertex_from_edge_coord((0, 4, 1.01), "Board_8", sort_key=1)
        self.assertListEqual(vertex_coord[0], [0.0, 2.5, 1.01])
        self.assertListEqual(vertex_coord[1], [0.0, 6.5, 1.01])

    def test_05_solid_loss(self):
        """
        Validate that SolidLoss are in range of 2% compared to reference
        """
        loss_data = self.m3d.post.get_report_data(expression="SolidLoss")
        loss_list = loss_data.data_magnitude(convert_to_SI=True)
        reference_loss = [3.080731857, 1.748884788, 0.5832313415, 0.1444371145, 0.03405255505, 0.008900580792,
                          0.002791398746, 0.001092512493, 0.0005868312835, 0.0005630288807, 0.0004394943406]

        for actual, ref in zip(loss_list, reference_loss):
            self.assertAlmostEqual(actual, ref, delta=ref*0.02)

    def test_06_core_loss(self):
        """
        Validate that CoreLoss are in range of 2% compared to reference
        """
        loss_data = self.m3d.post.get_report_data(expression="CoreLoss")
        loss_list = loss_data.data_magnitude(convert_to_SI=True)
        reference_loss = [0.000917459, 0.00165295, 0.00167635, 0.00121922, 0.000800248, 0.000512619,
                          0.000326723, 0.00020805, 0.000132453, 0.000126782, 8.43752e-05]

        for actual, ref in zip(loss_list, reference_loss):
            self.assertAlmostEqual(actual, ref, delta=ref*0.02)

    def test_07_leakage_inductance(self):
        """
        Validate that leakage is in range of 2% difference
        """
        self.compare_leakage("ieee_leakage.tab")
