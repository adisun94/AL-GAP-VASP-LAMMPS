import os
import shutil
import re
import re
import os
import sys
from ase.io.vasp import read_vasp_out

def restart_gapinput_file(current):

	z_atom={3:'Li',15:'P',16:'S',17:'Cl'}

	folders=os.listdir('vasp/'+str(current))
	folders.sort()

	f=open('xyz-temp','w')
	for i in folders:
		d=read_vasp_out('vasp/'+str(current)+'/'+i+'/OUTCAR')
		f.writelines(str(d.arrays['numbers'].shape[0])+'\n')
		f.writelines('energy='+str(d._calc.results['energy'])+' ')
		f.writelines('pbc="T T T"'+' ')
		f.writelines('Lattice="'+' '.join(d._cellobj[0].astype(str))+' '+' '.join(d._cellobj[1].astype(str))+' '+' '.join(d._cellobj[2].astype(str))+'" ')
		f.writelines('Properties=species:S:1:pos:R:3:Z:I:1:force:R:3')
		f.writelines('\n')
		for n in range(d.arrays['numbers'].shape[0]):
			f.writelines(z_atom[d.arrays['numbers'][n]]+' ')
			f.writelines(' '.join(d.arrays['positions'][n].astype(str))+' ')
			f.writelines(str(d.arrays['numbers'][n])+' ')
			f.writelines(' '.join(d._calc.results['forces'][n].astype(str)))
			f.writelines('\n')
	f.close()

if os.path.exists('RESTARTS')==False:
	os.mkdir('RESTARTS')

iters=[int(f) for f in os.listdir('vasp') if re.match('[0-9]',f)]
n=max(iters)

restart_gapinput_file(n)
os.system('cat gap/GAPinput%s.xyz xyz-temp > GAPinput.xyz'%(n))
os.system('rm xyz-temp')

s=[f for f in os.listdir() if re.match(r'slurm-*',f)][0]
l=os.listdir('RESTARTS')
new_folder='RESTARTS/'+str(len(l)+1)+'/'
os.mkdir(new_folder)
for f in ['gap','lammps','vasp',s,'DFTvsGAPerror']:
	shutil.move(f,new_folder)
