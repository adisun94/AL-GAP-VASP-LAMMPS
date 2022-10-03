# AL-GAP-VASP-LAMMPS

This repository contains an Active Learning workflow to generate Gaussian Approximate Potentials (GAP).

The GAP method is originally published in [Bartok et al.](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.104.136403)

Molecular dynamics simulations are run using the [LAMMPS](https://www.lammps.org/#gsc.tab=0) software, version 09Oct2020 compiled with the quip package.

The configuration energies and interatomic forces are evaluated at the Density Functional Theory (DFT) level using the [VASP](https://www.vasp.at/) software, version 5.4.4.
