from ase.io.lammpsrun import read_lammps_dump_text
from ase import io
import sys

configs_per_iter=int(sys.argv[2])
iteration=int(sys.argv[1])
z_atom={3:'Li',15:'P',16:'S',17:'Cl'}
d=io.read('dump',format='lammps-dump-text',index=':')

n=0
for i in range(1,len(d)):
	n=n+1
	f=open('POSCAR'+str(n),'w')
	f.writelines('New POSCAR file\n')
	f.writelines('1\n')
	for j in range(3):
		f.writelines(' '.join(d[i]._cellobj[j].astype(str))+'\n')
	f.writelines(' '.join(z_atom.values())+'\n')
	f.writelines('96 16 80 16\n')
	f.writelines('Cartesian\n')
	for j in range(d[i].arrays['numbers'].shape[0]):
		f.writelines(' '.join(d[i].arrays['positions'][j].astype(str))+'\n')
	f.close()

