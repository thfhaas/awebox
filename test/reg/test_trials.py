#!/usr/bin/python3
"""Template for trial tests

@author: Thilo Bronnenmeyer, kiteswarms 2018

- edit: Rachel Leuthold, Jochem De Schutter ALU-FR 2020-21
"""

import collections
import copy
import logging
import pdb
import casadi.tools as cas

import awebox.opts.kite_data.ampyx_data as ampyx_data
import awebox.opts.kite_data.bubbledancer_data as bubbledancer_data
import awebox.opts.kite_data.boeing747_data as boeing747_data
from ampyx_ap2_settings import set_ampyx_ap2_settings
import awebox.opts.options as options
import awebox.trial as awe_trial
import awebox.tools.print_operations as print_op

from awebox.logger.logger import Logger as awelogger
import matplotlib.pyplot as plt
awelogger.logger.setLevel(10)



logging.basicConfig(filemode='w',format='%(levelname)s:    %(message)s', level=logging.DEBUG)


def test_single_kite(final_homotopy_step='final'):
    trial_name = 'single_kite_trial'
    run_a_solve_and_check_test(trial_name, final_homotopy_step=final_homotopy_step)
    return None


def test_zoh():
    trial_name = 'zoh_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_basic_health(final_homotopy_step='final'):
    trial_name = 'basic_health_trial'
    run_a_solve_and_check_test(trial_name, final_homotopy_step=final_homotopy_step)
    return None


def test_dual_kite_basic_health(final_homotopy_step='final'):
    trial_name = 'dual_kite_basic_health_trial'
    run_a_solve_and_check_test(trial_name, final_homotopy_step=final_homotopy_step)
    return None

def test_drag_mode():
    trial_name = 'drag_mode_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_save_trial():
    trial_name = 'save_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_dual_kite(final_homotopy_step='final'):
    trial_name = 'dual_kite_trial'
    run_a_solve_and_check_test(trial_name, final_homotopy_step=final_homotopy_step)
    return None


def test_dual_kite_6_dof():
    trial_name = 'dual_kite_6_dof_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_small_dual_kite():
    trial_name = 'small_dual_kite_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_large_dual_kite():
    trial_name = 'large_dual_kite_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_actuator_qaxi():
    trial_name = 'actuator_qaxi_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_actuator_uaxi():
    trial_name = 'actuator_uaxi_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_actuator_qasym():
    trial_name = 'actuator_qasym_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_actuator_uasym():
    trial_name = 'actuator_uasym_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_actuator_comparison():
    trial_name = 'actuator_comparison_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_dual_kite_tracking():
    trial_name = 'dual_kite_tracking_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_dual_kite_tracking_winch():
    trial_name = 'dual_kite_tracking_winch_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_vortex_force_zero():
    trial_name = 'vortex_force_zero_trial'
    run_a_solve_and_check_test(trial_name)
    return None


def test_vortex():
    options_dict = generate_options_dict()
    trial_name = 'vortex_trial'
    solve_trial(options_dict[trial_name], trial_name)
    return None


def generate_options_dict():
    """
    Set options for the trials that should be tested and store them in dictionary
    :return: dictionary with trial options
    """

    # set options
    single_kite_options = {}
    single_kite_options['user_options.system_model.architecture'] = {1: 0}
    single_kite_options = set_ampyx_ap2_settings(single_kite_options)
    single_kite_options['solver.linear_solver'] = 'ma57'
    single_kite_options['visualization.cosmetics.plot_bounds'] = True
    single_kite_options['solver.weights.q'] = 1e0
    single_kite_options['solver.weights.dq'] = 1.e-1
    single_kite_options['solver.weights.l_t'] = 1e-5
    single_kite_options['solver.weights.dl_t'] = 1e-3
    single_kite_options['solver.weights.ddl_t'] = 1e-1
    single_kite_options['solver.weights.dddl_t'] = 1e-1
    single_kite_options['solver.weights.coeff'] = 1e-6
    single_kite_options['solver.cost.fictitious.0'] = 1.e0
    single_kite_options['solver.cost.fictitious.1'] = 1.e3
    single_kite_options['solver.cost.u_regularisation.0'] = 1e-3
    single_kite_options['solver.cost_factor.power'] = 1e8
    single_kite_options['solver.cost.tracking.0'] = 1.e2
    single_kite_options['solver.cost.theta_regularisation.0'] = 1.e1
    # single_kite_options['solver.initialization.groundspeed'] = (13. + 32.)/2.

    basic_health_options = copy.deepcopy(single_kite_options)
    basic_health_options['user_options.trajectory.lift_mode.windings'] = 1
    basic_health_options['nlp.n_k'] = 10
    basic_health_options['solver.health_check.when'] = 'always'
    basic_health_options['solver.hippo_strategy'] = False
    basic_health_options['nlp.collocation.u_param'] = 'zoh'
    basic_health_options['solver.homotopy_method.advance_despite_max_iter'] = False
    basic_health_options['solver.homotopy_method.advance_despite_ill_health'] = False
    basic_health_options['solver.initialization.use_reference_to_check_scaling'] = True
    basic_health_options['solver.max_iter'] = 300
    basic_health_options['solver.health_check.raise_exception'] = True
    basic_health_options['solver.health_check.spy_matrices'] = False
    basic_health_options['nlp.collocation.name_constraints'] = True #False
    basic_health_options['solver.health_check.help_with_debugging'] = True #False

    zoh_options = copy.deepcopy(single_kite_options)
    zoh_options['nlp.collocation.u_param'] = 'zoh'

    drag_mode_options = copy.deepcopy(single_kite_options)
    drag_mode_options['user_options.trajectory.system_type'] = 'drag_mode'
    drag_mode_options['quality.test_param.power_balance_thresh'] = 2.
    drag_mode_options['model.system_bounds.theta.t_f'] = [20., 70.]  # [s]

    save_trial_options = copy.deepcopy(single_kite_options)
    save_trial_options['solver.save_trial'] = True

    dual_kite_options = copy.deepcopy(single_kite_options)
    dual_kite_options['user_options.system_model.architecture'] = {1: 0, 2: 1, 3: 1}
    # dual_kite_options['model.system_bounds.theta.t_f'] = [20., 70.]  # [s]
    # dual_kite_options['solver.cost.fictitious.0'] = 1.e-1
    # dual_kite_options['solver.cost.fictitious.1'] = 1.e3
    # dual_kite_options['solver.cost.tracking.0'] = 1.e3

    dual_kite_basic_health_options = copy.deepcopy(dual_kite_options)
    dual_kite_basic_health_options['user_options.trajectory.lift_mode.windings'] = 1
    dual_kite_basic_health_options['nlp.n_k'] = 10
    dual_kite_basic_health_options['solver.health_check.when'] = 'always'
    dual_kite_basic_health_options['solver.hippo_strategy'] = False
    dual_kite_basic_health_options['nlp.collocation.u_param'] = 'zoh'
    dual_kite_basic_health_options['solver.homotopy_method.advance_despite_max_iter'] = False
    dual_kite_basic_health_options['solver.homotopy_method.advance_despite_ill_health'] = False
    dual_kite_basic_health_options['solver.initialization.use_reference_to_check_scaling'] = True
    dual_kite_basic_health_options['solver.max_iter'] = 300
    dual_kite_basic_health_options['solver.health_check.raise_exception'] = True
    dual_kite_basic_health_options['solver.health_check.spy_matrices'] = False
    dual_kite_basic_health_options['nlp.collocation.name_constraints'] = True
    dual_kite_basic_health_options['solver.health_check.help_with_debugging'] = True

    dual_kite_6_dof_options = copy.deepcopy(dual_kite_options)
    dual_kite_6_dof_options['user_options.system_model.kite_dof'] = 6

    small_dual_kite_options = copy.deepcopy(dual_kite_6_dof_options)
    small_dual_kite_options['user_options.kite_standard'] = bubbledancer_data.data_dict()
    small_dual_kite_options['user_options.trajectory.lift_mode.windings'] = 1

    large_dual_kite_options = copy.deepcopy(small_dual_kite_options)
    large_dual_kite_options['user_options.kite_standard'] = boeing747_data.data_dict()

    actuator_qaxi_options = {}
    actuator_qaxi_options['user_options.system_model.architecture'] = {1: 0, 2: 1, 3: 1}
    actuator_qaxi_options['user_options.kite_standard'] = ampyx_data.data_dict()
    actuator_qaxi_options['user_options.system_model.kite_dof'] = 6
    actuator_qaxi_options['user_options.tether_drag_model'] = 'split'
    actuator_qaxi_options['user_options.induction_model'] = 'actuator'
    actuator_qaxi_options['model.aero.actuator.steadyness'] = 'quasi-steady'
    actuator_qaxi_options['model.aero.actuator.symmetry'] = 'axisymmetric'
    actuator_qaxi_options['user_options.trajectory.lift_mode.windings'] = 1
    actuator_qaxi_options['model.aero.overwrite.alpha_max_deg'] = 20.
    actuator_qaxi_options['model.aero.overwrite.alpha_min_deg'] = -20.
    actuator_qaxi_options['model.aero.overwrite.beta_max_deg'] = 20.
    actuator_qaxi_options['model.aero.overwrite.beta_min_deg'] = -20.
    actuator_qaxi_options['model.model_bounds.tether_stress.scaling'] = 10.
    actuator_qaxi_options['model.tether.lift_tether_force'] = True
    actuator_qaxi_options['model.aero.lift_aero_force'] = True
    actuator_qaxi_options['nlp.collocation.u_param'] = 'zoh'
    actuator_qaxi_options['solver.cost.fictitious.0'] = 1.e3
    actuator_qaxi_options['nlp.n_k'] = 15

    actuator_uaxi_options = copy.deepcopy(actuator_qaxi_options)
    actuator_uaxi_options['model.aero.actuator.steadyness'] = 'unsteady'
    actuator_uaxi_options['model.model_bounds.tether_stress.scaling'] = 10.

    actuator_qasym_options = copy.deepcopy(actuator_qaxi_options)
    actuator_qasym_options['model.aero.actuator.symmetry'] = 'asymmetric'
    actuator_qasym_options['solver.cost.psi.1'] = 1.e1

    actuator_uasym_options = copy.deepcopy(actuator_qaxi_options)
    actuator_uasym_options['model.aero.actuator.symmetry'] = 'asymmetric'
    actuator_uasym_options['model.aero.actuator.symmetry'] = 'asymmetric'
    actuator_uasym_options['solver.cost.psi.1'] = 1.e1

    actuator_comparison_options = copy.deepcopy(actuator_qaxi_options)
    actuator_comparison_options['model.aero.actuator.steadyness_comparison'] = ['q', 'u']
    actuator_comparison_options['user_options.system_model.kite_dof'] = 6

    vortex_options = {}
    vortex_options['user_options.system_model.architecture'] = {1: 0}
    vortex_options['user_options.trajectory.lift_mode.windings'] = 1
    vortex_options['user_options.kite_standard'] = ampyx_data.data_dict()
    vortex_options['user_options.system_model.kite_dof'] = 6
    vortex_options['user_options.induction_model'] = 'vortex'
    vortex_options['user_options.tether_drag_model'] = 'split'
    vortex_options['nlp.n_k'] = 8
    vortex_options['model.aero.vortex.wake_nodes'] = 10
    vortex_options['model.aero.vortex.representation'] = 'alg'
    vortex_options['model.aero.overwrite.alpha_max_deg'] = 20.
    vortex_options['model.aero.overwrite.alpha_min_deg'] = -20.
    # vortex_options['model.tether.lift_tether_force'] = True
    # vortex_options['model.aero.lift_aero_force'] = True
    vortex_options['nlp.collocation.u_param'] = 'zoh'

    vortex_force_zero_options = copy.deepcopy(vortex_options)
    vortex_force_zero_options['model.aero.vortex.force_zero'] = True

    dual_kite_tracking_options = copy.deepcopy(dual_kite_6_dof_options)
    dual_kite_tracking_options['user_options.trajectory.type'] = 'tracking'
    dual_kite_tracking_options['user_options.trajectory.lift_mode.windings'] = 1
    # dual_kite_tracking_options['user_options.trajectory.tracking.fix_tether_length'] = True
    dual_kite_tracking_options['nlp.n_k'] = 20

    dual_kite_tracking_winch_options = copy.deepcopy(dual_kite_tracking_options)
    dual_kite_tracking_winch_options['user_options.trajectory.tracking.fix_tether_length'] = False

    # nominal landing
    nominal_landing_options = copy.deepcopy(dual_kite_options)
    nominal_landing_options['user_options.trajectory.type'] = 'nominal_landing'
    nominal_landing_options['user_options.trajectory.transition.initial_trajectory'] = 'dual_kite_trial.dict'
    nominal_landing_options['solver.initialization.initialization_type'] = 'modular'

    # compromised landing
    compromised_landing_options = copy.deepcopy(nominal_landing_options)
    compromised_landing_options['user_options.trajectory.type'] = 'compromised_landing'
    compromised_landing_options['model.model_bounds.dcoeff_compromised_factor'] = 0.0
    compromised_landing_options['user_options.trajectory.compromised_landing.emergency_scenario'] = ('broken_roll', 2)
    compromised_landing_options['user_options.trajectory.compromised_landing.xi_0_initial'] = 0.8



    # define options list
    options_dict = collections.OrderedDict()
    options_dict['single_kite_trial'] = single_kite_options
    options_dict['zoh_trial'] = zoh_options
    options_dict['drag_mode_trial'] = drag_mode_options
    options_dict['save_trial'] = save_trial_options
    options_dict['dual_kite_trial'] = dual_kite_options
    options_dict['small_dual_kite_trial'] = small_dual_kite_options
    options_dict['large_dual_kite_trial'] = large_dual_kite_options
    options_dict['dual_kite_6_dof_trial'] = dual_kite_6_dof_options
    options_dict['actuator_qaxi_trial'] = actuator_qaxi_options
    options_dict['actuator_uaxi_trial'] = actuator_uaxi_options
    options_dict['actuator_qasym_trial'] = actuator_qasym_options
    options_dict['actuator_uasym_trial'] = actuator_uasym_options
    options_dict['actuator_comparison_trial'] = actuator_comparison_options
    options_dict['vortex_force_zero_trial'] = vortex_force_zero_options
    options_dict['vortex_trial'] = vortex_options
    options_dict['dual_kite_tracking_trial'] = dual_kite_tracking_options
    options_dict['dual_kite_tracking_winch_trial'] = dual_kite_tracking_winch_options
    # options_dict['nominal_landing_trial'] = nominal_landing_options
    # options_dict['compromised_landing_trial'] = compromised_landing_options
    options_dict['basic_health_trial'] = basic_health_options
    options_dict['dual_kite_basic_health_trial'] = dual_kite_basic_health_options

    return options_dict


def run_a_solve_and_check_test(trial_name, final_homotopy_step='final'):
    """
    Solve one individual trial and run tests on it
    :param trial_name: name of the trial
    :return: None
    """

    options_dict = generate_options_dict()
    trial_options = options_dict[trial_name]

    # compute trajectory solution
    trial = solve_trial(trial_options, trial_name, final_homotopy_step=final_homotopy_step)

    # evaluate results
    evaluate_results(trial.quality.results, trial_name)

    return None


def evaluate_results(results, trial_name):

    # loop over all results
    for test_name in list(results.keys()):
        assert results[test_name], 'Test failed for ' + trial_name + ', Test regarding ' + test_name + ' failed.'

    return None


def solve_trial(trial_options, trial_name, final_homotopy_step='final'):
    """
    Set up and solve trial
    :return: solved trial
    """

    trial = awe_trial.Trial(trial_options, trial_name)
    trial.build()
    trial.optimize(final_homotopy_step=final_homotopy_step)

    # trial.print_cost_information()
    # trial.plot('level_1')
    # plt.show()

    return trial

test_single_kite()
# test_basic_health()
# test_zoh()
# test_drag_mode()
# test_save_trial()
test_dual_kite(final_homotopy_step='fictitious')
# test_dual_kite_basic_health(final_homotopy_step='initial')
# test_small_dual_kite()
# test_large_dual_kite()
# test_dual_kite_6_dof()
# test_actuator_qaxi()
# test_actuator_qasym()
# test_actuator_uaxi()
# test_actuator_uasym()
# test_actuator_comparison()
# test_vortex()
# test_dual_kite_tracking()
# test_dual_kite_tracking_winch()