.. image:: /docs/images/logo-small.png
   :target: https://github.com/iqm-finland/KQCircuits
   :alt: KQCircuits
   :width: 300
   :align: center

**KQCircuits** is a Python library developed by IQM for automating the design of
superconducting quantum circuits. It uses the `KLayout <https://klayout.de>`__ layout design program
API. **This fork is intended for the use during 2023 iteration of the Winter School
as it includes exercises to get familiar with KQCircuits**.

.. image:: https://github.com/iqm-finland/KQCircuits/actions/workflows/ci.yaml/badge.svg
   :target: https://github.com/iqm-finland/KQCircuits/actions/workflows/ci.yaml
   :alt: Continuous Integration

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4944796.svg
   :target: https://doi.org/10.5281/zenodo.4944796
   :alt: DOI

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://github.com/iqm-finland/kqcircuits/blob/master/LICENSE
   :alt: License

.. image:: https://img.shields.io/github/v/tag/iqm-finland/KQCircuits?label=version&sort=semver
   :target: https://github.com/iqm-finland/KQCircuits/releases/
   :alt: Latest version

.. image:: https://img.shields.io/badge/click-for%20documentation%20%F0%9F%93%92-lightgrey
   :target: https://iqm-finland.github.io/KQCircuits/index.html
   :alt: Click for documentation


----

KQCircuits generates multi-layer 2-dimensional-geometry representing common structures in quantum
processing units (QPU). It includes definitions of parametrized geometrical objects or “elements”,
framework to easily define your own elements, framework to get geometry from the elements by setting
values to parameters and a framework to assemble a full QPU design by combining many of the elements
in different geometrical relations. Among other templates, are also structures to combine QPU
designs to create optical mask layout and EBL patterns for fabrication of quantum circuits and
export a set of files for a mask as needed for QPU fabrication.

.. image:: /docs/images/readme/design_flow.svg
   :alt: QPU design workflow
   :width: 700

⠀

.. image:: /docs/images/readme/single_xmons_chip_3.png
   :alt: Example layout

Discord channel
^^^^^^^^^^^^^^^

Over the course of this one-week course we will provide help over
`our Discord channel <https://discord.gg/FW9Pj9U5hM>`__.

Installation guide for Winter School 2023 participants
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prerequisites
-------------

The system needs to have ``Python`` (version >= 3.7) and ``pip`` installed.
Run the following commands and check for errors to make sure that you have the required software installed.

   ``python --version``

   ``pip --version``

Install KLayout
---------------

We start by downloading and installing the latest ``KLayout`` application. There are options:

1. Download and install package from `the KLayout site <https://www.klayout.de/build.html>`__ - **recommended for Windows and Linux platforms**

   Choose the installation package according to your platform (Windows, Linux, etc).

   Open the installer and follow the instructions with default suggested ``Destination Folder``.

2. Download and install package from package manager like ``brew`` - **recommended for macOS platforms**

   We recommend using `Homebrew <https://brew.sh/>`__ to install KLayout on a MacOS platform.
   After installing Homebrew make sure that python and pip can be run from terminal, and if not, run: ``brew install python``

   Next install KLayout:

      ``brew install --cask klayout``

   Homebrew might place the ``klayout.app`` package in ``/Applications/KLayout/`` directory.
   In this case simply move the ``klayout.app`` package so that its path is ``/Applications/klayout.app``

   Attempt to start up KLayout, which might not work right away for following reasons:

   a. macOS might prompt to install Rosetta to support KLayout - follow macOS instructions to do so.

   b. macOS might not trust the KLayout application and refuse to run it. In that case do the following:

      - open ``Applications`` folder

      - control+click ``klayout.app`` executable, choose ``open``

      - macOS will again complain about untrusted applications, but this time provide an ``open`` option which should be chosen to override security

      - After launching KLayout once there should be no further issues on subsequent launches

Set up git
----------

We will use the ``git`` tool to download and install the ``KQCircuits`` source code present in this fork.
This tool can also be used to contribute to the KQCircuits project after this course if you wish to do so.
**Linux** and **macOS** platforms have git installed by default.

For **Windows** an external git distribution needs to be used.
We recommend `this Windows application <https://git-scm.com/downloads>`__.
After install you will have access to the ``Git Bash`` command line application which can be used to run **git** commands.
Open the ``Git Bash`` terminal and navigate to the folder of your choice using the ``cd`` command.
(the default location is the ``HOME`` directory, which is ``C:/Users/<UserName>``)

Install KQCircuits
------------------

Clone the KQCircuits repository:

   ``git clone https://github.com/iqm-finland/KQCircuits-winter-school.git KQCircuits``

This creates the KQCircuits directory at the working directory.

The following commands will configure KLayout to use the KQCircuits library

   ``cd KQCircuits``

   ``python setup_within_klayout.py``

In case the pip tool is invoked in your terminal with ``pip3`` rather than ``pip``, open ``setup_within_klayout.py`` with a text editor and edit the second last line https://github.com/iqm-finland/KQCircuits-winter-school/blob/03c48e3c066a8b9f7c4cf528bc82917742fc172a/setup_within_klayout.py#L84 to:

   ``os.system(f"pip3 install -r {pip_args}")``

Confirm KQCircuits is installed correctly
-----------------------------------------

We are now ready to use ``KQCircuits``. On **Windows** open the ``KLayout (Editor)`` application, for other platforms open ``klayout`` application.

Make sure that the ``KQCircuits`` works correctly with ``KLayout`` by checking the following:

- ``KQCircuits`` entry should be present in the top toolbar.
- On the bottom left in the ``Libraries`` panel the ``Chip Library`` option should be available from the dropdown menu. Choose it to see multiple ready made chips available for preview. You can drag any of the chips into the center layout to see its contents.

.. image:: https://github.com/iqm-finland/KQCircuits-winter-school/blob/main/check-kqcircuits-works.png?raw=true
   :alt: These should be available if KQCircuits works

If the KLayout doesn't seem to allow drag-and-dropping chips etc on to the layout, check the following:

- From top toolbar, choose ``File > Setup`` (**Windows**) or ``klayout > Preferences`` (**macOS**)
- Choose ``Application > Editing mode`` window
- Make sure ``Use editing mode by default`` is checked

.. image:: https://github.com/iqm-finland/KQCircuits-winter-school/blob/main/check-editing-mode-1.png?raw=true
   :alt: Enable Editing Mode
.. image:: https://github.com/iqm-finland/KQCircuits-winter-school/blob/main/check-editing-mode-2.png?raw=true
   :alt: Enable Editing Mode

Quick editor tips to get started. Of course more techniques will be taught in subsequent lectures.

- Use ``F2`` to center the view
- Use ``*`` key to view every available layer
- ``Left click`` to choose elements on the layout
- Double click to edit properties of the element on the layout
- Drag with ``Right click`` to zoom to the selected region
- ``Middle click`` to drag the layout, scroll to zoom

The content in the layout might look needlessly complicated like so:

.. image:: https://github.com/iqm-finland/KQCircuits-winter-school/blob/main/check-layer-properties-before.png?raw=true
   :alt: Before choosing layer properties

This can be simplified by choosing from the top toolbar: ``File`` > ``Load layer properties`` and navigating to: ``KQCircuits/klayout_package/python/kqcircuits/layer_config/default_layer_props.lym``

.. image:: https://github.com/iqm-finland/KQCircuits-winter-school/blob/main/check-layer-properties-during.png?raw=true
   :alt: Choosing layer properties

The results should look like this:

.. image:: https://github.com/iqm-finland/KQCircuits-winter-school/blob/main/check-layer-properties-after.png?raw=true
   :alt: After choosing layer properties

Modifying the KQCircuits code
-----------------------------

During this course you will be modifying certain parts of the code in the ``KQCircuits`` code as exercise.
You're free to choose the editor: `PyCharm <https://www.jetbrains.com/pycharm/>`__ and `Visual Studio Code <https://code.visualstudio.com/>`__ are quite good.
For the code changes to take into effect the KLayout instance
needs to be closed and reopened. If ``Chip Library`` panel does not show up, there most likely has been an error
with the KQCircuits code. Changes in the ``Chip`` or ``Element`` design code can also be taken into effect
without reopening KLayout by choosing from the top toolbar: ``KQCircuits > Reload libraries``

Installing KQCircuits as a Python module
----------------------------------------

So far we have set everything up to work for most of the course.
However, on the latter half of the course we will be exporting geometry
produced by KQCircuits into data to be used by third-party simulator software.
To make this happen we need to have KQCircuits installed as a module in pip.

``cd`` to the ``KQCircuits`` directory then run

   ``python -m pip install -e klayout_package/python``

This might take 5-10 minutes to execute so don't be worried.

   **macOS** users! While installing KQCircuits, ``pip`` will attempt to install KLayout as a dependency.
   However, most recent KLayout distributions in pip may not work for **macOS**. To remedy this,
   the KQCircuit ``klayout_package/python/setup.py`` can be configured to install an older KLayout version
   that has shown to work for **macOS**. Change the following line
   https://github.com/iqm-finland/KQCircuits-winter-school/blob/c33ff820d9bae3fbb293e82a645ca5154ae759b3/klayout_package/python/setup.py#L44
   to ``"klayout==0.27.9",``

To test that this got set up correctly, try running

``python klayout_package/python/scripts/simulations/waveguides_sim_compare.py``

This should cause KLayout to open with the following content:

.. image:: https://raw.githubusercontent.com/iqm-finland/KQCircuits-winter-school/main/check-standalone-works.png
   :alt: Simulation window

``cd`` to ``KQCircuits/tmp`` and there should be a ``waveguides_sim_elmer`` directory.

Video tutorials (might be outdated)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We have previously recorded video tutorials for the GUI installation available on YouTube.
These might be helpful, but we advise to follow the instructions as stated above or as presented in the first lecture.
Also always feel free to ask for help on
`discord <https://discord.gg/FW9Pj9U5hM>`__.

.. raw:: html

   <div style="overflow:auto;">
     <table style="">
       <tr>
         <th>
           Windows
         </th>
         <th>
           Ubuntu
         </th>
         <th>
           MacOS
         </th>
       </tr>
       <tr>
         <th>
           <a href="https://youtu.be/9ra_5s2i3eU">
             <img src="https://img.youtube.com/vi/9ra_5s2i3eU/mqdefault.jpg" width=300 alt="KQCircuits Getting Started (Windows)">
           </a>
         </th>
         <th>
           <a href="https://youtu.be/ml773WtfnT0">
             <img src="https://img.youtube.com/vi/ml773WtfnT0/mqdefault.jpg" width=300 alt="KQCircuits Getting Started (Ubuntu)">
           </a>
         </th>
         <th>
           <a href="https://youtu.be/lt5ThOQ-caU">
             <img src="https://img.youtube.com/vi/lt5ThOQ-caU/mqdefault.jpg" width=300 alt="KQCircuits Getting Started (MacOS)">
           </a>
         </th>
       </tr>
     </table>
   </div>



Documentation
^^^^^^^^^^^^^

Documentation for KQCircuits can be found `here <https://iqm-finland.github.io/KQCircuits/>`__.

It may also be generated from the sources with ``make html`` in the docs directory.

   For **Winter school** we advise to follow the installation guide as layed out above instead of following
   the installation guide presented in the documentation. If you experience some installation issue
   that was not addressed above, contact us by
   `discord <https://discord.gg/FW9Pj9U5hM>`__.

Contributing
^^^^^^^^^^^^

Contributions to KQC are welcome from the community and we would be happy to
accept contributions from the **Winter School** participants after the course.

   **Please note that the contributions are accepted in the**
   `official KQCircuits repository <https://github.com/iqm-finland/KQCircuits>`__
   **rather than this Winter School fork.**

Contributors are expected to accept IQM
Individual Contributor License Agreement by filling `a form at IQM website
<https://meetiqm.com/developers/clas>`__. See also section `Contributing
<https://iqm-finland.github.io/KQCircuits/contributing.html>`__ in the
documentation.

Citation
^^^^^^^^
Please see the
`documentation <https://iqm-finland.github.io/KQCircuits/citing.html>`__
for instructions on how to cite KQCircuits in your projects and publications.

Copyright
^^^^^^^^^

This code is part of KQCircuits

Copyright (C) 2021-2023 IQM Finland Oy

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see
https://www.gnu.org/licenses/gpl-3.0.html.

The software distribution should follow IQM trademark policy for open-source software
(`meetiqm.com/developers/osstmpolicy <https://meetiqm.com/developers/osstmpolicy/>`__).
IQM welcomes contributions to the code. Please see our contribution agreements for individuals
(`meetiqm.com/developers/clas/individual <https://meetiqm.com/developers/clas/individual/>`__)
and organizations (`meetiqm.com/developers/clas/organization <https://meetiqm.com/developers/clas/organization/>`__).

Trademarks
^^^^^^^^^^

KQCircuits is a registered trademark of IQM. Please see
`IQM open source software trademark policy <https://meetiqm.com/developers/osstmpolicy>`__.
