import plotly.express as go
import plotly.graph_objects as go
from Services.SizingUAVService import SizingUAVService
from Services.CSVService import get_aerodynamic_profile, get_batteries, get_solar_cells


def select_color(i):
    if i == 0:
        return '#f54242'
    if i == 1:
        return '#29a9ff'
    if i == 2:
        return '#3ce66f'
    if i == 3:
        return '#e6e33c'
    if i == 4:
        return '#ad1a8d'
    if i == 5:
        return '#ad1a1a'


takeoff_altitude = 0
cruise_altitude = 500
flight_speed = 9
flight_endurance = 3
solar_energy = 3000
payload_power = 0.1
payload_weight = 0.02
wing_area = 0.2
smc = 0.20
wingspan = 1
propulsion_efficiency = 0.6
solar_cell_wing_covering = 0.7

aerodynamic_profile = get_aerodynamic_profile('xf-e210-il')
battery = get_batteries('18650B - Panasonic ')
solar_cell = get_solar_cells('SunPower C60')

solar_uav_list = []
fig = go.Figure()
fig_2 = go.Figure()


simulation = 1

for i in range(0, 6):

    wing_area += 0.2
    variable_parameter_name = 'Wing Area  - ' + '%.2f' % wing_area
    unit = 'm '

    wingspan = 1
    x_list = []
    energy_list = []
    mass_list = []

    while wingspan <= 4:
        wingspan += 0.1

        solar_uav = SizingUAVService.sizing_uav(takeoff_altitude, cruise_altitude, flight_speed,
                                                flight_endurance, solar_energy, payload_power, payload_weight,
                                                wing_area, wingspan, aerodynamic_profile, solar_cell, battery,
                                                propulsion_efficiency, solar_cell_wing_covering, 0, 0, 1)

        x_list.append(solar_uav[1])
        energy_list.append(solar_uav[27])
        mass_list.append(solar_uav[26])

    fig.add_trace(go.Scatter(x=x_list, y=energy_list, mode='lines', marker={'color': select_color(i)},
                             name=variable_parameter_name + unit))

    fig_2.add_trace(go.Scatter(x=x_list, y=mass_list, mode='lines', marker={'color': select_color(i)},
                               name=variable_parameter_name + unit))

fig.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Total Energy Consumed (W)', font=dict(size=15, ))
fig_2.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Aircraft Total Weight (N)', font=dict(size=15, ))

fig.show()
fig_2.show()


wing_area = 0.6
propulsion_efficiency = 0.05
solar_uav_list = []
fig = go.Figure()
fig_2 = go.Figure()

for i in range(0, 6):
    propulsion_efficiency += 0.15
    variable_parameter_name = 'Propulsion Efficiency  - ' + '%.2f' % propulsion_efficiency
    unit = '% '

    wingspan = 1
    x_list = []
    energy_list = []
    mass_list = []

    while wingspan <= 4:
        wingspan += 0.1

        solar_uav = SizingUAVService.sizing_uav(takeoff_altitude, cruise_altitude, flight_speed,
                                                flight_endurance, solar_energy, payload_power, payload_weight,
                                                wing_area, wingspan, aerodynamic_profile, solar_cell, battery,
                                                propulsion_efficiency, solar_cell_wing_covering, 0, 0, 1)

        x_list.append(solar_uav[1])
        energy_list.append(solar_uav[27])
        mass_list.append(solar_uav[26])

    fig.add_trace(go.Scatter(x=x_list, y=energy_list, mode='lines', marker={'color': select_color(i)},
                             name=variable_parameter_name + unit))

    fig_2.add_trace(go.Scatter(x=x_list, y=mass_list, mode='lines', marker={'color': select_color(i)},
                               name=variable_parameter_name + unit))

fig.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Total Energy Consumed (W)', font=dict(size=15, ))
fig_2.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Aircraft Total Weight (N)', font=dict(size=15, ))

fig.show()
fig_2.show()


propulsion_efficiency = 0.6
flight_endurance = 3

solar_uav_list = []
fig = go.Figure()
fig_2 = go.Figure()

for i in range(0, 6):
    flight_endurance += 1
    variable_parameter_name = 'Flight Endurance  - ' + '%.2f' % flight_endurance
    unit = 'h '

    wingspan = 1
    x_list = []
    energy_list = []
    mass_list = []

    while wingspan <= 4:
        wingspan += 0.1

        solar_uav = SizingUAVService.sizing_uav(takeoff_altitude, cruise_altitude, flight_speed,
                                                flight_endurance, solar_energy, payload_power, payload_weight,
                                                wing_area, wingspan, aerodynamic_profile, solar_cell, battery,
                                                propulsion_efficiency, solar_cell_wing_covering, 0, 0, 1)

        x_list.append(solar_uav[1])
        energy_list.append(solar_uav[27])
        mass_list.append(solar_uav[26])

    fig.add_trace(go.Scatter(x=x_list, y=energy_list, mode='lines', marker={'color': select_color(i)},
                             name=variable_parameter_name + unit))

    fig_2.add_trace(go.Scatter(x=x_list, y=mass_list, mode='lines', marker={'color': select_color(i)},
                               name=variable_parameter_name + unit))

fig.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Total Energy Consumed (W)', font=dict(size=15, ))
fig_2.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Aircraft Total Weight (N)', font=dict(size=15, ))

fig.show()
fig_2.show()


flight_endurance = 3
flight_speed = 6

solar_uav_list = []
fig = go.Figure()
fig_2 = go.Figure()

for i in range(0, 6):
    flight_speed += 1
    variable_parameter_name = 'Flight Speed  - ' + '%.2f' % flight_speed
    unit = 'm/s '

    wingspan = 1
    x_list = []
    energy_list = []
    mass_list = []

    while wingspan <= 4:
        wingspan += 0.1

        solar_uav = SizingUAVService.sizing_uav(takeoff_altitude, cruise_altitude, flight_speed,
                                                flight_endurance, solar_energy, payload_power, payload_weight,
                                                wing_area, wingspan, aerodynamic_profile, solar_cell, battery,
                                                propulsion_efficiency, solar_cell_wing_covering, 0, 0, 1)

        x_list.append(solar_uav[1])
        energy_list.append(solar_uav[27])
        mass_list.append(solar_uav[26])

    fig.add_trace(go.Scatter(x=x_list, y=energy_list, mode='lines', marker={'color': select_color(i)},
                             name=variable_parameter_name + unit))

    fig_2.add_trace(go.Scatter(x=x_list, y=mass_list, mode='lines', marker={'color': select_color(i)},
                               name=variable_parameter_name + unit))

fig.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Total Energy Consumed (W)', font=dict(size=15, ))
fig_2.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Aircraft Total Weight (N)', font=dict(size=15, ))

fig.show()
fig_2.show()


flight_speed = 9
payload_power = 1

solar_uav_list = []
fig = go.Figure()
fig_2 = go.Figure()

for i in range(0, 6):
    payload_power += 1
    variable_parameter_name = 'Payload Power  - ' + '%.2f' % payload_power
    unit = 'W '

    wingspan = 1
    x_list = []
    energy_list = []
    mass_list = []

    while wingspan <= 4:
        wingspan += 0.1

        solar_uav = SizingUAVService.sizing_uav(takeoff_altitude, cruise_altitude, flight_speed,
                                                flight_endurance, solar_energy, payload_power, payload_weight,
                                                wing_area, wingspan, aerodynamic_profile, solar_cell, battery,
                                                propulsion_efficiency, solar_cell_wing_covering, 0, 0, 1)

        x_list.append(solar_uav[1])
        energy_list.append(solar_uav[27])
        mass_list.append(solar_uav[26])

    fig.add_trace(go.Scatter(x=x_list, y=energy_list, mode='lines', marker={'color': select_color(i)},
                             name=variable_parameter_name + unit))

    fig_2.add_trace(go.Scatter(x=x_list, y=mass_list, mode='lines', marker={'color': select_color(i)},
                               name=variable_parameter_name + unit))

fig.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Total Energy Consumed (W)', font=dict(size=15, ))
fig_2.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Aircraft Total Weight (N)', font=dict(size=15, ))

fig.show()
fig_2.show()

payload_power = 0.1
payload_weight = 1

solar_uav_list = []
fig = go.Figure()
fig_2 = go.Figure()

for i in range(0, 6):
    payload_weight += 1
    variable_parameter_name = 'Payload Weight  - ' + '%.2f' % payload_weight
    unit = 'N '

    wingspan = 1
    x_list = []
    energy_list = []
    mass_list = []

    while wingspan <= 4:
        wingspan += 0.1

        solar_uav = SizingUAVService.sizing_uav(takeoff_altitude, cruise_altitude, flight_speed,
                                                flight_endurance, solar_energy, payload_power, payload_weight,
                                                wing_area, wingspan, aerodynamic_profile, solar_cell, battery,
                                                propulsion_efficiency, solar_cell_wing_covering, 0, 0, 1)

        x_list.append(solar_uav[1])
        energy_list.append(solar_uav[27])
        mass_list.append(solar_uav[26])

    fig.add_trace(go.Scatter(x=x_list, y=energy_list, mode='lines', marker={'color': select_color(i)},
                             name=variable_parameter_name + unit))

    fig_2.add_trace(go.Scatter(x=x_list, y=mass_list, mode='lines', marker={'color': select_color(i)},
                               name=variable_parameter_name + unit))

fig.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Total Energy Consumed (W)', font=dict(size=15, ))
fig_2.update_layout(title='', xaxis_title='Wingspan (m)', yaxis_title='Aircraft Total Weight (N)', font=dict(size=15, ))

fig.show()
fig_2.show()

