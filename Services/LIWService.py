from Models.SolarCell import SolarCell
from Models.Battery import Battery
from Models.AerodynamicProfile import AerodynamicProfile
from Services.SizingUAVService import SizingUAVService


class LIWService:
    @staticmethod
    def sizing_uav_list(takeoff_altitude, cruise_altitude, flight_speed, flight_endurance, solar_energy,
                        payload_power, payload_weight, solar_cell=SolarCell(),
                        battery=Battery(), aerodynamic_profile=AerodynamicProfile(), propulsion_efficiency=0,
                        solar_cell_wing_covering=1):

        solar_uav_list = []

        wingspan = 1

        while wingspan <= 4:
            wingspan += 0.2
            wing_area = 0.15
            while wing_area < 1.2:
                wing_area += 0.1

                solar_uav = SizingUAVService.sizing_uav(takeoff_altitude, cruise_altitude, flight_speed,
                                                        flight_endurance, solar_energy, payload_power, payload_weight,
                                                        wing_area, wingspan, aerodynamic_profile, solar_cell, battery,
                                                        propulsion_efficiency, solar_cell_wing_covering)

                if sum(solar_uav) > 0:
                    solar_uav_list.append(solar_uav)

        if len(solar_uav_list) == 0:
            solar_uav = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            solar_uav_list.append(solar_uav)
            return solar_uav_list

        solar_uav_list = LIWService.sort_uav_list(solar_uav_list)

        return solar_uav_list

    @staticmethod
    def sort_uav_list(uav_list):
        wing_area_list = []
        indexes = []
        for count, uav in enumerate(uav_list):
            if (uav[0], uav[1]) not in wing_area_list:
                wing_area_list.append((uav[0], uav[1]))
                indexes.append(count)

        unique_solar_uav_list = []

        for index in indexes:
            unique_solar_uav_list.append(uav_list[index])

        unique_solar_uav_list.sort(key=lambda x: x[27], reverse=True)

        return unique_solar_uav_list
