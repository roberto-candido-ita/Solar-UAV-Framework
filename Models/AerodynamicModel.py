import math


def model(wingspan, wing_area, air_density_initial, flight_speed, airfoil_lift_coefficient, airfoil_drag):
    aspect_ratio = get_aspect_ratio(wingspan, wing_area)
    standard_mean_chord = wingspan / aspect_ratio

    lift_force = get_lift_force(air_density_initial,
                                flight_speed, wing_area,
                                airfoil_lift_coefficient, )

    cdi = get_induced_drag(lift_force, aspect_ratio)

    drag_coefficient = get_drag_coefficient(airfoil_drag,
                                            airfoil_lift_coefficient,
                                            aspect_ratio)

    drag_force = get_drag_force(air_density_initial,
                                flight_speed, wing_area,
                                drag_coefficient)

    vcl = 1.2 * get_stall_speed(air_density_initial, lift_force, wing_area,
                                airfoil_lift_coefficient)

    take_off_distance, landing_distance = get_take_off_and_landing_distances(wing_area, aspect_ratio,
                                                                             lift_force, air_density_initial,
                                                                             vcl, drag_force, airfoil_lift_coefficient,
                                                                             airfoil_drag, cdi)

    return aspect_ratio, standard_mean_chord, lift_force, drag_coefficient, drag_force, vcl, take_off_distance, landing_distance


def get_aspect_ratio(wingspan, wing_area):
    return math.pow(wingspan, 2) / wing_area if wing_area > 0 else 0


def get_lift_force(air_density, flight_velocity, wing_area, lift_coefficient):
    return (0.5 * air_density) * math.pow(flight_velocity, 2) * wing_area * lift_coefficient


def get_drag_coefficient(profile_drag, lift_coefficient, aspect_ratio):
    cdi = get_induced_drag(lift_coefficient, aspect_ratio)
    return cdi + profile_drag


def get_oswald_factor(aspect_ratio):
    return 1 / (1.05 + 0.007 * math.pi * aspect_ratio)


def get_induced_drag(lift_coefficient, aspect_ratio):
    e = get_oswald_factor(aspect_ratio)
    return math.pow(lift_coefficient, 2) / (math.pi * e * aspect_ratio)


def get_drag_force(air_density, flight_velocity, wing_area, drag_coefficient):
    return 0.5 * air_density * math.pow(flight_velocity, 2) * wing_area * drag_coefficient


def get_stall_speed(air_density, lift_force, wing_area, cl_max):
    weight = lift_force * 0.9
    return math.sqrt((2 * weight) / (air_density * wing_area * cl_max))


def get_ground_effect(aspect_ratio):
    return math.pow(4.8 / aspect_ratio, 2) / (1 + math.pow(4.8 / aspect_ratio, 2))


def get_take_off_lift_force(air_density, vcl, wing_area, cl):
    return 0.5 * air_density * (math.pow(0.7 * vcl, 2) * wing_area * cl)


def get_take_off_drag_force(air_density, vcl, wing_area, profile_drag, ground_effect, cdi):
    return 0.5 * air_density * (math.pow(0.7 * vcl, 2) * wing_area * (profile_drag + (ground_effect * cdi)))


def get_take_off_and_landing_distances(wing_area, aspect_ratio, lift_force, air_density_initial, vcl, trust,
                                       airfoil_lift_coefficient, airfoil_drag, cdi):
    weight = lift_force * 0.9
    ground_effect = get_ground_effect(aspect_ratio)

    L = get_take_off_lift_force(air_density_initial, vcl, wing_area,
                                airfoil_lift_coefficient)

    D = get_take_off_drag_force(air_density_initial, vcl, wing_area,
                                airfoil_drag, ground_effect, cdi)

    return abs(
        (1.44 * math.pow(weight, 2)) / (9.801 * air_density_initial * wing_area * airfoil_lift_coefficient * (
                trust - (D + 0.05 * (weight - L))))), \
        abs((1.69 * math.pow(weight, 2)) / (
                9.801 * air_density_initial * wing_area * airfoil_lift_coefficient * (D + 0.05 * (weight - L))))
