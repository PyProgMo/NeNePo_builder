# NeNePo_builder

What is NeNePo? 

NeNePo stands for Negative, Neutral, Positive:
1. an ensemble of negative charged Ions (anions) is ionized once to neutral, 
(usually via a ultra fast fs laser pulse to create a approximately vertical ionisation in the anionic geometry) 
2. The ionisation creates a wave packet, that can evolve especially in small molecules over the 3N-5 vibration modes
3. A second delayed vertical ionization happens with a second laser pulse again (approximately vertical on the fs timescale) and a positive species (cations) is created. 
4. The NeNePo Signal describes the amount of cation over time. The dominant frequency should reveal the most relevant molecular frequency (stfft or kaiser transformation can reveal shifts in the domonant frequency)

Important note, the dynamics computation requires imports and uses the velocityverlet packet that runs the dynamics on the cluster what this not 

Needs the optimized anionic files. builds complete input Dynamic input for "on the fly" dynamic to get the NeNePo spectrum. 



