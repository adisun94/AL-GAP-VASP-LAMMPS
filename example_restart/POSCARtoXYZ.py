import re
import os
import sys
from ase.io.vasp import read_vasp_out

z_atom={3:'Li',15:'P',16:'S',17:'Cl'}
iteration = str(int(sys.argv[1]))

folders=os.listdir('../vasp/'+iteration)
folders.sort()

f=open('xyz-temp','w')
for i in folders:
	d=read_vasp_out('../vasp/'+iteration+'/'+i+'/OUTCAR')
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
