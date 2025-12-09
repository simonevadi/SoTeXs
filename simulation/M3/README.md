# Simulations
In this folder the simulations to make sure that M3 is focusing on the exit slit. 
For all the simulations:

* reflectivity is 100%
* exporting the exit slit

The following simulations are included:
* *simulation_m3.py*: set the energy badwidth of the source to 0 and change the M3 radius of curvature to get smaller possible focus on the exit slit. -> results in sotexs_M§_radius.png, best radius is around 232 mm
* *simulation_cff.py*: for different values of the M3 radius, change the cff value and scan vs energy. Plot the results of trasmitted bandwidth and flux, plot are named *sotexs_cff_m3radius<radius>*.png -> confirm the previous results that the best radius is around 232 mm. However, it seems that cff=10 does not bring any advantage in terms of transmitted bandwidth.
* *simulation_cff_m1par.py*: similar to the previous round of simulations, but now M1 is focusing on the exit slits (horizontal focus). The situation for cff 10 now does not improve compared to cff5, but also does not make it worse. This is done just for curiosity. 