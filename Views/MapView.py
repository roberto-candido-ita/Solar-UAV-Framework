import io
import os

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QHBoxLayout, QWidget, \
    QVBoxLayout, QMessageBox, QLabel
import folium

import geocoder
from folium import plugins
from matplotlib import pyplot as plt

from Views.css.Styles import Style
from Models import SolarResourceModel

widget_map = QWidget


class Map(QMainWindow):
    def __init__(self):
        super().__init__()

        ######################## Variables   ###################################
        self.coordinates = [-23.21079743146222, -45.87544497731788]
        self.location = ' Praça Marechal Eduardo Gomes, 50 - Vila das Acacias, São José dos Campos]'

        coldest_day_of_the_year, self.hourly_radiation, self.hours_with_sunlight_list = \
            SolarResourceModel.model(self.coordinates[0], self.coordinates[1])

        self.hours_without_sunlight = 24 - min(self.hours_with_sunlight_list)
        self.date = SolarResourceModel.get_date_by_day_number(coldest_day_of_the_year)

        daily_radiation_chart(self.hourly_radiation, self.date)

        ######################## End of Variables   ##############################

        ######################## Main windown ###################################
        self.setStyleSheet(Style.map)
        self.web_view = QWebEngineView()
        self.web_view.page().profile().downloadRequested.connect(self.handle_downloadRequested)
        ######################## End ofMain windown #############################

        ######################## Layouts ###################################
        self.main_layout = QVBoxLayout()
        self.layout_top = QHBoxLayout()

        ######################## End ofLayouts #############################

        ######################## Labels ####################################
        self.location_text = QLabel('Location')
        font = QFont("Arial", 14)

        self.location_text.setFont(font)
        self.location_text.setStyleSheet(Style.label)

        ######################## End ofLabels ##############################

        ######################## Input Text ################################
        self.location_input_text = QLineEdit(self)
        self.location_input_text.move(10, 10)
        self.location_input_text.resize(200, 30)
        self.location_input_text.setStyleSheet(Style.input_text)

        ######################## End of input Texts ########################

        ######################## Buttons ###################################
        self.search_button = QPushButton('Search', self)
        self.search_button.move(100, 100)
        self.search_button.resize(140, 50)
        self.search_button.setIcon(QIcon('Assets/img/search.png'))
        self.search_button.setStyleSheet(Style.button)
        self.search_button.clicked.connect(self.search_location)

        ######################## End ofButtons #############################

        ######################## Set Layouts ###############################
        self.widget_map = create_maps(self.coordinates, self.location, self.web_view, self.hourly_radiation, self.date)
        self.layout_top.addWidget(self.location_text)
        self.layout_top.addWidget(self.location_input_text)
        self.layout_top.addWidget(self.search_button)
        self.main_layout.addLayout(self.layout_top)
        self.main_layout.addWidget(self.widget_map)

        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)
        ######################## End of Set Layouts #########################

    ######################## Functions ######################################
    def search_location(self):
        text = self.location_input_text.text()
        if text != '':
            g = geocoder.arcgis(text)
            self.coordinates = g.latlng
            self.location = g.current_result

            coldest_day_of_the_year, self.hourly_radiation, self.hours_with_sunlight_list = \
                SolarResourceModel.model(self.coordinates[0], self.coordinates[1])

            self.hours_without_sunlight = 24 - min(self.hours_with_sunlight_list)

            self.date = SolarResourceModel.get_date_by_day_number(coldest_day_of_the_year)

            daily_radiation_chart(self.hourly_radiation, self.date)

            widget_map = create_maps(self.coordinates, self.location, self.web_view, self.hourly_radiation, self.date)

            layout = QVBoxLayout()
            layout_top = QHBoxLayout()
            layout_top.addWidget(self.location_text)
            layout_top.addWidget(self.location_input_text)
            layout_top.addWidget(self.search_button)
            layout.addLayout(layout_top)
            layout.addWidget(widget_map)
            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Attention")
            msg.setInformativeText("You must enter a valid address")
            msg.setWindowTitle("Erro")
            msg.setDetailedText("Use the following format: \nStreet, Neighborhood, City")
            msg.show()
            msg.exec_()

    def handle_downloadRequested(self, item):
        item.setPath('./')
        item.accept()


######################## Global  Functions ######################################
def create_maps(coordinate, location, view, hourly_radiation, date):
    web_view = view
    layout = QHBoxLayout()

    m = folium.Map(
        tiles='OpenStreetMap',
        zoom_start=13,
        location=coordinate,
        control=False,
    )
    # Earth
    tile = folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        name="Esri Terrain",
        attr="Esri",
        zoom_start=13,
        location=coordinate,
        overlay=True,
        control=True,
    )

    html = ''
    text = str(location)
    text = text[:-1]

    elevation = SolarResourceModel.get_elevation(coordinate[0], coordinate[1])
    text = text + ', Elevação: ' + str(elevation) + ' Metros '
    solar_energy = round(sum(hourly_radiation))
    day_of_the_year = str(date[2]) + ' de ' + date[3]
    text = text + ', Irradiação Solar Total: ' + str(solar_energy) + ' W '
    text = text + ', Dia do ano: ' + day_of_the_year + ']'
    text = text[1:-1]
    x = text.split(", ")

    for i in x:
        html += ('<br>' + i)
    iframe = folium.IFrame(html)
    popup = folium.Popup(iframe,
                         min_width=250,
                         max_width=250)
    folium.Marker(
        location=coordinate,
        popup=popup,
        icon=folium.Icon(icon="info-sign"),
    ).add_to(m)

    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite Hibrid',
        overlay=True,
        control=True
    ).add_to(m)
    # Earth
    tile = folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Satellite",
        overlay=True,
        control=True,
    ).add_to(m)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Terrain',
        overlay=True,
        control=True
    ).add_to(m)
    # ROADMAP
    tile = folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Maps",
        overlay=True,
        control=True,
    ).add_to(m)
    formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    plugins.MousePosition(
        position='topright',
        separator=' | ',
        empty_string='NaN',
        lng_first=True,
        num_digits=20,
        prefix='Coordinates:',
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m)

    folium.LayerControl().add_to(m)
    dirname = os.path.dirname(__file__)
    dirname = dirname + '/Data/'
    names = os.listdir(dirname)
    for name in names:
        if 'data' in name:
            os.remove(dirname + name)
    plugins.Draw(
        export=True,
        filename=dirname + "data.download",
        position="topleft",
        draw_options={
            "polyline": {"shapeOptions": {
                "stroke": True,
                "weight": 8,
                "opacity": 0.5,
                "fill": False,
                "clickable": True
            }},
            "rectangle": {"shapeOptions": {
                "weight": 4,
                "opacity": 0.8,
                "color": '#f25252',
            }},

            "circle": False,
            "polygon": False,
            "circlemarker": False,
            "marker": False,
        },
        edit_options={"poly": {"allowIntersection": True}, },
    ).add_to(m)

    data = io.BytesIO()
    m.save(data, close_file=False)
    web_view.setHtml(data.getvalue().decode())
    layout.addWidget(web_view)
    return web_view


def daily_radiation_chart(hourly_radiation, date):
    x = []
    for i in range(0, 24):
        x.append(i)
    fig = plt.figure(figsize=(4, 3))
    fig, ax = plt.subplots()

    ax.legend = 'Total: ' + str(int(sum(hourly_radiation)))
    ax.set_title('Solar Irradiation - Total: ' + str(int(sum(hourly_radiation))) + ' W Day ' + str(date[2]) + '/'
                 + str(date[3]), fontsize=10)

    ax.axes.set_ylabel('Solar Irradiation (Wh/m^2)', fontsize=10)
    ax.axes.set_xlabel('Time of day (h)', fontsize=10)

    plt.bar(x, hourly_radiation)
    path = os.path.abspath(__file__ + "/../../")
    plt.savefig(path + "/database/simulations/" + "hourly_radiation.png")
    plt.close()
