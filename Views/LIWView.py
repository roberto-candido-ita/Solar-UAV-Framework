from operator import itemgetter
import pandas as pd
from PyQt5 import QtWidgets
import json
import geopy.distance
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont, QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QHBoxLayout, QWidget, \
    QVBoxLayout, QMessageBox, QSlider, QSpinBox, QDoubleSpinBox

from Services.LIWService import LIWService
from Views.MapView import Map
from Views.css.Styles import Style
from Constants import Atmosphere
import os
from Services.SizingUAVService import SizingUAVService
from Services.CSVService import get_aerodynamic_profile, get_batteries, get_solar_cells
from Services.PDFService import create_pdf
from Models.SolarCell import SolarCell
from Models.Battery import Battery

widget_map = QWidget


class LIWView(QMainWindow):
    def __init__(self):
        super().__init__()

        ######################## Variables ###################################
        self.map = Map()
        self.cruise_altitude = 0
        self.takeoff_altitude = 0
        self.flight_speed = 0
        self.flight_endurance = 0
        self.payload_power = 0
        self.payload_weight = 0
        self.aerodynamic_profile = ''
        self.wing_chord = ''
        self.solar_cell = ''
        self.battery = ''
        self.air_density = 1.2250
        self.distances = []
        self.propulsion_efficiency = 0.5
        self.solar_cell_wing_covering = 0.5
        self.solar_energy = 0
        self.location = ''
        self.hourly_radiation = []
        self.date = 0
        self.hours_without_sunlight = 0
        self.battery_name = ''
        self.solar_cell_name = ''
        self.aerodynamic_profile_name = ''
        self.index = 4
        self.loads = []
        ######################## End of Variables ##################################

        ######################## Layouts Definition  ###############################
        self.main_layout = QVBoxLayout()
        self.button_add_layout = QHBoxLayout()
        self.button_size_layout = QHBoxLayout()
        self.center_layout = QHBoxLayout()
        self.layout_left = QVBoxLayout()
        self.layout_right = QVBoxLayout()
        self.takeoff_altitude_layout = QVBoxLayout()
        self.cruise_altitude_layout = QVBoxLayout()
        self.flight_speed_layout = QVBoxLayout()
        self.payload_power_layout = QVBoxLayout()
        self.payload_weight_layout = QVBoxLayout()
        self.airfoil_layout = QVBoxLayout()
        self.solar_cell_layout = QVBoxLayout()
        self.battery_layout = QVBoxLayout()
        self.flight_endurance_layout = QVBoxLayout()
        self.altitude_and_speed_layout = QHBoxLayout()
        self.layout_top_02 = QHBoxLayout()
        self.layout_top_03 = QHBoxLayout()
        self.layout_top_04 = QHBoxLayout()
        self.layout_propulsion_efficiency = QHBoxLayout()
        self.layout_solar_cell_wing_covering = QHBoxLayout()
        ############################ End of Layouts #############################

        ###########################  Labels  #####################################
        self.take_off_altitude_text = QLabel('Take off Altitude (m)')
        self.cruise_altitude_text = QLabel('Cruise Altitude (m)')
        self.propulsion_efficiency_text = QLabel('Propulsion Efficiency (%)')
        self.solar_cell_wing_covering_text = QLabel('Solar Cell Wing Covering(%)')
        self.flight_speed_text = QLabel('Flight Speed (m/s)')
        self.fight_endurance = QLabel('Flight Endurance (h)')
        self.payload_power_text = QLabel('Payload Power(W)')
        self.payload_weight_text = QLabel('Payload Weight (Kg)')
        self.airfoil_text = QLabel('Airfoil ')
        self.solar_cell_text = QLabel('Solar Cell Model')
        self.battery_text = QLabel('Battery')
        self.solar_cell_wing_covering_label = QLabel('50', self)
        self.propulsion_efficiency_label = QLabel('50', self)

        font = QFont("Arial", 14)
        self.payload_power_text.setFont(font)
        self.payload_weight_text.setFont(font)
        self.airfoil_text.setFont(font)
        self.solar_cell_text.setFont(font)
        self.battery_text.setFont(font)
        self.take_off_altitude_text.setFont(font)
        self.cruise_altitude_text.setFont(font)
        self.flight_speed_text.setFont(font)
        self.fight_endurance.setFont(font)
        self.solar_cell_wing_covering_text.setFont(font)
        self.propulsion_efficiency_text.setFont(font)
        self.solar_cell_wing_covering_label.setFont(font)

        self.payload_power_text.setStyleSheet(Style.label)
        self.payload_weight_text.setStyleSheet(Style.label)
        self.airfoil_text.setStyleSheet(Style.label)
        self.solar_cell_text.setStyleSheet(Style.label)
        self.battery_text.setStyleSheet(Style.label)
        self.propulsion_efficiency_text.setStyleSheet(Style.label)
        self.solar_cell_wing_covering_text.setStyleSheet(Style.label)
        self.take_off_altitude_text.setStyleSheet(Style.label)
        self.cruise_altitude_text.setStyleSheet(Style.label)
        self.flight_speed_text.setStyleSheet(Style.label)
        self.fight_endurance.setStyleSheet(Style.label)
        self.propulsion_efficiency_label.setFont(font)
        self.solar_cell_wing_covering_label.setStyleSheet(Style.label)
        self.propulsion_efficiency_label.setStyleSheet(Style.label)
        ########################### End of Labels  ################################

        ###########################  Imputs Boxes    ##############################
        self.takeoff_altitude_input = QSpinBox(self)
        self.takeoff_altitude_input.move(10, 10)
        self.takeoff_altitude_input.resize(150, 30)
        self.takeoff_altitude_input.setMaximum(2400)
        self.takeoff_altitude_input.setSingleStep(100)
        self.cruise_altitude_input = QSpinBox(self)
        self.cruise_altitude_input.move(10, 10)
        self.cruise_altitude_input.resize(150, 30)
        self.cruise_altitude_input.setMinimum(100)
        self.cruise_altitude_input.setMaximum(2500)
        self.cruise_altitude_input.setSingleStep(100)
        self.flight_speed_input = QDoubleSpinBox(self)
        self.flight_speed_input.move(10, 10)
        self.flight_speed_input.resize(150, 30)
        self.flight_speed_input.setMinimum(7.0)
        self.flight_speed_input.setMaximum(14.0)
        self.flight_speed_input.setSingleStep(0.1)
        self.flight_endurance_input = QDoubleSpinBox(self)
        self.flight_endurance_input.move(10, 10)
        self.flight_endurance_input.resize(150, 30)
        self.flight_endurance_input.setMinimum(1.0)
        self.flight_endurance_input.setMaximum(self.map.hours_without_sunlight)
        self.flight_endurance_input.setSingleStep(0.5)
        self.payload_power_input = QDoubleSpinBox(self)
        self.payload_power_input.move(10, 10)
        self.payload_power_input.resize(200, 30)
        self.payload_power_input.setMinimum(0.05)
        self.payload_power_input.setMaximum(5)
        self.payload_power_input.setSingleStep(0.05)
        self.payload_weight_input = QDoubleSpinBox(self)
        self.payload_weight_input.move(10, 10)
        self.payload_weight_input.resize(200, 30)
        self.payload_weight_input.setMinimum(0.05)
        self.payload_weight_input.setMaximum(2)
        self.payload_weight_input.setSingleStep(0.05)
        self.airfoil_input = QtWidgets.QComboBox(self)
        self.airfoil_input.move(10, 10)
        self.airfoil_input.resize(200, 30)
        self.solar_cell_input = QtWidgets.QComboBox(self)
        self.solar_cell_input.move(10, 10)
        self.solar_cell_input.resize(200, 30)
        self.battery_input = QtWidgets.QComboBox(self)
        self.battery_input.move(10, 10)
        self.battery_input.resize(200, 30)
        self.takeoff_altitude_input.setStyleSheet(Style.spin_box)
        self.cruise_altitude_input.setStyleSheet(Style.spin_box)
        self.flight_speed_input.setStyleSheet(Style.double_spin_box)
        self.flight_endurance_input.setStyleSheet(Style.double_spin_box)
        self.payload_power_input.setStyleSheet(Style.double_spin_box)
        self.payload_weight_input.setStyleSheet(Style.double_spin_box)
        self.airfoil_input.setStyleSheet(Style.combo_box)
        self.solar_cell_input.setStyleSheet(Style.combo_box)
        self.battery_input.setStyleSheet(Style.combo_box)
        ###########################  End of Imputs Boxes  ############################

        ###########################  Sliders   #######################################
        self.propulsion_efficiency_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.propulsion_efficiency_slider.setRange(20, 75)
        self.propulsion_efficiency_slider.setPageStep(1)
        self.propulsion_efficiency_slider.setValue(50)
        self.propulsion_efficiency_slider.setStyleSheet(Style.qslider)

        self.solar_cell_wing_covering_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.solar_cell_wing_covering_slider.setRange(20, 90)
        self.solar_cell_wing_covering_slider.setPageStep(1)
        self.solar_cell_wing_covering_slider.setValue(50)
        self.solar_cell_wing_covering_slider.setStyleSheet(Style.qslider)

        self.propulsion_efficiency_slider.valueChanged.connect(self.update_propulsion_efficiency)
        self.solar_cell_wing_covering_slider.valueChanged.connect(self.update_solar_cell_fill_factor)
        ###########################  End of Sliders   #################################

        ###########################    Buttons   ######################################

        self.button_add_parameters = QPushButton('Add parameters', self)
        self.button_add_parameters.setGeometry(200, 150, 100, 40)
        self.button_add_parameters.setIcon(QIcon('../img/plus.png'))

        self.button_sizing = QPushButton('Sizing', self)
        self.button_sizing.setGeometry(200, 150, 100, 40)
        self.button_sizing.setIcon(QIcon('../img/flash.png'))

        self.button_add_parameters.setStyleSheet(Style.table_button)
        self.button_sizing.setStyleSheet(Style.table_button)

        self.button_add_parameters.clicked.connect(self.add_parameters_for_sizing)
        self.button_sizing.clicked.connect(self.sizing_uav)
        ###########################   End  Buttons  ##################################

        ###########################   Imput Combo Box Fill  ##########################

        airfoil_names = os.listdir('../Database/Airfoils')

        for name in airfoil_names:
            self.airfoil_input.addItem(name[:-4])

        battery_file = pd.read_csv('../Database/Batteries/Batteries.csv')
        battery_names = battery_file.Name

        for name in battery_names:
            self.battery_input.addItem(name)

        solar_cell_file = pd.read_csv('../Database/Solar Cells/Solar Cell.csv')
        solar_cell_names = solar_cell_file.Name

        for name in solar_cell_names:
            self.solar_cell_input.addItem(name)
        ###########################  End Imput Combo Box Fill  ##########################

        ######################## Add components to Layouts  #############################
        self.takeoff_altitude_layout.addWidget(self.take_off_altitude_text)
        self.takeoff_altitude_layout.addWidget(self.takeoff_altitude_input)

        self.cruise_altitude_layout.addWidget(self.cruise_altitude_text)
        self.cruise_altitude_layout.addWidget(self.cruise_altitude_input)

        self.flight_speed_layout.addWidget(self.flight_speed_text)
        self.flight_speed_layout.addWidget(self.flight_speed_input)

        self.altitude_and_speed_layout.addLayout(self.takeoff_altitude_layout)
        self.altitude_and_speed_layout.addLayout(self.cruise_altitude_layout)
        self.altitude_and_speed_layout.addLayout(self.flight_speed_layout)

        self.payload_power_layout.addWidget(self.payload_power_text)
        self.payload_power_layout.addWidget(self.payload_power_input)

        self.payload_weight_layout.addWidget(self.payload_weight_text)
        self.payload_weight_layout.addWidget(self.payload_weight_input)

        self.flight_endurance_layout.addWidget(self.fight_endurance)
        self.flight_endurance_layout.addWidget(self.flight_endurance_input)

        self.airfoil_layout.addWidget(self.airfoil_text)
        self.airfoil_layout.addWidget(self.airfoil_input)

        self.solar_cell_layout.addWidget(self.solar_cell_text)
        self.solar_cell_layout.addWidget(self.solar_cell_input)

        self.battery_layout.addWidget(self.battery_text)
        self.battery_layout.addWidget(self.battery_input)

        self.layout_top_02.addLayout(self.payload_power_layout)
        self.layout_top_02.addLayout(self.payload_weight_layout)
        self.layout_top_02.addLayout(self.flight_endurance_layout)

        self.layout_top_04.addLayout(self.airfoil_layout)
        self.layout_top_04.addLayout(self.solar_cell_layout)
        self.layout_top_04.addLayout(self.battery_layout)

        self.layout_left.addLayout(self.altitude_and_speed_layout)
        self.layout_left.addSpacing(25)
        self.layout_left.addLayout(self.layout_top_02)

        self.layout_left.addSpacing(25)
        self.layout_left.addLayout(self.layout_top_04)

        self.layout_propulsion_efficiency.addWidget(self.propulsion_efficiency_slider)
        self.layout_propulsion_efficiency.addWidget(self.propulsion_efficiency_label)

        self.layout_solar_cell_wing_covering.addWidget(self.solar_cell_wing_covering_slider)
        self.layout_solar_cell_wing_covering.addWidget(self.solar_cell_wing_covering_label)

        self.layout_right.addWidget(self.propulsion_efficiency_text)
        self.layout_right.addSpacing(15)
        self.layout_right.addLayout(self.layout_propulsion_efficiency)
        self.layout_right.addSpacing(25)
        self.layout_right.addWidget(self.solar_cell_wing_covering_text)
        self.layout_right.addSpacing(15)
        self.layout_right.addLayout(self.layout_solar_cell_wing_covering)
        self.layout_right.addStretch(1)

        self.center_layout.addLayout(self.layout_left, 4)
        self.center_layout.addSpacing(50)

        self.center_layout.addLayout(self.layout_right, 3)
        self.center_layout.addSpacing(50)

        self.main_layout.addLayout(self.center_layout)

        self.button_add_layout.addWidget(self.button_add_parameters)
        self.button_size_layout.addWidget(self.button_sizing)

        self.layout_left.addSpacing(30)
        self.layout_left.addLayout(self.button_add_layout)

        self.layout_right.addSpacing(30)
        self.layout_right.addLayout(self.button_size_layout)

        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)
        ######################## End Add components in Layouts  ##########################

    ######################## Functions  ##################################################
    def add_parameters_for_sizing(self):
        if len(self.get_aircraft_route()) < 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Atention")
            msg.setInformativeText("Set a Route for the Aircraft")
            msg.setWindowTitle("Erro")
            msg.setDetailedText("")
            msg.show()
            msg.exec_()

        else:

            if self.flight_speed_input.value() != 0 \
                    and self.payload_power_input.value() != 0 \
                    and self.payload_weight_input.value() != 0 \
                    and self.cruise_altitude_input.value() != 0 \
                    and self.flight_endurance_input.value() != 0:

                self.takeoff_altitude = self.takeoff_altitude_input.value()
                self.cruise_altitude = self.cruise_altitude_input.value()
                self.flight_speed = self.flight_speed_input.value()
                self.flight_endurance = self.flight_endurance_input.value()
                self.payload_power = self.payload_power_input.value()
                self.payload_weight = self.payload_weight_input.value()

                self.aerodynamic_profile_name = str(self.airfoil_input.currentText())
                self.solar_cell_name = str(self.solar_cell_input.currentText())
                self.battery_name = str(self.battery_input.currentText())

                self.air_density = Atmosphere.get_air_density(self.cruise_altitude)

                msg = QMessageBox()

                msg.setInformativeText("Parameters Added Successfully!")
                msg.setWindowTitle("Success")
                msg.setDetailedText("")
                msg.show()
                msg.exec_()

            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)

                msg.setText("Attention")
                msg.setInformativeText("It is necessary to fill in all fields")
                msg.setWindowTitle("Erro")
                msg.setDetailedText("")
                msg.show()
                msg.exec_()

    def get_aircraft_route(self):
        self.distances = []
        names = os.listdir('Data/')
        names.sort()

        if len(names) > 2:
            f = open('Data/' + names[-3], )
        elif len(names) == 2:
            f = open('Data/' + names[-2], )
        else:
            f = open('Data/' + names[0], )

        data = json.load(f)

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

    def update_propulsion_efficiency(self, value):
        self.propulsion_efficiency_label.setText(str(value))
        self.propulsion_efficiency = (value / 100)

    def update_solar_cell_fill_factor(self, value):
        self.solar_cell_wing_covering_label.setText(str(value))
        self.solar_cell_wing_covering = (value / 100)

    def sizing_uav(self):
        if self.solar_energy != 0 and self.flight_speed != 0 and self.flight_endurance != 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Sizing...")
            msg.setInformativeText("This may take a while")
            msg.setWindowTitle("Attention!")
            msg.setDetailedText("")
            msg.show()
            msg.exec_()

            solar_cell = SolarCell()
            battery = Battery()

            aerodynamic_profile = get_aerodynamic_profile(self.aerodynamic_profile_name)
            battery = get_batteries(self.battery_name)
            solar_cell = get_solar_cells(self.solar_cell_name)

            solar_uav_list = LIWService.sizing_uav_list(self.takeoff_altitude, self.cruise_altitude,
                                                        self.flight_speed, self.flight_endurance,
                                                        self.solar_energy, self.payload_power, self.payload_weight,
                                                        solar_cell, battery, aerodynamic_profile,
                                                        self.propulsion_efficiency, self.solar_cell_wing_covering)

            create_pdf(solar_uav_list, self.takeoff_altitude, self.cruise_altitude, self.location, self.solar_energy,
                       self.hourly_radiation, self.date, self.map.hours_without_sunlight, self.aerodynamic_profile_name,
                       self.battery_name, self.solar_cell_name)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Attention")
            msg.setInformativeText("Add Mission Parameters")
            msg.setWindowTitle("Error")
            msg.setDetailedText("")
            msg.show()
            msg.exec_()
    ######################## End of Functions  ###############################################
