import math
import os

import numpy as np
import pandas as pd
from deap import base
from deap import creator
from deap import tools
import random
from Services.CSVService import get_aerodynamic_profile, get_batteries, get_solar_cells
from Services.SizingUAVService import SizingUAVService
import plotly.graph_objects as go


class MPOService:
    def __init__(self, low_flight_velocity, upper_flight_velocity, low_payload_power, upper_payload_power,
                 low_payload_weight, upper_payload_weight, solar_energy, air_density, altitude_initial,
                 altitude_final, airfoil_name, battery_name, solar_cell_name, select_airfoil, select_battery,
                 select_solar_cell, fitness_strategy, low_flight_endurance,
                 upper_flight_endurance, low_solar_cell_wing_covering, upper_solar_cell_wing_covering,
                 low_propulsion_efficiency, upper_propulsion_efficiency, low_wing_area, upper_wing_area,
                 low_wingspan, upper_wingspan, airframe_weight=0, propulsion_weight=0):

        super().__init__()

        # Variables
        self.solar_cell_names = None
        self.solar_cell_file = None
        self.battery_names = None
        self.battery_file = None
        self.airfoil_names = None
        self.aerodynamic_profile = None
        self.selected_battery = None
        self.selected_solar_cell = None
        self.best_individual = []
        self.airfoil_list = []
        self.solar_cell_list = []
        self.battery_list = []

        # Genetic Algorithm constants
        self.POPULATION_SIZE = 400
        self.P_CROSSOVER = 0.9  # probability for crossover
        self.P_MUTATION = 0.1  # probability for mutating an individual
        self.MAX_GENERATIONS = 300

        # Solar UAV wings constraints
        self.low_wing_area = low_wing_area
        self.upper_wing_area = upper_wing_area
        self.low_wingspan = low_wingspan
        self.upper_wingspan = upper_wingspan

        self.low_solar_cell_wing_covering = low_solar_cell_wing_covering
        self.upper_solar_cell_wing_covering = upper_solar_cell_wing_covering

        self.low_propulsion_efficiency = low_propulsion_efficiency
        self.upper_propulsion_efficiency = upper_propulsion_efficiency

        # Solar UAV Mission constraints
        self.low_flight_endurance = low_flight_endurance
        self.upper_flight_endurance = upper_flight_endurance
        self.low_flight_velocity = low_flight_velocity
        self.upper_flight_velocity = upper_flight_velocity

        self.low_payload_power = low_payload_power
        self.upper_payload_power = upper_payload_power
        self.low_payload_weight = low_payload_weight
        self.upper_payload_weight = upper_payload_weight

        self.solar_energy = solar_energy
        self.air_density = air_density
        self.cruise_altitude = altitude_initial
        self.takeoff_altitude = altitude_final
        self.airfoil_name = airfoil_name
        self.battery_name = battery_name
        self.airfoil_name = airfoil_name
        self.solar_cell_name = solar_cell_name

        self.airfoil_select = select_airfoil
        self.battery_select = select_battery
        self.solar_cell_select = select_solar_cell

        self.airframe_weight = airframe_weight
        self.propulsion_weight = propulsion_weight

        # Set fitness strategy
        self.fitness_strategy = fitness_strategy
        self.fitness_index = 0
        self.fitness_weight = 1

        # set the random seed:
        self.RANDOM_SEED = 47
        random.seed(self.RANDOM_SEED)

        self.toolbox = base.Toolbox()

        # get all database models (Airfoil, Battery, Solar Cells)
        self.get_database_parameters()

        # set fitness weight from fitness strategy
        self.set_fitness_weight()

        # define a single objective, maximizing fitness strategy:
        creator.create("FitnessMax", base.Fitness, weights=(self.fitness_weight,))

        # create an operator that returns a model from an index:
        self.toolbox.register("selectAirfoil", self.select_airfoil)
        self.toolbox.register("selectBattery", self.select_battery)
        self.toolbox.register("selectSolarCell", self.select_solar_cell)

        # create the Individual class based on list:
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # create the individual operator to fill up an Individual instance:
        self.toolbox.register("individualCreator", tools.initIterate, creator.Individual,
                              self.random_float_parameters_for_solar_uav)

        # create the population operator to generate a list of individuals:
        self.toolbox.register("populationCreator", tools.initRepeat, list, self.toolbox.individualCreator)

        # define fitness function
        self.toolbox.register("evaluate", self.solar_uav_fitness)

        # genetic operators:

        # Tournament selection with tournament size of 3:
        self.toolbox.register("select", tools.selTournament, tournsize=3)

        # Gaussian Mutation - indpb: Independent probability for each attribute to be flipped
        self.toolbox.register("mutate", tools.mutGaussian, mu=0.0005, sigma=0.00001, indpb=0.1)

        # Simulated binary crossover:
        self.toolbox.register("mate", tools.cxSimulatedBinaryBounded, eta=1,
                              low=[self.low_wing_area, self.low_wingspan, 0,
                                   self.low_flight_velocity, self.low_flight_endurance, self.low_payload_weight,
                                   self.low_payload_power,
                                   0, 0, self.low_solar_cell_wing_covering, self.low_propulsion_efficiency],

                              up=[self.upper_wing_area, self.upper_wingspan, len(self.airfoil_list) - 0.1,
                                  self.upper_flight_velocity, self.upper_flight_endurance, self.upper_payload_weight,
                                  self.upper_payload_power, len(self.solar_cell_list) - 0.1,
                                  len(self.battery_list) - 0.1, self.upper_solar_cell_wing_covering,
                                  self.upper_propulsion_efficiency])

    def main(self):
        # create initial population (generation 0):
        population = self.toolbox.populationCreator(n=self.POPULATION_SIZE)
        generationCounter = 0

        # calculate fitness tuple for each individual in the population:
        fitnessValues = list(map(self.toolbox.evaluate, population))

        for individual, fitnessValue in zip(population, fitnessValues):
            individual.fitness.values = fitnessValue

        fitnessValues = [individual.fitness.values for individual in population]

        # initialize statistics accumulators:
        maxFitnessValues = []
        meanFitnessValues = []
        wing_area_list = []
        wingspan_list = []
        payload_power_list = []
        payload_weight_list = []
        flight_speed_list = []
        flight_endurance_list = []
        propulsion_efficiency_list = []
        solar_cell_wing_area_list = []


        # main evolutionary loop:
        # stop if the number of generations exceeded the preset value
        while generationCounter < self.MAX_GENERATIONS:
            # update counter:
            generationCounter += 1

            # apply the selection operator, to select the next generation's individuals:
            offspring = self.toolbox.select(population, len(population))

            # clone the selected individuals:
            offspring = list(map(self.toolbox.clone, offspring))

            # apply the crossover operator to pairs of offspring:
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.P_CROSSOVER:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < self.P_MUTATION:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # calculate fitness for the individuals with no previous calculated fitness value:
            freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
            freshFitnessValues = list(map(self.toolbox.evaluate, freshIndividuals))

            for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
                individual.fitness.values = fitnessValue

            # replace the current population with the offspring:
            population[:] = offspring

            # collect fitnessValues into a list, update statistics and print:
            fitnessValues = [ind.fitness.values[0] for ind in population]

            maxFitness = max(fitnessValues)
            meanFitness = sum(fitnessValues) / len(population)
            maxFitnessValues.append(maxFitness)
            meanFitnessValues.append(meanFitness)
            print("- Generation {}: Max Fitness = {}, Avg Fitness = {}".format(generationCounter, maxFitness,
                                                                               meanFitness))

            # find and print best individual:
            best_index = fitnessValues.index(max(fitnessValues))
            best_individual = population[best_index]

            self.best_individual = best_individual

            wing_area_list.append(best_individual[0])
            wingspan_list.append(best_individual[1])
            flight_speed_list.append(best_individual[3])
            flight_endurance_list.append(best_individual[4])
            payload_power_list.append(best_individual[5])
            payload_weight_list.append(best_individual[6] * 9.81)
            propulsion_efficiency_list.append(int(best_individual[10] * 100))
            solar_cell_wing_area_list.append(best_individual[0] * best_individual[9])

            print("Best Individual = ", best_individual, "\n",
                  "Aerodynamic Profile: "
                  + self.airfoil_name,
                  " Solar Cell: "
                  + self.solar_cell_name,
                  " Battery: "
                  + self.battery_name,
                  "\n")

        # Genetic Algorithm is done - plot statistics:
        self.show_traces(wing_area_list, wingspan_list, flight_speed_list, flight_endurance_list, payload_power_list,
                         payload_weight_list, propulsion_efficiency_list, solar_cell_wing_area_list)

    # Fitness function of Solar UAV
    def solar_uav_fitness(self, individual):
        aerodynamic_profile = None
        wing_area = individual[0]
        wingspan = individual[1]
        airfoil_index = individual[2]
        flight_speed = individual[3]
        flight_endurance = individual[4]
        payload_weight = individual[5]
        payload_power = individual[6]
        solar_cell_index = individual[7]
        battery_index = individual[8]
        solar_cell_wing_covering = individual[9]
        propulsion_efficiency = individual[10]

        if not self.airfoil_select:
            aerodynamic_profile = self.airfoil_list[int(airfoil_index)]
            self.airfoil_name = aerodynamic_profile.model
        else:
            aerodynamic_profile = self.aerodynamic_profile

        if not self.battery_select:
            battery = self.battery_list[int(battery_index)]
            self.battery_name = battery.name
        else:
            battery = self.selected_battery
            self.battery_name = battery.name

        if not self.solar_cell_select:
            solar_cell = self.solar_cell_list[int(solar_cell_index)]
            self.solar_cell_name = solar_cell.name
        else:
            solar_cell = self.selected_solar_cell
            self.solar_cell_name = solar_cell.name

        solar_uav = SizingUAVService.sizing_uav(self.takeoff_altitude, self.cruise_altitude, flight_speed,
                                                flight_endurance, self.solar_energy, payload_power, payload_weight,
                                                wing_area, wingspan, aerodynamic_profile, solar_cell, battery,
                                                propulsion_efficiency, solar_cell_wing_covering, self.airframe_weight,
                                                self.propulsion_weight)
        return solar_uav[self.fitness_index],

    def random_float_parameters_for_solar_uav(self):
        return [np.random.uniform(self.low_wing_area, self.upper_wing_area),
                np.random.uniform(self.low_wingspan, self.upper_wingspan),
                np.random.uniform(0, len(self.airfoil_list) - 0.1),
                np.random.uniform(self.low_flight_velocity, self.upper_flight_velocity),
                np.random.uniform(self.low_flight_endurance, self.upper_flight_endurance),
                np.random.uniform(self.low_payload_weight, self.upper_payload_weight),
                np.random.uniform(self.low_payload_power, self.upper_payload_power),
                np.random.uniform(0, len(self.solar_cell_list) - 0.1),
                np.random.uniform(0, len(self.battery_list) - 0.1),
                np.random.uniform(self.low_solar_cell_wing_covering, self.upper_solar_cell_wing_covering),
                np.random.uniform(self.low_propulsion_efficiency, self.upper_propulsion_efficiency), ]

    def select_airfoil(self, i):
        index = int(math.floor(i * len(self.airfoil_names)))
        aerodynamic_profile_name = self.airfoil_names[index]
        return aerodynamic_profile_name[:-4]

    def select_solar_cell(self, i):
        index = int(math.floor(i))
        solar_cell_name = self.solar_cell_names[index]
        return solar_cell_name

    def select_battery(self, i):
        index = int(math.floor(i))
        battery_name = self.battery_names[index]
        return battery_name

    def get_database_parameters(self):
        # Get Airfoil Model by model name
        if self.airfoil_name != 'Select by Genetic Algorithm':
            self.aerodynamic_profile = get_aerodynamic_profile(self.airfoil_name)

        if self.battery_name != 'Select by Genetic Algorithm':
            self.selected_battery = get_batteries(self.battery_name)

        if self.solar_cell_name != 'Select by Genetic Algorithm':
            self.selected_solar_cell = get_solar_cells(self.solar_cell_name)

        # Get All Airfoil Models from database
        self.airfoil_names = os.listdir('../Database/Airfoils')

        for name in self.airfoil_names:
            airfoil = get_aerodynamic_profile(name[:-4])
            airfoil.model = name[:-4]
            self.airfoil_list.append(airfoil)

        # Get All Battery Models from database
        self.battery_file = pd.read_csv('../Database/Batteries/Batteries.csv')
        self.battery_names = self.battery_file.Name

        for name in self.battery_names:
            battery = get_batteries(name)
            battery.name = name
            self.battery_list.append(battery)

        # Get All Solar Cell Models from database
        self.solar_cell_file = pd.read_csv('../Database/Solar Cells/Solar Cell.csv')
        self.solar_cell_names = self.solar_cell_file.Name

        for name in self.solar_cell_names:
            solar_cell = get_solar_cells(name)
            solar_cell.name = name
            self.solar_cell_list.append(solar_cell)

    # Set Fitness weight
    def set_fitness_weight(self):
        if self.fitness_strategy == 'Payload Weight (Max)':
            self.fitness_weight = 0.25
            self.fitness_index = 21  # payload_weight
        if self.fitness_strategy == 'Wing Area (Min)':
            self.fitness_index = 1  # payload_weight
            self.fitness_weight = -0.1  # payload_weight
        if self.fitness_strategy == 'Payload Power (Max)':
            self.fitness_weight = 0.25
            self.fitness_index = 12
        if self.fitness_strategy == 'Flight Endurance (Max)':
            self.fitness_index = 5
            self.fitness_weight = 0.01

        # self.fitness_weight = 1
        # self.fitness_index = 21
        # self.fitness_strategy = 'Payload Weight (Max)'

    def show_traces(self, wing_area_list, wingspan_list, flight_speed_list, flight_endurance_list, payload_power_list,
                    payload_weight_list, propulsion_efficiency_list, solar_cell_wing_area):
        fig = go.Figure()
        fig_2 = go.Figure()

        fig.add_trace(go.Scatter(x=list(range(1, self.MAX_GENERATIONS)), y=wing_area_list,
                                 mode='markers',
                                 marker=dict(
                                     color='#0dffd3',
                                     size=10,
                                     symbol="diamond",
                                     line=dict(
                                         width=1,
                                         color="DarkSlateGrey"
                                     )),
                                 name="Wing Area (m)"
                                 ))

        fig.add_trace(go.Scatter(x=list(range(1, self.MAX_GENERATIONS)), y=wingspan_list,
                                 mode='markers',
                                 marker=dict(
                                     color='#f3ff05',
                                     size=10,
                                     symbol="hexagon",
                                     line=dict(
                                         width=1,
                                         color="DarkSlateGrey"
                                     )),
                                 name="Wingspan (m)"
                                 ))

        fig.add_trace(go.Scatter(x=list(range(1, self.MAX_GENERATIONS)), y=flight_speed_list,
                                 mode='markers',
                                 marker=dict(
                                     color='#ff4c05',
                                     size=10,
                                     symbol="square",
                                     line=dict(
                                         width=1,
                                         color="DarkSlateGrey"
                                     )),
                                 name="Flight Speed (m/s)"
                                 ))

        fig.add_trace(go.Scatter(x=list(range(1, self.MAX_GENERATIONS)), y=flight_endurance_list,
                                 mode='markers',
                                 marker=dict(
                                     color='#b405ff',
                                     size=10,
                                     symbol="circle",
                                     line=dict(
                                         width=1,
                                         color="DarkSlateGrey"
                                     )),
                                 name="Flight Endurance (h)"
                                 ))

        fig.add_trace(go.Scatter(x=list(range(1, self.MAX_GENERATIONS)), y=payload_power_list,
                                 mode='markers',
                                 marker=dict(
                                     color='#ff0565',
                                     size=10,
                                     symbol="diamond-wide",
                                     line=dict(
                                         width=1,
                                         color="DarkSlateGrey"
                                     )),
                                 name="Payload Power (W)"
                                 ))

        fig.add_trace(go.Scatter(x=list(range(1, self.MAX_GENERATIONS)), y=payload_weight_list,
                                 mode='markers',
                                 marker=dict(
                                     color='#05d1ff',
                                     size=10,
                                     symbol="pentagon",
                                     line=dict(
                                         width=1,
                                         color="DarkSlateGrey"
                                     )),
                                 name="Payload Weight (N)"
                                 ))

        fig.add_trace(go.Scatter(x=list(range(1, self.MAX_GENERATIONS)), y=solar_cell_wing_area,
                                 mode='markers',
                                 marker=dict(
                                     color='#ffe205',
                                     size=10,
                                     symbol="x",
                                     line=dict(
                                         width=1,
                                         color="DarkSlateGrey"
                                     )),
                                 name="Solar Panel Area (m)"
                                 ))

        fig_2.add_trace(go.Scatter(x=list(range(1, self.MAX_GENERATIONS)), y=propulsion_efficiency_list,
                                   mode='markers',
                                   marker=dict(
                                       color='#1f8c26',
                                       size=10,

                                   ),
                                   name="Propulsion Efficiency (%)"
                                   ))

        fig.update_layout(title='Multi-Parameter Optimization - ' + self.fitness_strategy,
                          xaxis_title='Generation',
                          yaxis_title='',
                          font=dict(
                              size=25,
                          ))

        fig_2.update_layout(title='',
                            xaxis_title='Generation',
                            yaxis_title='',
                            font=dict(
                                size=18,
                            ))

        fig.show()
        # fig_2.show()
