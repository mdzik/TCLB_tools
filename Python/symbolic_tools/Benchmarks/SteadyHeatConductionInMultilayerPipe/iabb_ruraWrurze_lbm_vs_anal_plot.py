

from DataIO.helpers import find_oldest_iteration, get_vti_from_iteration, strip_folder_name, eat_dots_for_texmaker, get_r_from_xy
from DataIO.helpers import calc_L2, calc_mse
import pwd
from Benchmarks.PoiseuilleFlow.pipe_poiseuille_plots import cntr_plot, slice_plot
from Benchmarks.SteadyHeatConductionInMultilayerPipe.contour_and_slice_plot import cntr_plot
from Benchmarks.SteadyHeatConductionInMultilayerPipe.steady_two_layer_cylinder_analytical_2D import PipeWithinPipeDirichlet
from DataIO.VTIFile import VTIFile
import os
import pwd
import numpy as np

# eff_pipe_diam = np.array([30, 46, 66, 94, 118])
# eff_cyl_diam = np.array([15, 23, 33, 47, 59])

# eff_pipe_diam = 118
# eff_cyl_diam = 59

eff_pipe_diam = 66
eff_cyl_diam = 33
conductivity = 0.1
kin_visc = 0.1

solver = 'walberla'  # 'TCLB' or 'walberla

wd = os.getcwd()
wd = os.path.dirname(wd)  # go level up
home = pwd.getpwuid(os.getuid()).pw_dir

if solver == 'walberla':
    main_folder = os.path.join(home, 'DATA_FOR_PLOTS', 'walberla_IABB_ruraWrurze')
    # case_folder = os.path.join('vtk_test', 'thermal_field')
    # case_folder = os.path.join('vtk_test_old', 'thermal_field')
    case_folder = os.path.join(f'vtk_eff_pipe_diam_{eff_pipe_diam}', 'thermal_field')
elif solver == 'TCLB':
    main_folder = os.path.join(home, 'DATA_FOR_PLOTS', 'batch_IABB_ruraWrurze')
    case_folder = f'abb_ruraWrurze_Dirichlet_Cumulants_k_{conductivity}_nu_{kin_visc}_effdiam_{eff_pipe_diam}'
else:
    raise Exception("Choose solver [\'TCLB\' or \'walberla\'] ")


def read_data_from_lbm(_case_folder):
    if solver == 'walberla':
        oldest = find_oldest_iteration(_case_folder, extension='.vti')
        filename_vtk = get_vti_from_iteration(_case_folder, oldest, extension='.vti', prefix='simulation_step_')  # walberla
        filepath_vtk = os.path.join(_case_folder, filename_vtk)
        vti_reader = VTIFile(filepath_vtk, parallel=False)  # walberla
    elif solver == 'TCLB':
        oldest = find_oldest_iteration(_case_folder)  # TCLB
        filename_vtk = get_vti_from_iteration(_case_folder, oldest, extension='.pvti') # TCLB
        filepath_vtk = os.path.join(_case_folder, filename_vtk)
        vti_reader = VTIFile(filepath_vtk, parallel=True)  # TCLB
    else:
        raise Exception("Choose solver [\'TCLB\' or \'walberla\'] ")

    T_num = vti_reader.get("T")
    T_num_slice = T_num[:, :, 1]

    # [ux_num, uy_num, uz_num] = vti_reader.get("U", is_vector=True)
    # ny, nx, nz = T_num.shape
    # uz_num_slice = uz_num[:, :, 1]
    # y = np.linspace(start=0, stop=1, num=ny, endpoint=False)
    return T_num_slice


T_num_slice = read_data_from_lbm(os.path.join(main_folder, case_folder))
ny, nx = T_num_slice.shape

# -------- anal solution ---------------

x0 = 64  # center of the cylinder/pipe
y0 = 64  # center of the cylinder/pipe

r0 = eff_cyl_diam/2.  # inner radius
r2 = eff_pipe_diam/2.  # outer radius
r1 = (r0 + r2)/2.  # interface between layers

pwp = PipeWithinPipeDirichlet(r0, r1, r2, conductivity, conductivity, T0=11, T2=10)

x_grid = np.linspace(0, nx, nx, endpoint=False) + 0.5
y_grid = np.linspace(0, ny, ny, endpoint=False) + 0.5
xx, yy = np.meshgrid(x_grid, y_grid)

T_anal = np.zeros((ny, nx))
r_anal = np.zeros((ny, nx))

# cuttoff_r2 = eff_pipe_diam / 2. - 1
# cuttoff_r0 = eff_cyl_diam / 2. + 1

cuttoff_r2 = eff_pipe_diam / 2. - 1
cuttoff_r0 = eff_cyl_diam / 2. + 1

for i in range(ny):
    for j in range(nx):
        r = get_r_from_xy(xx[i][j], yy[i][j], x0, y0)
        r_anal[i, j] = r
        T_anal[i, j] = pwp.get_temperature_r(r)
        if r < cuttoff_r0 or r > cuttoff_r2:
            T_anal[i, j] = np.nan


not_nan_mask = ~np.isnan(T_anal)
T_anal_masked = T_anal[not_nan_mask]
T_num_slice_masked = T_num_slice[not_nan_mask]
r_anal_masked = r_anal[not_nan_mask]

T_mse = calc_mse(T_anal_masked, T_num_slice_masked)
T_L2 = calc_L2(T_anal_masked, T_num_slice_masked)

# print(f"T_mse={T_mse[g]:.2e} for grid {xSIZE} x {xSIZE} [lu]")
# print(f"T_L2={T_L2[g]:.2e} for grid {xSIZE} x {xSIZE} [lu]")

cntr_plot(T_anal, T_num_slice, xx, yy, conductivity, eff_pipe_diam)
# # 2D clip
# r_anal = r_anal[:, 63]
# u_anal = u_anal[:, 63]
# uz_num_slice = uz_num_slice[:, int(nx / 2)]
# slice_plot(u_anal, uz_num_slice, kin_visc, effdiam, r_anal)

print('bye')
