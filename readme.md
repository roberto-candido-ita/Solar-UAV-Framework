#Solar-UAV-Framework

This is a brief guide on how to set up a Python virtual environment and install the necessary dependencies for this project.

## Getting Started

Follow these steps to create a virtual environment and install the required dependencies:

1. **Create a Virtual Environment**: Open your terminal and navigate to the project directory. Run the following command to create a virtual environment named `venv` (you can choose a different name if you prefer):

    ```bash
    python -m venv venv
    ```

2. **Activate the Virtual Environment**: Depending on your operating system, use one of the following commands to activate the virtual environment:

    - For Windows:

    ```bash
    venv\Scripts\activate
    ```

    - For macOS and Linux:

    ```bash
    source venv/bin/activate
    ```

3. **Install Dependencies**: Once the virtual environment is activated, you can use `pip` to install the required Python packages:

    ```bash
    pip install PyQt5 PyQtWebEngine folium geocoder pandas geopy matplotlib reportlab deap seaborn plotly
    ```

    This command will install the following packages:

    - PyQt5
    - PyQtWebEngine
    - folium
    - geocoder
    - pandas
    - geopy
    - matplotlib
    - reportlab
    - deap
    - seaborn
    - plotly

4. **Start the Project**: You are now ready to start working on your Python project with the necessary dependencies installed. Run MainWindow.py in the views directory.

## Contributing

Feel free to contribute to this project by creating issues, submitting pull requests, or providing feedback. We welcome your contributions!

## License

This project is licensed under the [MIT License](LICENSE).
