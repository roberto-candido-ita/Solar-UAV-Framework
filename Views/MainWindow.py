import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QTabWidget

from MapView import Map
from Views.css.Styles import Style
from LIWView import LIWView
from Views.MPOView import MPOView
from Views.AdaptUAVView import AdaptUAVView


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        ######################## Variables ###################################
        self.coordinates = []
        self.map = Map()
        self.mission = LIWView()
        self.optimization_view = MPOView()
        self.adapt_uav_view = AdaptUAVView()
        self.optimization_view.map = self.map
        self.index = 0
        self.coordinates = self.map.coordinates
        self.take_off = []
        ######################## End of Variables ############################

        ######################## Main Window #################################
        self.setWindowTitle('Instituto Tecnológico de Aeronáutica')
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)
        self.setWindowIcon(QIcon('/Assets/img/solar-panel.png'))
        self.setStyleSheet("Window {""background-color: #212121;""}")
        ######################## End of Main Window ###########################

        ######################## Create layouts ###############################
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        ######################## End of Create layouts ########################

        ######################## Buttons ######################################
        self.mission_location_button = QPushButton('  Mission Location', self)
        self.sizing_button = QPushButton('  Linear Increment of Wingspan', self)
        self.sizing_optimization_button = QPushButton('  Multi - parameter Optimization', self)
        self.adapt_uav_button = QPushButton('  Convert UAV to Solar UAV', self)

        self.mission_location_button.clicked.connect(self.button1_click)
        self.sizing_button.clicked.connect(self.button2_click)
        self.sizing_optimization_button.clicked.connect(self.button3_click)
        self.adapt_uav_button.clicked.connect(self.button4_click)

        # self.mission_location_button.setIcon(QIcon('Assets/img/mapa.png'))
        # self.sizing_button.setIcon(QIcon('Assets/img/uav (1).png'))
        # self.sizing_optimization_button.setIcon(QIcon('Assets/img/optimization.png'))

        self.mission_location_button.setStyleSheet(Style.button)
        self.sizing_button.setStyleSheet(Style.button)
        self.sizing_optimization_button.setStyleSheet(Style.button)
        self.adapt_uav_button.setStyleSheet(Style.button)
        ######################## End of Buttons ##############################

        ######################## Create Tabs #################################
        self.tab1 = self.set_layout_to_tab1()
        self.tab2 = self.set_layout_to_tab2()
        self.tab3 = self.set_layout_to_tab3()
        self.tab4 = self.set_layout_to_tab4()
        ######################## End of Tabs #################################

        ######################## Set Layouts  ################################
        left_layout.addWidget(self.mission_location_button)
        left_layout.addWidget(self.sizing_button)
        left_layout.addWidget(self.sizing_optimization_button)
        left_layout.addWidget(self.adapt_uav_button)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")
        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.setCurrentIndex(self.index)
        self.right_widget.setStyleSheet(Style.right_widget)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        ######################## End of Set Layouts  ################################

    ######################## Buttons click Functions  ################################################
    def button1_click(self):
        self.right_widget.setCurrentIndex(0)

    def button2_click(self):
        self.right_widget.setCurrentIndex(1)
        self.mission.location = self.map.location
        self.mission.solar_energy = sum(self.map.hourly_radiation)
        self.mission.hourly_radiation = self.map.hourly_radiation
        self.mission.date = self.map.date
        self.mission.map = self.map

    def button3_click(self):
        self.right_widget.setCurrentIndex(2)
        self.optimization_view.location = self.map.location
        self.optimization_view.solar_energy = sum(self.map.hourly_radiation)
        self.optimization_view.hourly_radiation = self.map.hourly_radiation
        self.optimization_view.date = self.map.date
        self.optimization_view.hours_without_sunlight = self.map.hours_without_sunlight

    def button4_click(self):
        self.right_widget.setCurrentIndex(3)
        self.adapt_uav_view.location = self.map.location
        self.adapt_uav_view.solar_energy = sum(self.map.hourly_radiation)
        self.adapt_uav_view.hourly_radiation = self.map.hourly_radiation
        self.adapt_uav_view.date = self.map.date
        self.adapt_uav_view.hours_without_sunlight = self.map.hours_without_sunlight
    ######################## End of Buttons click Functions  ################################################

    ######################## Set Layout Functions  ################################################
    def set_layout_to_tab1(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.map)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def set_layout_to_tab2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.mission)
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def set_layout_to_tab3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.optimization_view)
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def set_layout_to_tab4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.adapt_uav_view)
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
    ######################## End of Set Layout Functions  ################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())
