import json
from operator import itemgetter

import pandas as pd
from PyQt5 import QtWidgets
import geopy.distance
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QHBoxLayout, QWidget, \
    QVBoxLayout, QMessageBox, QSlider, QGridLayout, QSplitter, QRadioButton, QSpinBox, QDoubleSpinBox
from PyQt5.uic.properties import QtCore, QtGui

from Services.CSVService import get_aerodynamic_profile, get_batteries, get_solar_cells
from Services.PDFService import create_pdf
from Services.SizingUAVService import SizingUAVService
from Views.MapView import Map
from Views.css.Styles import Style
from Constants import Atmosphere
import os

from Services.MPOService import MPOService as uav_optimization

widget_map = QWidget


class AdaptUAVView(QMainWindow):
    def __init__(self):
        super().__init__()
        ######################## Variables ###################################
        self.map = Map()
        self.cruise_altitude = 0
        self.takeoff_altitude = 0
        self.velocity_min = 0
        self.autonomy = 0
        self.payload_power_min = 0
        self.payload_weight_min = 0
        self.aerodynamic_profile = ''
        self.solar_cell = ''
        self.battery = ''
        self.air_density = 1.2250
        self.distances = []
        self.flight_endurance_max = int(self.map.hours_without_sunlight)//2
        self.select_airfoil = True
        self.select_battery = True
        self.select_solar_cell = True
        self.airfoil_name = ''
        self.fitness_strategy = 'Flight Endurance (Max)'
        self.battery_name = ''
        self.solar_cell_name = ''
        self.propulsion_efficiency = 0.5
        self.wing_area = 0
        self.wingspan = 0
        self.propulsion_group_weight = 0
        self.airframe_weight = 0

        self.location = ''
        self.solar_energy = 0
        self.solar_energy = 0
        self.hourly_radiation = []
        self.date = 0
        self.hours_without_sunlight = self
        self.index = 4

        ######################## End of Variables ##################################

        ######################## Layouts Definition  ###############################
        self.layout_left = QVBoxLayout()
        self.layout_right = QVBoxLayout()
        self.layout_center = QHBoxLayout()
        self.button_add_layout = QHBoxLayout()
        self.button_size_layout = QHBoxLayout()
        self.main_layout = QVBoxLayout()
        self.layout_take_off_altitude = QVBoxLayout()
        self.layout_cruise_altitude = QVBoxLayout()
        self.layout_velocity_min = QVBoxLayout()

        self.layout_payload_power_min = QVBoxLayout()
        self.layout_payload_weight_min = QVBoxLayout()
        self.layout_flight_endurance_min = QVBoxLayout()
        self.layout_airfoil_selection = QVBoxLayout()
        self.layout_battery_selection = QVBoxLayout()
        self.layout_solar_cell_selection = QVBoxLayout()
        self.layout_propulsion_efficiency = QVBoxLayout()
        self.layout_flight_endurance_max = QVBoxLayout()
        self.layout_slider_propulsion_efficiency = QHBoxLayout()
        self.layout_slider_flight_endurance = QHBoxLayout()
        self.layout_wing_area = QVBoxLayout()
        self.layout_wingspan = QVBoxLayout()
        self.layout_airframe_weight = QVBoxLayout()
        self.layout_propulsion_group_weight = QVBoxLayout()
        self.layout_altitude = QHBoxLayout()
        self.layout_velocity = QHBoxLayout()
        self.layout_payload_power = QHBoxLayout()
        self.layout_propulsion = QHBoxLayout()
        self.layout_payload_weight = QHBoxLayout()

        ############################ End of Layouts definition #############################

        ###########################  Labels  ####################################

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Janela')

        self.take_off_altitude_text = QLabel('Take off Altitude (m)')
        self.cruise_altitude_text = QLabel('Cruise Altitude (m)')
        self.velocity_min_text = QLabel('Velocity (m/s)')

        self.payload_power_min_text = QLabel('Payload Power (W)')
        self.payload_weight_min_text = QLabel('Payload Weight (Kg)')
        self.propulsion_efficiency_text = QLabel('Propulsion Efficiency (%)')
        self.flight_endurance_text = QLabel('Max Flight Endurance (h)')
        self.airfoil_selection_text = QLabel("Select Airfoil")
        self.battery_selection_text = QLabel('Battery Model')
        self.wing_area_text = QLabel('Wing Area (m)')
        self.wingspan_text = QLabel('Wingspan (m)')
        self.airframe_weight_text = QLabel('Airframe Weight (kg)')
        self.propulsion_group_weight_text = QLabel('Propulsion Group Weight (kg)')
        self.solar_cell_selection_text = QLabel('Solar Cell Model')

        self.propulsion_efficiency_label = QLabel('50', self)
        self.flight_endurance_label = QLabel(str(int(self.map.hours_without_sunlight)//2), self)

        font = QFont("Arial", 14)

        self.take_off_altitude_text.setFont(font)
        self.cruise_altitude_text.setFont(font)
        self.velocity_min_text.setFont(font)

        self.payload_power_min_text.setFont(font)
        self.payload_weight_min_text.setFont(font)

        self.propulsion_efficiency_text.setFont(font)
        self.flight_endurance_text.setFont(font)
        self.airfoil_selection_text.setFont(font)
        self.battery_selection_text.setFont(font)
        self.solar_cell_selection_text.setFont(font)
        self.propulsion_efficiency_label.setFont(font)
        self.flight_endurance_label.setFont(font)

        self.wing_area_text.setFont(font)
        self.wingspan_text.setFont(font)
        self.airframe_weight_text.setFont(font)
        self.propulsion_group_weight_text.setFont(font)

        self.take_off_altitude_text.setStyleSheet(Style.label)
        self.cruise_altitude_text.setStyleSheet(Style.label)
        self.velocity_min_text.setStyleSheet(Style.label)

        self.payload_power_min_text.setStyleSheet(Style.label)
        self.payload_weight_min_text.setStyleSheet(Style.label)

        self.propulsion_efficiency_text.setStyleSheet(Style.label)
        self.flight_endurance_text.setStyleSheet(Style.label)

        self.airfoil_selection_text.setStyleSheet(Style.label)
        self.battery_selection_text.setStyleSheet(Style.label)
        self.solar_cell_selection_text.setStyleSheet(Style.label)
        self.propulsion_efficiency_label.setStyleSheet(Style.label)
        self.flight_endurance_label.setStyleSheet(Style.label)

        self.wing_area_text.setStyleSheet(Style.label)
        self.wingspan_text.setStyleSheet(Style.label)
        self.airframe_weight_text.setStyleSheet(Style.label)
        self.propulsion_group_weight_text.setStyleSheet(Style.label)
        ########################### End of Labels  ################################

        ###########################  Imputs Boxes    ##############################

        self.input_take_off_altitude = QSpinBox(self)
        self.input_take_off_altitude.move(10, 10)
        self.input_take_off_altitude.resize(150, 30)
        self.input_take_off_altitude.setMaximum(2400)
        self.input_take_off_altitude.setSingleStep(100)

        self.input_cruise_altitude = QSpinBox(self)
        self.input_cruise_altitude.move(10, 10)
        self.input_cruise_altitude.resize(150, 30)
        self.input_cruise_altitude.setMaximum(2500)
        self.input_cruise_altitude.setSingleStep(100)

        self.input_velocity_min = QDoubleSpinBox(self)
        self.input_velocity_min.move(10, 10)
        self.input_velocity_min.resize(150, 30)
        self.input_velocity_min.setMinimum(6.0)
        self.input_velocity_min.setMaximum(13.9)
        self.input_velocity_min.setSingleStep(0.1)

        self.input_wing_area = QDoubleSpinBox(self)
        self.input_wing_area.move(10, 10)
        self.input_wing_area.resize(150, 30)
        self.input_wing_area.setMinimum(0.1)
        self.input_wing_area.setMaximum(1.2)
        self.input_wing_area.setSingleStep(0.1)

        self.input_wingspan = QDoubleSpinBox(self)
        self.input_wingspan.move(10, 10)
        self.input_wingspan.resize(150, 30)
        self.input_wingspan.setMinimum(1.0)
        self.input_wingspan.setMaximum(4.0)
        self.input_wingspan.setSingleStep(0.1)

        self.input_airframe_weight = QDoubleSpinBox(self)
        self.input_airframe_weight.move(10, 10)
        self.input_airframe_weight.resize(150, 30)
        self.input_airframe_weight.setMinimum(0.01)
        self.input_airframe_weight.setMaximum(2.0)
        self.input_airframe_weight.setSingleStep(0.1)
        self.input_airframe_weight.setDecimals(3)

        self.input_propulsion_group_weight = QDoubleSpinBox(self)
        self.input_propulsion_group_weight.move(10, 10)
        self.input_propulsion_group_weight.resize(150, 30)
        self.input_propulsion_group_weight.setMinimum(0.001)
        self.input_propulsion_group_weight.setMaximum(1.0)
        self.input_propulsion_group_weight.setSingleStep(0.001)
        self.input_propulsion_group_weight.setDecimals(3)

        self.input_payload_power_min = QDoubleSpinBox(self)
        self.input_payload_power_min.move(10, 10)
        self.input_payload_power_min.resize(200, 30)
        self.input_payload_power_min.setMinimum(0.001)
        self.input_payload_power_min.setMaximum(4.90)
        self.input_payload_power_min.setSingleStep(0.001)
        self.input_payload_power_min.setDecimals(3)

        self.input_payload_weight_min = QDoubleSpinBox(self)
        self.input_payload_weight_min.move(10, 10)
        self.input_payload_weight_min.resize(200, 30)
        self.input_payload_weight_min.setMinimum(0.001)
        self.input_payload_weight_min.setMaximum(0.95)
        self.input_payload_weight_min.setSingleStep(0.01)
        self.input_payload_weight_min.setDecimals(3)

        self.input_take_off_altitude.setStyleSheet(Style.spin_box)
        self.input_cruise_altitude.setStyleSheet(Style.spin_box)
        self.input_velocity_min.setStyleSheet(Style.double_spin_box)
        self.input_payload_power_min.setStyleSheet(Style.double_spin_box)
        self.input_payload_weight_min.setStyleSheet(Style.double_spin_box)
        self.input_wing_area.setStyleSheet(Style.double_spin_box)
        self.input_wingspan.setStyleSheet(Style.double_spin_box)
        self.input_airframe_weight.setStyleSheet(Style.double_spin_box)
        self.input_propulsion_group_weight.setStyleSheet(Style.double_spin_box)
        ###########################  End of Imputs Boxes  ############################


        ###########################  Sliders   #######################################
        self.propulsion_efficiency_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.propulsion_efficiency_slider.setRange(20, 85)
        self.propulsion_efficiency_slider.setPageStep(1)
        self.propulsion_efficiency_slider.setValue(50)
        self.propulsion_efficiency_slider.setStyleSheet(Style.qslider)

        self.flight_endurance_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.flight_endurance_slider.setRange(1, int(self.map.hours_without_sunlight))
        self.flight_endurance_slider.setPageStep(1)
        self.flight_endurance_slider.setValue(int(self.map.hours_without_sunlight)//2)
        self.flight_endurance_slider.setStyleSheet(Style.qslider)

        self.propulsion_efficiency_slider.valueChanged.connect(self.update_propulsion_efficiency)
        self.flight_endurance_slider.valueChanged.connect(self.update_flight_endurance)

        ###########################  Combo Box   #####################################

        self.combo_box_airfoil_selection = QtWidgets.QComboBox(self)
        self.combo_box_airfoil_selection.move(10, 10)
        self.combo_box_airfoil_selection.resize(200, 30)

        self.combo_battery_selection = QtWidgets.QComboBox(self)
        self.combo_battery_selection.move(10, 10)
        self.combo_battery_selection.resize(200, 30)

        self.combo_solar_cell_selection = QtWidgets.QComboBox(self)
        self.combo_solar_cell_selection.move(10, 10)
        self.combo_solar_cell_selection.resize(200, 30)

        self.combo_box_airfoil_selection.setStyleSheet(Style.combo_box)
        self.combo_battery_selection.setStyleSheet(Style.combo_box)
        self.combo_solar_cell_selection.setStyleSheet(Style.combo_box)

        self.airfoil_names = os.listdir('../Database/Airfoils')

        self.fitness_strategy_names = ['Flight Endurance (Max)']

        for name in self.airfoil_names:
            self.combo_box_airfoil_selection.addItem(name[:-4])

        battery_file = pd.read_csv('../Database/Batteries/Batteries.csv')
        self.battery_names = battery_file.Name

        for name in self.battery_names:
            self.combo_battery_selection.addItem(name)

        solar_cell_file = pd.read_csv('../Database/Solar Cells/Solar Cell.csv')
        solar_cell_names = solar_cell_file.Name

        for name in solar_cell_names:
            self.combo_solar_cell_selection.addItem(name)

        ###########################  End Combo Box   #####################################

        ###########################  Buttons   ###########################################
        self.add_button = QPushButton('Add parameters', self)
        self.add_button.move(100, 100)
        self.add_button.resize(140, 50)

        self.add_button.setIcon(QIcon('../img/plus.png'))
        self.setStyleSheet(Style.window)
        self.add_button.setStyleSheet(Style.table_button)

        self.add_button.clicked.connect(self.add)

        self.sizing_button = QPushButton('Sizing', self)
        self.sizing_button.move(100, 100)
        self.sizing_button.resize(140, 50)

        self.sizing_button.setIcon(QIcon('../img/flash.png'))
        self.setStyleSheet(Style.window)
        self.sizing_button.setStyleSheet(Style.table_button)

        self.sizing_button.clicked.connect(self.sizing)

        ###########################  Layouts Arrangement   ###########################################
        self.layout_take_off_altitude.addWidget(self.take_off_altitude_text)
        self.layout_take_off_altitude.addWidget(self.input_take_off_altitude)

        self.layout_cruise_altitude.addWidget(self.cruise_altitude_text)
        self.layout_cruise_altitude.addWidget(self.input_cruise_altitude)

        self.layout_velocity_min.addWidget(self.velocity_min_text)
        self.layout_velocity_min.addWidget(self.input_velocity_min)

        self.layout_payload_power_min.addWidget(self.payload_power_min_text)
        self.layout_payload_power_min.addWidget(self.input_payload_power_min)

        self.layout_payload_weight_min.addWidget(self.payload_weight_min_text)
        self.layout_payload_weight_min.addWidget(self.input_payload_weight_min)

        self.layout_airframe_weight.addWidget(self.airframe_weight_text)
        self.layout_airframe_weight.addWidget(self.input_airframe_weight)

        self.layout_wing_area.addWidget(self.wing_area_text)
        self.layout_wing_area.addWidget(self.input_wing_area)

        self.layout_wingspan.addWidget(self.wingspan_text)
        self.layout_wingspan.addWidget(self.input_wingspan)

        self.layout_altitude.addLayout(self.layout_take_off_altitude)
        self.layout_altitude.addSpacing(10)
        self.layout_altitude.addLayout(self.layout_cruise_altitude)
        self.layout_altitude.addSpacing(30)

        self.layout_velocity.addLayout(self.layout_velocity_min)
        self.layout_velocity.addSpacing(10)
        self.layout_velocity.addLayout(self.layout_payload_power_min)
        self.layout_velocity.addSpacing(30)

        self.layout_payload_weight.addLayout(self.layout_payload_weight_min)
        self.layout_payload_weight.addSpacing(10)
        self.layout_payload_weight.addLayout(self.layout_airframe_weight)
        self.layout_payload_weight.addSpacing(30)

        self.layout_payload_power.addLayout(self.layout_wing_area)
        self.layout_payload_power.addSpacing(10)
        self.layout_payload_power.addLayout(self.layout_wingspan)
        self.layout_payload_power.addSpacing(30)

        self.layout_propulsion_group_weight.addWidget(self.propulsion_group_weight_text)
        self.layout_propulsion_group_weight.addSpacing(10)
        self.layout_propulsion_group_weight.addWidget(self.input_propulsion_group_weight)

        self.layout_propulsion.addLayout(self.layout_propulsion_group_weight)
        self.layout_propulsion.addSpacing(30)
        self.layout_propulsion.addLayout(self.layout_propulsion_efficiency)
        self.layout_propulsion.addSpacing(30)

        self.layout_left.addLayout(self.layout_altitude)
        self.layout_left.addSpacing(10)
        self.layout_left.addLayout(self.layout_velocity)
        self.layout_left.addSpacing(10)
        self.layout_left.addLayout(self.layout_payload_power)
        self.layout_left.addSpacing(10)
        self.layout_left.addLayout(self.layout_payload_weight)
        self.layout_left.addSpacing(10)
        self.layout_left.addLayout(self.layout_propulsion)

        self.layout_airfoil_selection.addWidget(self.airfoil_selection_text)
        self.layout_airfoil_selection.addWidget(self.combo_box_airfoil_selection)

        self.layout_battery_selection.addWidget(self.battery_selection_text)
        self.layout_battery_selection.addWidget(self.combo_battery_selection)

        self.layout_solar_cell_selection.addWidget(self.solar_cell_selection_text)
        self.layout_solar_cell_selection.addWidget(self.combo_solar_cell_selection)

        self.layout_flight_endurance_max.addWidget(self.flight_endurance_text)
        self.layout_flight_endurance_max.addSpacing(10)
        self.layout_slider_flight_endurance.addWidget(self.flight_endurance_slider)
        self.layout_slider_flight_endurance.addWidget(self.flight_endurance_label)

        self.layout_flight_endurance_max.addLayout(self.layout_slider_flight_endurance)

        self.layout_propulsion_efficiency.addWidget(self.propulsion_efficiency_text)

        self.layout_slider_propulsion_efficiency.addWidget(self.propulsion_efficiency_slider)
        self.layout_slider_propulsion_efficiency.addWidget(self.propulsion_efficiency_label)

        self.layout_propulsion_efficiency.addLayout(self.layout_slider_propulsion_efficiency)

        self.layout_right.addLayout(self.layout_flight_endurance_max)
        self.layout_right.addSpacing(20)
        self.layout_right.addLayout(self.layout_airfoil_selection)
        self.layout_right.addSpacing(10)
        self.layout_right.addLayout(self.layout_battery_selection)
        self.layout_right.addSpacing(10)
        self.layout_right.addLayout(self.layout_solar_cell_selection)
        self.layout_right.addStretch(1)

        self.layout_center.addLayout(self.layout_left, 1)
        self.layout_center.addSpacing(1)

        self.layout_center.addLayout(self.layout_right, 1)
        self.layout_center.addSpacing(1)

        self.main_layout.addLayout(self.layout_center)
        self.main_layout.addSpacing(25)

        self.button_add_layout.addWidget(self.add_button)
        self.button_size_layout.addWidget(self.sizing_button)

        self.button_add_layout.addSpacing(30)
        self.button_size_layout.addSpacing(30)

        self.layout_left.addSpacing(30)
        self.layout_right.addSpacing(30)

        self.layout_left.addLayout(self.button_add_layout)
        self.layout_right.addLayout(self.button_size_layout)

        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

        ########################### End Layouts definition   ###########################################

    def update_propulsion_efficiency(self, value):
        self.propulsion_efficiency_label.setText(str(value))
        self.propulsion_efficiency = (value / 100)

    def update_flight_endurance(self, value):
        self.flight_endurance_label.setText(str(value))
        self.flight_endurance_max = value

    def add(self):
        if len(self.get_distances()) < 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Atenção")
            msg.setInformativeText("Defina uma Rota para a Aeronave")
            msg.setWindowTitle("Erro")
            msg.setDetailedText("")
            msg.show()
            msg.exec_()

        else:

            if self.input_velocity_min.value() != 0 \
                    and self.input_payload_power_min.value() != 0 \
                    and self.input_payload_weight_min.value() != 0 \
                    and self.input_cruise_altitude.value() != 0\
                    and self.input_wingspan.value() != 0 \
                    and self.input_wing_area.value() != 0 \
                    and self.input_propulsion_group_weight.value() != 0 \
                    and self.input_airframe_weight.value() != 0:

                self.takeoff_altitude = self.input_take_off_altitude.value()
                self.cruise_altitude = self.input_cruise_altitude.value()

                self.velocity_min = self.input_velocity_min.value()

                self.wing_area = self.input_wing_area.value()
                self.wingspan = self.input_wingspan.value()
                self.propulsion_group_weight = self.input_propulsion_group_weight.value()
                self.airframe_weight = self.input_airframe_weight.value()

                self.payload_power_min = self.input_payload_power_min.value()
                self.payload_weight_min = self.input_payload_weight_min.value()
                self.air_density = Atmosphere.get_air_density(self.cruise_altitude)

                self.autonomy = max(self.get_distances()) / (self.velocity_min * 3.6)  # int(self.input_text_03.text())
                self.airfoil_name = self.combo_box_airfoil_selection.currentText()
                self.battery_name = self.combo_battery_selection.currentText()
                self.solar_cell_name = self.combo_solar_cell_selection.currentText()

                msg = QMessageBox()

                msg.setInformativeText("Parametros Adicionados com Sucesso!")
                msg.setWindowTitle("Sucesso")
                msg.setDetailedText("")
                msg.show()
                msg.exec_()

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText("Atenção")
                msg.setInformativeText("É Necessário Preencher Todos os Campos")
                msg.setWindowTitle("Erro")
                msg.setDetailedText("")
                msg.show()
                msg.exec_()

    def sizing(self):
        if self.solar_energy != 0 and self.velocity_min != 0 \
                and self.cruise_altitude != 0 \
                and self.payload_power_min != 0 \
                and self.payload_weight_min != 0\
                and self.input_wingspan.value() != 0 \
                and self.input_wing_area.value() != 0 \
                and self.input_propulsion_group_weight.value() != 0 \
                and self.input_airframe_weight.value() != 0:


            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Calculando...")
            msg.setInformativeText("Isso pode demorar")
            msg.setWindowTitle("Atenção!")
            msg.setDetailedText("")
            msg.show()
            msg.exec_()

            genetic = uav_optimization(self.velocity_min, self.velocity_min, self.payload_power_min,
                                       self.payload_power_min, self.payload_weight_min, self.payload_weight_min,
                                       self.solar_energy, self.air_density, self.takeoff_altitude, self.cruise_altitude,
                                       self.airfoil_name, self.battery_name, self.solar_cell_name,
                                       self.select_airfoil, self.select_battery, self.select_solar_cell,
                                       self.fitness_strategy, 1, self.flight_endurance_max, 0.3, 0.7,
                                       self.propulsion_efficiency, self.propulsion_efficiency,
                                       self.wing_area, self.wing_area, self.wingspan, self.wingspan,
                                       self.airframe_weight, self.propulsion_group_weight)
            genetic.main()

            flight_speed = genetic.best_individual[3]
            flight_endurance = genetic.best_individual[4]
            payload_weight = genetic.best_individual[5]
            payload_power = genetic.best_individual[6]
            solar_cell_wing_covering = genetic.best_individual[9]
            propulsion_efficiency = genetic.best_individual[10]

            print(payload_weight)
            print(payload_power)

            aerodynamic_profile = get_aerodynamic_profile(genetic.airfoil_name)
            battery = get_batteries(genetic.battery_name)
            solar_cell = get_solar_cells(genetic.solar_cell_name)

            solar_uav = SizingUAVService.sizing_uav(self.takeoff_altitude, self.cruise_altitude, flight_speed,
                                                    flight_endurance, self.solar_energy, payload_power, payload_weight,
                                                    genetic.best_individual[0], genetic.best_individual[1],
                                                    aerodynamic_profile, solar_cell, battery, propulsion_efficiency,
                                                    solar_cell_wing_covering, self.airframe_weight,
                                                    self.propulsion_group_weight)

            uav_list = [solar_uav]

            create_pdf(uav_list, self.takeoff_altitude, self.cruise_altitude, self.location, self.solar_energy,
                       self.hourly_radiation, self.date, self.hours_without_sunlight, genetic.airfoil_name,
                       battery.name, solar_cell.name)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Atenção")
            msg.setInformativeText("Adicione os Parâmetros da Missão")
            msg.setWindowTitle("Erro")
            msg.setDetailedText("")
            msg.show()
            msg.exec_()

    def get_distances(self):
        # Opening JSON file
        self.distances = []
        names = os.listdir('Data/')
        names.sort()
        if len(names) > 2:
            f = open('Data/' + names[-3], )
        elif len(names) == 2:
            f = open('Data/' + names[-2], )
        else:
            f = open('Data/' + names[0], )
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        # Iterating through the json
        # list

        points = []
        f.close()
        if data != 'None':
            for i in data['features']:
                if i['geometry']['type'] == 'LineString':
                    points.append(i['geometry'])

            for i in points:
                coordinates = i['coordinates']
                distance = 0
                for c in range(1, len(coordinates)):
                    coords_1 = coordinates[c - 1]
                    coords_2 = coordinates[c]
                    distance = distance + geopy.distance.distance(coords_1, coords_2).km
                self.distances.append(distance)

        return self.distances
