import json
import os
from unittest import TestCase
from AEDTLib.Desktop import Desktop
from AEDTLib.Maxwell import Maxwell3D

import src.ElectronicTransformer.etk_callback as etk


class BaseAEDT(TestCase):
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

    def vertex_from_edge_coord(self, coord, name, sort_key=1):
        edge = self.m3d.modeler.primitives.get_edgeid_from_position(coord, obj_name=name)
        vertices = self.m3d.modeler.primitives.get_edge_vertices(edge)
        vertex_coord = [self.m3d.modeler.primitives.get_vertex_position(vertex) for vertex in vertices]
        vertex_coord.sort(key=lambda x: x[sort_key])
        return vertex_coord


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
        loss_list = loss_data.data_real()
        reference_loss = [3.081896003, 1.74967242, 0.58353638669999996,
                          0.14452348509999999, 0.034080710239999999, 0.0089145264179999999,
                          0.0027996223349999998, 0.0010978606290000001, 0.0005911507562,
                          0.00044453803220000001, 3.4544006230000002e-06]

        for actual, ref in zip(loss_list, reference_loss):
            self.assertAlmostEqual(actual, ref, delta=ref*0.02)
