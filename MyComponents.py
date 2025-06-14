from PyOpticL import optomech
import math
inch = 25.4

class BaseComponent:
    '''
    Base class for all components in the module.
    This class is not meant to be instantiated directly.
    It provides common functionality for all components.
    '''
    type = "Mesh::FeaturePython"
    
    def __init__(self, obj, stl, color=optomech.glass_color, thumbscrews=False, drill=True):
        # required for all object classes
        self.stl = stl

        obj.Proxy = self
        optomech.ViewProvider(obj.ViewObject)
        obj.ViewObject.ShapeColor = color
        obj.addProperty('App::PropertyBool', 'Drill').Drill = drill
        obj.addProperty('Part::PropertyPartShape', 'DrillPart')
        obj.addProperty('App::PropertyBool', 'Thumbscrew').Thumbscrew = thumbscrews
        self.max_angle = 10
        self.max_width = 1


    def execute(self, obj):
    #change for other stls
        mesh = optomech._import_stl(self.stl[0], self.stl[1], self.stl[2])
        mesh.Placement = obj.Mesh.Placement
        obj.Mesh = mesh

        part = optomech._bounding_box(obj, 1, 1)
        part.Placement = obj.Placement
        obj.DrillPart = part

class KM05(BaseComponent):
    def __init__(self, obj, stl=("KM05-Step.stl", (90, 0, 90), (2.084, -1.148, 0.498)), color=optomech.adapter_color, drill=True, thumbscrews=True):
        super().__init__(obj, stl=stl, drill=drill, color=color, thumbscrews=thumbscrews)

class LA1472(BaseComponent):
    def __init__(self, obj, stl=("LA1472-B-Step.stl", (90, 0, 90), (1.265, 0, 0)), drill=True):
        super().__init__(obj, stl, drill=drill)

class LC2067(BaseComponent):
    def __init__(self, obj, stl=("LC2067-B-Step.stl", (90, 0, 90), (1, 0, 0)), drill=True):
        super().__init__(obj, stl, drill=drill)

class LMR05(BaseComponent):
    def __init__(self, obj, stl=("LMR05-Step.stl", (90, 0, 90), (1.651, 0, 0)), drill=True):
        super().__init__(obj, stl, drill=drill)

class LMR9(BaseComponent):
    def __init__(self, obj, stl=("LMR9-Step.stl", (90, 0, 90), (1.651, 0, 0)), drill=True):
        super().__init__(obj, stl, drill=drill)

class Polarizer05(BaseComponent):
    def __init__(self, obj, stl=("polarizer05.stl", (90, 0, 90), (0, 0, -0)), drill=True):
        super().__init__(obj, stl, drill=drill)
        self.transmission = True

class BeamSplitter(optomech.cube_splitter):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj, *args, **kwargs)
        obj.addProperty('App::PropertyBool', 'Drill').Drill = True
        obj.addProperty('Part::PropertyPartShape', 'DrillPart')

    def execute(self, obj):
        super().execute(obj)
        part = optomech._bounding_box(obj, 3, 4)
        part.Placement = obj.Placement
        obj.DrillPart = part

class Photodetector(optomech.photodetector_pda10a2):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj, *args, **kwargs)

class CircularMirror(optomech.circular_mirror):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj, *args, **kwargs)

class Fiberport(optomech.fiberport_mount_hca3):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj, *args, **kwargs)


class AVC():
    type = 'Part::FeaturePython'
    def __init__(self, obj, drill=True, thickness=24, diameter=10, part_number='', mount_type=None, mount_args=dict()):
        obj.Proxy = self
        optomech.ViewProvider(obj.ViewObject)

        obj.addProperty('App::PropertyBool', 'Drill').Drill = drill
        obj.addProperty('Part::PropertyPartShape', 'DrillPart')
        obj.addProperty('App::PropertyLength', 'Thickness').Thickness = thickness
        obj.addProperty('App::PropertyLength', 'Diameter').Diameter = diameter

        if mount_type != None:
            optomech._add_linked_object(obj, "Mount", mount_type, pos_offset=(-thickness/2, 0, 0), **mount_args)

        obj.ViewObject.ShapeColor = optomech.glass_color
        obj.ViewObject.Transparency=50
        self.part_numbers = [part_number]
        self.transmission = True
        self.max_angle = 90
        self.max_width = diameter

    def execute(self, obj):
        angle = -math.radians(5)
        part = optomech._custom_cylinder(
            dia=obj.Diameter.Value, dz=obj.Thickness.Value,
            x=-obj.Thickness.Value/2, y=math.sin(angle), z=0,
            dir=(math.cos(angle), math.sin(angle), 0)
        )
        obj.Shape = part
        part = optomech._bounding_box(obj, 1, 1)
        part.Placement = obj.Placement
        obj.DrillPart = part  # <- ADD THIS LINE

        

"""    def execute(self, obj):
        mesh = optomech._import_stl("AVC_.stl", (0, 0, 90), (12, 0, 0))
        mesh.Placement = obj.Mesh.Placement
        obj.Mesh = mesh

        part = optomech._bounding_box(obj, 6, 3)
        dx = 90
        for x, y in [(1,1), (-1,1), (1,-1), (-1,-1)]:
            part = part.fuse(optomech._custom_cylinder(dia=optomech.bolt_8_32['tap_dia'], dz=optomech.drill_depth,
                                         x=x*dx/2, y=y*15.7, z=-layout.inch/2))
        part = part.fuse(optomech._custom_cylinder(dia=optomech.bolt_8_32['tap_dia'], dz=optomech.drill_depth,
                                     x=45, y=-15.7, z=-layout.inch/2))
        for x in [1,-1]:
            part = part.fuse(optomech._custom_cylinder(dia=optomech.bolt_8_32['tap_dia'], dz=optomech.drill_depth,
                                         x=x*dx/2, y=25.7, z=-layout.inch/2))
        part.Placement = obj.Placement
        obj.DrillPart = part"""
