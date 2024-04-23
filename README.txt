This repository accompanies the manuscript "Bounding seed loss from isolated 
habitat patches" by Benjamin R. Hafner and Katherine Meyer.

seed_loss_monte_carlo.py houses the bulk of the code. It uses a Monte Carlo 
approach to compute the probability a seed is lost from a habitat (defined by a 
polygon) given a dispersal kernel (defined by a random sampling function). When 
run, the program computes the probability of seed loss for a population of 
Asclepias syriaca (common milkweed) in McKnight Prairie. It also generates 
visualizations of seed loss overlaid with an aerial photo (McKnight.png) to 
produce the images in Figure 6 (SYMMETRIC.png and ASYMMETRIC.png).

To help parameterize common milkweed's dispersal kernel, we made use of wind 
speed data collected at Cedar Creek Ecosystem Science Reserve (e080_Hourly 
climate data.txt, from https://cedarcreek.umn.edu/environmental-monitoring) 
which is processed by wind_reader.py. 

Finally, the programs scaling_computations.py and scaling_plots.py explore the
impact of habitat scale on seed loss probability and produce the plots in 
Figure 7 (plots.svg).

Contact: benrhafner@gmail.com
