# Copyright (c) 2019-2022 IQM Finland Oy.
#
# All rights reserved. Confidential and proprietary.
#
# Distribution or reproduction of any information contained herein is prohibited without IQM Finland Oy's prior
# written permission.

from autologging import logged

from kqcircuits.chips.chip import Chip
from kqcircuits.elements.meander import Meander
from kqcircuits.elements.waveguide_composite import WaveguideComposite, Node
from kqcircuits.elements.waveguide_coplanar_splitter import WaveguideCoplanarSplitter
from kqcircuits.pya_resolver import pya
from kqcircuits.qubits.concentric_transmon import ConcentricTransmon
from kqcircuits.util.coupler_lib import cap_params
from kqcircuits.util.parameters import Param, pdt


@logged
class ConcentricQubitsDemo(Chip):
    """Demonstration chip with two concentric qubits, two readout resonators, one probe line,
    two drivelines and one resonant coupler.
    """

    name_chip = Param(pdt.TypeString, "Name of the chip", "WS1")

    readout_res_lengths = Param(pdt.TypeList, "Readout resonator lengths", [8000, 10000], unit="[μm]")
    kappa_finger_control = Param(pdt.TypeList, "Finger control for the input capacitor",
                                 default=[1.99, 2.035], unit="[μm]")

    coupler_length = Param(pdt.TypeDouble, "Resonant coupler length", 10000)

    couplers_a = Param(pdt.TypeList, "Width of the coupler waveguide's center conductors", [[10, 3], [10, 3]],
                       unit="[μm]")
    couplers_b = Param(pdt.TypeList, "Width of the coupler waveguide's gaps", [[6, 32], [6, 32]], unit="[μm]")
    couplers_angle = Param(pdt.TypeList,
                           "Positioning angles of the couplers, where 0deg corresponds to positive x-axis",
                           [[225, 315], [315, 225]], unit="[degrees]")
    couplers_width = Param(pdt.TypeList, "Radial widths of the arc couplers", [[10, 10], [10, 10]], unit="[μm]")
    couplers_arc_amplitude = Param(pdt.TypeList, "Couplers angular extension", [[35, 55], [45, 55]], unit="[degrees]")

    drive_line_offsets = Param(pdt.TypeList, "Distance between the end of a drive line and the qubit pair", [450.0] * 2)

    def build(self):
        # Define launchpads positioning and function
        launcher_assignments = {
            1: "DL-QB1",
            2: "DL-QB2",
            5: "PL-OUT",
            6: "PL-IN",
        }
        # Use an 8 port default launcher
        self.produce_launchers("SMA8", launcher_assignments)
        self.produce_qubits()
        self.produce_coupler()
        self.produce_drivelines()
        self.produce_probeline()
        self.produce_readout_resonators()

    def produce_qubits(self):
        # Position the qubits
        tranformations = [pya.DCplxTrans(1, 0, False, 3000, 7000),
                          pya.DCplxTrans(1, 0, False, 7000, 7000)]
        drive_angles = [110, 70]

        # Make a function to add a single qubit
        def produce_qubit(name, trans, couplers_a, couplers_b, couplers_angle, couplers_width, couplers_arc_amplitude,
                          drive_angle, drive_line_offset):
            qubit_cell = self.add_element(ConcentricTransmon,
                                          r_inner=100,
                                          r_outer=280,
                                          outer_island_width=80,
                                          ground_gap=40,
                                          squid_angle=90,
                                          drive_angle=drive_angle,
                                          drive_distance=drive_line_offset,
                                          couplers_r=300,
                                          couplers_a=couplers_a,
                                          couplers_b=couplers_b,
                                          couplers_angle=couplers_angle,
                                          couplers_width=couplers_width,
                                          couplers_arc_amplitude=couplers_arc_amplitude
                                          )
            self.insert_cell(qubit_cell, trans, name, rec_levels=None)

        # Insert all the qubits
        for i, (trans, c_a, c_b, c_angle, c_width, c_arc_ampl, drive_angle, drive_line_offset) in enumerate(
                zip(tranformations, self.couplers_a, self.couplers_b, self.couplers_angle, self.couplers_width,
                    self.couplers_arc_amplitude, drive_angles, self.drive_line_offsets)):
            produce_qubit(f'QB{i + 1}', trans, c_a, c_b, c_angle, c_width, c_arc_ampl, drive_angle, drive_line_offset)

    def produce_coupler(self):
        # Insert a fixed coupler of a variable meander size in between qubits
        _, _, length = WaveguideComposite.produce_fixed_length_waveguide(self, lambda x: [
            Node(self.refpoints["QB1_port_coupler_2"]),
            Node(self.refpoints["QB1_port_coupler_2_corner"], n_bridges=1),
            Node(pya.DPoint(4500, 6500), n_bridges=2),
            Node(pya.DPoint(5500, 6500), length_before=x, n_bridges=6),
            Node(self.refpoints["QB2_port_coupler_2_corner"], n_bridges=2),
            Node(self.refpoints["QB2_port_coupler_2"], n_bridges=1),
        ], initial_guess=5000, length=self.coupler_length, a=float(self.couplers_a[0][1]),
                                                                         b=float(self.couplers_b[0][1]), term1=0,
                                                                         term2=0)

        self.__log.info(f"Coupler line length: {length:.2f}")

    def produce_drivelines(self):
        # Connect the drivelines to the qubit ports
        for qubit_nr in range(1, 3):
            self.insert_cell(WaveguideComposite, nodes=[
                Node(self.refpoints[f"DL-QB{qubit_nr}_base"]),
                Node(self.refpoints[f"DL-QB{qubit_nr}_port_corner"], n_bridges=1),
                Node(self.refpoints[f"DL-QB{qubit_nr}_port_corner"] + pya.DPoint(0, -1200), n_bridges=1),
                Node(self.refpoints[f"QB{qubit_nr}_port_drive_corner"], n_bridges=1),
                Node(self.refpoints[f"QB{qubit_nr}_port_drive"]),
            ], term2=self.b)

    def produce_probeline(self):
        y_coordinate = 3500  # where the probeline is passing
        # Make the probeline pass through the resonators tees
        probeline = self.add_element(WaveguideComposite, nodes=[
            Node(self.refpoints["PL-IN_base"]),
            Node(self.refpoints["PL-IN_port_corner"], n_bridges=1),
            Node(pya.DPoint(self.refpoints["PL-IN_base"].x, y_coordinate), n_bridges=2),
            Node(pya.DPoint(self.refpoints["PL-IN_base"].x + 200, y_coordinate), WaveguideCoplanarSplitter,
                 align=("port_a", "port_c"), angles=[180, 135, 0], lengths=[50, 150, 50], inst_name="QB1_tee"),
            Node(pya.DPoint(self.refpoints["PL-OUT_base"].x - 200, y_coordinate), WaveguideCoplanarSplitter,
                 align=("port_a", "port_c"), angles=[180, 45, 0], lengths=[50, 150, 50], inst_name="QB2_tee",
                 n_bridges=3),
            Node(pya.DPoint(self.refpoints["PL-OUT_base"].x, y_coordinate)),
            Node(self.refpoints["PL-OUT_port_corner"], n_bridges=2),
            Node(self.refpoints["PL-OUT_base"], n_bridges=1),
        ], a=self.a, b=self.b, term1=0, term2=0)
        self.insert_cell(probeline, inst_name='pl')

    def produce_readout_resonators(self):
        # Break down the resonator in few parts for simplicity
        tee_angles = [135, 45]
        for i, t_angle in enumerate(tee_angles):
            capacitor = self.add_element(
                **cap_params(
                    fingers=float(self.kappa_finger_control[i]),
                    coupler_type="smooth",
                    element_key='cls',
                    fixed_length=160
                )
            )
            _, cplr_ref = self.insert_cell(capacitor, trans=pya.DCplxTrans(1, t_angle, False, 0, 0),
                                           align_to=f'pl_QB{i + 1}_tee_port_b',
                                           align="port_a")
            # Add the lower part of the resonator, align it, measure it
            resonator_bottom, _ = self.insert_cell(WaveguideComposite, nodes=[
                Node(cplr_ref['port_b']),
                Node(cplr_ref['port_b_corner']),
                Node(
                    pya.DPoint(self.refpoints[f"QB{i + 1}_port_coupler_1_corner"].x, cplr_ref['port_b_corner'].y + 50)),
                Node(pya.DPoint(self.refpoints[f"QB{i + 1}_port_coupler_1_corner"].x,
                                cplr_ref['port_b_corner'].y + 100), n_bridges=1),
            ], inst_name=f'resonator_bottom_{i + 1}')
            length_nonmeander_bottom = resonator_bottom.cell.length()
            # Add the upper part of the resonator, align it, measure it
            resonator_top, resonator_top_ref = self.insert_cell(WaveguideComposite, nodes=[
                Node(self.refpoints[f"QB{i + 1}_port_coupler_1"]),
                Node(self.refpoints[f"QB{i + 1}_port_coupler_1_corner"]),
                Node(self.refpoints[f"QB{i + 1}_port_coupler_1_corner"] + pya.DPoint(0, -300)),
            ], inst_name=f'resonator_top_{i + 1}')
            length_nonmeander_top = resonator_top.cell.length()
            # Add the missing part in the center in the correct length
            meander, _ = self.insert_cell(Meander,
                                          start=resonator_top_ref["port_b"],
                                          end=self.refpoints[f'resonator_bottom_{i + 1}_port_b'],
                                          length=float(self.readout_res_lengths[
                                                           i]) - length_nonmeander_top - length_nonmeander_bottom,
                                          n_bridges=10,
                                          n=300
                                          )
            self.__log.info(
                f"Resonator QB{i + 1} length: {length_nonmeander_bottom + length_nonmeander_top + meander.cell.length()}")
