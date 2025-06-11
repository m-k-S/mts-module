from PyOpticL import optomech

class BaseComponent:
    '''
    Base class for all components in the module.
    This class is not meant to be instantiated directly.
    It provides common functionality for all components.
    '''
    type = "Mesh::FeaturePython"
    
    def __init__(self, obj, stl, color=optomech.adapter_color, **kwargs):
        self.stl = stl
        drill = kwargs.get('drill', False)
        thumbscrews = kwargs.get('thumbscrews', False)

        obj.Proxy = self
        optomech.ViewProvider(obj.ViewObject)
        obj.ViewObject.ShapeColor = color
        obj.addProperty('App::PropertyBool', 'Drill').Drill = drill
        obj.addProperty('App::PropertyBool', 'Thumbscrew').Thumbscrew = thumbscrews

    def execute(self, obj):
    #change for other stls
        mesh = optomech._import_stl(self.stl[0], self.stl[1], self.stl[2])
        mesh.Placement = obj.Mesh.Placement
        obj.Mesh = mesh

class AVC(BaseComponent):
    def __init__(self, obj, stl=("AVC.stl", (0, 0, 90), (12, 0, 0)), drill=True):
        super().__init__(obj, stl, drill=drill)

class KM05(BaseComponent):
    def __init__(self, obj, stl=("KM05-Step.stl", (90, 0, 90), (2.084, -1.148, 0.498)), drill=True, thumbscrews=True):
        super().__init__(obj, stl=stl, drill=drill)

class LA1472(BaseComponent):
    def __init__(self, obj, stl=("LA1472-B-Step.stl", (90, 0, 90), (1.265, 0, 0)), drill=False):
        super().__init__(obj, stl, drill=drill)

class LC2067(BaseComponent):
    def __init__(self, obj, stl=("LC2067-B-Step.stl", (90, 0, 90), (1, 0, 0)), drill=False):
        super().__init__(obj, stl, drill=drill)

class LMR05(BaseComponent):
    def __init__(self, obj, stl=("LMR05-Step.stl", (90, 0, 90), (1.651, 0, 0)), drill=False):
        super().__init__(obj, stl, drill=drill)

class LMR9(BaseComponent):
    def __init__(self, obj, stl=("LMR9-Step.stl", (90, 0, 90), (1.651, 0, 0)), drill=False):
        super().__init__(obj, stl, drill=drill)

class Polarizer05(BaseComponent):
    def __init__(self, obj, stl=("polarizer05.stl", (90, 0, 90), (0, 0, -0)), drill=False):
        super().__init__(obj, stl, drill=drill)

class BeamSplitter(optomech.cube_splitter):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj, *args, **kwargs)

class Photodetector(optomech.photodetector_pda10a2):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj, *args, **kwargs)

class CircularMirror(optomech.circular_mirror):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj, *args, **kwargs)

class Fiberport(optomech.fiberport_mount_hca3):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(obj, *args, **kwargs)