import sys, os
sys.path.append(os.path.dirname(__file__))
import MyComponents

from PyOpticL import layout, optomech
from datetime import datetime

# Adding name and date to keep a track of the updates
name = "MTS"
date_time = datetime.now().strftime("%m/%d/%Y")
label = name + " " +  date_time

dx,dy,dz = 13,7,1.5

# Dimension of the baseplate
base_dx = dx*layout.inch
base_dy = dy*layout.inch
base_dz = dz*layout.inch
gap = layout.inch/8
input_y = (dy-2)*layout.inch

mount_holes = [(0,0), (dx-1, 0), (0,dy-1), (dx-1, dy-1)]

# Combining the baseplate with the beam and all other optical componenets.
def MTS(x=0, y=0, angle=0, thumbscrews=True):
   
	# Difining the baseplate
	baseplate = layout.baseplate(base_dx, base_dy, base_dz, x=x, y=y, angle=angle, optics_dz = 2.5,
	                         gap=gap, name=name, label=label, mount_holes=mount_holes)

	# Adding the beams to the baseplate
	beam = baseplate.add_beam_path(x=gap, y=input_y, angle=layout.cardinal['right'])
	
	# add input fiberport, defined at the same coordinates as beam
	baseplate.place_element("Input Fiberport", optomech.fiberport_mount_hca3, 
	                    x=gap, y=input_y, angle=layout.cardinal['right'])
	
	baseplate.place_element_along_beam("Polarizer_1", MyComponents.Polarizer05, beam,
	                               beam_index=0b1, distance=0.5*layout.inch, angle=layout.cardinal['right'])
	
	baseplate.place_element_along_beam("Beam_Splitter", MyComponents.BeamSplitter, beam,
                                       beam_index=0b1, distance=1.5*layout.inch, angle=layout.cardinal['up'])
	
	baseplate.place_element_along_beam("Vapor_Cell", MyComponents.AVC, beam,
	                               beam_index=0b10, distance=3*layout.inch, angle=layout.cardinal['left'])

	baseplate.place_element_along_beam("Mirror_1", MyComponents.CircularMirror, beam,
	                               beam_index=0b11, distance=2.5*layout.inch, angle=layout.turn['down-right'],
								   mount_type=MyComponents.KM05)
	
	baseplate.place_element_along_beam("Polarizer_2", MyComponents.Polarizer05, beam,
									beam_index=0b11, distance=1*layout.inch, angle=layout.cardinal['left'])
	
	baseplate.place_element_along_beam("EOM", MyComponents.Polarizer05, beam,
									beam_index=0b11, distance=2*layout.inch, angle=layout.cardinal['right'])
	
	baseplate.place_element_along_beam("Mirror_2", MyComponents.CircularMirror, beam,
	                               beam_index=0b11, distance=3*layout.inch, angle=layout.turn['right-up'],
	                               mount_type=MyComponents.KM05)
	
	baseplate.place_element_along_beam("Polarizer_3", MyComponents.Polarizer05, beam,
									beam_index=0b11, distance=1.25*layout.inch, angle=layout.cardinal['down'])

	#baseplate.place_element_along_beam("Polarizer_3", MyComponents.Polarizer05, beam,
	#								beam_index=0b10, distance=1*layout.inch, angle=layout.cardinal['left'])

	baseplate.place_element_along_beam("Beam_Splitter_2", MyComponents.BeamSplitter, beam,
	                               beam_index=0b11, distance=1.25*layout.inch, angle=layout.cardinal['down'], invert=True)
	
	baseplate.place_element_along_beam("Photodetector", optomech.photodetector_pda10a2, beam,
	                               beam_index=0b111, distance=2*layout.inch, angle=layout.cardinal['left'])

if __name__ == "__main__":
	MTS()
	print("MTS layout created successfully.")
	layout.redraw()