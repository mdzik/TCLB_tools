
import numpy as np
import matplotlib.pyplot as plt
from Benchmarks.ADE.steady_two_layer_cylinder_analytical_2D import PipeWithinPipe

r0 = 0.1  # inner radius
r1 = 1  # interface between layers
r2 = 3  # outer radius

k1 = 1E5  # inner layer - heat conductivity for r0 < r < r1
k2 = 1E5  # outer layer - heat conductivity for r1 < r < r2

T0 = 10  # temperature for r = r0
T2 = 100  # temperature for r = r2


pwp = PipeWithinPipe(r0, r1, r2, k1, k2, T0, T2)
step = 0.01

r = np.arange(r0, r2, step)
y = np.array([pwp.get_temperature(r_) for r_ in r])


fig_name = f'pipe_within_pipe_k1{k1}_k2{k2}.png'


# -------------------- make dummy plot --------------------
plt.rcParams.update({'font.size': 14})
plt.figure(figsize=(14, 8))

axes = plt.gca()
plt.plot(r, y,
         color="black", marker="", markevery=1, markersize=15, linestyle="--", linewidth=2,
         label='analytical solution')

# ------ format y axis ------ #
yll = y.min()
yhl = y.max()
axes.set_ylim([yll, yhl])
# axes.set_yticks(np.linspace(yll, yhl, 5))
# axes.set_yticks(np.arange(yll, yhl, 1E-2))
# axes.set_yticks([1E-4, 1E-6, 1E-8, 1E-10, 1E-12])
# axes.yaxis.set_major_formatter(xfmt)

# plt.yscale('log')


# ------ format x axis ------ #
plt.xlim(r.min(), r.max())

# plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
# plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))  # scilimits=(-8, 8)


plt.title(f'Sample plot\n '
          # r'$x_{range}$' + f'={x_range}'
          f'; \t'
          r'$x_{step}$' + f'={step:.4f}')
plt.xlabel(r'$r$')
plt.ylabel(r'$Temperature$')
plt.legend()
plt.grid()

fig = plt.gcf()  # get current figure
fig.savefig(fig_name, bbox_inches='tight')
plt.show()

# plt.close(fig)  # close the figure


