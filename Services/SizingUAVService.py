from Constants import Atmosphere
from Models import AerodynamicModel, PowerModel, MassEstimationModel
from Models.SolarCell import SolarCell
from Models.Battery import Battery
from Models.AerodynamicProfile import AerodynamicProfile


class SizingUAVService:

    @staticmethod
    def sizing_uav(takeoff_altitude, cruise_altitude, flight_speed, flight_endurance, solar_energy, payload_power,
                   payload_weight, wing_area, wingspan, aerodynamic_profile=AerodynamicProfile(),
                   solar_cell=SolarCell(),
                   battery=Battery(), propulsion_efficiency=0, solar_cell_wing_covering=1, airframe_weight=0,
                   propulsion_weight=0, simulation=0):

        air_density_final = Atmosphere.get_air_density(takeoff_altitude)
        air_density_initial = Atmosphere.get_air_density(cruise_altitude)

        panel_area = wing_area * solar_cell_wing_covering

        aspect_ratio, standard_mean_chord, lift_force, drag_coefficient, drag_force, vcl, take_off_distance, \
            landing_distance = AerodynamicModel.model(wingspan, wing_area,
                                                      air_density_initial,
                                                      flight_speed,
                                                      aerodynamic_profile.lift_coefficient,
                                                      aerodynamic_profile.profile_drag)

        aircraft_assumed_weight = lift_force * 0.9

        propulsion_power, power_for_take_off, climb_power, total_climb_power, time_to_take_off, time_to_climb, \
            time_to_landing = PowerModel.model(air_density_final, wing_area, aspect_ratio,
                                               drag_coefficient,
                                               aerodynamic_profile.lift_coefficient,
                                               aircraft_assumed_weight,
                                               payload_power,
                                               propulsion_efficiency,
                                               drag_force, vcl,
                                               takeoff_altitude,
                                               cruise_altitude,
                                               flight_speed,
                                               take_off_distance,
                                               landing_distance)

        airframe_estimated_weight, solar_panel_estimated_weight, battery_estimated_weight, \
            propulsion_group_estimated_weight, \
            aircraft_total_weight = MassEstimationModel.model(wing_area,
                                                              aspect_ratio,
                                                              propulsion_power,
                                                              panel_area,
                                                              solar_cell.weight,
                                                              solar_cell.area,
                                                              solar_cell.encapsulation,
                                                              battery.energy_density,
                                                              battery.efficiency,
                                                              flight_endurance,
                                                              total_climb_power,
                                                              payload_weight,
                                                              airframe_weight,
                                                              propulsion_weight)

        total_time_to_climb = time_to_climb * 2 + time_to_landing + time_to_take_off

        total_energy = (propulsion_power * flight_endurance) + total_climb_power
        solar_energy_collected = solar_energy * panel_area * solar_cell.efficiency * 0.84
        mass_power_ratio = aircraft_total_weight / propulsion_power

        if 8 <= aspect_ratio <= 20 and aircraft_total_weight <= aircraft_assumed_weight \
                and total_energy < solar_energy_collected:

            return [wing_area, wingspan, aspect_ratio, standard_mean_chord, flight_speed, flight_endurance,
                    lift_force, drag_coefficient, drag_force, vcl, take_off_distance, landing_distance,
                    payload_power, power_for_take_off, climb_power, total_climb_power, propulsion_power,
                    time_to_take_off, time_to_climb, time_to_landing, total_time_to_climb, payload_weight,
                    airframe_estimated_weight, solar_panel_estimated_weight, battery_estimated_weight,
                    propulsion_group_estimated_weight, aircraft_total_weight, total_energy,
                    solar_energy_collected, mass_power_ratio, panel_area]
        else:

            if simulation == 0:
                return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            return [wing_area, wingspan, aspect_ratio, standard_mean_chord, flight_speed, flight_endurance,
                    lift_force, drag_coefficient, drag_force, vcl, take_off_distance, landing_distance,
                    payload_power, power_for_take_off, climb_power, total_climb_power, propulsion_power,
                    time_to_take_off, time_to_climb, time_to_landing, total_time_to_climb, payload_weight,
                    airframe_estimated_weight, solar_panel_estimated_weight, battery_estimated_weight,
                    propulsion_group_estimated_weight, aircraft_total_weight, total_energy,
                    solar_energy_collected, mass_power_ratio
                    ]
