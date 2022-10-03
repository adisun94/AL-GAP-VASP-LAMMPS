import re
import sys

iteration=str(int(sys.argv[1]))
configs_per_iter=int(sys.argv[2])
n_atoms=0
lat=[]
pos_atoms=[]
with open('../gap/GAPinput'+iteration+'.xyz') as f:
    n=0
    for line in f:
        if n==0:
            n_atoms=int(line)
        elif n==1:
            l=line.split()
            for i in l[4:13]:
                lat.append(float(re.sub("[^0-9^.]","",i)))
        elif (n_atoms+2)*configs_per_iter > n > (n_atoms+2)*(configs_per_iter-1)+1:
            pos_atoms.append(line.split()[:4])            
        n=n+1
     
atom_types={}
n=1
for j in [i[0] for i in pos_atoms]:
	if j not in atom_types.keys():
		atom_types[j]=n
		n=n+1

f=open('lammpsdata','w')
f.writelines('INPUT data for lammps\n\n')
f.writelines(str(n_atoms)+' atoms\n')
f.writelines('4 atom types\n')
f.writelines('0.0 '+str(lat[0])+' xlo xhi\n')
f.writelines('0.0 '+str(lat[4])+' ylo yhi\n')
f.writelines('0.0 '+str(lat[8])+' zlo zhi\n\n')
f.writelines('Masses\n\n')
f.writelines('1 6.941\n')
f.writelines('2 30.973\n')
f.writelines('3 32.06\n')
f.writelines('4 35.453\n\n')
f.writelines('Atoms\n\n')
for i in range(len(pos_atoms)):
	f.writelines(str(i+1)+' '+str(atom_types[pos_atoms[i][0]])+' '+' '.join(pos_atoms[i][1:])+'\n')
f.close()
print("-----------------------------------------------------------------")
print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print("-----------------------------------------------------------------")
print('Generated LAMMPS input datafile for next run')
print("-----------------------------------------------------------------")
print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
print("-----------------------------------------------------------------")
