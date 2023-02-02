# This code is part of KQCircuits
# Copyright (C) 2021 IQM Finland Oy
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


# Example XSection process description file

chip_distance = 10.0 # distance between bottom chip and top chip
wafer_thickness = 100.0

# Basic options
below(2.0) # default=2.0
depth(wafer_thickness*2 + chip_distance) # default=2.0
height(10.0) # default=2.0
# Declare the basic accuracy used to remove artefacts for example:
delta(5 * dbu)

# Input layers from layout

layer_b_base_metal_gap = layer("130/1")
layer_b_SIS_junction = layer("136/1")
layer_b_SIS_shadow = layer("137/1")
layer_b_airbridge_pads = layer("146/1")
layer_b_airbridge_flyover = layer("147/1")
layer_b_underbump_metallization = layer("148/1")
layer_b_indium_bump = layer("149/1")

layer_t_base_metal_gap = layer("2/2")
layer_t_SIS_junction = layer("8/2")
layer_t_SIS_shadow = layer("9/2")
layer_t_airbridge_pads = layer("18/2")
layer_t_airbridge_flyover = layer("19/2")
layer_t_underbump_metallization = layer("20/2")
layer_t_indium_bump = layer("21/2")

# general parameters

base_metal_height = 0.2
ubm_height = 0.02


################# Bottom chip ##################

# substrate
material_b_substrate = bulk # creates a substrate with top edge at y=0

# XSection always creates the bulk (wafer, substrate) at the same position and it cannot be moved. 
# In order to have two chips at different vertical positions, we thus have to remove the top part of 
# the bottom wafer first, so that later a top chip can be created there.
etch(wafer_thickness + chip_distance, :into => material_b_substrate)

# deposit base metal
material_b_base_metal = deposit(base_metal_height)
# etch base metal
mask(layer_b_base_metal_gap).etch(base_metal_height, -0.1, :mode => :round, :into => [ material_b_base_metal, material_b_substrate ])

# SIS
material_b_SIS_shadow = mask(layer_b_SIS_shadow).grow(0.1, 0.1, :mode => :round)
material_b_SIS_junction = mask(layer_b_SIS_junction).grow(0.1, 0.1, :mode => :round)

# create patterned resist for airbridges
material_b_airbridge_resist = mask(layer_b_airbridge_pads.inverted).grow(3.0, -50.0, :mode => :round)
planarize(:less => 0.3, :into => material_b_airbridge_resist)
# deposit metal for airbridges in patterned area 
material_b_airbridge_metal = mask(layer_b_airbridge_pads.or(layer_b_airbridge_flyover)).grow(0.3, -0.2, :mode => :round)
# remove resist for airbridges 
planarize(:downto => material_b_substrate, :into => material_b_airbridge_resist)

# deposit underbump metallization
material_b_underbump_metallization = mask(layer_b_underbump_metallization).grow(ubm_height, -0.1, :mode => :round)
# deposit indium bumps
material_b_indium_bump = mask(layer_b_indium_bump).grow(chip_distance/2 - ubm_height - base_metal_height, 0.1, :mode => :round)

# output the material data for bottom chip to the target layout
output("12/0", material_b_substrate)
output("10/0", material_b_base_metal)
output("17/0", material_b_SIS_junction)
output("18/0", material_b_SIS_shadow)
output("28/0", material_b_airbridge_resist)
output("29/0", material_b_airbridge_metal)
output("32/0", material_b_underbump_metallization)
output("33/0", material_b_indium_bump)

################# Top chip ##################

material_t_substrate = bulk # this creates a new substrate with top edge at y=0
flip()

# Remove the part of top chip substrate which is within bottom chip area (see earlier comment for bottom chip).
etch(wafer_thickness + chip_distance, :into => material_t_substrate)

# deposit base metal
material_t_base_metal = deposit(base_metal_height)
# etch base metal
mask(layer_t_base_metal_gap).etch(base_metal_height, -0.1, :mode => :round, :into => [ material_t_base_metal, material_t_substrate ])

# deposit underbump metallization
material_t_underbump_metallization = mask(layer_t_underbump_metallization).grow(ubm_height, -0.1, :mode => :round)
# deposit indium bumps
material_t_indium_bump = mask(layer_t_indium_bump).grow(chip_distance/2 - ubm_height - base_metal_height, 0.1, :mode => :round)

# output the material data for top chip to the target layout
output("42/0", material_t_substrate)
output("40/0", material_t_base_metal)
output("62/0", material_t_underbump_metallization)
output("63/0", material_t_indium_bump)
