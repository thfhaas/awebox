#
#    This file is part of awebox.
#
#    awebox -- A modeling and optimization framework for multi-kite AWE systems.
#    Copyright (C) 2017-2020 Jochem De Schutter, Rachel Leuthold, Moritz Diehl,
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
import casadi.tools as cas
import matplotlib.pyplot as plt
import numpy as np
from awebox.logger.logger import Logger as awelogger
import awebox.viz.tools as tools
import awebox.tools.vector_operations as vect_op

import pdb

def draw_wake_nodes(ax, side, plot_dict, index):

    vortex_info_exists = determine_if_vortex_info_exists(plot_dict)
    if vortex_info_exists:

        filament_list = reconstruct_filament_list(plot_dict, index)

        n_filaments = filament_list.shape[1]

        for fdx in range(n_filaments):
            seg_data = filament_list[:, fdx]
            start_point = seg_data[:3].T
            end_point = seg_data[3:6].T
            gamma = seg_data[6]

            points = cas.vertcat(start_point, end_point)
            wake_color = convert_gamma_to_color(gamma, plot_dict)
            try:
                tools.make_side_plot(ax, points, side, wake_color)
            except:
                awelogger.logger.error('error in side plot production')

    return None

def determine_if_vortex_info_exists(plot_dict):
    vortex_exists = 'vortex' in plot_dict['outputs'].keys()
    filament_list_exists = vortex_exists and ('filament_list' in plot_dict['outputs']['vortex'].keys())

    return filament_list_exists

def reconstruct_filament_list(plot_dict, index):

    all_time = plot_dict['outputs']['vortex']['filament_list']
    n_entries = len(all_time)
    n_filaments = int(n_entries / 7)

    filament_list = []
    for edx in range(n_entries):
        new_entry = all_time[edx][index]
        filament_list = cas.vertcat(filament_list, new_entry)

    filament_list = cas.reshape(filament_list, (7, n_filaments))

    return filament_list

def get_gamma_extrema(plot_dict):
    n_k = plot_dict['n_k']
    d = plot_dict['d']
    kite_nodes = plot_dict['architecture'].kite_nodes
    parent_map = plot_dict['architecture'].parent_map
    periods_tracked = plot_dict['options']['model']['aero']['vortex']['periods_tracked']

    gamma_max = -1.e5
    gamma_min = 1.e5

    for kite in kite_nodes:
        parent = parent_map[kite]
        for period in range(periods_tracked):

            if period > 1:
                period = 1

            for ndx in range(n_k):
                for ddx in range(d):
                    gamma_name = 'wg' + '_' + str(period) + '_' + str(kite) + str(parent)
                    var = plot_dict['V_plot']['coll_var', ndx, ddx, 'xl', gamma_name]

                    gamma_max = np.max(np.array(cas.vertcat(gamma_max, var)))
                    gamma_min = np.min(np.array(cas.vertcat(gamma_min, var)))

    # so that gamma = 0 vortex filaments will be drawn in white...
    gamma_max = np.max(np.array([gamma_max, -1. * gamma_min]))
    gamma_min = -1. * gamma_max

    return gamma_min, gamma_max


def convert_gamma_to_color(gamma_val, plot_dict):

    gamma_min, gamma_max = get_gamma_extrema(plot_dict)
    cmap = plt.get_cmap('seismic')
    gamma_scaled = float( (gamma_val - gamma_min) / (gamma_max - gamma_min) )

    color = cmap(gamma_scaled)
    return color

def plot_vortex_verification(plot_dict, cosmetics, fig_name, fig_num=None):

    if 'haas_grid' in plot_dict['outputs'].keys():
        haas_grid = plot_dict['outputs']['haas_grid']

        number_entries = len(haas_grid.keys())
        verification_points = np.sqrt(float(number_entries))

        slice_index = -1

        y_matr = []
        z_matr = []
        a_matr = []
        idx = 0

        y_row = []
        z_row = []
        a_row = []

        for ndx in range(number_entries):

            idx += 1

            local_y = haas_grid['p' + str(ndx)][0][slice_index]
            local_z = haas_grid['p' + str(ndx)][1][slice_index]
            local_a = haas_grid['p' + str(ndx)][2][slice_index]

            y_row = cas.horzcat(y_row, local_y)
            z_row = cas.horzcat(z_row, local_z)
            a_row = cas.horzcat(a_row, local_a)

            if float(idx) == (verification_points):
                y_matr = cas.vertcat(y_matr, y_row)
                z_matr = cas.vertcat(z_matr, z_row)
                a_matr = cas.vertcat(a_matr, a_row)

                y_row = []
                z_row = []
                a_row = []
                idx = 0

        y_matr = np.array(y_matr)
        z_matr = np.array(z_matr)
        a_matr = np.array(a_matr)

        y_matr_list = np.array(cas.vertcat(y_matr))
        z_matr_list = np.array(cas.vertcat(z_matr))

        max_y = np.max(y_matr_list)
        min_y = np.min(y_matr_list)
        max_z = np.max(z_matr_list)
        min_z = np.min(z_matr_list)
        max_axes = np.max(np.array([max_y, -1. * min_y, max_z, -1. * min_z]))

        mu_min_by_path = float(plot_dict['outputs']['haas_mu']['mu_min_by_path'][0][0])
        mu_max_by_path = float(plot_dict['outputs']['haas_mu']['mu_max_by_path'][0][0])

        ### points plot

        fig_points, ax_points = plt.subplots(1, 1)
        add_annulus_background(ax_points, mu_min_by_path, mu_max_by_path)
        ax_points.scatter(y_matr_list, z_matr_list)
        plt.grid(True)
        plt.title('induction factors over the kite plane')
        plt.xlabel("y/r [-]")
        plt.ylabel("z/r [-]")
        ax_points.set_xlim([-1. * max_axes, max_axes])
        ax_points.set_ylim([-1. * max_axes, max_axes])

        # ax_points.invert_xaxis() # to get view along u_infty

        fig_points.savefig('points.pdf')

        #### contour plot

        fig_contour, ax_contour = plt.subplots(1, 1)
        add_annulus_background(ax_contour, mu_min_by_path, mu_max_by_path)

        levels = [-0.05, 0., 0.2]
        colors = ['red', 'green', 'blue']

        cs = ax_contour.contour(y_matr, z_matr, a_matr, levels, colors=colors)
        plt.clabel(cs, inline=1, fontsize=10)
        for i in range(len(levels)):
            cs.collections[i].set_label(levels[i])
        plt.legend(loc='lower right')

        plt.grid(True)
        plt.title('induction factors over the kite plane')
        plt.xlabel("y/r [-]")
        plt.ylabel("z/r [-]")
        ax_contour.set_xlim([-1. * max_axes, max_axes])
        ax_contour.set_ylim([-1. * max_axes, max_axes])

        # ax_contour.invert_xaxis()  # to get view along u_infty

        fig_contour.savefig('contour.pdf')


def add_annulus_background(ax, mu_min_by_path, mu_max_by_path):
    n, radii = 50, [mu_min_by_path, mu_max_by_path]
    theta = np.linspace(0, 2 * np.pi, n, endpoint=True)
    xs = np.outer(radii, np.cos(theta))
    ys = np.outer(radii, np.sin(theta))

    # in order to have a closed area, the circles
    # should be traversed in opposite directions
    xs[1, :] = xs[1, ::-1]
    ys[1, :] = ys[1, ::-1]

    color = (0.83,0.83,0.83,0.5)

    ax.fill(np.ravel(xs), np.ravel(ys), color=color)
