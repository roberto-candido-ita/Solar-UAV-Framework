import pandas as pd
from Models.AerodynamicProfile import AerodynamicProfile
from Models.Battery import Battery
from Models.SolarCell import SolarCell


def get_aerodynamic_profile(name):
    file = pd.read_csv('../Database/Airfoils/' + name + '.csv', skiprows=[i for i in range(100, 120)])
    alphas = file.Alpha
    cls = file.Cl
    cds = file.Cd
    cdps = file.Cdp

    max_cl_cd = cls[0] / cds[0]
    index = 0

    airfoil = AerodynamicProfile()

    for i in range(len(alphas)):
        if cls[i] / cds[i] > max_cl_cd:
            max_cl_cd = cls[i] / cds[i]
            index = i

    airfoil.profile_drag = cdps[index]
    airfoil.lift_coefficient = cls[index]
    airfoil.cl_cd = max_cl_cd
    airfoil.model = name
    return airfoil


def get_batteries(name):
    file = pd.read_csv('../Database/Batteries/Batteries.csv')
    names = file.Name
    densities = file.Energy_density
    manufactures = file.Manufacturer
    voltages = file.Voltage
    currents = file.Current
    efficiencys = file.Efficiency

    battery = Battery()
    index = 0

    for i in range(len(names)):
        if names[i] == name:
            index = i
            battery.name = names[i]

    battery.voltage = voltages[index]
    battery.current = currents[index]
    battery.efficiency = efficiencys[index]
    battery.energy_density = densities[index]
    battery.manufacturer = manufactures[index]
    battery.unity_power = battery.voltage * battery.current

    return battery


def get_solar_cells(name):
    solar_cell = SolarCell()

    file = pd.read_csv('../Database/Solar Cells/Solar Cell.csv')
    names = file.Name
    efficiencies = file.Efficiency
    weights = file.Weight
    areas = file.Area
    encapsulation_weights = file.Encapsulation_weight
    index = 0

    for i in range(len(names)):
        if names[i] == name:
            index = i
            solar_cell.name = names[i]

    solar_cell.area = areas[index]
    solar_cell.weight = weights[index]
    solar_cell.encapsulation = encapsulation_weights[index]
    solar_cell.efficiency = efficiencies[index]

    return solar_cell
