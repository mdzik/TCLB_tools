from sympy.matrices import eye

from SymbolicCollisions.core.cm_symbols import omega_ade

from SymbolicCollisions.core.cm_symbols import moments_dict
from SymbolicCollisions.core.printers import print_as_vector, get_print_symbols_in_m_notation, get_vector_of_eq_central_moments
from SymbolicCollisions.core.printers import print_sigma_sir
from SymbolicCollisions.core.MatrixGenerator import get_m_order_as_in_r, get_e_as_in_r, MatrixGenerator
from sympy.matrices import Matrix, diag
import numpy as np
import pandas as pd

from SymbolicCollisions.core.cm_symbols import Sigma2asSymbol, rho
from sympy import Symbol

# https://www.maa.org/press/periodicals/loci/joma/the-sir-model-for-spread-of-disease-the-differential-equation-model
### PRELIMINARIES ###
clip_z_dimension = True

m_seed = [0, 1, 2]
rmoments_order = get_m_order_as_in_r(m_seed, m_seed, m_seed)

e_seed = [0, 1, -1]
ex_D3Q27new, ey_D3Q27new, ez_D3Q27new, e_D3Q27new = get_e_as_in_r(e_seed, e_seed, e_seed)

if clip_z_dimension:
    rmoments_order = rmoments_order[0:9]
    q, d = rmoments_order.shape
    d = 2
    ex_D3Q27new = ex_D3Q27new[0:9]
    ey_D3Q27new = ey_D3Q27new[0:9]
    ez_D3Q27new = ez_D3Q27new[0:9]
    e_D3Q27new = e_D3Q27new[0:9, :]
else:
    q, d = rmoments_order.shape

moments_order = np.array(moments_dict[f'D{d}Q{q}'])

print(f"order of moments | rmoments: \n "
      f"{pd.concat([pd.DataFrame.from_records(moments_order),pd.DataFrame.from_records(rmoments_order)], axis=1)}")

print(f"lattice velocities - e: \n {np.array(e_D3Q27new)}")

### PREPARE ENVIROMENT ###
Relaxation_matrix = diag(1, omega_ade, omega_ade, 1, 1, 1, omega_ade, omega_ade, 1)

beta = Symbol('sir_beta', positive=True)
gamma = Symbol('sir_gamma', positive=True)

S = Symbol('S', positive=True)  # number
I = Symbol('I', positive=True)
R = Symbol('R', positive=True)

s = Symbol('s', positive=True)  # fraction
i = Symbol('i', positive=True)
r = Symbol('r', positive=True)

s_m_source = get_vector_of_eq_central_moments(-beta * s * i, Sigma2asSymbol)
i_m_source = get_vector_of_eq_central_moments(beta * s * i - gamma * i, Sigma2asSymbol)
r_m_source = get_vector_of_eq_central_moments(gamma * i, Sigma2asSymbol)

# ARRANGE STUFF
matrixGenerator = MatrixGenerator(ex_D3Q27new, ey_D3Q27new, ez_D3Q27new, moments_order)
Mraw = matrixGenerator.get_raw_moments_matrix()
Nraw = matrixGenerator.get_shift_matrix()

# from sympy import pprint
# pprint(Mraw)  # see what you have done
# pprint(Nraw)

temp_pop_str = 'temp'  # symbol defining populations

### GENERATE CODE ###
print(f"CudaDeviceFunction void relax_and_collide_SIR_M(real_t rho, real_t {omega_ade}) \n{{")
print("\t//=== THIS IS AUTOMATICALLY GENERATED CODE ===")

print_sigma_sir()

rtemp_populations = get_print_symbols_in_m_notation(rmoments_order, temp_pop_str)
temp_populations = get_print_symbols_in_m_notation(moments_order, temp_pop_str)

print(f"\treal_t {S} = {sum(get_print_symbols_in_m_notation(moments_order, s))};")
print(f"\treal_t {I} = {sum(get_print_symbols_in_m_notation(moments_order, i))};")
print(f"\treal_t {R} = {sum(get_print_symbols_in_m_notation(moments_order, r))};")

print(f"\treal_t {s} = {S/rho};")
print(f"\treal_t {i} = {I/rho};")
print(f"\treal_t {r} = {R/rho};")


for t in temp_populations:
    print(f"\treal_t {t};")

# for m_eq, source, pop_in_str in zip([s_m_eq, i_m_eq, r_m_eq], [s_m_source, i_m_source, r_m_source], ['s', 'i', 'r']):
for source, pop_in_str in zip([s_m_source, i_m_source, r_m_source], ['s', 'i', 'r']):
    print(f"\t //--- processing {pop_in_str} ---")

    m_eq = get_vector_of_eq_central_moments(Symbol(pop_in_str.upper(), positive=True), Sigma2asSymbol)
    populations = get_print_symbols_in_m_notation(moments_order, pop_in_str)
    collided_populations_str = pop_in_str + "_star_"
    collided_populations = get_print_symbols_in_m_notation(moments_order, collided_populations_str)

    for t, p in zip(temp_populations, populations):
        print(f"\t{t} = {p};")

    print("\n\t//raw moments from density-probability functions")

    print_as_vector(Mraw * rtemp_populations, outprint_symbol=pop_in_str, output_order_of_moments=moments_order)

    print("\n\t//collide")
    # Relax 1,3,5 moments for ADE, SOI without force
    m_after_collision = (eye(q) - Relaxation_matrix) * populations + Relaxation_matrix * m_eq + source
    print_as_vector(m_after_collision, outprint_symbol="real_t " + collided_populations_str, output_order_of_moments=moments_order)

    print("\n\t//back to density-probability functions")
    print_as_vector(Mraw.inv() * collided_populations, outprint_symbol=pop_in_str, output_order_of_moments=rmoments_order)
    print("\n\n")

print("}\n")
