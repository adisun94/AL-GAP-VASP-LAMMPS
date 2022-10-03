#!/bin/bash

#SBATCH --job-name=LPSC
#SBATCH --account=MVCATHODE
#SBATCH --partition=knlall
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --mail-user=asundar@anl.gov>     # Optional if you require email
#SBATCH --mail-type=ALL                  # Optional if you require email
#SBATCH --time=5:00:00

mkdir vasp
cp POTCAR INCAR KPOINTS submit.sh vasp/
mkdir gap
cp GAPinput.xyz POSCARtoXYZ.py gap/
mkdir lammps
module load lammps/09Oct20_quip
cp in.lmp.temp GAPtoLMP.py DUMPtoPOSCAR.py lammps/

iters=4
configs_per_iter=2
cut_e=0.003
cut_f=0.1

for ((i=1;i<=iters;i++))
do

# Fit GAP to initial DFT dataset

cd gap

if [ 1 -eq "$(echo "${i} == 1" | bc)" ]
then
	cp GAPinput.xyz GAPinput$i.xyz
fi

if [ 1 -eq "$(echo "${i} > 1" | bc)" ]
then
	echo "-----------------------------------------------------------------"
	echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
	echo "-----------------------------------------------------------------"
	echo "Adding configurations to the training dataset"
	echo "-----------------------------------------------------------------"
	echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
	echo "-----------------------------------------------------------------"
	python3.6 POSCARtoXYZ.py $((i-1))
	cat GAPinput$((i-1)).xyz xyz-temp > GAPinput$i.xyz
	rm xyz-temp
fi

echo "-----------------------------------------------------------------"
echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
echo "-----------------------------------------------------------------"
echo "Fitting GAP force field"
echo "-----------------------------------------------------------------"
echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
echo "-----------------------------------------------------------------"
rm GAP.xml*
gap_fit atoms_filename=GAPinput$i.xyz gp_file=GAP.xml gap={soap l_max=4 n_max=4 covariance_type=dot_product zeta=4 delta=0.2 cutoff=4 atom_sigma=0.5 n_sparse=200} default_sigma={0.002 0.1 0.1 0.0} e0={Li:-.29849279,P:-1.8869919,S:-.89046138,Cl:-.25791124}

quip E=T F=T atoms_filename=GAPinput$i.xyz param_filename=GAP.xml | grep AT | sed 's/AT//' > GAPoutput$i.xyz

version=$(grep gap_version GAP.xml | cut -d '=' -f 3 | cut -d '>' -f 1 | cut -d '"' -f 2)
xml=$(grep gap_version GAP.xml | cut -d '=' -f 2 | cut -d '"' -f 2)

sed "s/$version/1618098511/g" GAP.xml > gl
mv gl GAP.xml
cd ../lammps

# Convert to lammps input data format

python3.6 GAPtoLMP.py $i ${configs_per_iter}
cp lammpsdata lammpsdata$i
sed "s/Q/$xml/g" in.lmp.temp > in.lmp.temp2
sed "s/Z/$((configs_per_iter**$i*5))/g" in.lmp.temp2 > in.lmp.temp3
sed "s/Y/$i/g" in.lmp.temp3 > in.lmp
rm in.lmp.temp2 in.lmp.temp3

# Run lammps to explore configuration space

mpirun -np 64 lmp_intel_cpu_intelmpi < in.lmp > log.lammps
echo "-----------------------------------------------------------------"
echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
echo "-----------------------------------------------------------------"
echo "LAMMPS complete"
echo "-----------------------------------------------------------------"
echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
echo "-----------------------------------------------------------------"
cp log.lammps log.lammps$i
cp dump dump$i
python3.6 DUMPtoPOSCAR.py $i ${configs_per_iter}
mv POSCAR* ../vasp/
cd ../vasp/
mkdir $i
cd $i

# Run VASP on sampled configuations

for ((j=1;j<=configs_per_iter;j++))
do

mkdir $j
cp ../POTCAR $j
cp ../INCAR $j
cp ../KPOINTS $j
mv ../POSCAR$j $j
cd $j
cp POSCAR$j POSCAR
echo "-----------------------------------------------------------------"
echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
echo "-----------------------------------------------------------------"
echo "Starting VASP calculation"
echo "-----------------------------------------------------------------"
echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
echo "-----------------------------------------------------------------"
mpirun -np 64 /soft/vasp/vasp.5.4.4.pl2/bdw/vasp_std
cd ../

done
cd ../../

python3.6 accuracy.py $i ${configs_per_iter}
mae_e=$(grep "Iteration = ${i}" DFTvsGAPerror | cut -d '=' -f 4 | cut -d ' ' -f 2)
mae_f=$(grep "Iteration = ${i}" DFTvsGAPerror | cut -d '=' -f 6 | cut -d ' ' -f 2)
if [ 1 -eq "$(echo "${mae_e} > ${cut_e}" | bc)" ]
then
	echo "-----------------------------------------------------------------"
	echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
	echo "-----------------------------------------------------------------"
	echo "Energy MAE too high"
	echo "Need to increase training dataset"
	echo "-----------------------------------------------------------------"
	echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
	echo "-----------------------------------------------------------------"
fi
if [ 1 -eq "$(echo "${mae_f} > ${cut_f}" | bc)" ]
then
    echo "-----------------------------------------------------------------"
    echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
    echo "-----------------------------------------------------------------"
    echo "Force MAE too high"
    echo "Need to increase training dataset"
    echo "-----------------------------------------------------------------"
    echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
    echo "-----------------------------------------------------------------"
fi
if [ 1 -eq "$(echo "${mae_e} < ${cut_e}" | bc)" ] && [ 1 -eq "$(echo "${mae_f} < ${cut_f}" | bc)" ]
then
	echo "-----------------------------------------------------------------"
	echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
	echo "-----------------------------------------------------------------"
	echo "Energy MAE and Force MAE good enough"
	echo "-----------------------------------------------------------------"
	echo "*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*"
	echo "-----------------------------------------------------------------"
	echo "EXITING"
	exit 1
fi

done
