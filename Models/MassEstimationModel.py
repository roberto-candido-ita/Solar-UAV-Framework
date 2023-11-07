import math

from Models import PowerModel


def model(wing_area, AR, propulsion_power, panel_area, cell_weight,
          cell_area, k, battery_energy_density, battery_efficiency, flight_endurance,
          climb_power, payload_weight, airframe_weight=0, propulsion_weight=0):
    battery_energy = PowerModel.get_storage_energy(propulsion_power, battery_efficiency, flight_endurance,
                                                   climb_power)

    airframe_estimated_weight = get_airframe_weight(wing_area, AR)
    panel_estimated_weight = get_solar_cells_weight(panel_area, cell_weight, cell_area, k) * 1.1
    battery_estimated_weight = get_battery_weight(battery_energy, battery_energy_density) * 1.1
    propulsion_estimated_weight = get_propulsion_weight(propulsion_power)

    if airframe_weight != 0 and propulsion_weight != 0:
        airframe_estimated_weight = airframe_weight * 9.81
        propulsion_estimated_weight = propulsion_weight * 9.81

    aircraft_total_weight = (payload_weight * 9.81) + airframe_estimated_weight + panel_estimated_weight + \
                            battery_estimated_weight + propulsion_estimated_weight

    return airframe_estimated_weight, panel_estimated_weight, battery_estimated_weight, propulsion_estimated_weight, \
        aircraft_total_weight


def get_airframe_weight(wing_area, AR):
    k = 0.78  # 0.44
    x1 = 1.55  # 1.55
    x2 = 1.27  # 1.30
    airframe_weight = k * math.pow(wing_area, x1) * math.pow(AR, x2)
    return airframe_weight


def get_propulsion_weight(power_required):
    return 0.008 * power_required * 9.81


def get_solar_cells_weight(panel_area, cell_weight, cell_area, k):
    return (panel_area / cell_area) * cell_weight * (k + 1) * 9.81


def get_battery_weight(storage_energy, battery_density):
    return (storage_energy / battery_density) * 9.81


def get_total_weight(battery_weight, solar_cells_weight, propulsion_weight, airframe_weight, payload_weight):
    return battery_weight + solar_cells_weight + propulsion_weight + airframe_weight + payload_weight
