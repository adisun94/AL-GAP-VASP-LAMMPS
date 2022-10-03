# AL-GAP-VASP-LAMMPS

This repository contains an Active Learning workflow to generate Gaussian Approximate Potentials (GAP).

The GAP method is originally published in [Bartok et al.](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.104.136403)

Molecular dynamics simulations are run using the [LAMMPS](https://www.lammps.org/#gsc.tab=0) software, version 09Oct2020 compiled with the quip package.

The configuration energies and interatomic forces are evaluated at the Density Functional Theory (DFT) level using the [VASP](https://www.vasp.at/) software, version 5.4.4.

#### ---- ActiveLearning
/GAPinput.xyz : input file from Step 0.0, used to train the GAP force field while starting the workflow.

/submit.sh : bash script to start workflow

/GAPtoLMP.py : convert xyz files to LAMMPS input format

/in.lmp.temp : LAMMPS input script

/DUMPtoPOSCAR.py : convert dump files to VASP input format

/INCAR, /KPOINTS, /POTCAR : VASP input scripts

#### ---- example
/gap/GAP.xml : latest trained GAP force field

/gap/GAPintput$i$.xyz : Input configurations for $i$<sup>th</sup> iteration

/lammps/lammpsdata$i$ : input configuration for the $i$<sup>th</sup> iteration

/lammps/dump$i$ : dump file containing coordinates and forces generated after the $i$<sup>th</sup> iteration

/lammps/energy$i$ : energy of configurations generated after the $i$<sup>th</sup> iteration

/lammps/log.lammps$i$ : output of the $i$<sup>th</sup> iteration

/vasp/$i$ : directory containing data from single point calculations for $n$ configurations selected in the $i$<sup>th</sup> iteration

