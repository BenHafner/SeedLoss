'''
This program makes plots of the data produced by scalling_computations.py
'''

import numpy as np
import matplotlib.pyplot as plt

# copied from output of scaling_computations.py (with n = 10**7):
scale      =     np.array([0.03125, 0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16, 32])
h_over_l   =     np.array([2.2182530804482767, 4.4365061608965535, 8.873012321793107, 17.746024643586214, 35.49204928717243, 70.98409857434486, 141.9681971486897, 283.9363942973794, 567.8727885947588, 1135.7455771895177, 2271.4911543790354])
p_sym      = 100*np.array([0.5673157, 0.420066, 0.2927652, 0.1913927, 0.117206, 0.0668523, 0.0358667, 0.0184645, 0.0093023, 0.0046493, 0.0023376])
p_N        = 100*np.array([0.6277089, 0.4733638, 0.3350304, 0.2226012, 0.1387787, 0.0804096, 0.0434225, 0.0223067, 0.0113031, 0.005653, 0.002812])
p_W        = 100*np.array([0.4785456, 0.3435267, 0.2320897, 0.1470505, 0.0874576, 0.0488124, 0.0257874, 0.0131865, 0.0066644, 0.0033332, 0.0016746])
p_SE       = 100*np.array([0.5835402, 0.433953, 0.3031891, 0.1989517, 0.1222777, 0.0701516, 0.0376369, 0.0193562, 0.0097261, 0.0049004, 0.0024762])
bound_sym  = 100*np.array([2.4002317628324454, 1.2001158814162227, 0.6000579407081114, 0.3000289703540557, 0.15001448517702784, 0.07500724258851392, 0.03750362129425696, 0.01875181064712848, 0.00937590532356424, 0.00468795266178212, 0.00234397633089106])
bound_asym = 100*np.array([3.770275236513645, 1.8851376182568225, 0.9425688091284112, 0.4712844045642056, 0.2356422022821028, 0.1178211011410514, 0.0589105505705257, 0.02945527528526285, 0.014727637642631426, 0.007363818821315713, 0.0036819094106578564])

# pull out red points:
h_over_l_red = [h_over_l[5]]
p_sym_red    = [p_sym[5]]
p_N_red      = [p_N[5]]
# cover tracks:
p_sym[5] = 0
p_N[5] = 0

# initialize plots:
fig, ax = plt.subplots(1, 2, figsize=[8,4], sharey=True, sharex=True)

# plot bounds:
ax[0].plot(h_over_l, bound_sym, '--', color='black')
ax[1].plot(h_over_l, bound_sym, '--', color='black')
ax[0].plot(h_over_l, bound_asym, '-', color='black')
ax[1].plot(h_over_l, bound_asym, '-', color='black')

# custom markers:
from matplotlib.path import Path
circle = Path.circle(radius=0.4)
codes = [Path.MOVETO, Path.LINETO]
verts = [(0,1), (0,0.4)]
arrow_N = Path(verts, codes)
arrow_N = Path.make_compound_path(arrow_N, circle)

from matplotlib.transforms import Affine2D
arrow_W  = arrow_N.transformed(Affine2D().rotate(np.pi/2))
arrow_SE = arrow_N.transformed(Affine2D().rotate(-3*np.pi/4))

#plot black points:
ax[0].plot(h_over_l, p_sym, marker=circle, markersize=7,
           color='black', markeredgewidth=1.5, markerfacecolor='none',
           linestyle='none', label='Symmetric dispersal')
ax[1].plot(h_over_l, p_N, marker=arrow_N, color='black',
           markersize=16, markeredgewidth=1.5, markerfacecolor='none',
           linestyle='none', zorder=3, label='North bias')
ax[1].plot(h_over_l, p_SE, marker=arrow_SE, color=(0.5,0.5,0.5),
           markersize=11, markeredgewidth=1.5, markerfacecolor='none',
           linestyle='none', zorder=2, label='South-east bias')
ax[1].plot(h_over_l, p_W, marker=arrow_W, color=(0.75,0.75,0.75),
           markersize=16, markeredgewidth=1.5, markerfacecolor='none',
           linestyle='none', zorder=1, label='West bias')

# plot red points:
ax[0].plot(h_over_l_red, p_sym_red, linestyle='none', marker=circle, color='red',
           markersize=7, markerfacecolor='none', markeredgewidth=1.5)
ax[1].plot(h_over_l_red, p_N_red, linestyle='none', marker=arrow_N, color='red',
           markersize=16, markerfacecolor='none', markeredgewidth=1.5)

# set up plots:
ax[0].set_aspect('equal')
ax[1].set_aspect('equal')
ax[0].set_xscale('log')
ax[0].set_yscale('log')
ax[0].set_xlabel('A/L [m]')
ax[1].set_xlabel('A/L [m]')
ax[0].set_ylabel('Seed loss probability [%]')
ax[0].set_xlim(3.1, 1800)
ax[0].set_ylim(0.25, 100)
from matplotlib.ticker import StrMethodFormatter
ax[0].xaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
ax[0].yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
ax[0].legend(loc='lower left', frameon=False)
ax[1].legend(loc='lower left', frameon=False)

plt.savefig('plots.svg')
plt.show()
