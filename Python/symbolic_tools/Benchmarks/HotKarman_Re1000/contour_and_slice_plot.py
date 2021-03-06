import matplotlib.pylab as pylab
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.pyplot as plt
import os
import numpy as np
from DataIO.helpers import find_oldest_iteration, get_vti_from_iteration, strip_folder_name, eat_dots_for_texmaker, get_r_from_xy


def Nu_phi_plot(values, phi_deg, title='', file_name=''):

    params = {'legend.fontsize': 'xx-large',
              'figure.figsize': (14, 8),
              'axes.labelsize': 'xx-large',
              'axes.titlesize': 'xx-large',
              'xtick.labelsize': 'xx-large',
              'ytick.labelsize': 'xx-large'}
    pylab.rcParams.update(params)

    # -------------------- make dummy plot --------------------
    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=(14, 8))

    axes = plt.gca()

    plt.plot(phi_deg, values,
             color="black", marker=".", markevery=1, markersize=7, linestyle="", linewidth=2,
             # label=r'$numerical \, solution$'
             )

    plt.title(title)

    plt.xlabel(r'$\phi$')
    # plt.ylabel(r'$T$')
    plt.legend()
    plt.grid()

    fig = plt.gcf()  # get current figure
    if not os.path.exists('plots'):
        os.makedirs('plots')

    fig_name = f'plots/Circumferential_interpolation_{file_name}.png'
    fig.savefig(fig_name, bbox_inches='tight')
    plt.show()
    plt.close()


def cntr_plot(anal_field, num_field, xx, yy, title='dummy_tittle', extra_points=None):
    print("---------- PLOTTING -------------")
    fig = plt.figure(figsize=(12, 8))
    # ax = fig.gca(projection='3d')
    ax = fig.gca()
    # alpha=1, rstride=1, cstride=1)
    # ax.plot_surface(xx, yy, T_err_field, cmap='winter', linewidth=0.5, antialiased=True, zorder=0.5, label='T_err_field')
    # ax.plot_surface(xx, yy, T_num_slice,  cmap='summer', linewidth=0.5, antialiased=True, zorder=0.25, label='T_num')
    # ax.plot_surface(xx, yy, T_anal,  cmap='autumn', linewidth=0.5, antialiased=True, zorder=0.1, label='T_anal')
    # ax.contourf(xx, yy, T_num_slice,  cmap='summer', linewidth=0.5, antialiased=True, label='T_num')

    cntr = ax.pcolormesh(xx, yy, num_field, cmap='coolwarm', label='T_nu,', vmin=10, vmax=11)  # this one has smooth colors
    # cntr = ax.pcolormesh(xx, yy, num_field - anal_field, cmap='coolwarm', label='T_err')  # this one has smooth colors
    # cntr = ax.contourf(xx, yy, T_num_slice, cmap='coolwarm', antialiased=True)  # this one is has step colors
    plt.plot(extra_points[0, :], extra_points[1, :],  color="black", marker="x", markevery=1, markersize=7, linestyle="", linewidth=2, label=r'interpolation points')
    # plt.plot(phi_deg, Tr,
    #          color="black", marker="x", markevery=1, markersize=7, linestyle="", linewidth=2,
    #          # label=r'$numerical \, solution$'
    #          )

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    ax.set_aspect('equal')

    # Customize the z axis.
    # ax.set_zlim(-.1, 1.05)
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # ax.zaxis.set_major_formatter(FormatStrFormatter('%.1e'))

    # Add a color bar which maps values to colors.

    fig.colorbar(cntr, shrink=0.5, aspect=5)

    plt.title(f'T field: {title}')

    nx = xx.shape[1]
    ny = xx.shape[0]
    # # Major ticks every 20, minor ticks every 5
    major_x_ticks = np.arange(0, nx, nx/5)
    major_y_ticks = np.arange(0, ny, ny/5)
    minor_x_ticks = np.arange(0, nx, 1)
    minor_y_ticks = np.arange(0, ny, 1)
    #
    ax.set_xticks(major_x_ticks)
    # ax.set_xticks(minor_x_ticks, minor=True)

    ax.set_yticks(major_y_ticks)
    # ax.set_yticks(minor_y_ticks, minor=True)
    #
    # # And a corresponding grid
    ax.grid(which='both')
    #
    # # Or if you want different settings for the grids:
    # ax.grid(which='minor', alpha=0.2)
    # ax.grid(which='major', alpha=0.5)
    # plt.grid(True)  # or use default grid

    # fake2Dline = mpl.lines.Line2D([0], [0], linestyle="none", c='b', marker='o')
    # ax.legend([fake2Dline], [r'$Err_{T} = T_{anal} - T_{num}$'], numpoints=1)

    if not os.path.exists('plots'):
        os.makedirs('plots')
    fig_name = f'plots/cntr_{title}.png'

    fig.savefig(fig_name, bbox_inches='tight')
    plt.show()
    plt.close(fig)  # close the figure
    # print('bye')


def slice_plot(anal_field, num_field, y, title='dummy_title'):

        params = {'legend.fontsize': 'xx-large',
                  'figure.figsize': (14, 8),
                  'axes.labelsize': 'xx-large',
                  'axes.titlesize': 'xx-large',
                  'xtick.labelsize': 'xx-large',
                  'ytick.labelsize': 'xx-large'}
        pylab.rcParams.update(params)

        # -------------------- make dummy plot --------------------
        plt.rcParams.update({'font.size': 14})
        plt.figure(figsize=(14, 8))

        axes = plt.gca()

        plt.plot(anal_field, y,
                 color="black", marker="o", markevery=1, markersize=5, linestyle=":", linewidth=2,
                 label=r'$analytical \, solution$')

        # plt.plot(u_anal, y_anal + len(y_grid) / 2,
        #          color="black", marker="o", markevery=1, markersize=5, linestyle=":", linewidth=2,
        #          label=r'$analytical \, solution$')

        # plt.plot(u_fd, y_fd + len(y_grid) / 2,
        #          color="black", marker="", markevery=1, markersize=5, linestyle="-", linewidth=2,
        #          label=r'$FD \, solution$')

        plt.plot(num_field, y,
                 color="black", marker="x", markevery=1, markersize=7, linestyle="", linewidth=2,
                 label=r'$numerical \, solution$')
        #
        # plt.plot(U_bb_num_x_slice, y_grid,
        #          color="black", marker="v", markevery=1, markersize=6, linestyle="", linewidth=2,
        #          label=r'$LBM \, BB$')
        #
        # # ------ format y axis ------ #
        # yll = y_grid.min()
        # yhl = y_grid.max()

        # axes.set_ylim([0, 2. + effdiam / 2.])

        # axes.set_yticks(np.linspace(yll, yhl, 8))
        # axes.set_yticks(np.arange(yll, yhl, 1E-2))
        # axes.set_yticks([1E-4, 1E-6, 1E-8, 1E-10, 1E-12])
        # axes.set_yticks([0.5, 1.5, 2.5, 31.5, 32, 32.5, 61.5, 62.5, 63.5])
        # axes.yaxis.set_major_formatter(xfmt)

        # plt.yscale('log')
        # ------ format x axis ------ #
        # plt.xlim(0, 0.011)
        # plt.xlim(int(xSIZE / 2), xSIZE)

        # plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        # plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))  # scilimits=(-8, 8)

        # title = f'IBB Poiseuille flow:\n' + r'$ \nu = $' + f'{kin_visc:.2e} ' + r'$D_{eff}=$' + f'{effdiam:.2e}'
        # title = ''  # skip title for .tex
        plt.title(title)

        plt.xlabel(r'$T$')
        plt.ylabel(r'$h$')
        plt.legend()
        plt.grid()

        fig = plt.gcf()  # get current figure
        if not os.path.exists('plots'):
            os.makedirs('plots')

        fig_name = f'plots/slice_{title}.png'
        fig.savefig(fig_name, bbox_inches='tight')
        plt.show()

        # plt.close(fig)  # close the figure
