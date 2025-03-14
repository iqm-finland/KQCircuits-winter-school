# This code is part of KQCircuits
# Copyright (C) 2022 IQM Finland Oy
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see
# https://www.gnu.org/licenses/gpl-3.0.html.
#
# The software distribution should follow IQM trademark policy for open-source software
# (meetiqm.com/developers/osstmpolicy). IQM welcomes contributions to the code. Please see our contribution agreements
# for individuals (meetiqm.com/developers/clas/individual) and organizations (meetiqm.com/developers/clas/organization).

import sys
import logging
from pathlib import Path

from kqcircuits.pya_resolver import pya
from kqcircuits.simulations.export.simulation_export import export_simulation_oas, sweep_simulation
from kqcircuits.simulations.export.elmer.cross_section_elmer_export import export_cross_section_elmer
from kqcircuits.simulations.export.xsection.xsection_export import create_xsections_from_simulations, \
    separate_signal_layer_shapes
from kqcircuits.simulations.waveguides_sim import WaveGuidesSim
from kqcircuits.util.export_helper import create_or_empty_tmp_directory, get_active_or_new_layout, \
    open_with_klayout_or_default_application


# This testcase is derived from waveguides_sim_compare.py and
# provides an example of how to use the XSection tool to produce cross section simulations.
#
# Simulation parameters
sim_class = WaveGuidesSim  # pylint: disable=invalid-name

multiface = True

sweep_parameters = {
    'n_guides': [1, 2, 3]
}

path = create_or_empty_tmp_directory(Path(__file__).stem + "_output")

cpw_length = 100
sim_box_height = 1000
sim_parameters = {
    'name': 'waveguides',
    'box': pya.DBox(pya.DPoint(-cpw_length/2., -sim_box_height/2.), pya.DPoint(cpw_length/2., sim_box_height/2.)),
    'cpw_length': cpw_length,
    'face_stack': ['1t1', '2b1'] if multiface else ['1t1']
}

workflow = {
    'run_gmsh': True,
    'run_gmsh_gui': True,
    'run_elmergrid': True,
    'run_elmer': True,
    'run_paraview': True,  # this is visual view of the results which can be removed to speed up the process
    'python_executable': 'python', # use 'kqclib' when using singularity image (you can also put a full path)
    'elmer_n_processes': -1,  # -1 means all the physical cores
}

mesh_size = {
    'vacuum': 100,
    'b_substrate': 100,
    # 'b_signal_1': 1,
    # 'b_signal_2': 1,
    # 'b_signal_3': 1,
    'b_simulation_ground': 4,
    'ma_layer': 1,
    'ms_layer': 1,
    'sa_layer': 1,
    't_substrate': 100,
    't_simulation_ground': 4,
}

# Get layout
logging.basicConfig(level=logging.WARN, stream=sys.stdout)
layout = get_active_or_new_layout()

simulations = sweep_simulation(layout, sim_class, sim_parameters, sweep_parameters)
for simulation in simulations:
    separate_signal_layer_shapes(simulation)

# Create cross sections using xsection tool
# Oxide layer permittivity and thickness values same as in double_pads_sim.py simulation
xsection_simulations = create_xsections_from_simulations(simulations,
    (pya.DPoint(0, 150), pya.DPoint(0, -150)), # Cut coordinates
    ma_permittivity=8.0,
    ms_permittivity=11.4,
    sa_permittivity=4.0,
    ma_thickness=0.0048,
    ms_thickness=0.0003,
    sa_thickness=0.0024,
    magnification_order=3 # Zoom to nanometers due to thin oxide layers
)
open_with_klayout_or_default_application(export_simulation_oas(xsection_simulations, path))
export_cross_section_elmer(xsection_simulations, path, mesh_size=mesh_size, workflow=workflow)
