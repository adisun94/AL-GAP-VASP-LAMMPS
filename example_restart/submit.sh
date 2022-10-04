#!/bin/bash

#SBATCH --job-name=LPSC
#SBATCH --account=MVCATHODE
#SBATCH --partition=knlall
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=64
#SBATCH --mail-user=asundar@anl.gov>     # Optional if you require email
#SBATCH --mail-type=ALL                  # Optional if you require email
#SBATCH --time=5:00:00

# Setup My Environment
module purge
module add StdEnv
module add gcc/9.2.0-pkmzczt
module add intel-parallel-studio/cluster.2019.5-zqvneip
export PATH=/soft/vasp/5.4.4.pl2/bdw:$PATH

ulimit -s unlimited

mpirun -np $SLURM_NTASKS vasp_std
