import os
import shutil
import urbs


input_files = 'Romania.xlsx'  # for single year file name, for intertemporal folder name
input_dir = 'Input'
input_path = os.path.join(input_dir, input_files)

result_name = 'Romania'
result_dir = urbs.prepare_result_directory(result_name)  # name + time stamp

# copy input file to result directory
try:
    shutil.copytree(input_path, os.path.join(result_dir, input_dir))
except NotADirectoryError:
    shutil.copyfile(input_path, os.path.join(result_dir, input_files))
# copy run file to result directory
shutil.copy(__file__, result_dir)

# objective function
objective = 'cost'  # set either 'cost' or 'CO2' as objective

# Choose Solver (cplex, glpk, gurobi, ...)
solver = 'gurobi'

# simulation timesteps
(offset, length) = (0, 8760)  # time step selection
timesteps = range(offset, offset+length+1)
dt = 1  # length of each time step (unit: hours)

# detailed reporting commodity/sites
report_tuples = [
    (2020, 'Muntenia', 'Elec'),
    (2020, 'Muntenia', 'Heat'),
    (2020, 'Moldova', 'Elec'),
    (2020, 'Dobrogea', 'Elec'),
    (2020, 'Transilvania', 'Elec'),
    (2020, 'Oltenia', 'Elec'),
    (2020, ['Muntenia', 'Moldova', 'Dobrogea', 'Transilvania', 'Oltenia'], 'Elec')
    ]
 # optional: define names for sites in report_tuples
report_sites_name = {('Muntenia', 'Moldova', 'Dobrogea', 'Transilvania', 'Oltenia'): 'All'}

# plotting commodities/sites
plot_tuples = [
    (2020, 'Muntenia', 'Elec'),
    (2020, 'Muntenia', 'Heat'),
    (2020, 'Moldova', 'Elec'),
    (2020, 'Dobrogea', 'Elec'),
    (2020, 'Transilvania', 'Elec'),
    (2020, 'Oltenia', 'Elec'),
    (2020, ['Muntenia', 'Moldova', 'Dobrogea', 'Transilvania', 'Oltenia'], 'Elec')
    ]

# optional: define names for sites in plot_tuples
plot_sites_name = {('Muntenia', 'Moldova', 'Dobrogea', 'Transilvania', 'Oltenia'): 'All'}

# plotting timesteps
plot_periods = {
    'all': timesteps[1:]
}

# add or change plot colors
my_colors = {
    'Muntenia': (230, 200, 200),
    'Moldova': (200, 230, 200),
    'Dobrogea': (200, 200, 230),
    'Transilvania': (240, 200, 200),
    'Oltenia': (200, 240, 200)}
for country, color in my_colors.items():
    urbs.COLORS[country] = color

# select scenarios to be run
scenarios = [
             urbs.scenario_base,
             # urbs.scenario_stock_prices,
             # urbs.scenario_co2_limit,
             # urbs.scenario_co2_tax_mid,
             # urbs.scenario_no_dsm,
             # urbs.scenario_north_process_caps,
             # urbs.scenario_all_together
            ]

for scenario in scenarios:
    prob = urbs.run_scenario(input_path, solver, timesteps, scenario,
                             result_dir, dt, objective,
                             plot_tuples=plot_tuples,
                             plot_sites_name=plot_sites_name,
                             plot_periods=plot_periods,
                             report_tuples=report_tuples,
                             report_sites_name=report_sites_name)
