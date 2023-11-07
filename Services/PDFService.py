from io import BytesIO
from typing import List

import matplotlib.pyplot as plt
import webbrowser

from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ParaLines, Image, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
import time
import sys, os

line = '------------------------------------------------------------------------------------------------------------------ '


def create_pdf(uav_list, takeoff_altitude, cruise_altitude, location, solar_energy,
               hourly_radiation, date, hours_without_sunlight, airfoil_name, battery_name, solar_cell_name):

    for uav in uav_list:
        for i in range(0, len(uav)):
            uav[i] = '%.2f ' % uav[i]

    number = round(time.time() * 1000)
    doc = SimpleDocTemplate(
        "../database/simulations/sizing_" + str(number) + ".pdf",
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=18,
    )
    styles = getSampleStyleSheet()
    flowables = []

    # [wing_area, wingspan, aspect_ratio, standard_mean_chord, flight_speed, flight_endurance,
    #         lift_force, drag_coefficient, drag_force, vcl, take_off_distance, landing_distance,
    #         payload_power, power_for_take_off, climb_power, total_climb_power, propulsion_power, time_to_take_off,
    #         time_to_climb, time_to_landing, total_time_to_climb, payload_weight, airframe_load, panel_load,
    #         battery_load, propulsion_load, total_load, total_energy, solar_energy_collected, mass_power_ratio
    #         ]

    # [
    #
    #         time_to_take_off 17
    #         time_to_climb 18, time_to_landing 19
    #         ]

    style = ParagraphStyle(
        name='Normal',
        fontSize=12,
        spaceAfter=5,
    )
    text = 'Solar UAV Sizing Report'
    para = Paragraph(text, style=styles["Title"])
    flowables.append(para)

    para = Paragraph('Solar Resource', style=styles["Heading2"])
    flowables.append(para)

    para = Paragraph('Location: ' + str(location)[1:-1], style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Available Solar Energy: ' + '%.2f ' % solar_energy + ' W', style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Day of the year with less incidence os sunlight: ' + str(date[2]) + '/' + str(date[3]),
                     style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Hours Without Sunlight: ' + '%.2f ' % hours_without_sunlight + 'h', style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('', style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('----------------------------------------------------------- Solar Energy Distribution -----'
                     '--------------------------------------------------'
                     , style=styles["Heading5"])
    flowables.append(para)

    data = [['hour (h)', 'power (W)']]

    for count, value in enumerate(hourly_radiation):
        if value > 0 and count < 10:
            data.append(['0' + str(count), '%.2f' % value])

        if value > 0 and count >= 10:
            data.append([str(count), '%.2f' % value])

    t = Table(data)
    flowables.append(t)

    path = os.path.abspath(__file__ + "/../../")
    img_file = Image(path + "/database/simulations/" + "hourly_radiation.png")
    img_file.drawHeight = 2 * inch
    img_file.drawWidth = 3 * inch

    flowables.append(img_file)

    uav = uav_list[0]

    para = Paragraph('Mission Profile', style=styles["Heading2"])
    flowables.append(para)

    para = Paragraph('Take off altitude: ' + str(takeoff_altitude) + ' (m)', style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Cruise altitude: ' + str(cruise_altitude) + ' (m)', style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Flight Speed: ' + uav[4] + ' (m/s)', style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Flight Endurance: ' + uav[5] + ' (h)', style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Payload Power: ' + uav[12] + ' (W)', style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Payload Weight: ' + uav[21] + ' (N)', style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Airfoil Model: ' + airfoil_name, style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Battery Model: ' + battery_name, style=styles["Normal"])
    flowables.append(para)

    para = Paragraph('Solar Cell Model: ' + solar_cell_name, style=styles["Normal"])
    flowables.append(para)

    flowables.append(PageBreak())

    for i, uav in enumerate(uav_list):
        para = Paragraph('UAV Solution ' + str(i + 1), style=styles["Heading3"])
        flowables.append(para)

        para = Paragraph('----------------------------------------- Wing Settings -----------------------'
                         , style=styles["Heading2"])
        flowables.append(para)
        para = Paragraph('Wing Area: ' + uav[0] + ' (m)', style=style)
        flowables.append(para)

        para = Paragraph('Wingspan: ' + uav[1] + ' (m)', style=style)
        flowables.append(para)

        para = Paragraph('Aspect Ratio: ' + uav[2], style=style)
        flowables.append(para)

        para = Paragraph('Standard Mean Chord: ' + uav[3] + ' (m)', style=style)
        flowables.append(para)

        para = Paragraph('Solar Panel Area: ' + uav[30] + ' (m)', style=style)
        flowables.append(para)

        para = Paragraph('----------------------------------------- Power Settings ----------------------'
                         , style=styles["Heading2"])

        flowables.append(para)
        para = Paragraph('Total Energy Collected: ' + uav[28] + ' (W)', style=style)
        flowables.append(para)

        para = Paragraph('Total Energy Consumed: ' + uav[27] + ' (W)', style=style)
        flowables.append(para)

        para = Paragraph('Propulsion Power: ' + uav[16] + ' (W)', style=style)
        flowables.append(para)

        para = Paragraph('Power for Takeoff: ' + uav[13] + ' (W)', style=style)
        flowables.append(para)

        para = Paragraph('Climb Power: ' + uav[14] + ' (W)', style=style)
        flowables.append(para)

        para = Paragraph('Total Climb Power: ' + uav[15] + ' (W)', style=style)
        flowables.append(para)

        para = Paragraph('------------------------------------------ Weight Settings --------------------'
                         , style=styles["Heading2"])

        flowables.append(para)
        para = Paragraph('Total Weight: ' + uav[26] + ' (N)', style=style)
        flowables.append(para)

        para = Paragraph('Airframe Weight: ' + uav[22] + ' (N)', style=style)
        flowables.append(para)

        para = Paragraph('Solar Panel Weight: ' + uav[23] + ' (N)', style=style)
        flowables.append(para)

        para = Paragraph('Battery Weight: ' + uav[24] + ' (N)', style=style)
        flowables.append(para)

        para = Paragraph('Propulsion Group Weight: ' + uav[25] + ' (N)', style=style)
        flowables.append(para)

        para = Paragraph('----------------------------------- Aerodynamic Settings -------------------'
                         , style=styles["Heading2"])

        flowables.append(para)
        para = Paragraph('Lift Force: ' + uav[6] + ' (N)', style=style)
        flowables.append(para)

        para = Paragraph('Drag Force: ' + uav[8] + ' (N)', style=style)
        flowables.append(para)

        para = Paragraph('Climbing Speed: ' + uav[9] + ' (m/s)', style=style)
        flowables.append(para)

        para = Paragraph('Takeoff Distance: ' + uav[10] + ' (m)', style=style)
        flowables.append(para)

        para = Paragraph('Landing Distance: ' + uav[11] + ' (m)', style=style)
        flowables.append(para)

        para = Paragraph('Total Time for Climb: ' + uav[20] + ' (s)', style=style)
        flowables.append(para)

        para = Paragraph('Time for Takeoff: ' + uav[17] + ' (s)', style=style)
        flowables.append(para)

        para = Paragraph('Time to climb: ' + uav[18] + ' (s)', style=style)
        flowables.append(para)

        para = Paragraph('Time to Landing: ' + uav[19] + ' (s)', style=style)
        flowables.append(para)

        para = Paragraph(line, style=styles["Heading3"])
        flowables.append(para)

        flowables.append(PageBreak())

    doc.build(flowables)
    path = os.path.abspath(__file__ + "/../../")
    webbrowser.open_new(path + "/database/simulations/sizing_" + str(number) + ".pdf")
