# Copyright (c) 2019-2022 IQM Finland Oy.
#
# All rights reserved. Confidential and proprietary.
#
# Distribution or reproduction of any information contained herein is prohibited without IQM Finland Oy's prior
# written permission.

import math

from kqcircuits.elements.element import Element
from kqcircuits.pya_resolver import pya
from kqcircuits.qubits.qubit import Qubit
from kqcircuits.util.geometry_helper import circle_polygon, arc_points
from kqcircuits.util.parameters import Param, pdt, add_parameters_from


@add_parameters_from(Element, n=180)
class ConcentricTransmon(Qubit):
    """The PCell declaration for a concentric transmon.

    WINTER SCHOOL 2023 ASSIGNMENT - replace ... with working code to implement the ConcentricTransmon qubit

    A concentric transmon consists of two islands, one inner and one outer, connected by a Josephson Junction/s. Multiple
    couplers can be defined. They can have custom waveguide impedance, size and shape.
    Each coupler has reference points, numbered starting from 1. Driveline can be connected to the drive port.

    """
    # Qubit geometry
    r_inner = Param(pdt.TypeDouble, "Internal island radius", 120, unit="μm",
                    docstring="Radius of the outer edge of the inner island")
    r_outer = Param(pdt.TypeDouble, "External island radius, measured at the outer edge", 250, unit="μm",
                    docstring="Radius of the external coupler island")
    outer_island_width = Param(pdt.TypeDouble, "Outer island radial width", 80, unit="μm",
                               docstring="Width of the external island")
    ground_gap = Param(pdt.TypeDouble, "Ground plane padding", 80, unit="μm")
    squid_angle = Param(pdt.TypeDouble, "Angular position of the Josephson Junction/s, where the positive x-axis",
                        120, unit="degrees")

    # Couplers parameters (the list size define the number of couplers)
    couplers_r = Param(pdt.TypeDouble, "Radius of the couplers positioning", 290, unit="[μm]")
    couplers_a = Param(pdt.TypeList, "Width of the coupler waveguide's center conductors", [10, 3, 4.5], unit="[μm]")
    couplers_b = Param(pdt.TypeList, "Width of the coupler waveguide's gaps", [6, 32, 20], unit="[μm]")
    couplers_angle = Param(pdt.TypeList,
                           "Positioning angles of the couplers, where 0deg corresponds to positive x-axis",
                           [340, 60, 210], unit="[degrees]")
    couplers_width = Param(pdt.TypeList, "Radial widths of the arc couplers", [10, 20, 30], unit="[μm]")
    couplers_arc_amplitude = Param(pdt.TypeList, "Couplers angular extension", [35, 45, 15], unit="[degrees]")

    # Drive port parameters
    drive_angle = Param(pdt.TypeDouble, "Angle of the drive port, where 0deg corresponds to positive x-axis", 300,
                        unit="degrees")
    drive_distance = Param(pdt.TypeDouble, "Distance of the driveline, measured from qubit centre", 400, unit="µm")

    def build(self):
        self.x_end = self.r_outer + self.ground_gap  # Define the outermost qubit coordinate

        # Generate the qubit islands (they are the negative shape of the final geometry)
        qubit_negative = self._make_qubit_islands()

        # Generate the coupler islands
        coupler_islands_region = self._make_coupler_island()

        # Add the waveguides connecting the couplers to external waveguides
        waveguide, waveguide_gap = self._make_waveguides()

        # Add the Josephson Junction/s
        self._add_junction(qubit_negative)

        # Define the capacitor in the ground (final polarity)
        ground_region = self._make_ground_region()
        qubit = ground_region - qubit_negative + waveguide_gap - coupler_islands_region - \
                waveguide  # Operations order is important!
        self.cell.shapes(self.get_layer("base_metal_gap_wo_grid")).insert(qubit)

        # Protection region from the ground grid
        region_protection = self._get_protection_region(ground_region)
        self.cell.shapes(self.get_layer("ground_grid_avoidance")).insert(region_protection)

        # Couplers and driveline ports
        self._add_ports()

    def _make_arc_island(self, island_outer_radius, island_width, swept_angle):
        """WINTER SCHOOL 2023 - uncomment code below and fill in the missing parts"""

        # # Generate a polygon arc of any size and angle

        # angle_rad = math.radians(swept_angle)
        # points_outside = arc_points(island_outer_radius, ..., ..., ...)
        # points_inside = arc_points(island_outer_radius - island_width, ..., ..., ...)
        # points = ...
        # arc_island = ...

        # return arc_island

        return None  # WINTER SCHOOL 2023 - Remove this line when done

    def _make_qubit_islands(self):
        """WINTER SCHOOL 2023 - uncomment code below and fill in the missing parts"""

        # Generate a region of the qubit shunting capacitor
        # capacitor_islands = []
        # # Inner circular island
        # inner_island = circle_polygon(..., ...)
        # capacitor_islands.append(inner_island)
        # # Outer cylindrical island
        # outer_island = self._make_arc_island(..., ..., ...)
        # capacitor_islands.append(outer_island)

        # return pya.Region([poly.to_itype(self.layout.dbu) for poly in capacitor_islands])

        raise ValueError("Start the WINTER SCHOOL exercise by implementing _make_qubit_islands")  # WINTER SCHOOL 2023 - Remove this line when done

    def _make_coupler_island(self):
        """WINTER SCHOOL 2023 - uncomment code below and fill in the missing parts"""

        # Generate the regions of the coupler islands.
        round_corner = 5
        coupler_islands_region = pya.Region()
        # # Generate all the couplers in the same region
        # for i, (c_angle, c_width, c_arc_ampl) in enumerate(
        #         zip(..., ..., ...)):
        #     coupler_island = self._make_arc_island(..., float(c_width), ...)
        #     coupler_island_region = pya.Region(...).round_corners(
        #         round_corner / self.layout.dbu, round_corner / self.layout.dbu, self.n).transformed(
        #         pya.ICplxTrans(..., ..., ..., ..., ...))
        #     coupler_islands_region += ...

        return coupler_islands_region

    def _make_waveguides(self):
        """WINTER SCHOOL 2023 - uncomment code below and fill in the missing parts"""

        # Make the waveguides for each coupler with custom impedance and return the region
        waveguides_signal_region = pya.Region()
        waveguides_gap_region = pya.Region()
        # Add the waveguides inside the ground padding
        overlapping_margin = 0.5
        # for i, (c_a, c_b, c_angle) in enumerate(zip(..., ..., ...)):
        #     waveguide_signal = pya.Region([pya.DPolygon([
        #         pya.DPoint(...+overlapping_margin, float(c_a) / 2),
        #         pya.DPoint(..., float(c_a) / 2),
        #         pya.DPoint(..., -float(c_a) / 2),
        #         pya.DPoint(...+overlapping_margin, -float(c_a) / 2),
        #     ]).to_itype(self.layout.dbu)]).transformed(pya.ICplxTrans(1, ..., False, 0, 0))
        #     waveguide_gap = pya.Region([pya.DPolygon([
        #         pya.DPoint(self.x_end, ...),
        #         pya.DPoint(self.couplers_r, ...),
        #         pya.DPoint(self.couplers_r, ...),
        #         pya.DPoint(self.x_end, ...),
        #     ]).to_itype(self.layout.dbu)]).transformed(pya.ICplxTrans(1, ..., False, 0, 0))
        #     waveguides_signal_region += waveguide_signal
        #     waveguides_gap_region += waveguide_gap
        return waveguides_signal_region, waveguides_gap_region

    def _add_junction(self, region):
        """WINTER SCHOOL 2023 - uncomment code below and fill in the missing parts"""

        # # Add the junction to the qubit islands
        # squid_origin = arc_points(..., ..., 2 * math.pi, self.n, pya.DPoint(0, 0))[0]
        # squid_transf = pya.DCplxTrans(..., ..., ..., ...)
        # self.produce_squid(squid_transf)
        # squid_distance_from_centre = self.refpoints['squid_port_common'].distance(self.refpoints['base'])
        # # Connect the junction to the inner island
        # squid_connection = pya.Region(squid_transf * pya.DPolygon([
        #     pya.DPoint(-4, 0),
        #     pya.DPoint(-4, -squid_distance_from_centre - 0.5),
        #     pya.DPoint(4, -squid_distance_from_centre - 0.5),
        #     pya.DPoint(4, 0)]
        # ).to_itype(self.layout.dbu))
        # region += ...

        return None  # WINTER SCHOOL 2023 - Remove this line when done

    def _make_ground_region(self):
        """WINTER SCHOOL 2023 - uncomment code below and fill in the missing parts"""

        # # Generate the ground region as a filled circle of the maximum size
        # n_points = self.n
        # return pya.Region(... .to_itype(self.layout.dbu))

        return pya.Region()  # WINTER SCHOOL 2023 - Remove this line when done

    def _add_ports(self):
        """WINTER SCHOOL 2023 - uncomment code below and fill in the missing parts"""

        # # Add couplers ports
        # for i, c_angle in enumerate(map(float, self.couplers_angle)):
        #     coupler_origin = arc_points(..., ..., 2 * math.pi, self.n, pya.DPoint(0, 0))[0]
        #     coupler_transf = pya.DCplxTrans(1, ..., False, ...)
        #     self.add_port(f"coupler_{i + 1}", ...,
        #                   direction=pya.DVector(coupler_transf * pya.DPoint(0, 0)))
        # # Add driveline port
        # drive_origin = arc_points(..., ..., 2 * math.pi, self.n,
        #                           pya.DPoint(0, 0))[0]
        # drive_transf = pya.DCplxTrans(1, ..., False, ...)
        # self.add_port("drive", ..., direction=pya.DVector(drive_transf * pya.DPoint(0, 0)))

        return None  # WINTER SCHOOL 2023 - Remove this line when done

    def _get_protection_region(self, region):
        """WINTER SCHOOL 2023 - uncomment code below and fill in the missing parts"""

        # # Region which we don't want to cover with the automatically generated ground grid
        # protection_region = region.sized(...)

        # return protection_region

        return pya.Region()  # WINTER SCHOOL 2023 - Remove this line when done
