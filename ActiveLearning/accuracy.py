import numpy as np
import sys
import os
import matplotlib.pyplot as plt
from ase import io
import ase.io
from ase.io.vasp import read_vasp_xml, read_vasp_xdatcar, read_vasp_out
from sklearn.metrics import mean_squared_error, mean_absolute_error

configs_per_iter=int(sys.argv[2])
error1, error2, error3, error4 = [],[],[],[]

energy_dft,force_dft=[],[]
energy_gap,force_gap=[],[]

iteration=str(int(sys.argv[1]))
n_configs=len(os.listdir('vasp/'+iteration))

# Configurations from the previous iteration

in_atoms = ase.io.read('gap/GAPinput'+iteration+'.xyz',':')
out_atoms = ase.io.read('gap/GAPoutput'+iteration+'.xyz',':')

for i in range(len(in_atoms)):
	n_atoms=in_atoms[i].arrays['numbers'].shape[0]
	energy_dft.append(in_atoms[i].get_potential_energy()/n_atoms)
	for j in in_atoms[i].arrays['force']:
		for k in j:
			force_dft.append(k)

for i in range(len(out_atoms)):
	n_atoms=out_atoms[i].arrays['numbers'].shape[0]
	energy_gap.append(out_atoms[i].get_potential_energy()/n_atoms)
	for j in out_atoms[i].arrays['force']:
		for k in j:
			force_gap.append(k)

# Additional configurations in this iteration

# VASP E and F

folders=os.listdir('vasp/'+iteration)
folders.sort()

for f in folders:  

	d=read_vasp_out('vasp/'+iteration+'/'+f+'/OUTCAR')
	n_atoms=d.arrays['numbers'].shape[0]
	energy_dft.append(d._calc.results['energy']/n_atoms)	
	for n in range(d.arrays['numbers'].shape[0]):
		for n2 in range(3):
			force_dft.append(d._calc.results['forces'][n][n2])	

# LAMMPS-GAP E and F

n=0
eg=[]
with open('lammps/energy'+iteration) as f:
	for line in f:
		n=n+1
		if n>=2:
			eg.append(float(line.split()[2]))
eg=eg[::20][1:]
for i in eg:
	energy_gap.append(i/n_atoms)

d=io.read('lammps/dump'+iteration,format='lammps-dump-text',index=':')
for f in range(1,configs_per_iter+1):
	for n in range(d[f].arrays['numbers'].shape[0]):
		for n2 in range(3):
			force_gap.append(d[f]._calc.results['forces'][n][n2]) 

#print(len(energy_dft))
#print(len(energy_gap))
#print(len(force_dft))
#print(len(force_gap))

file_error = open('DFTvsGAPerror','a')
file_error.write('Iteration = '+iteration+', num_energies = '+str(len(energy_dft))+', Energy MAE = '+str(mean_absolute_error(energy_dft,energy_gap))+' eV/atom, num_forces = '+str(len(force_dft))+', Force MAE = '+str(mean_absolute_error(force_dft,force_gap))+' eV/A \n')
file_error.close()

print('done')
