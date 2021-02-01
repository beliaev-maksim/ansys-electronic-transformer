import copy
import json
import os
from unittest import TestCase
from AEDTLib.Desktop import Desktop

import src.ElectronicTransformer.etk_callback as etk
from src.ElectronicTransformer.circuit import Circuit
from src.ElectronicTransformer.cores_geometry import (ECore, EFDCore, EICore, EPCore, ETDCore,
                                                      PCore, PQCore, UCore, UICore, RMCore)


class BaseAEDT(TestCase):
    desktop = None
    project = None
    tests_dir = None
    root_dir = None

    @classmethod
    def setUpClass(cls):
        cls.desktop = Desktop("2021.1")
        cls.project = cls.desktop._main.oDesktop.NewProject()
        cls.tests_dir = os.path.abspath(os.path.dirname(__file__))
        cls.root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        etk.oDesktop = cls.desktop._main.oDesktop
        etk.ECore = ECore
        etk.EFDCore = EFDCore
        etk.EICore = EICore
        etk.EPCore = EPCore
        etk.ETDCore = ETDCore
        etk.PCore = PCore
        etk.PQCore = PQCore
        etk.UCore = UCore
        etk.UICore = UICore
        etk.RMCore = RMCore
        etk.Circuit = Circuit

    @classmethod
    def tearDownClass(cls):
        cls.desktop.release_desktop(close_projects=True)


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

    def test_ieee(self):
        pass
