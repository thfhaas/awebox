#
#    This file is part of awebox.
#
#    awebox -- A modeling and optimization framework for multi-kite AWE systems.
#    Copyright (C) 2017-2021 Jochem De Schutter, Rachel Leuthold, Moritz Diehl,
#                            ALU Freiburg.
#    Copyright (C) 2018-2020 Thilo Bronnenmeyer, Kiteswarms Ltd.
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
constraints to create "intermediate condition" fixing constraints on the positions of the wake nodes,
to be referenced/used from ocp.constraints
_python-3.5 / casadi-3.4.5
- author: rachel leuthold, alu-fr 2020-21
'''

# ################# define the actual constraint
#
# def get_constraint(nlp_options, V, Outputs, model, time_grids):
#
#     cstr_list = cstr_op.ConstraintList()
#
#     if vortex_tools.vortices_are_modelled(nlp_options):
#
#         vortex_representation = nlp_options['induction']['vortex_representation']
#         if vortex_representation == 'state':
#             cstr_list.append(get_state_repr_fixing_constraint(nlp_options, V, Outputs, model))
#
#             vortex_far_wake_model = nlp_options['induction']['vortex_far_wake_model']
#             if vortex_far_wake_model == 'pathwise_filament':
#                 cstr_list.append(get_farwake_convection_velocity_constraint(nlp_options, V, model))
#
#             if 'cylinder' in vortex_far_wake_model:
#                 cstr_list.append(get_vortex_cylinder_center_constraint(nlp_options, V, Outputs, model))
#                 cstr_list.append(get_vortex_cylinder_pitch_constraint(nlp_options, V, Outputs, model))
#
#         elif vortex_representation == 'alg':
#             cstr_list.append(alg_fixing.get_constraint(nlp_options, V, Outputs, model, time_grids))
#
#         else:
#             message = 'specified vortex representation ' + vortex_representation + ' is not allowed'
#             awelogger.logger.error(message)
#             raise Exception(message)
#
#     return cstr_list
#
# ############# state representation
#
# def get_state_repr_fixing_constraint(options, V, Outputs, model):
#
#     n_k = options['n_k']
#
#     wake_nodes = options['induction']['vortex_wake_nodes']
#     kite_nodes = model.architecture.kite_nodes
#     wingtips = ['ext', 'int']
#
#     cstr_list = cstr_op.ConstraintList()
#
#     for kite in kite_nodes:
#         for tip in wingtips:
#             for wake_node in range(wake_nodes):
#                 local_name = 'wake_fixing_' + str(kite) + '_' + str(tip) + '_' + str(wake_node)
#
#                 if wake_node < n_k:
#
#                     # working out:
#                     # n_k = 3
#                     # wn:0 fixed at shooting node 3, corresponds to ndx=2, ddx=-1
#                     # wn:1 fixed at shooting node 2, corresponds to ndx=1, ddx=-1
#                     # wn:2 fixed at shooting node 1, corresponds to ndx=0, ddx=-1
#                     # wn   fixed at shooting node n_k - wn, corresponds to ndx=n_k - wn - 1, ddx=-1
#                     # ... then, switch to periodic fixing
#
#                     shooting_ndx = n_k - wake_node
#                     collocation_ndx = shooting_ndx - 1
#
#                     var_name = 'wx_' + str(kite) + '_' + str(tip) + '_' + str(wake_node)
#                     wx_scaled = V['xd', shooting_ndx, var_name]
#                     wx_si = struct_op.var_scaled_to_si('xd', var_name, wx_scaled, model.scaling)
#
#                     wingtip_pos_si = Outputs['coll_outputs', collocation_ndx, -1, 'aerodynamics', 'wingtip_' + tip + str(kite)]
#
#                     local_resi_si = wx_si - wingtip_pos_si
#                     local_resi = struct_op.var_si_to_scaled('xd', var_name, local_resi_si, model.scaling)
#
#                 else:
#
#                     # working out for n_k = 3
#                     # wn:0, n_k-1=2
#                     # wn:1, n_k-2=1
#                     # wn:2=n_k-1, n_k-3=0
#                     # ... switch to periodic fixing
#                     # wn:3 at t_0 must be equal to -> wn:0 at t_final
#                     # wn:4 at t_0 must be equal to -> wn:1 at t_final
#                     # wn:5 at t_0 must be equal to -> wn:2 at t_final
#                     # wn:6 at t_0 must be equal to -> wn:3 at t_final
#                     # wn:7 at t_0 must be equal to -> wn:4 at t_final
#
#                     var_name_local = 'wx_' + str(kite) + '_' + str(tip) + '_' + str(wake_node)
#                     wx_local = V['xd', 0, var_name_local]
#
#                     wake_node_upstream = wake_node - n_k
#                     var_name_upsteam = 'wx_' + str(kite) + '_' + str(tip) + '_' + str(wake_node_upstream)
#                     wx_upstream = V['xd', -1, var_name_upsteam]
#
#                     local_resi = wx_local - wx_upstream
#
#                 local_cstr = cstr_op.Constraint(expr = local_resi,
#                                                 name = local_name,
#                                                 cstr_type='eq')
#                 cstr_list.append(local_cstr)
#
#     return cstr_list
#
#
# ################ farwake
#
# def get_farwake_convection_velocity_constraint(options, V, model):
#
#     n_k = options['n_k']
#
#     kite_nodes = model.architecture.kite_nodes
#     wingtips = ['ext', 'int']
#
#     cstr_list = cstr_op.ConstraintList()
#
#     for kite in kite_nodes:
#         for tip in wingtips:
#             var_name = 'wu_farwake_' + str(kite) + '_' + tip
#
#             for ndx in range(n_k):
#
#                 local_name = 'far_wake_convection_velocity_' + str(kite) + '_' + str(tip) + '_' + str(ndx)
#
#                 wu_scaled = V['xl', ndx, var_name]
#                 wu_si = struct_op.var_scaled_to_si('xd', var_name, wu_scaled, model.scaling)
#
#                 velocity = get_far_wake_velocity_val(options, V, model, kite, ndx)
#
#                 local_resi_si = wu_si - velocity
#                 local_resi = struct_op.var_si_to_scaled('xl', var_name, local_resi_si, model.scaling)
#
#                 local_cstr = cstr_op.Constraint(expr = local_resi,
#                                                 name = local_name,
#                                                 cstr_type='eq')
#                 cstr_list.append(local_cstr)
#
#                 for ddx in range(options['collocation']['d']):
#                     local_name = 'far_wake_convection_velocity_' + str(kite) + '_' + str(tip) + '_' + str(ndx) + ',' + str(ddx)
#
#                     wu_scaled = V['coll_var', ndx, ddx, 'xl', var_name]
#                     wu_si = struct_op.var_scaled_to_si('xl', var_name, wu_scaled, model.scaling)
#
#                     velocity = get_far_wake_velocity_val(options, V, model, kite, ndx, ddx)
#
#                     local_resi_si = wu_si - velocity
#                     local_resi = struct_op.var_si_to_scaled('xl', var_name, local_resi_si, model.scaling)
#
#                     local_cstr = cstr_op.Constraint(expr=local_resi,
#                                                     name=local_name,
#                                                     cstr_type='eq')
#                     cstr_list.append(local_cstr)
#
#     return cstr_list
#
# def get_far_wake_velocity_val(options, V, model, kite, ndx, ddx=None):
#
#     parent = model.architecture.parent_map[kite]
#
#     vortex_far_wake_model = options['induction']['vortex_far_wake_model']
#     vortex_representation = options['induction']['vortex_representation']
#
#     n_k = options['n_k']
#
#     wake_nodes = options['induction']['vortex_wake_nodes']
#     wake_node = wake_nodes - 1
#
#     if vortex_far_wake_model == 'freestream_filament':
#         velocity = model.wind.get_speed_ref(from_parameters=False) * vect_op.xhat()
#         return velocity
#
#     elif (vortex_far_wake_model == 'pathwise_filament') and (vortex_representation == 'state'):
#         shooting_ndx = n_k - wake_node
#         collocation_ndx = shooting_ndx - 1
#         modular_ndx = np.mod(collocation_ndx, n_k)
#
#         shedding_ndx = modular_ndx
#         shedding_ddx = -1
#
#     elif (vortex_far_wake_model == 'pathwise_filament') and (vortex_representation == 'alg'):
#
#         if ddx is None:
#             ndx_collocation = ndx - 1
#             ddx_collocation = -1
#         else:
#             ndx_collocation = ndx
#             ddx_collocation = ddx
#
#         subtracted_ndx = ndx_collocation - wake_node
#         shedding_ndx = np.mod(subtracted_ndx, n_k)
#
#         if wake_node == 0:
#             shedding_ddx = ddx_collocation
#         else:
#             shedding_ddx = -1
#
#     else:
#         message = 'unknown vortex far wake model specified: ' + vortex_far_wake_model
#         awelogger.logger.error(message)
#         raise Exception(message)
#
#
#     q_kite_scaled = V['coll_var', shedding_ndx, shedding_ddx, 'xd', 'q' + str(kite) + str(parent)]
#     q_kite = struct_op.var_scaled_to_si('xd', 'q' + str(kite) + str(parent), q_kite_scaled,
#                                         model.scaling)
#     u_infty = model.wind.get_velocity(q_kite[2])
#
#     dq_kite_scaled = V['coll_var', shedding_ndx, shedding_ddx, 'xd', 'dq' + str(kite) + str(parent)]
#     dq_kite = struct_op.var_scaled_to_si('xd', 'dq' + str(kite) + str(parent), dq_kite_scaled,
#                                          model.scaling)
#
#     velocity = u_infty - dq_kite
#
#     return velocity
#
#
#
#
#
# ################ cylinder center
#
# def get_vortex_cylinder_center_constraint(options, V, Outputs, model):
#
#     n_k = options['n_k']
#
#     kite_nodes = model.architecture.kite_nodes
#
#     cstr_list = cstr_op.ConstraintList()
#
#     name_base = 'far_wake_convection_velocity_'
#
#     for kite in kite_nodes:
#         var_name = 'wx_center_' + str(kite)
#
#         for ndx in range(n_k):
#
#             local_name = name_base + str(kite) + '_' + str(ndx)
#
#             wx_scaled = V['xl', ndx, var_name]
#             wx_si = struct_op.var_scaled_to_si('xl', var_name, wx_scaled, model.scaling)
#
#             x_center = get_vortex_cylinder_center_val(options, Outputs, model, kite, ndx)
#
#             local_resi_si = wx_si - x_center
#             local_resi = struct_op.var_si_to_scaled('xl', var_name, local_resi_si, model.scaling)
#
#             local_cstr = cstr_op.Constraint(expr = local_resi,
#                                             name = local_name,
#                                             cstr_type='eq')
#             cstr_list.append(local_cstr)
#
#             for ddx in range(options['collocation']['d']):
#                 local_name = name_base + str(kite) + '_' + str(ndx) + ',' + str(ddx)
#
#                 wx_scaled = V['coll_var', ndx, ddx, 'xl', var_name]
#                 wx_si = struct_op.var_scaled_to_si('xl', var_name, wx_scaled, model.scaling)
#
#                 x_center = get_vortex_cylinder_center_val(options, Outputs, model, kite, ndx, ddx)
#
#                 local_resi_si = wx_si - x_center
#                 local_resi = struct_op.var_si_to_scaled('xl', var_name, local_resi_si, model.scaling)
#
#                 local_cstr = cstr_op.Constraint(expr=local_resi,
#                                                 name=local_name,
#                                                 cstr_type='eq')
#                 cstr_list.append(local_cstr)
#
#     return cstr_list
#
#
# def get_vortex_cylinder_center_val(options, Outputs, model, kite, ndx, ddx=None):
#     parent = model.architecture.parent_map[kite]
#     shedding_ndx, shedding_ddx = vortex_tools.get_shedding_ndx_and_ddx(options, ndx, ddx)
#     x_center = Outputs['coll_outputs', shedding_ndx, shedding_ddx, 'performance', 'actuator_center' + str(parent)]
#
#     return x_center
#
# def get_vortex_cylinder_radius_vector_val(options, V, model, kite, tip, ndx, ddx=None):
#
#     shedding_ndx, shedding_ddx = vortex_tools.get_shedding_ndx_and_ddx(options, ndx, ddx)
#
#     wake_nodes = options['induction']['vortex_wake_nodes']
#     vortex_representation = options['induction']['vortex_representation']
#
#     wake_node = wake_nodes - 1
#     l_hat = model.wind.get_wind_direction()
#
#     coord_name = 'wx_' + str(kite) + '_' + tip + '_' + str(wake_node)
#     if vortex_representation == 'state':
#         wx_node_var_type = 'xd'
#     elif vortex_representation == 'alg':
#         wx_node_var_type = 'xl'
#     else:
#         message = 'specified vortex representation ' + vortex_representation + ' is not supported'
#         awelogger.logger.error(message)
#         raise Exception(message)
#
#     try:
#         wx_node = V['coll_var', shedding_ndx, shedding_ddx, wx_node_var_type, coord_name]
#     except:
#         pdb.set_trace()
#
#     wx_node_si = struct_op.var_scaled_to_si(wx_node_var_type, coord_name, wx_node, model.scaling)
#
#     wx_center_name = 'wx_center_' + str(kite)
#     wx_center = V['coll_var', shedding_ndx, shedding_ddx, 'xl', wx_center_name]
#     wx_center_si = struct_op.var_scaled_to_si('xl', wx_center_name, wx_center, model.scaling)
#
#     radial_vec = wx_node_si - wx_center_si
#     radius_vec = radial_vec - cas.mtimes(radial_vec.T, l_hat) * l_hat
#
#     return radius_vec
#
#
# def get_vortex_cylinder_pitch_constraint(options, V, Outputs, model):
#
#     n_k = options['n_k']
#
#     kite_nodes = model.architecture.kite_nodes
#     wingtips = ['ext', 'int']
#
#     cstr_list = cstr_op.ConstraintList()
#
#     name_base = 'far_wake_convection_pitch_'
#
#     for kite in kite_nodes:
#
#         for tip in wingtips:
#             var_name = 'wh_' + str(kite) + '_' + tip
#
#             for ndx in range(n_k):
#
#                 local_name = name_base + str(kite) + '_' + tip + '_' + str(ndx)
#
#                 wx_scaled = V['xl', ndx, var_name]
#                 wx_si = struct_op.var_scaled_to_si('xl', var_name, wx_scaled, model.scaling)
#
#                 pitch_squared_eq = get_vortex_cylinder_pitch_squared_eq(wx_si, options, V, Outputs, model, kite, tip, ndx)
#
#                 local_resi_si = pitch_squared_eq
#                 local_resi = struct_op.var_si_to_scaled('xl', var_name, local_resi_si, model.scaling)
#
#                 local_cstr = cstr_op.Constraint(expr = local_resi,
#                                                 name = local_name,
#                                                 cstr_type='eq')
#                 cstr_list.append(local_cstr)
#
#                 for ddx in range(options['collocation']['d']):
#                     local_name = name_base + str(kite) + '_' + tip + '_' + str(ndx) + ',' + str(ddx)
#
#                     wx_scaled = V['coll_var', ndx, ddx, 'xl', var_name]
#                     wx_si = struct_op.var_scaled_to_si('xl', var_name, wx_scaled, model.scaling)
#
#                     pitch_squared_eq = get_vortex_cylinder_pitch_squared_eq(wx_si, options, V, Outputs, model, kite, tip, ndx, ddx)
#
#                     local_resi_si = pitch_squared_eq
#                     local_resi = struct_op.var_si_to_scaled('xl', var_name, local_resi_si, model.scaling)
#
#                     local_cstr = cstr_op.Constraint(expr=local_resi,
#                                                     name=local_name,
#                                                     cstr_type='eq')
#                     cstr_list.append(local_cstr)
#
#     return cstr_list
#
#
# def get_vortex_cylinder_pitch_squared_eq(pitch_var, options, V, Outputs, model, kite, tip, ndx, ddx=None):
#     shedding_ndx, shedding_ddx = vortex_tools.get_shedding_ndx_and_ddx(options, ndx, ddx=None)
#
#     parent = model.architecture.parent_map[kite]
#     u_zero = Outputs['coll_outputs', shedding_ndx, shedding_ddx, 'performance', 'u_zero' + str(parent)]
#     u_app_tip = Outputs['coll_outputs', shedding_ndx, shedding_ddx, 'aerodynamics', 'u_app_' + tip + str(kite)]
#     windspeed = model.wind.get_speed_ref(False)
#
#     l_hat = model.wind.get_wind_direction()
#     radius_vec = get_vortex_cylinder_radius_vector_val(options, V, model, kite, tip, ndx, ddx)
#
#     u_axial = cas.mtimes(u_zero.T, l_hat)
#
#     air_velocity_axial = cas.mtimes(u_app_tip.T, l_hat) * l_hat
#     air_velocity_radial = cas.mtimes(u_app_tip.T, radius_vec) * radius_vec / cas.mtimes(radius_vec.T, radius_vec)
#     air_velocity_tangential = u_app_tip - air_velocity_radial - air_velocity_axial
#
#     # u_tangential = vect_op.smooth_norm(air_velocity_tangential)
#     # pitch = 2. * np.pi * u_axial / u_tangential
#
#     pitch_squared_num = 4. * np.pi**2. * u_axial**2.
#     pitch_squared_denom = cas.mtimes(air_velocity_tangential.T, air_velocity_tangential)
#
#     pitch_squared_ref = 4. * np.pi**2. * windspeed**2.
#     pitch_squared_eq = (pitch_var**2. * pitch_squared_denom - pitch_squared_num) / pitch_squared_ref
#
#     return pitch_squared_eq