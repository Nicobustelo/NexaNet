import sys
from PyQt5.QtWidgets import QApplication
from frontend import GoogleMapsScraperApp

def main():
    app = QApplication(sys.argv)
    main_window = GoogleMapsScraperApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '_main_':
    main()