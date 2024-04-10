import seed_loss_monte_carlo as slmc
import numpy as np

'''
This program builds on seed_loss_monte_carlo.py to compute seed loss
probability for scaled-up or scaled-down versions of McKnight prairie,
and also tries three different wind directions: North, West, and South-East.
'''

h = slmc.h # polygonal habitat in the shape of McKnight Prairie
u = slmc.u # mu, mean dispersal distance for Wald distribution (meters)
l = slmc.l # lambda, shape parameter for Wald distribution (meters)

scale = [1/32, 1/16, 1/8, 1/4, 1/2, 1, 2, 4, 8, 16, 32]

n = 10**7

def compute_p(h, dispersal='sym'):
    bias_direction = {'sym': (0, 0),
                      'N'  : (np.sqrt(10), np.pi/2),
                      'W'  : (np.sqrt(10), 0),
                      'SE' : (np.sqrt(10), -3*np.pi/4)}
    def d():
        return slmc.wald_2D(u, l, *bias_direction[dispersal])

    return slmc.monte_carlo(h, d, n)

# quantities to report in results:
h_over_l = []
p_sym = []
p_N = []
p_W = []
p_SE = []
bound_sym = []
bound_asym = []

for s in scale:
    h_s = slmc.Polygon(h.verts*s)  # scaled version of habitat
    c = h_s.area()/h_s.perimeter() # area to perimiter ratio
    
    h_over_l.append(c)
    bound_sym .append(u/c/np.pi)
    bound_asym.append(u/c/2)
    p_sym.append(compute_p(h_s, 'sym'))
    p_N  .append(compute_p(h_s, 'N'))
    p_W  .append(compute_p(h_s, 'W'))
    p_SE .append(compute_p(h_s, 'SE'))

# print results (with probabilities multiplied by 100 to convert to %)
print(f'scale      =     np.array({scale})')
print(f'h_over_l   =     np.array({h_over_l})')
print(f'p_sym      = 100*np.array({p_sym})')
print(f'p_N        = 100*np.array({p_N})')
print(f'p_W        = 100*np.array({p_W})')
print(f'p_SE       = 100*np.array({p_SE})')
print(f'bound_sym  = 100*np.array({bound_sym})')
print(f'bound_asym = 100*np.array({bound_asym})')
# results are printed in this format to be easily copied into scaling_plots.py
