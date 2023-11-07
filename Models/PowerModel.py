import math

from Constants import Atmosphere
from Models import AerodynamicModel


def model(air_density_final, wing_area, aspect_ratio, drag_coefficient, airfoil_lift_coefficient,
          aircraft_weight, payload_power, propulsion_efficiency, drag_force, vcl, altitude_initial,
          altitude_final, flight_speed, take_off_distance, landing_distance):

    propulsion_power = get_power_for_cruise_flight(air_density_final,
                                                   wing_area,
                                                   drag_coefficient,
                                                   airfoil_lift_coefficient,
                                                   aircraft_weight,
                                                   payload_power,
                                                   propulsion_efficiency)

    power_for_take_off = get_power_for_take_off(vcl, drag_force, propulsion_efficiency)

    climb_power = get_power_for_climb_flight(vcl, drag_force, aircraft_weight, propulsion_efficiency)

    time_to_take_off = get_time_to_take_off_or_landing(take_off_distance, vcl)
    time_to_landing = get_time_to_take_off_or_landing(landing_distance, vcl)

    time_to_climb = get_time_to_climb(vcl, altitude_initial, altitude_final, aircraft_weight, flight_speed, wing_area,
                                      drag_coefficient, aspect_ratio)

    total_climb_power = (climb_power * 2 + power_for_take_off * 2) * (time_to_climb / 3600)

    return propulsion_power, power_for_take_off, climb_power, total_climb_power, time_to_take_off, time_to_climb, \
        time_to_landing


def get_power_for_cruise_flight(air_density, wing_area, drag_coefficient, lift_coefficient,
                                aircraft_weight, payload_power, propulsion_efficiency):
    power_required = (drag_coefficient / math.pow(lift_coefficient, 1.5)) * math.sqrt(
        (2 * math.pow(aircraft_weight, 3))
        / (air_density * wing_area))
    return (power_required / propulsion_efficiency) + payload_power


def get_power_for_take_off(vcl, drag, propulsion_efficiency):
    return (vcl * drag) / propulsion_efficiency


def get_power_for_climb_flight(vcl, drag, aircraft_weight, propulsion_efficiency, angle=15):
    trust = drag + aircraft_weight * math.sin(math.radians(angle))
    return (vcl * trust) / propulsion_efficiency


def get_time_to_take_off_or_landing(distance, vcl):
    return distance / (0.7 * vcl)


def get_time_to_climb(vcl, altitude_initial, altitude_final, weight, flight_velocity, wing_area,
                      profile_drag, aspect_ratio):
    angle = 15

    air_density_initial = Atmosphere.get_air_density(altitude_initial)
    air_density_final = Atmosphere.get_air_density(altitude_final)

    excess_power_initial = get_excess_power(weight, angle,
                                            air_density_initial,
                                            flight_velocity,
                                            wing_area, profile_drag, aspect_ratio)

    excess_power_final = get_excess_power(weight, angle,
                                          air_density_final,
                                          flight_velocity,
                                          wing_area, profile_drag, aspect_ratio)

    rc_initial = get_rc(vcl, excess_power_initial, weight)

    rc_final = get_rc(vcl, excess_power_final, weight)

    time_to_climb = (((1 / rc_initial) + (1 / rc_final)) * (altitude_final - altitude_initial)) / 2

    return time_to_climb


def get_excess_power(weight, angle, air_density, flight_velocity, wing_area, profile_drag,
                     aspect_ratio):
    cl = (weight * math.cos(math.radians(angle))) / (air_density * 0.5 * math.pow(flight_velocity, 2) * wing_area)

    drag_coefficient = AerodynamicModel.get_drag_coefficient(profile_drag, cl, aspect_ratio)
    drag = AerodynamicModel.get_drag_force(air_density, flight_velocity, wing_area, drag_coefficient)
    trust = drag + weight * math.sin(math.radians(angle))
    return trust - drag


def get_rc(vcl, excess_power, weight):
    return vcl * excess_power / weight


def get_storage_energy(propulsion_power, battery_efficiency, flight_endurance, climb_power):
    return ((propulsion_power / battery_efficiency) * flight_endurance) + climb_power
