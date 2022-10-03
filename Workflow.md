#### Step 0.0: Generate 10 configuration snapshots from a small AIMD simulation with 100 steps
#### Step 0.1: Specifications:

Threshold value for energy comparison = $\epsilon$<sub>E</sub> eV/atom.

Threshold value for force comparison = $\epsilon$<sub>F</sub> eV/${\AA}$.

#### Step 1: Generate GAP force field using the configuration energies and forces

#### Step 2: Run classical MD simulations using the GAP force field to generate $n$ additional configurations (using LAMMS)

#### Step 3: Evaluate true values for the energies and interatomic forces using VASP.

#### Step 4: If MAE(E<sub>DFT</sub>, E<sub>GAP</sub>) $\leq$  ($\epsilon$<sub>E</sub>) and MAE(E<sub>DFT</sub>, E<sub>GAP</sub>) $\leq$  ($\epsilon$<sub>E</sub>), exit. Else, return to Step 1. 
