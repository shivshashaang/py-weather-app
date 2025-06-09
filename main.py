import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt
from requests import RequestException


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter the name of the city:", self)
        self.city_input = QLineEdit(self)
        self.weather_button = QPushButton("Get weather", self)
        self.temp_label = QLabel(self)
        self.desc_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.weather_button)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.desc_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.desc_label.setAlignment(Qt.AlignCenter)


        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.weather_button.setObjectName("weather_button")
        self.temp_label.setObjectName("temp_label")
        self.desc_label.setObjectName("desc_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
                
            }
            QLineEdit#city_input{
                font-size: 40px;
            
            }
            
            QPushButton#weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            
            QLabel#temp_label{
                font-size: 75px;
            }
            
            QLabel#desc_label{
                font-size: 50px;
            }
        
        
        
        """)

        self.weather_button.clicked.connect(self.get_weather)

    def get_weather(self):

        api_key = ""
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.disp_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.disp_err("Bad request")
                case 401:
                    self.disp_err("Unauthorized")
                case 403:
                    self.disp_err("Forbidden")
                case 404:
                    self.disp_err("Not found")
                case 500:
                    self.disp_err("internal server error")
                case 502:
                    self.disp_err("Bad gateway")
                case 503:
                    self.disp_err("service unavailable")
                case 504:
                    self.disp_err("gateway timeout")
                case _:
                    self.disp_err(f"HTTP error \n{http_error}")


        except requests.exceptions.RequestException:
            pass


    def disp_err(self, message):
        self.temp_label.setStyleSheet("font-size: 30px;")
        self.temp_label.setText(message)

    def disp_weather(self, data):
        self.temp_label.setStyleSheet("font-size: 75px;")
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15
        temp_d = data["weather"][0]["description"]

        self.temp_label.setText(f"{temp_c:.0f}°C")
        self.desc_label.setText(temp_d)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())


