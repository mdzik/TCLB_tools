const real_t vC = dst->get(x, y, z, Stencil_T::idx[C]);
const real_t vN = dst->get(x, y, z, Stencil_T::idx[N]);
const real_t vS = dst->get(x, y, z, Stencil_T::idx[S]);
const real_t vW = dst->get(x, y, z, Stencil_T::idx[W]);
const real_t vE = dst->get(x, y, z, Stencil_T::idx[E]);
const real_t vT = dst->get(x, y, z, Stencil_T::idx[T]);
const real_t vB = dst->get(x, y, z, Stencil_T::idx[B]);
const real_t vNW = dst->get(x, y, z, Stencil_T::idx[NW]);
const real_t vNE = dst->get(x, y, z, Stencil_T::idx[NE]);
const real_t vSW = dst->get(x, y, z, Stencil_T::idx[SW]);
const real_t vSE = dst->get(x, y, z, Stencil_T::idx[SE]);
const real_t vTN = dst->get(x, y, z, Stencil_T::idx[TN]);
const real_t vTS = dst->get(x, y, z, Stencil_T::idx[TS]);
const real_t vTW = dst->get(x, y, z, Stencil_T::idx[TW]);
const real_t vTE = dst->get(x, y, z, Stencil_T::idx[TE]);
const real_t vBN = dst->get(x, y, z, Stencil_T::idx[BN]);
const real_t vBS = dst->get(x, y, z, Stencil_T::idx[BS]);
const real_t vBW = dst->get(x, y, z, Stencil_T::idx[BW]);
const real_t vBE = dst->get(x, y, z, Stencil_T::idx[BE]);
const real_t vTNE = dst->get(x, y, z, Stencil_T::idx[TNE]);
const real_t vTNW = dst->get(x, y, z, Stencil_T::idx[TNW]);
const real_t vTSE = dst->get(x, y, z, Stencil_T::idx[TSE]);
const real_t vTSW = dst->get(x, y, z, Stencil_T::idx[TSW]);
const real_t vBNE = dst->get(x, y, z, Stencil_T::idx[BNE]);
const real_t vBNW = dst->get(x, y, z, Stencil_T::idx[BNW]);
const real_t vBSE = dst->get(x, y, z, Stencil_T::idx[BSE]);
const real_t vBSW = dst->get(x, y, z, Stencil_T::idx[BSW]);