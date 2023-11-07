class Style:
    map = ("Map{"
           "background-color: #3b3b3b;"
           "border: 1px solid black;"
           "}"
           )
    window = ("Window{"
              "background-color: #3b3b3b;"
              "border: 1px solid black;"
              "padding: 50px;}"
              "}"
              )
    table = ("QTableWidget{"
              "background-color: #3b3b3b;"
             "color: white;"
              "}"
              )

    label= ("QLabel{"
             "color: white;"
             "text-align: center;"
             "}"
             )

    label_2 = ("QLabel{"
             "color: white;"
             "background-color: #404040;"
            "border: 1px  solid gray;"
            "text-align: center;"
            "border-radius: 6px;"
            "padding:  6px;"
             "}"
             )

    input_text = (
        "QLineEdit{"
        "background-color:#3b3b3b;"
        "border: 1px  solid gray;"
        "color: white;"
        "border-radius: 6px;"
        "padding: 8px;"
        "selection-background-color: darkgray;"
        "font-size: 25px;}"
        "QLineEdit:focus { "
        "border: 1px  solid #0d9adb;}"
        "}"
    )

    spin_box = (
        "QSpinBox{"
        "background-color:#3b3b3b;"
        "border: 1px  solid gray;"
        "color: white;"
        "border-radius: 6px;"
        "padding: 8px;"
        "selection-background-color: darkgray;"
        "font-size: 22px;}"
        "QSpinBox:focus { "
        "border: 1px  solid #0d9adb;}"
        "}"
    )

    double_spin_box = (
        "QDoubleSpinBox{"
        "background-color:#3b3b3b;"
        "border: 1px  solid gray;"
        "color: white;"
        "border-radius: 6px;"
        "padding: 8px;"
        "selection-background-color: darkgray;"
        "font-size: 22px;}"
        "QDoubleSpinBox:focus { "
        "border: 1px  solid #0d9adb;}"
        "}"
    )

    combo_box = (
        "QComboBox{"
        "background-color:#3b3b3b;"
        "border: 1px  solid gray;"
        "color: white;"
        "border-radius: 6px;"
        "padding: 8px;"
        "selection-background-color: darkgray;"
        "font-size: 22px;}"
        "QLineEdit:focus { "
        "border: 1px  solid #0d9adb;}"
        "}"
    )

    spinBox = (
        "QSpinBox{"
        "background-color:#3b3b3b;"
        "border: 1px  solid gray;"
        "color: white;"
        "border-radius: 6px;"
        "padding: 8px;"
        "selection-background-color: darkgray;"
        "font-size: 25px;}"
        "QLineEdit:focus { "
        "border: 1px  solid #0d9adb;}"
        "}"
    )

    button = ("QPushButton{"
              "text-align: left;"
              "color: #ffffff;"
              "padding-left: 10px;"
              "padding-right: 10px;"
              "border: 0px solid #4588f5;"
              "font-size: 20px;"
              "qproperty-iconSize: 35px;"
              "height : 50px;"
              "border-radius: 8px}"
              "QPushButton::hover"
              "{"
              "background-color : #525963;"
              "}"
              "QPushButton::pressed"
              "{"
              "background-color : #2b2b2b;"
              "}"
              )
    table_button = ("QPushButton{"
             "text-align: center;"
             "color: #ffffff;"
             "background-color: #023b52;"
             "padding-left: 10px;"
             "padding-right: 10px;"
             "border: 0px solid #4588f5;"
             "font-size: 20px;"
             "qproperty-iconSize: 35px;"
             "height : 50px;"
             "border-radius: 8px}"
             "QPushButton::hover"
             "{"
             "background-color : #525963;"
             "}"
             "QPushButton::pressed"
             "{"
             "background-color : #2b2b2b;"
             "}"
             )
    right_widget = (
        '''QTabBar::tab{width: 0; \
                    height: 0; margin: 0; padding: 0; border: none;fill: #3b3b3b;
                    }
                    QTabWidget::pane {             
                    border-width: 2px;         
                    border-style: solid;       
                    border-color: #3b3b3b;         
                    border-radius: 4px; 
    
                }                              
                QTabWidget::tab-bar {          
                    left: 5px; 
    
                } 
                    '''
    )

    qslider = (
        '''
            QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 12px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
            background:#3b3b3b;
            margin: 2px 1px;
            }

            QSlider::handle:horizontal {
            background: #0383ad;
            border: 1px solid #0383ad;
            width: 10px;
            height: 15px;
            margin: -6px 0px; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
            border-radius: 8px;
            
            }
            
            QSlider::add-page:horizontal {
            background: white;
            }

            QSlider::sub-page:horizontal {
            background: #25508f;
            }

            '''
    )

    radio_button = (
        '''
        QRadioButton
        {
        font : 20px Arial;
        color: white;
        }
        QRadioButton::indicator
        {
            width: 20px; 
            height: 20px;
        }
        '''
    )




