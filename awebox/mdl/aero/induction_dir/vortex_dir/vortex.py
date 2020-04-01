#
#    This file is part of awebox.
#
#    awebox -- A modeling and optimization framework for multi-kite AWE systems.
#    Copyright (C) 2017-2019 Jochem De Schutter, Rachel Leuthold, Moritz Diehl,
#                            ALU Freiburg.
#    Copyright (C) 2018-2019 Thilo Bronnenmeyer, Kiteswarms Ltd.
#    Copyright (C) 2016      Elena Malz, Sebastien Gros, Chalmers UT.
#
#    awebox is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 3 of the License, or (at your option) any later version.
#
#    awebox is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with awebox; if not, write to the Free Software Foundation,
#    Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#
'''
vortex model of awebox aerodynamics
_python-3.5 / casadi-3.4.5
- author: rachel leuthold, alu-fr 2019
'''

import casadi.tools as cas

import awebox.mdl.aero.induction_dir.vortex_dir.convection as convection
import awebox.mdl.aero.induction_dir.vortex_dir.flow as flow


def get_trivial_residual(options, atmos, wind, variables, parameters, outputs, architecture):
    resi_convect = convection.get_convection_residual(options, wind, variables, architecture)
    resi_ind = flow.get_residuals(options, variables, wind, architecture)
    resi = cas.vertcat(resi_convect, resi_ind)

    return resi

def get_final_residual(options, atmos, wind, variables, parameters, outputs, architecture):
    # no self-induction! rigid wake convection only!
    resi = get_trivial_residual(options, atmos, wind, variables, parameters, outputs, architecture)
    return resi

def collect_vortex_outputs(model_options, atmos, wind, variables, outputs, parameters, architecture):

    if 'vortex' not in list(outputs.keys()):
        outputs['vortex'] = {}

    kite_nodes = architecture.kite_nodes
    for kite in kite_nodes:

        outputs['vortex']['u_ind_vortex' + str(kite)] = flow.get_induced_velocity_at_kite(model_options, variables, kite, architecture)
        outputs['vortex']['local_a' + str(kite)] = flow.get_induction_factor_at_kite(model_options, wind, variables, kite, architecture)
        outputs['vortex']['last_a' + str(kite)] = flow.get_last_induction_factor_at_kite(model_options, wind, variables, kite, architecture)

    return outputs

