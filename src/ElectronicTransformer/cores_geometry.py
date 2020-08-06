# already done: E, EI, ETD = EC = EQ = ER(with argument), EFD, EP, PQ, P=PH=PT(with    argument), RM, U, UI

# super class Cores
# all sub classes for core creation will inherit from here basic parameters from GUI and
# take all functions for primitive creation like createBox, createPolyhedron, move, rename and so on
import math


class Cores(object):
    CS = 'Global'

    def __init__(self, args_list):
        transformer_definition = args_list[0]
        self.oProject = args_list[1]
        self.oDesign = args_list[2]
        self.oEditor = args_list[3]

        # Draw in Base Core
        self.dim_D1 = float(transformer_definition["core_dimensions"]["D_1"])
        self.dim_D2 = float(transformer_definition["core_dimensions"]["D_2"])
        self.dim_D3 = float(transformer_definition["core_dimensions"]["D_3"])
        self.dim_D4 = float(transformer_definition["core_dimensions"]["D_4"])
        self.dim_D5 = float(transformer_definition["core_dimensions"]["D_5"])
        self.dim_D6 = float(transformer_definition["core_dimensions"]["D_6"])
        self.dim_D7 = float(transformer_definition["core_dimensions"]["D_7"])
        self.dim_D8 = float(transformer_definition["core_dimensions"]["D_8"])

        self.segmentation_angle = transformer_definition["core_dimensions"]["segmentation_angle"]
        self.segments_number = 0 if self.segmentation_angle == 0 else int(360/self.segmentation_angle)

        self.airgap_side = 0
        self.airgap_center = 0
        self.airgap_both = 0

        airgap = transformer_definition["core_dimensions"]["airgap"]
        if airgap["define_airgap"]:
            airgap_size = float(airgap["airgap_value"])/2.0
            if airgap["airgap_on_leg"] == 'Center':
                self.airgap_center = airgap_size
            elif airgap["airgap_on_leg"] == 'Side':
                self.airgap_side = airgap_size
            else:
                self.airgap_both = airgap_size

        self.layer_type = transformer_definition["winding_definition"]["layer_type"]
        self.layer_spacing = float(transformer_definition["winding_definition"]["layer_spacing"])
        self.top_bottom_margin = float(transformer_definition["winding_definition"]["top_margin"])
        self.side_margin = float(transformer_definition["winding_definition"]["side_margin"])
        self.include_bobbin = transformer_definition["winding_definition"]["include_bobbin"]
        self.bobbin_thickness = float(transformer_definition["winding_definition"]["bobbin_board_thickness"])
        self.conductor_type = transformer_definition["winding_definition"]["conductor_type"]
        
        self.winding_parameters_dict = transformer_definition["winding_definition"]["layers_definition"]

    def create_polyline(self, points, segments, name, covered=True, closed=True, color='(165 42 42)'):
        created_name = self.oEditor.CreatePolyline(
            [
                "NAME:PolylineParameters",
                "IsPolylineCovered:=", covered,
                "IsPolylineClosed:=", closed,
                points,
                segments,
                [
                    "NAME:PolylineXSection",
                    "XSectionType:=", "None",
                    "XSectionOrient:=", "Auto",
                    "XSectionWidth:=", "0mm",
                    "XSectionTopWidth:=", "0mm",
                    "XSectionHeight:=", "0mm",
                    "XSectionNumSegments:=", "0",
                    "XSectionBendType:=", "Corner"
                ]
            ],
            [
                "NAME:Attributes",
                "Name:=", name,
                "Flags:=", "",
                "Color:=", color,
                "Transparency:=", 0,
                "PartCoordinateSystem:=", Cores.CS,
                "UDMId:=", "",
                "MaterialValue:=", '"ferrite"',
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:=", True,
                "IsMaterialEditable:=", True,
                "UseMaterialAppearance:=", False
            ])
        return created_name

    def move(self, selection, x, y, z):
        self.oEditor.Move(
            [
                "NAME:Selections",
                "Selections:=", selection,
                "NewPartsModelFlag:=", "Model"
            ],
            [
                "NAME:TranslateParameters",
                "TranslateVectorX:=", str(x) + 'mm',
                "TranslateVectorY:=", str(y) + 'mm',
                "TranslateVectorZ:=", str(z) + 'mm'
            ])

    def create_box(self, x_position, y_position, z_position, x_size, y_size, z_size, name, color='(165 42 42)'):
        self.oEditor.CreateBox(
            [
                "NAME:BoxParameters",
                "XPosition:=", str(x_position) + 'mm',
                "YPosition:=", str(y_position) + 'mm',
                "ZPosition:=", str(z_position) + 'mm',
                "XSize:=", str(x_size) + 'mm',
                "YSize:=", str(y_size) + 'mm',
                "ZSize:=", str(z_size) + 'mm'
            ],
            [
                "NAME:Attributes",
                "Name:=", name,
                "Flags:=", "",
                "Color:=", color,
                "Transparency:=", 0,
                "PartCoordinateSystem:=", Cores.CS,
                "UDMId:=", "",
                "MaterialValue:=", '"ferrite"',
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:=", True,
                "IsMaterialEditable:=", True,
                "UseMaterialAppearance:=", False
            ])

    def create_rectangle(self, x_position, y_position, z_position, x_size, z_size, name, covered=True):
        created_name = self.oEditor.CreateRectangle(
                    [
                        "NAME:RectangleParameters",
                        "IsCovered:=", covered,
                        "XStart:=", str(x_position) + 'mm',
                        "YStart:=", str(y_position) + 'mm',
                        "ZStart:=", str(z_position) + 'mm',
                        "Width:=", str(z_size) + 'mm',    # height of conductor
                        "Height:=", str(x_size) + 'mm',    # width
                        "WhichAxis:=", 'Y'
                    ],
                    [
                        "NAME:Attributes",
                        "Name:=", name,
                        "Flags:=", "",
                        "Color:=", "(143 175 143)",
                        "Transparency:=", 0,
                        "PartCoordinateSystem:=", Cores.CS,
                        "UDMId:=", "",
                        "MaterialValue:=", "\"vacuum\"",
                        "SurfaceMaterialValue:=", "\"\"",
                        "SolveInside:=", True,
                        "IsMaterialEditable:=", True,
                        "UseMaterialAppearance:=", False
                    ])
        return created_name

    def create_cylinder(self, x_position, y_position, z_position, diameter, height, seg_num, name, color='(165 42 42)'):
        self.oEditor.CreateCylinder(
            [
                "NAME:CylinderParameters",
                "XCenter:=", str(x_position) + 'mm',
                "YCenter:=", str(y_position) + 'mm',
                "ZCenter:=", str(z_position) + 'mm',
                "Radius:=", str(diameter/2) + 'mm',
                "Height:=", str(height) + 'mm',
                "WhichAxis:=", "Z",
                "NumSides:=", str(seg_num)
            ],
            [
                "NAME:Attributes",
                "Name:=", name,
                "Flags:=", "",
                "Color:=", color,
                "Transparency:=", 0,
                "PartCoordinateSystem:=", Cores.CS,
                "UDMId:=", "",
                "MaterialValue:=", '"ferrite"',
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:=", True,
                "IsMaterialEditable:=", True,
                "UseMaterialAppearance:=", False
            ])

    def create_circle(self, x_position, y_position, z_position, diameter, seg_num, name, axis, covered=True):
        created_name = self.oEditor.CreateCircle(
            [
                "NAME:CircleParameters",
                "IsCovered:=", covered,
                "XCenter:=", str(x_position) + 'mm',
                "YCenter:=", str(y_position) + 'mm',
                "ZCenter:=", str(z_position) + 'mm',
                "Radius:=", str(diameter/2) + 'mm',
                "WhichAxis:=", axis,
                "NumSegments:=", str(seg_num)
            ],
            [
                "NAME:Attributes",
                "Name:=", name,
                "Flags:=", "",
                "Color:=", "(143 175 143)",
                "Transparency:=", 0,
                "PartCoordinateSystem:=", Cores.CS,
                "UDMId:=", "",
                "MaterialValue:=", "\"vacuum\"",
                "SurfaceMaterialValue:=", "\"\"",
                "SolveInside:=", True,
                "IsMaterialEditable:=", True,
                "UseMaterialAppearance:=", False
            ])
        return created_name

    def fillet(self, body_name, radius, x, y, z):
        object_id = [
            self.oEditor.GetEdgeByPosition(
                                [
                                  "NAME:EdgeParameters",
                                  "BodyName:=", body_name,
                                  "XPosition:=", str(x) + 'mm',
                                  "YPosition:=", str(y) + 'mm',
                                  "ZPosition:=", str(z) + 'mm'
                                ])
        ]

        self.oEditor.Fillet(
                [
                    "NAME:Selections",
                    "Selections:=", body_name,
                    "NewPartsModelFlag:=", "Model"
                ],
                [
                    "NAME:Parameters",
                    [
                        "NAME:FilletParameters",
                        "Edges:=", object_id,
                        "Vertices:=", [],
                        "Radius:=", str(radius) + 'mm',
                        "Setback:=", "0mm"
                    ]
                ])

    def rename(self, old_name, new_name):
        self.oEditor.ChangeProperty(
            [
                "NAME:AllTabs",
                [
                    "NAME:Geometry3DAttributeTab",
                    ["NAME:PropServers", old_name],
                    [
                        "NAME:ChangedProps",
                        ["NAME:Name", "Value:=", new_name]
                    ]
                ]
            ])

    def unite(self, selection):
        self.oEditor.Unite(
            ["NAME:Selections", "Selections:=", selection],
            ["NAME:UniteParameters", "KeepOriginals:=", False])

    def subtract(self, selection, tool, keep=False):
        self.oEditor.Subtract(
            [
                "NAME:Selections",
                "Blank Parts:=", selection,
                "Tool Parts:=", tool
            ],
            ["NAME:SubtractParameters", "KeepOriginals:=", keep])

    def sweep_along_vector(self, selection, vec_z):
        self.oEditor.SweepAlongVector(
            [
                "NAME:Selections",
                "Selections:=", selection,
                "NewPartsModelFlag:=", "Model"
            ],
            [
                "NAME:VectorSweepParameters",
                "DraftAngle:=", "0deg",
                "DraftType:=", "Round",
                "CheckFaceFaceIntersection:=", False,
                "SweepVectorX:=", "0mm",
                "SweepVectorY:=", "0mm",
                "SweepVectorZ:=", str(vec_z) + 'mm'
            ])

    def sweep_along_path(self, selection):
        self.oEditor.SweepAlongPath(
            [
                "NAME:Selections",
                "Selections:=", selection,
                "NewPartsModelFlag:=", "Model"
            ],
            [
                "NAME:PathSweepParameters",
                "DraftAngle:=", "0deg",
                "DraftType:=", "Round",
                "CheckFaceFaceIntersection:=", False,
                "TwistAngle:=", "0deg"
            ])

    def duplicate_mirror(self, selection, X, Y, Z):
        self.oEditor.DuplicateMirror(
            [
                "NAME:Selections",
                "Selections:=", selection,
                "NewPartsModelFlag:=", "Model"
            ],
            [
                "NAME:DuplicateToMirrorParameters",
                "DuplicateMirrorBaseX:=", "0mm",
                "DuplicateMirrorBaseY:=", "0mm",
                "DuplicateMirrorBaseZ:=", "0mm",
                "DuplicateMirrorNormalX:=", str(X) + 'mm',
                "DuplicateMirrorNormalY:=", str(Y) + 'mm',
                "DuplicateMirrorNormalZ:=", str(Z) + 'mm'
            ],
            [
                "NAME:Options",
                "DuplicateAssignments:=", False
            ],
            [
                "CreateGroupsForNewObjects:=", False
            ])

    def duplicate_along_line(self, selection, x=0.0, y=0.0, z=0.0, num_clones=2):
        self.oEditor.DuplicateAlongLine(
            [
                "NAME:Selections",
                "Selections:=", ",".join(selection),
                "NewPartsModelFlag:=", "Model"
            ],
            [
                "NAME:DuplicateToAlongLineParameters",
                "CreateNewObjects:=", True,
                "XComponent:="	, "{}mm".format(x),
                "YComponent:="		, "{}mm".format(y),
                "ZComponent:="		, "{}mm".format(z),
                "NumClones:="		, str(num_clones)
            ],
            [
                "NAME:Options",
                "DuplicateAssignments:=", False
            ],
            [
                "CreateGroupsForNewObjects:=", False
            ])

    def points_segments_generator(self, points_list):
        for i in range(points_list.count([])):
            points_list.remove([])

        points_array = ["NAME:PolylinePoints"]
        segments_array = ["NAME:PolylineSegments"]
        for i in range(len(points_list)):
            points_array.append(self.polyline_point(points_list[i][0], points_list[i][1], points_list[i][2]))
            if i != len(points_list) - 1:
                segments_array.append(self.line_segment(i))
        return points_array, segments_array
    
    @staticmethod
    def polyline_point(x=0, y=0, z=0):
        point = [
                        "NAME:PLPoint",
                        "X:=", str(x) + 'mm',
                        "Y:=", str(y) + 'mm',
                        "Z:=", str(z) + 'mm'
                    ]
        return point

    @staticmethod
    def line_segment(index):
        segment = [
            "NAME:PLSegment",
            "SegmentType:=", "Line",
            "StartIndex:="	, index,
            "NoOfPoints:="		, 2
        ]
        return segment

    @staticmethod
    def arc_segment(index, segments_number, center_x, center_y, center_z):
        segment = [
            "NAME:PLSegment",
            "SegmentType:="	, "AngularArc",
            "StartIndex:="		, index,
            "NoOfPoints:="		, 3,
            "NoOfSegments:="	, str(segments_number),
            "ArcAngle:="		, "-90deg",
            "ArcCenterX:="		, "{}mm".format(center_x),
            "ArcCenterY:="		, "{}mm".format(center_y),
            "ArcCenterZ:="		, "{}mm".format(center_z),
            "ArcPlane:="		, "XY"
        ]
        return segment


class ECore(Cores):
    def __init__(self, args_list):
        super(ECore, self).__init__(args_list)
        self.core_length = self.dim_D1
        self.core_width = self.dim_D6
        self.core_height = self.dim_D4
        self.side_leg_width = (self.dim_D1 - self.dim_D2)/2
        self.center_leg_width = self.dim_D3
        self.slot_depth = self.dim_D5

    def draw_winding(self, dim_D2, dim_D3, dim_D5, dim_D6, ECoredim_D8=0.0):
        layer_spacing = self.layer_spacing
        top_bottom_margin = self.top_bottom_margin
        side_margin = self.side_margin
        bobbin_thickness = self.bobbin_thickness
        segmentation_angle = self.segmentation_angle
        winding_parameters_dict = self.winding_parameters_dict
        slot_height = dim_D5*2

        if self.layer_type == "Planar":
            margin = top_bottom_margin
            for layer_num, layer_name in enumerate(winding_parameters_dict):
                conductor_width = float(winding_parameters_dict[layer_name]["conductor_width"])
                conductor_height = float(winding_parameters_dict[layer_name]["conductor_height"])
                num_of_turns = int(winding_parameters_dict[layer_name]["turns_number"])
                turn_spacing = float(winding_parameters_dict[layer_name]["insulation_thickness"])

                if self.include_bobbin:
                    self.draw_board(slot_height, dim_D2, dim_D3,
                                    dim_D6, bobbin_thickness, -dim_D5 + margin,
                                    layer_num+1, ECoredim_D8)

                position_z = -dim_D5 + margin + conductor_height
                for turn_num in range(0, num_of_turns):
                    sweep_path_x = (
                        dim_D3 + 2*side_margin + ((2*turn_num + 1)*conductor_width) +
                        (2*turn_num*turn_spacing) + turn_spacing)

                    sweep_path_y = (
                        dim_D6 + 2*side_margin + ((2*turn_num + 1)*conductor_width) +
                        (2*turn_num*turn_spacing) + turn_spacing)

                    self.create_single_turn(sweep_path_x, sweep_path_y, position_z,
                                            layer_num+1, fillet_radius=(sweep_path_x - dim_D3)/2,
                                            segmentation_angle=segmentation_angle,
                                            profile_width=conductor_width, profile_height=conductor_height,
                                            turn_num=turn_num+1)

                margin += layer_spacing + conductor_height + bobbin_thickness

        else:
            # ---- Wound transformer ---- #
            if self.include_bobbin:
                self.draw_bobbin(slot_height - 2*top_bottom_margin + self.airgap_both, dim_D2, dim_D3,
                                 dim_D6, bobbin_thickness, ECoredim_D8)

            margin = side_margin + bobbin_thickness
            for layer_num, layer_name in enumerate(winding_parameters_dict):
                num_of_turns = int(winding_parameters_dict[layer_name]["turns_number"])
                insulation_thickness = float(winding_parameters_dict[layer_name]["insulation_thickness"])
                if self.conductor_type == 'Rectangular':
                    conductor_width = float(winding_parameters_dict[layer_name]["conductor_width"])
                    conductor_height = float(winding_parameters_dict[layer_name]["conductor_height"])
                    # factor of 2 is applied due to existence of margin and insulation on both sides
                    conductor_full_size = 2*margin + conductor_width + 2*insulation_thickness
                else:
                    conductor_diameter = float(winding_parameters_dict[layer_name]["conductor_diameter"])
                    segments_number = int(winding_parameters_dict[layer_name]["segments_number"])
                    # factor of 2 is applied due to existence of margin and insulation on both sides
                    conductor_full_size = 2*margin + conductor_diameter + 2*insulation_thickness

                conductor_z_position = dim_D5 - top_bottom_margin - bobbin_thickness - insulation_thickness

                sweep_path_x = dim_D3 + conductor_full_size
                sweep_path_y = dim_D6 + conductor_full_size

                fillet_radius = (sweep_path_x - dim_D3)/2

                if self.conductor_type == 'Rectangular':
                    conductor_z_position += -conductor_height/2.0
                    move_vec = 2*insulation_thickness + conductor_height
                    names = self.create_single_turn(sweep_path_x, sweep_path_y, conductor_z_position,
                                                    layer_num+1, fillet_radius, segmentation_angle,
                                                    profile_width=conductor_width, profile_height=conductor_height)
                    margin += layer_spacing + conductor_width + 2*insulation_thickness
                else:
                    conductor_z_position += -conductor_diameter/2.0
                    move_vec = 2*insulation_thickness + conductor_diameter
                    names = self.create_single_turn(sweep_path_x, sweep_path_y, conductor_z_position, layer_num+1,
                                                    fillet_radius, segmentation_angle,
                                                    profile_diameter=conductor_diameter,
                                                    profile_segments_num=segments_number)

                    margin += layer_spacing + conductor_diameter + 2*insulation_thickness
                
                if num_of_turns > 1:
                    self.duplicate_along_line(names, z=-move_vec, num_clones=num_of_turns)

    def create_single_turn(self, sweep_path_x, sweep_path_y, position_z_final,
                           layer_number, fillet_radius, segmentation_angle, profile_width=0.0,
                           profile_height=0.0, profile_diameter=0.0, profile_segments_num=8, turn_num=0):

        path_name = self.create_sweep_path(sweep_path_x, sweep_path_y, position_z_final, fillet_radius,
                                           layer_number, segmentation_angle, turn_num)

        profile_name = 'Layer{}'.format(layer_number)
        if turn_num != 0:
            profile_name += "_turn{}".format(turn_num)
        if self.conductor_type == 'Rectangular':
            profile_name = self.create_rectangle((sweep_path_x - profile_width)/2, 0,
                                                 (position_z_final - profile_height/2),
                                                 profile_width, profile_height, profile_name)
        else:
            profile_name = self.create_circle(sweep_path_x/2, 0, position_z_final,
                                              profile_diameter, profile_segments_num, profile_name, 'Y')

        self.sweep_along_path(profile_name + ',' + path_name)

        object_names = [profile_name]
        return object_names

    def create_sweep_path(self, sweep_path_x, sweep_path_y, position_z, fillet_radius,
                          layer_number, segmentation_angle=0, turn_num=0):
        """
        Function to create rectangular profile of the winding.
        Note: in this function we sacrifice code size for the explicitness. Generate points for each quadrant using
        polyline that consists of arcs and straight lines
        :param sweep_path_x: size of the coil in X direction
        :param sweep_path_y: size of the coil in Y direction
        :param position_z: position of the coil on Z axis
        :param fillet_radius: radius of the fillet, to make round corners of the coil
        :param layer_number: layer number for the body_name
        :param segmentation_angle: segmentation angle, true surface would be mesh overkill
        :param turn_num: turn number is used for planar transformers to append path name. Otherwise will get lots of
        warnings in the UI
        :return: body_name: body_name of the winding
        """

        segments_number = 12 if segmentation_angle == 0 else int(90/segmentation_angle)*2

        points = ["NAME:PolylinePoints"]
        points.append(self.polyline_point(x=-sweep_path_x/2 + fillet_radius,
                                          y=sweep_path_y/2,
                                          z=position_z))
        points.append(self.polyline_point(x=sweep_path_x/2 - fillet_radius,
                                          y=sweep_path_y/2,
                                          z=position_z))
        points.append(self.polyline_point(z=position_z))  # dummy point, aedt needs it
        points.append(self.polyline_point(x=sweep_path_x/2,
                                          y=sweep_path_y/2 - fillet_radius,
                                          z=position_z))
        points.append(self.polyline_point(x=sweep_path_x/2,
                                          y=-sweep_path_y/2 + fillet_radius,
                                          z=position_z))
        points.append(self.polyline_point())  # dummy point
        points.append(self.polyline_point(x=sweep_path_x/2 - fillet_radius,
                                          y=-sweep_path_y/2,
                                          z=position_z))
        points.append(self.polyline_point(x=-sweep_path_x/2 + fillet_radius,
                                          y=-sweep_path_y/2,
                                          z=position_z))
        points.append(self.polyline_point(z=position_z))  # dummy point
        points.append(self.polyline_point(x=-sweep_path_x/2,
                                          y=-sweep_path_y/2 + fillet_radius,
                                          z=position_z))
        points.append(self.polyline_point(x=-sweep_path_x/2,
                                          y=sweep_path_y/2 - fillet_radius,
                                          z=position_z))
        points.append(self.polyline_point(z=position_z))  # dummy point
        points.append(self.polyline_point(x=-sweep_path_x/2 + fillet_radius,
                                          y=sweep_path_y/2,
                                          z=position_z))

        segments = ["NAME:PolylineSegments"]
        segments.append(self.line_segment(0))
        segments.append(self.arc_segment(index=1,
                                         segments_number=segments_number,
                                         center_x=sweep_path_x/2 - fillet_radius,
                                         center_y=sweep_path_y/2 - fillet_radius,
                                         center_z=position_z))
        segments.append(self.line_segment(3))
        segments.append(self.arc_segment(index=4,
                                         segments_number=segments_number,
                                         center_x=sweep_path_x/2 - fillet_radius,
                                         center_y=-sweep_path_y/2 + fillet_radius,
                                         center_z=position_z))
        segments.append(self.line_segment(6))
        segments.append(self.arc_segment(index=7,
                                         segments_number=segments_number,
                                         center_x=-sweep_path_x/2 + fillet_radius,
                                         center_y=-sweep_path_y/2 + fillet_radius,
                                         center_z=position_z))
        segments.append(self.line_segment(9))
        segments.append(self.arc_segment(index=10,
                                         segments_number=segments_number,
                                         center_x=-sweep_path_x/2 + fillet_radius,
                                         center_y=sweep_path_y/2 - fillet_radius,
                                         center_z=position_z))

        name = "Tool{}".format(layer_number)
        if turn_num != 0:
            name += "_turn{}".format(turn_num)
        name = self.create_polyline(points, segments, name, covered=False, closed=True)

        return name

    def draw_bobbin(self, slot_height, dim_D2, dim_D3, dim_D6, bobbin_thickness, e_coredim_d8=0.0):
        fillet_rad = (dim_D2 - dim_D3)/2

        y_size = dim_D6 + (dim_D2 - dim_D3)
        self.create_box(-dim_D2/2 + e_coredim_d8, -y_size/2, -slot_height/2,
                        dim_D2 - 2*e_coredim_d8, y_size, bobbin_thickness, 'Bobbin', '(255, 248, 157)')

        self.create_box(-dim_D2/2 + e_coredim_d8, -y_size/2, slot_height/2,
                        dim_D2 - 2*e_coredim_d8, y_size, -bobbin_thickness, 'BobT2')

        self.create_box(-dim_D3/2 - bobbin_thickness, -dim_D6/2 - bobbin_thickness, -slot_height/2,
                        dim_D3 + 2*bobbin_thickness, dim_D6 + 2*bobbin_thickness, slot_height, 'BobT3')

        self.unite('Bobbin,BobT2,BobT3')

        self.create_box(-dim_D3/2, -dim_D6/2, -slot_height/2,
                        dim_D3, dim_D6, slot_height, 'BobSlot')
        self.subtract('Bobbin', 'BobSlot')

        # - - - fillet(NameOfObject, Radius, XCoord, YCoord, ZCoord)
        x_edge_pos = dim_D2/2 - e_coredim_d8
        y_edge_pos = y_size/2
        z_edge_pos = (slot_height - bobbin_thickness)/2
        self.fillet('Bobbin', fillet_rad, -x_edge_pos, -y_edge_pos, -z_edge_pos)
        self.fillet('Bobbin', fillet_rad, -x_edge_pos, y_edge_pos, -z_edge_pos)
        self.fillet('Bobbin', fillet_rad, x_edge_pos, -y_edge_pos, -z_edge_pos)
        self.fillet('Bobbin', fillet_rad, x_edge_pos, y_edge_pos, -z_edge_pos)
        self.fillet('Bobbin', fillet_rad, -x_edge_pos, -y_edge_pos, z_edge_pos)
        self.fillet('Bobbin', fillet_rad, -x_edge_pos, y_edge_pos, z_edge_pos)
        self.fillet('Bobbin', fillet_rad, x_edge_pos, -y_edge_pos, z_edge_pos)
        self.fillet('Bobbin', fillet_rad, x_edge_pos, y_edge_pos, z_edge_pos)

    def draw_board(self, slot_height, dim_D2, dim_D3, dim_D6, board_thickness, z_position, 
                   layer_number, e_coredim_d8=0.0):
        y_size = dim_D6 + (dim_D2-dim_D3)
        self.create_box(-dim_D2/2 + e_coredim_d8, -y_size/2, z_position,
                        dim_D2 - 2*e_coredim_d8, y_size, board_thickness, 'Board_{}'.format(layer_number),
                        '(0, 128, 0)')

        # subtract full slot, no need to calculate precisely
        self.create_box(-dim_D3/2, -dim_D6/2, z_position,
                        dim_D3, dim_D6, slot_height, 'BoardSlot_{}'.format(layer_number))
        self.subtract('Board_{}'.format(layer_number), 'BoardSlot_{}'.format(layer_number))

    def draw_geometry(self):
        self.create_box(-(self.core_length/2), -(self.core_width/2), -self.core_height - self.airgap_both,
                        self.core_length, self.core_width, (self.core_height - self.slot_depth), 'E_Core_Bottom')

        self.create_box(-(self.core_length/2), -(self.core_width/2), -self.core_height - self.airgap_both,
                        self.side_leg_width, self.core_width, self.core_height - self.airgap_side, 'Leg1')

        self.create_box(-(self.center_leg_width/2), -(self.core_width/2), -self.core_height - self.airgap_both,
                        self.center_leg_width, self.core_width, self.core_height - self.airgap_center, 'Leg2')

        self.create_box((self.core_length/2) - self.side_leg_width, -(self.core_width/2),
                        -self.core_height - self.airgap_both,
                        self.side_leg_width, self.core_width, self.core_height - self.airgap_side, 'Leg3')

        self.unite('E_Core_Bottom,Leg1,Leg2,Leg3')

        # outer edges D_7
        self.fillet('E_Core_Bottom', self.dim_D7, -self.dim_D1/2, 0, -self.dim_D4 - self.airgap_both)
        self.fillet('E_Core_Bottom', self.dim_D7, self.dim_D1/2, 0, -self.dim_D4 - self.airgap_both)
        # inner edges D_8
        self.fillet('E_Core_Bottom', self.dim_D8, -self.dim_D2/2, 0, -self.dim_D5 - self.airgap_both)
        self.fillet('E_Core_Bottom', self.dim_D8, self.dim_D2/2, 0, -self.dim_D5 - self.airgap_both)

        self.duplicate_mirror('E_Core_Bottom', 0, 0, 1)

        self.rename('E_Core_Bottom_1', 'E_Core_Top')
        self.oEditor.FitAll()

        self.draw_winding(self.dim_D2, self.dim_D3, self.dim_D5, self.dim_D6, self.dim_D8)


class EICore(ECore):
    def draw_geometry(self):
        self.create_box(-(self.core_length/2), -(self.core_width/2), -self.core_height,
                        self.core_length, self.core_width, (self.core_height - self.slot_depth), 'E_Core')

        self.create_box(-(self.core_length/2), -(self.core_width/2), -self.core_height,
                        self.side_leg_width, self.core_width, self.core_height - 2*self.airgap_side, 'Leg1')

        self.create_box(-(self.center_leg_width/2), -(self.core_width/2), -self.core_height,
                        self.center_leg_width, self.core_width, self.core_height - 2*self.airgap_center, 'Leg2')

        self.create_box((self.core_length/2) - self.side_leg_width, -(self.core_width/2), -self.core_height,
                        self.side_leg_width, self.core_width, self.core_height - 2*self.airgap_side, 'Leg3')

        self.unite('E_Core,Leg1,Leg2,Leg3')

        self.fillet('E_Core', self.dim_D7, -self.dim_D1/2, -self.dim_D6/2, -(self.dim_D4/2) - 2*self.airgap_both)
        self.fillet('E_Core', self.dim_D7, -self.dim_D1/2, self.dim_D6/2, -(self.dim_D4/2) - 2*self.airgap_both)
        self.fillet('E_Core', self.dim_D7, self.dim_D1/2, -self.dim_D6/2, -(self.dim_D4/2) - 2*self.airgap_both)
        self.fillet('E_Core', self.dim_D7, self.dim_D1/2, self.dim_D6/2, -(self.dim_D4/2) - 2*self.airgap_both)

        # scale airgap by 2 due to no symmetry as in cores like in ECore (where due to mirror operation
        # we double airgap)
        self.create_box(-self.dim_D1/2, -self.dim_D6/2, 2*self.airgap_both,
                        self.dim_D1, self.dim_D6, self.dim_D8, 'I_Core')

        self.fillet('I_Core', self.dim_D7, -self.dim_D1/2, -self.dim_D6/2, (self.dim_D8/2) - 2*self.airgap_both)
        self.fillet('I_Core', self.dim_D7, -self.dim_D1/2, self.dim_D6/2, (self.dim_D8/2) - 2*self.airgap_both)
        self.fillet('I_Core', self.dim_D7, self.dim_D1/2, -self.dim_D6/2, (self.dim_D8/2) - 2*self.airgap_both)
        self.fillet('I_Core', self.dim_D7, self.dim_D1/2, self.dim_D6/2, (self.dim_D8/2) - 2*self.airgap_both)

        self.move('E_Core,I_Core', 0, 0, self.dim_D5/2)

        self.oEditor.FitAll()

        self.draw_winding(self.dim_D2, self.dim_D3, self.dim_D5/2 + 2*self.airgap_both, self.dim_D6)


class EFDCore(ECore):
    def draw_geometry(self):
        self.create_box(-(self.core_length/2), -(self.core_width/2), -self.core_height - self.airgap_both,
                        self.core_length, self.core_width, (self.core_height - self.slot_depth), 'EFD_Core_Bottom')

        self.create_box(-(self.core_length/2), -(self.core_width/2), -self.core_height - self.airgap_both,
                        self.side_leg_width, self.core_width, self.core_height - self.airgap_side, 'Leg1')

        self.create_box(-(self.center_leg_width/2), -(self.core_width/2) - self.dim_D8, -self.core_height - self.airgap_both,
                        self.center_leg_width, self.dim_D7, self.core_height - self.airgap_center, 'Leg2')

        self.create_box((self.core_length/2) - self.side_leg_width, -(self.core_width/2),
                        -self.core_height - self.airgap_both,
                        self.side_leg_width, self.core_width, self.core_height - self.airgap_side, 'Leg3')

        self.unite('EFD_Core_Bottom,Leg1,Leg2,Leg3')

        self.duplicate_mirror('EFD_Core_Bottom', 0, 0, 1)
        self.rename('EFD_Core_Bottom_1', 'E_Core_Top')
        self.oEditor.FitAll()

        # difference between ECore and EFD is only offset of central leg.
        # We can compensate it by using relative CS for winding and bobbin

        self.oEditor.CreateRelativeCS(
            [
                "NAME:RelativeCSParameters",
                "Mode:=", "Axis/Position",
                "OriginX:=", "0mm",
                "OriginY:=", str((self.dim_D7 - self.dim_D6)/2 - self.dim_D8) + 'mm',
                "OriginZ:=", "0mm",
                "XAxisXvec:=", "1mm",
                "XAxisYvec:=", "0mm",
                "XAxisZvec:=", "0mm",
                "YAxisXvec:=", "0mm",
                "YAxisYvec:=", "1mm",
                "YAxisZvec:=", "0mm"
            ],
            [
                "NAME:Attributes",
                "Name:=", 'CentralLegCS'
            ])
        Cores.CS = 'CentralLegCS'

        self.draw_winding(self.dim_D2, self.dim_D3, self.dim_D5, self.dim_D7)


# UCore inherit from ECore functions CreateSingleTurn, draw_bobbin, drawBoard
class UCore(ECore):
    def __init__(self, args_list):
        super(UCore, self).__init__(args_list)

        self.MECoreLength = self.dim_D1
        self.MECoreWidth = self.dim_D5
        self.MECoreHeight = self.dim_D3

    def draw_winding(self, dim_D1, dim_D2, dim_D3, dim_D4, dim_D5, segmentation_angle):
        MLSpacing = self.layer_spacing
        Mtop_margin = self.top_bottom_margin
        Mside_margin = self.side_margin
        MBobbinThk = self.bobbin_thickness
        WdgParDict = self.winding_parameters_dict
        MSlotHeight = dim_D4*2
        LegWidth = (dim_D1 - dim_D2)/2

        if self.include_bobbin and self.layer_type == "Wound":
            self.draw_bobbin(MSlotHeight - 2*Mtop_margin, dim_D2 + LegWidth/2, LegWidth/2.0 + MBobbinThk,
                             dim_D5/2.0 + MBobbinThk, MBobbinThk)

        if self.layer_type == "Planar":
            MTDx = Mtop_margin
            for MAx in self.winding_parameters_dict:
                if self.include_bobbin:
                    self.draw_board(MSlotHeight - 2*Mtop_margin, dim_D2 + LegWidth/2, LegWidth/2.0 + MBobbinThk,
                                    (dim_D5/2.0) + MBobbinThk, MBobbinThk, -dim_D4 + MTDx, MAx)

                for layerTurn in range(0, int(self.winding_parameters_dict[MAx][2])):
                    rectangle_size_x = (LegWidth + 2*Mside_margin + ((2*layerTurn + 1)*self.winding_parameters_dict[MAx][0]) +
                                        (2*layerTurn*2*self.winding_parameters_dict[MAx][3]) + 2*self.winding_parameters_dict[MAx][3])

                    rectangle_size_y = (dim_D5 + 2*Mside_margin + ((2*layerTurn + 1)*self.winding_parameters_dict[MAx][0]) +
                                        (2*layerTurn*2*self.winding_parameters_dict[MAx][3]) + 2*self.winding_parameters_dict[MAx][3])

                    rectangle_size_z = -self.winding_parameters_dict[MAx][1]/2.0
                    self.create_single_turn(rectangle_size_x, rectangle_size_y, rectangle_size_z,
                                            self.winding_parameters_dict[MAx][0], self.winding_parameters_dict[MAx][1],
                                            (-dim_D4 + MTDx + MBobbinThk + WdgParDict[MAx][1]), MAx,
                                            layerTurn, (rectangle_size_x - LegWidth)/2, segmentation_angle)

                MTDx += MLSpacing + self.winding_parameters_dict[MAx][1] + MBobbinThk

        else:
            # ---- Wound transformer ---- #
            MTDx = Mside_margin + MBobbinThk
            for MAx in self.winding_parameters_dict.keys():
                for MBx in range(0, int(self.winding_parameters_dict[MAx][2])):
                    rectangle_size_x = LegWidth + (2*(MTDx + (self.winding_parameters_dict[MAx][0]/2.0))) + 2*self.winding_parameters_dict[MAx][3]
                    rectangle_size_y = dim_D5 + (2*(MTDx + (self.winding_parameters_dict[MAx][0]/2.0))) + 2*self.winding_parameters_dict[MAx][3]
                    if self.conductor_type == 'Rectangular':
                        rectangle_size_z = -self.winding_parameters_dict[MAx][1]/2.0
                        ZProf = (dim_D4 - Mtop_margin - MBobbinThk - (self.winding_parameters_dict[MAx][3]) -
                                 MBx*(2*self.winding_parameters_dict[MAx][3] + self.winding_parameters_dict[MAx][1]))

                        self.create_single_turn(rectangle_size_x, rectangle_size_y, rectangle_size_z,
                                                self.winding_parameters_dict[MAx][0], self.winding_parameters_dict[MAx][1], ZProf, MAx, MBx,
                                                (rectangle_size_x - LegWidth)/2, segmentation_angle)
                    else:
                        rectangle_size_z = -self.winding_parameters_dict[MAx][0]/2.0
                        ZProf = (dim_D4 - Mtop_margin - MBobbinThk - (self.winding_parameters_dict[MAx][3]) -
                                 MBx*(2*self.winding_parameters_dict[MAx][3] + self.winding_parameters_dict[MAx][0]))

                        self.create_single_turn(rectangle_size_x, rectangle_size_y, rectangle_size_z,
                                                self.winding_parameters_dict[MAx][0], self.winding_parameters_dict[MAx][1], ZProf, MAx, MBx,
                                                (rectangle_size_x - LegWidth)/2, segmentation_angle)

                MTDx = MTDx + MLSpacing + self.winding_parameters_dict[MAx][0] + 2*self.winding_parameters_dict[MAx][3]

    def draw_geometry(self):
        self.create_box(-(self.dim_D1 - self.dim_D2)/4, -(self.MECoreWidth/2), -self.MECoreHeight - self.airgap_both,
                        self.MECoreLength, self.MECoreWidth, self.MECoreHeight, 'U_Core_Bottom')

        self.create_box((self.dim_D1 - self.dim_D2)/4, -self.MECoreWidth/2, -self.dim_D4 - self.airgap_both,
                        self.dim_D2, self.MECoreWidth, self.dim_D4, 'XSlot')

        self.subtract('U_Core_Bottom', 'XSlot')

        if self.airgap_center > 0:
            self.create_box(-(self.dim_D1 - self.dim_D2)/4, -self.MECoreWidth/2, -self.airgap_center,
                            (self.dim_D1 - self.dim_D2)/2, self.MECoreWidth, self.airgap_center, 'AgC')

            self.subtract('U_Core_Bottom', 'AgC')

        if self.airgap_side > 0:
            self.create_box(self.dim_D2 + (self.dim_D1 - self.dim_D2)/4, -self.MECoreWidth/2, -self.airgap_side,
                            (self.dim_D1 - self.dim_D2)/2, self.MECoreWidth, self.airgap_side, 'AgS')

            self.subtract('U_Core_Bottom', 'AgS')

        self.duplicate_mirror('U_Core_Bottom', 0, 0, 1)
        self.rename('U_Core_Bottom_1', 'U_Core_Top')
        self.oEditor.FitAll()

        self.draw_winding(self.dim_D1, self.dim_D2, self.dim_D3, (self.dim_D4 + self.airgap_both), self.dim_D5,
                          self.segmentation_angle)


# UICore inherit from ECore functions CreateSingleTurn, draw_bobbin, drawBoard
# and from UCore inherit DrawWdg
class UICore(UCore):
    def draw_geometry(self):
        self.create_box(-(self.dim_D1 - self.dim_D2)/4, -(self.MECoreWidth/2), (self.dim_D4/2) - self.MECoreHeight,
                        self.MECoreLength, self.MECoreWidth, self.MECoreHeight, 'U_Core')

        self.create_box((self.dim_D1 - self.dim_D2)/4, -self.MECoreWidth/2, -self.dim_D4/2,
                        self.dim_D2, self.MECoreWidth, self.dim_D4, 'XSlot')

        self.subtract('U_Core', 'XSlot')

        if self.airgap_center > 0:
            self.create_box((self.dim_D1 - self.dim_D2)/4, -self.MECoreWidth/2, (self.dim_D4/2) - 2*self.airgap_center,
                            -(self.dim_D1 - self.dim_D2)/2, self.MECoreWidth, 2*self.airgap_center, 'AgC')
            self.subtract('U_Core', 'AgC')

        if self.airgap_side > 0:
            self.create_box(self.dim_D2 + (self.dim_D1 - self.dim_D2)/4, -self.MECoreWidth/2,
                            (self.dim_D4/2) - 2*self.airgap_side,
                            (self.dim_D1 - self.dim_D2)/2, self.MECoreWidth, 2*self.airgap_side, 'AgS')
            self.subtract('U_Core', 'AgS')

        self.create_box(-(self.dim_D1 - self.dim_D2)/4 + (self.dim_D1 - self.dim_D6)/2, -self.dim_D7/2,
                        (self.dim_D4/2) + 2*self.airgap_both,
                        self.dim_D6, self.dim_D7, self.dim_D8, 'I_Core')

        self.oEditor.FitAll()

        self.draw_winding(self.dim_D1, self.dim_D2, self.dim_D3/2, (self.dim_D4/2) + 2*self.airgap_both,
                          self.dim_D5, self.segmentation_angle)


class PQCore(Cores):
    def __init__(self, args_list):
        super(PQCore, self).__init__(args_list)
        self.MECoreLength = self.dim_D1
        self.MECoreWidth = self.dim_D6
        self.MECoreHeight = self.dim_D4
        self.MSLegWidth = (self.dim_D1 - self.dim_D2)/2
        self.MCLegWidth = self.dim_D3
        self.MSlotDepth = self.dim_D5

    def draw_wdg(self, dim_D2, dim_D3, dim_D5, segmentation_angle):
        MLSpacing = self.layer_spacing
        Mtop_margin = self.top_bottom_margin
        Mside_margin = self.side_margin
        MBobbinThk = self.bobbin_thickness
        WdgParDict = self.winding_parameters_dict
        MSlotHeight = dim_D5*2

        if self.include_bobbin and self.layer_type == "Wound":
            self.draw_bobbin(MSlotHeight - 2*Mtop_margin, (dim_D2/2.0), (dim_D3/2.0) + MBobbinThk, MBobbinThk)

        if self.layer_type == "Planar":
            MTDx = Mtop_margin
            for MAx in self.winding_parameters_dict:
                if self.include_bobbin:
                    self.drawBoard(MSlotHeight - 2*Mtop_margin, (dim_D2/2.0), (dim_D3/2.0) + MBobbinThk,
                                   MBobbinThk, -dim_D5 + MTDx, MAx)

                for layerTurn in range(0, int(self.winding_parameters_dict[MAx][2])):
                    rectangle_size_x = (dim_D3 + 2*Mside_margin + ((2*layerTurn + 1)*self.winding_parameters_dict[MAx][0]) +
                                        (2*layerTurn*2*self.winding_parameters_dict[MAx][3]) + 2*self.winding_parameters_dict[MAx][3])

                    rectangle_size_z = -self.winding_parameters_dict[MAx][1]/2.0

                    self.create_single_turn(rectangle_size_x, rectangle_size_z, self.winding_parameters_dict[MAx][0],
                                            self.winding_parameters_dict[MAx][1], -dim_D5 + MTDx + MBobbinThk + WdgParDict[MAx][1],
                                            MAx, layerTurn, segmentation_angle)

                MTDx += MLSpacing + self.winding_parameters_dict[MAx][1] + MBobbinThk
        else:
            # ---- Wound transformer ---- #
            MTDx = Mside_margin + MBobbinThk
            for MAx in self.winding_parameters_dict.keys():
                for MBx in range(0, int(self.winding_parameters_dict[MAx][2])):
                    rectangle_size_x = dim_D3 + (2*(MTDx + (self.winding_parameters_dict[MAx][0]/2.0))) + 2*self.winding_parameters_dict[MAx][3]
                    if self.conductor_type == 'Rectangular':
                        rectangle_size_z = -self.winding_parameters_dict[MAx][1]/2.0
                        ZProf = (dim_D5 - Mtop_margin - MBobbinThk - self.winding_parameters_dict[MAx][3] -
                                 MBx*(2*self.winding_parameters_dict[MAx][3] + self.winding_parameters_dict[MAx][1]))

                        self.create_single_turn(rectangle_size_x, rectangle_size_z, self.winding_parameters_dict[MAx][0],
                                                self.winding_parameters_dict[MAx][1], ZProf, MAx, MBx, segmentation_angle)
                    else:
                        rectangle_size_z = -self.winding_parameters_dict[MAx][0]/2.0
                        ZProf = (dim_D5 - Mtop_margin - MBobbinThk - self.winding_parameters_dict[MAx][3] -
                                 MBx*(2*self.winding_parameters_dict[MAx][3] + self.winding_parameters_dict[MAx][0]))

                        self.create_single_turn(rectangle_size_x, rectangle_size_z, self.winding_parameters_dict[MAx][0],
                                                self.winding_parameters_dict[MAx][1], ZProf, MAx, MBx, segmentation_angle)

                MTDx = MTDx + MLSpacing + self.winding_parameters_dict[MAx][0] + 2*self.winding_parameters_dict[MAx][3]

    def create_single_turn(self, sweep_path_x, sweep_path_z, ProfAX, ProfZ, ZPos, layer_number, turn_number, segmentation_angle):
        segments_number = 0 if segmentation_angle == 0 else int(360/segmentation_angle)

        self.create_circle(0, 0, sweep_path_z,
                           sweep_path_x, segments_number, 'pathLine', 'Z', covered=False)

        if self.conductor_type == 'Rectangular':
            self.create_rectangle((sweep_path_x/2 - ProfAX/2), 0, (sweep_path_z - ProfZ/2),
                                  ProfAX, ProfZ, 'sweep_profile')
        else:
            self.create_circle(sweep_path_x/2, 0, sweep_path_z,
                               ProfAX, ProfZ, 'sweep_profile', 'Y')

        self.rename('pathLine', 'Tool%s_%s' % (layer_number, turn_number + 1))
        self.sweep_along_path('sweep_profile,Tool%s_%s' % (layer_number, turn_number + 1))

        self.move('sweep_profile', 0, 0, ZPos)
        self.rename('sweep_profile', 'Layer%s_%s' % (layer_number, turn_number + 1))

    def draw_bobbin(self, Hb, Db1, Db2, Tb):
        self.create_cylinder(0, 0, - Tb + (Hb/2.0),
                             Db1*2, Tb, self.segments_number, 'Bobbin', '(255, 248, 157)')

        self.create_cylinder(0, 0, -(Hb/2.0),
                             Db1*2, Tb, self.segments_number, 'BobT2')

        self.create_cylinder(0, 0, Tb - (Hb/2.0),
                             Db2*2, Hb - 2*Tb, self.segments_number, 'BobT3')

        self.unite('Bobbin,BobT2,BobT3')
        self.create_cylinder(0, 0, - Hb/2.0,
                             (Db2 - Tb)*2, Hb, self.segments_number, 'BobT4')

        self.subtract('Bobbin', 'BobT4')

    def drawBoard(self, Hb, Db1, Db2, Tb, ZStart, layer_number):
        self.create_cylinder(0, 0, ZStart,
                             Db1*2, Tb, self.segments_number, 'Board_{}'.format(layer_number), '(0, 128, 0)')

        self.create_cylinder(0, 0, ZStart,
                             (Db2 - Tb)*2, Hb, self.segments_number, 'BoardSlot_{}'.format(layer_number))

        self.subtract('Board_{}'.format(layer_number), 'BoardSlot_{}'.format(layer_number))

    def draw_geometry(self):
        self.create_box(-self.dim_D1/2, -self.dim_D8/2, -(self.dim_D4/2) - self.airgap_both,
                        (self.dim_D1 - self.dim_D6)/2, self.dim_D8, (self.dim_D4/2) - self.airgap_side, 'PQ_Core_Bottom')

        IntL = math.sqrt(((self.dim_D3/2) ** 2) - ((self.dim_D7/2) ** 2))
        vertices1 = [[-self.dim_D6/2, - 0.4*self.dim_D8, -(self.dim_D4/2) - self.airgap_both],
                     [-self.dim_D6/2, 0.4*self.dim_D8, -(self.dim_D4/2) - self.airgap_both],
                     [-self.dim_D7/2, +IntL, -(self.dim_D4/2) - self.airgap_both],
                     [-self.dim_D7/2, - IntL, -(self.dim_D4/2) - self.airgap_both]]
        vertices1.append(vertices1[0])

        points_array, segments_array = self.points_segments_generator(vertices1)
        self.create_polyline(points_array, segments_array, "Polyline1")
        self.sweep_along_vector("Polyline1", (self.dim_D4/2) - self.airgap_side)

        self.unite('PQ_Core_Bottom,Polyline1')

        self.create_cylinder(0, 0, -(self.dim_D5/2) - self.airgap_both,
                             self.dim_D2, self.dim_D5/2, self.segments_number, 'XCyl1')

        self.subtract('PQ_Core_Bottom', 'XCyl1')
        self.duplicate_mirror('PQ_Core_Bottom', 1, 0, 0)

        self.create_cylinder(0, 0, -(self.dim_D4/2) - self.airgap_both,
                             self.dim_D3, self.dim_D4/2 - self.airgap_center, self.segments_number, 'XCyl2')

        self.unite('PQ_Core_Bottom,PQ_Core_Bottom_1,XCyl2')
        self.duplicate_mirror('PQ_Core_Bottom', 0, 0, 1)

        self.rename('PQ_Core_Bottom_2', 'PQ_Core_Top')
        self.oEditor.FitAll()

        self.draw_wdg(self.dim_D2, self.dim_D3, self.dim_D5/2 + self.airgap_both, self.segmentation_angle)


# ETDCore inherit from PQCore functions DrawWdg, CreateSingleTurn, draw_bobbin
class ETDCore(PQCore):
    def draw_geometry(self, coreName):
        self.create_box(-(self.MECoreLength/2), -(self.MECoreWidth/2), -self.MECoreHeight - self.airgap_both,
                        self.MECoreLength, self.MECoreWidth, self.MECoreHeight - self.airgap_side,
                        coreName + '_Core_Bottom')

        self.create_cylinder(0, 0, -self.MSlotDepth - self.airgap_both,
                             self.dim_D2, self.MSlotDepth, self.segments_number, 'XCyl1')

        self.subtract(coreName + '_Core_Bottom', 'XCyl1')

        if coreName == 'ER' and self.dim_D7 > 0:
            self.create_box(-self.dim_D7/2, -self.MECoreWidth/2, -self.MSlotDepth - self.airgap_both,
                            self.dim_D7, self.MECoreWidth, self.MSlotDepth, 'Tool')
            self.subtract(coreName + '_Core_Bottom', 'Tool')

        self.create_cylinder(0, 0, -self.MSlotDepth - self.airgap_both,
                             self.dim_D3, self.MSlotDepth - self.airgap_center, self.segments_number, 'XCyl2')

        self.unite(coreName + '_Core_Bottom,XCyl2')
        self.duplicate_mirror(coreName + '_Core_Bottom', 0, 0, 1)
        self.rename(coreName + '_Core_Bottom_1', coreName + '_Core_Top')

        self.oEditor.FitAll()

        self.draw_wdg(self.dim_D2, self.dim_D3, (self.dim_D5 + self.airgap_both), self.segmentation_angle)


# RMCore inherit from PQCore functions DrawWdg, CreateSingleTurn, draw_bobbin
class RMCore(PQCore):
    def draw_geometry(self):
        Dia = self.dim_D7/math.sqrt(2)

        vertices1 = [[-self.dim_D1/2, (Dia - (self.dim_D1/2)), -self.airgap_side - self.airgap_both]]
        vertices1.append([-(Dia/2), (Dia/2), -self.airgap_side - self.airgap_both])
        vertices1.append([-(self.dim_D8/2), (self.dim_D8/2), -self.airgap_side - self.airgap_both])
        vertices1.append([(self.dim_D8/2), (self.dim_D8/2), -self.airgap_side - self.airgap_both])
        vertices1.append([(Dia/2), (Dia/2), -self.airgap_side - self.airgap_both])
        vertices1.append([self.dim_D1/2, (Dia - (self.dim_D1/2)), -self.airgap_side - self.airgap_both])
        vertices1.append([self.dim_D1/2, -(Dia - (self.dim_D1/2)), -self.airgap_side - self.airgap_both])
        vertices1.append([(Dia/2), -(Dia/2), -self.airgap_side - self.airgap_both])
        vertices1.append([(self.dim_D8/2), -(self.dim_D8/2), -self.airgap_side - self.airgap_both])
        vertices1.append([-(self.dim_D8/2), -(self.dim_D8/2), -self.airgap_side - self.airgap_both])
        vertices1.append([-(Dia/2), -(Dia/2), -self.airgap_side - self.airgap_both])
        vertices1.append([-self.dim_D1/2, -(Dia - (self.dim_D1/2)), -self.airgap_side - self.airgap_both])
        vertices1.append(vertices1[0])

        pointsArray, segmentsArray = self.points_segments_generator(vertices1)
        self.create_polyline(pointsArray, segmentsArray, 'RM_Core_Bottom')
        self.sweep_along_vector('RM_Core_Bottom', -(self.dim_D4/2) + self.airgap_side)

        self.create_cylinder(0, 0, -(self.dim_D5/2) - self.airgap_both,
                             self.dim_D2, self.dim_D5/2, self.segments_number, 'XCyl1')
        self.subtract('RM_Core_Bottom', 'XCyl1')

        self.create_cylinder(0, 0, -(self.dim_D5/2) - self.airgap_both,
                             self.dim_D3, self.dim_D5/2 - self.airgap_center, self.segments_number, 'XCyl2')

        self.unite('RM_Core_Bottom,XCyl2')
        if self.dim_D6 != 0:
            self.create_cylinder(0, 0, -(self.dim_D4/2) - self.airgap_both,
                                 self.dim_D6, self.dim_D4/2, self.segments_number, 'XCyl3')

            self.subtract('RM_Core_Bottom', 'XCyl3')

        self.duplicate_mirror('RM_Core_Bottom', 0, 0, 1)

        self.rename('RM_Core_Bottom_1', 'RM_Core_Top')
        self.oEditor.FitAll()

        self.draw_wdg(self.dim_D2, self.dim_D3, self.dim_D5/2 + self.airgap_both, self.segmentation_angle)


# depending on bobbin we can inherit bobbin, createturn, drawwdg from PQCore. speak with JMark
class EPCore(PQCore):
    def __init__(self, args_list):
        super(EPCore, self).__init__(args_list)

        self.MECoreLength = self.dim_D1
        self.MECoreWidth = self.dim_D6
        self.MECoreHeight = self.dim_D4/2
        self.MSLegWidth = (self.dim_D1 - self.dim_D2)/2
        self.MCLegWidth = self.dim_D3
        self.MSlotDepth = self.dim_D5/2

    def draw_geometry(self, core_type='EP'):
        self.create_box(-(self.MECoreLength/2), -(self.MECoreWidth/2), -self.MECoreHeight - self.airgap_both,
                        self.MECoreLength, self.MECoreWidth, self.MECoreHeight - self.airgap_side,
                        core_type + '_Core_Bottom')

        self.create_cylinder(0, (self.dim_D6/2) - self.dim_D7, -self.MSlotDepth - self.airgap_both,
                             self.dim_D2, self.MSlotDepth, self.segments_number, 'XCyl1')

        self.create_box(-self.dim_D2/2, (self.dim_D6/2) - self.dim_D7, -self.MSlotDepth - self.airgap_both,
                        self.dim_D2, self.dim_D7, self.MSlotDepth, 'Box2')

        self.unite('Box2,XCyl1')
        self.subtract(core_type + '_Core_Bottom', 'Box2')

        self.create_cylinder(0, (self.dim_D6/2) - self.dim_D7, -self.MSlotDepth - self.airgap_both,
                             self.dim_D3, self.MSlotDepth, self.segments_number, 'XCyl2')

        self.unite(core_type + '_Core_Bottom,XCyl2')
        self.move(core_type + '_Core_Bottom', 0, (-self.dim_D6/2.0) + self.dim_D7, 0)

        self.duplicate_mirror(core_type + '_Core_Bottom', 0, 0, 1)
        self.rename(core_type + '_Core_Bottom_1', core_type + '_Core_Top')

        self.oEditor.FitAll()
        self.draw_wdg(self.dim_D2, self.dim_D3, (self.dim_D5/2 + self.airgap_both), self.segmentation_angle)


class PCore(PQCore):
    def draw_geometry(self, core_name):
        if core_name == 'PH':
            self.dim_D4 *= 2
            self.dim_D5 *= 2

        self.create_cylinder(0, 0, -(self.dim_D4/2) - self.airgap_both, self.dim_D1,
                             (self.dim_D4/2) - self.airgap_side, self.segments_number, core_name + '_Core_Bottom')

        self.create_cylinder(0, 0, -(self.dim_D5/2) - self.airgap_both,
                             self.dim_D2, self.dim_D5/2, self.segments_number, 'XCyl1')
        self.subtract(core_name + '_Core_Bottom', 'XCyl1')

        self.create_cylinder(0, 0, -(self.dim_D5/2) - self.airgap_both,
                             self.dim_D3, self.dim_D5/2 - self.airgap_center, self.segments_number, 'XCyl2')
        self.unite(core_name + '_Core_Bottom,XCyl2')

        if self.dim_D6 != 0:
            self.create_cylinder(0, 0, -(self.dim_D4/2),
                                 self.dim_D6, self.dim_D4/2, self.segments_number, 'Tool')
            self.subtract(core_name + '_Core_Bottom', 'Tool')

        if self.dim_D7 != 0:
            self.create_box(-self.dim_D1/2, -self.dim_D7/2, -(self.dim_D4/2) - self.airgap_both,
                            (self.dim_D1 - self.dim_D8)/2, self.dim_D7, self.dim_D4/2, 'Slot1')

            self.create_box(self.dim_D1/2, -self.dim_D7/2, -(self.dim_D4/2) - self.airgap_both,
                            -(self.dim_D1 - self.dim_D8)/2, self.dim_D7, self.dim_D4/2, 'Slot2')

            self.subtract(core_name + '_Core_Bottom', 'Slot1,Slot2')

        self.duplicate_mirror(core_name + '_Core_Bottom', 0, 0, 1)
        self.rename(core_name + '_Core_Bottom_1', core_name + '_Core_Top')

        if core_name == 'PT':
            self.create_box(-self.dim_D1/2, -self.dim_D1/2, (self.dim_D4/2) + self.airgap_both,
                            (self.dim_D1 - self.dim_D8)/2, self.dim_D1, -self.dim_D4/2, 'Slot3')

            self.create_box(self.dim_D1/2, -self.dim_D1/2, (self.dim_D4/2) + self.airgap_both,
                            -(self.dim_D1 - self.dim_D8)/2, self.dim_D1, -self.dim_D4/2, 'Slot4')

            self.subtract(core_name + '_Core_Top', 'Slot3,Slot4')

        self.oEditor.FitAll()
        self.draw_wdg(self.dim_D2, self.dim_D3, (self.dim_D5/2 + self.airgap_both), self.segmentation_angle)