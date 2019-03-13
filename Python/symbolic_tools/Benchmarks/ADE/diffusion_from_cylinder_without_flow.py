#  See chapter 8.6.2, eq 8.67, p324 from
# 'The Lattice Boltzmann Method: Principles and Practice'
#  by T.Krüger, H.Kusumaatmaja, A.Kuzmin, O.Shardt, G.Silva, E.M.Viggen
# which origins from section 2.1 p334 from
# 'Hydrodynamics, Mass and Meat Transfer in Chemical Engineering'
# A.D. Polyanin, A.M. Kutepov, A.V. Vyazmin and D.A. Kazenin


import matplotlib.pyplot as plt
import numpy as np
import os
import numpy as np
import scipy.special as special
# import scipy.special.j0 as J0
# import scipy.special.j1 as J1


# initial concentration = 0
cc = 1  # concentration at the boundary
a = 40  # [lu] radius of the cylinder
D = 0.0052  # [lu2/ts] diffusivity


n_bessel_roots = 5
# [2.4048, 5.5201, 8.6537, 11.7915, 14.9309] # first five roots of the zeroth order Bessel function
# as n --> inf the difference between subsequent roots is pi.
bessel_roots = special.jn_zeros(0, n_bessel_roots)


def concentration(r, t):
    temp = 0

    for i in range(n_bessel_roots):
        temp += 2.*special.j0(bessel_roots[i] * r / a)  \
                * np.exp(-bessel_roots[i] * bessel_roots[i] * D * t / (a * a)) \
                / (bessel_roots[i] * special.j1(bessel_roots[i]))

    # for i in range(n_bessel_roots):
    #     temp += 2. * special.spherical_jn(0, bessel_roots[i] * r / a) \
    #             * np.exp(-bessel_roots[i] * bessel_roots[i] * D * t / (a * a))\
    #             / (bessel_roots[i] * special.spherical_jn(1, bessel_roots[i]))

    result = cc*(1-temp)
    return result


time = 0.1095
x = np.linspace(0, a, 40)
y = [concentration(i, time/(a*a)) for i in x]

# make plot
plt.rcParams.update({'font.size': 18})
plt.figure(figsize=(14, 9))

plt.plot(x/a, y, color="black", linestyle=":",  linewidth=3, label=f'analytical solution t={time}')

time = 0.0547
x = np.linspace(0, a, 100)
y = [concentration(i, time/(a*a)) for i in x]
plt.plot(x/a, y, color="black", marker=">", markersize=9, linestyle="", label=f'analytical solution t={time}')
#
# plt.plot(u_fd, y_fd, color="black", linestyle="-",  linewidth=2, label='FD - diffuse interface')
# plt.plot(u_diff, (x_diff - len(x_diff)/2 + 0.5), color="black", marker="o", markersize=9, linestyle="", label='current model - diffuse interface')

axes = plt.gca()
# axes.set_yticks(np.arange(-50, 51, 25))
# axes.set_ylim([-50, 50])
#
# plt.xlim(0, 0.12)
# axes.set_xticks(np.arange(0., 0.12, 0.02))
#     plt.ylim(y1.min(), y1.max())
#     plt.ylim(1.25*min(y1.min(), y2.min()), 1.25*max(y1.max(), y2.max()))


plt.ylabel(r'$C/C_c$')
plt.xlabel(r'$r/a$')

# plt.title('two phase Poiseuille flow')
plt.grid(True)
plt.legend()


# plt.text(0.0, 5E-6, r'$\mu^* = %s$' % str(mu_ratio))
# plt.text(0.0, 5E-6, r'$\rho^* = %s$' % str(rho_l/rho_g))
fig = plt.gcf()  # get current figure
fig.savefig(f'test.pdf', bbox_inches='tight')
plt.show()
