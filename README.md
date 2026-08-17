# NeNePo_builder

What is NeNePo? 

NeNePo stands for Negative, Neutral, Positive:
1. an ensemble of negative charged Ions (anions) is ionized once to neutral, 
(usually via a ultra fast fs laser pulse to create a approximately vertical ionisation in the anionic geometry) 
2. The ionisation creates a wave packet, that can evolve especially in small molecules over the 3N-5 vibration modes
3. A second delayed vertical ionization happens with a second laser pulse again (approximately vertical on the fs timescale) and a positive species (cations) is created. 
4. The NeNePo Signal describes the amount of cation over time. The dominant frequency should reveal the most relevant molecular frequency (stfft or kaiser transformation can reveal shifts in the domonant frequency)

Important note, the dynamics computation requires imports and uses the velocityverlet packet that runs the dynamics on the cluster

Needs the optimized anionic files. builds complete input Dynamic input for "on the fly" dynamic to get the NeNePo spectrum. 

For the dynamics to run, the locally generated dynamics folder must be copied onto a node of the cluster which has slurm running (otherwise the submission script must be updated to fit the cluster protocol) and the submission script must be run to submit the N trajectory propagation jobs to the cluster. One important note is, that the python that starts the propagation (in first ionized and 2nd ionized state) is run_dynamic.py which must be able to access the relevant scripts from the provided site-packages folder. 
The intention is, to put the required folders into the site-packages folder of the python installation on the cluster. If not possible, try to put them into the same path as run_dynamics.py (but this was never tested). 

Since the Dynamics Algorithm (Velocity Verlet) is also shipped within the project, it can be further developed and improved if any changes are required. 


