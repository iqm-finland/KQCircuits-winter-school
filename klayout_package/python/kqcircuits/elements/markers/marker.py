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


from autologging import logged

from kqcircuits.pya_resolver import pya
from kqcircuits.util.parameters import Param, pdt
from kqcircuits.elements.element import Element
from kqcircuits.defaults import default_marker_type


@logged
class Marker(Element):
    """Base Class for Markers."""

    default_type = default_marker_type

    diagonal_squares = Param(pdt.TypeInt, "Number of diagonal squares in the marker", 10)
    window = Param(pdt.TypeBoolean, "Window in airbridge flyover layer", False)

    @classmethod
    def create(cls, layout, library=None, marker_type=None, **parameters):
        """Create a Marker cell in layout."""
        return cls.create_subtype(layout, library, marker_type, **parameters)[0]

    def produce_geometry(self):
        """Produce common marker geometry."""

        layer_gap = self.get_layer("base_metal_gap_wo_grid")
        layer_pads = self.get_layer("airbridge_pads")
        layer_flyover = self.get_layer("airbridge_flyover")
        layer_gap_for_ebl = self.get_layer("base_metal_gap_for_EBL")
        layer_protection = self.get_layer("ground_grid_avoidance")

        def insert_to_main_layers(shape):
            self.cell.shapes(layer_gap).insert(shape)
            self.cell.shapes(layer_gap_for_ebl).insert(shape)
            if not self.window:
                self.cell.shapes(layer_flyover).insert(shape)

        # protection for the box
        protection_box = pya.DBox(
            pya.DPoint(220, 220),
            pya.DPoint(-220, -220)
        )
        self.cell.shapes(layer_protection).insert(protection_box)

        # make corners
        corner = pya.DPolygon([
            pya.DPoint(100, 100),
            pya.DPoint(10, 100),
            pya.DPoint(10, 80),
            pya.DPoint(80, 80),
            pya.DPoint(80, 10),
            pya.DPoint(100, 10),
        ])
        inner_corners = [pya.DTrans(a) * corner for a in [0, 1, 2, 3]]
        outer_corners = [pya.DCplxTrans(2, a * 90., False, pya.DVector()) * corner for a in [0, 1, 2, 3]]
        corners = pya.Region([s.to_itype(self.layout.dbu) for s in inner_corners + outer_corners])
        insert_to_main_layers(corners)

        # center box
        sqr_uni = pya.DBox(
            pya.DPoint(10, 10),
            pya.DPoint(-10, -10),
        )
        insert_to_main_layers(sqr_uni)

        self.inv_corners = pya.Region([protection_box.to_itype(self.layout.dbu)])
        self.inv_corners -= corners
        self.cell.shapes(layer_pads).insert(self.inv_corners - pya.Region(sqr_uni.to_itype(self.layout.dbu)))

        # window for airbridge flyover layer
        aflw = pya.DPolygon([
            pya.DPoint(800, 800),
            pya.DPoint(800, 10),
            pya.DPoint(80, 10),
            pya.DPoint(80, 2),
            pya.DPoint(2, 2),
            pya.DPoint(2, 80),
            pya.DPoint(10, 80),
            pya.DPoint(10, 800)
        ])
        if self.window:
            for alpha in [0, 1, 2, 3]:
                self.cell.shapes(layer_flyover).insert(pya.DTrans(alpha) * aflw)

        # marker diagonal
        sqr = pya.DBox(
            pya.DPoint(10, 10),
            pya.DPoint(2, 2),
        )
        self.diagonals = pya.Region()
        for i in range(5, 5 + self.diagonal_squares):
            ds = pya.DCplxTrans(3, 0, False, pya.DVector(50 * i - 3 * 6, 50 * i - 3 * 6)) * sqr
            insert_to_main_layers(ds)
            self.cell.shapes(layer_pads).insert(ds)
            self.diagonals += ds.to_itype(self.layout.dbu)
            self.cell.shapes(layer_protection).insert(
                pya.DCplxTrans(20, 0, False, pya.DVector(50 * i - 20 * 6, 50 * i - 20 * 6)) * sqr)
