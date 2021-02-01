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
    modeler = None

    @classmethod
    def setUpClass(cls):
        cls.desktop = Desktop("2021.1")
        cls.project = cls.desktop._main.oDesktop.NewProject()
        cls.tests_dir = os.path.abspath(os.path.dirname(__file__))
        cls.root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        etk.oDesktop = cls.desktop._main.oDesktop

    @classmethod
    def tearDownClass(cls):
        cls.desktop.release_desktop(close_projects=True)

    def vertex_from_edge_coord(self, coord, name, sort_key=1):
        edge = self.modeler.primitives.get_edgeid_from_position(coord, obj_name=name)
        vertices = self.modeler.primitives.get_edge_vertices(edge)
        vertex_coord = [self.modeler.primitives.get_vertex_position(vertex) for vertex in vertices]
        vertex_coord.sort(key=lambda x: x[sort_key])
        return vertex_coord


class TestIEEE(BaseAEDT):
    @classmethod
    def setUpClass(cls):
        super(TestIEEE, cls).setUpClass()

        cls.transformer = etk.TransformerClass(None)
        cls.transformer.read_material_data()
        with open(os.path.join(cls.root_dir, "src/ElectronicTransformer/examples/Demo_IEEE.json")) as file:
            etk.transformer_definition = json.load(file)
        etk.transformer_definition["setup_definition"]["project_path"] = cls.tests_dir

        cls.transformer.project = cls.project
        cls.transformer.setup_analysis()
        cls.modeler = Maxwell3D().modeler

    def test_airgap(self):
        """
        Check that airgap exists only on central leg
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

    def test_layer_turns(self):
        """
        Check that only 7 turns are created on layer 8
        """
        layers_list = self.modeler.get_matched_object_name("Layer8*")
        self.assertEqual(len(layers_list), 7)

    def test_conductor_dimensions(self):
        # width
        vertex_coord = self.vertex_from_edge_coord((0, 5.005, 0.27), "Layer3_3")
        self.assertListEqual(vertex_coord[0], [0.0, 4.32, 0.27])
        self.assertListEqual(vertex_coord[1], [0.0, 5.69, 0.27])

        # height
        vertex_coord = self.vertex_from_edge_coord((0, 5.69, 0.24), "Layer3_3", sort_key=2)
        self.assertListEqual(vertex_coord[0], [0.0, 5.69, 0.2])
        self.assertListEqual(vertex_coord[1], [0.0, 5.69, 0.27])

    def test_board_dimensions(self):
        # legth X
        vertex_coord = self.vertex_from_edge_coord((-2, 6.5, 1.01), "Board_8", sort_key=0)
        self.assertListEqual(vertex_coord[0], [-5.5, 6.5, 1.01])
        self.assertListEqual(vertex_coord[1], [0.0, 6.5, 1.01])

        # height Z
        vertex_coord = self.vertex_from_edge_coord((0, 6.5, 0.9), "Board_8", sort_key=2)
        self.assertListEqual(vertex_coord[0], [0.0, 6.5, 0.81])
        self.assertListEqual(vertex_coord[1], [0.0, 6.5, 1.01])

        # width Y
        vertex_coord = self.vertex_from_edge_coord((0, 4, 1.01), "Board_8", sort_key=2)
        self.assertListEqual(vertex_coord[0], [0.0, 2.5, 1.01])
        self.assertListEqual(vertex_coord[1], [0.0, 6.5, 1.01])
