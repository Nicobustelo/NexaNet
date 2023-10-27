import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox, QHBoxLayout, QProgressBar
from src import config
from src.scrape_google_maps_links_task import ScrapeGoogleMapsLinksTask
from bose.launch_tasks import launch_tasks

class GoogleMapsScraperApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NexaNet")
        self.setGeometry(500, 200, 400, 200)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Business label and input
        self.business_label = QLabel("Rubro")
        self.business_input = QLineEdit()
        self.layout.addWidget(self.business_label)
        self.layout.addWidget(self.business_input)

        # Location label and input
        self.location_label = QLabel("Ciudad")
        self.location_input = QLineEdit()
        self.layout.addWidget(self.location_label)
        self.layout.addWidget(self.location_input)

        # Country label and input
        self.country_label = QLabel("País")
        self.country_input = QLineEdit()
        self.layout.addWidget(self.country_label)
        self.layout.addWidget(self.country_input)

        # Results label and input
        self.results_label = QLabel("Número de Resultados")
        self.results_input = QLineEdit()
        self.layout.addWidget(self.results_label)
        self.layout.addWidget(self.results_input)

        # Rating label and input
        self.rating_label = QLabel("Calificación Minima")
        self.rating_input = QLineEdit()
        self.layout.addWidget(self.rating_label)
        self.layout.addWidget(self.rating_input)

        # Reviews label and input
        self.reviews_label = QLabel("Minima Cantidad de Reseñas")
        self.reviews_input = QLineEdit()
        self.layout.addWidget(self.reviews_label)
        self.layout.addWidget(self.reviews_input)

        # Scrapers label and input
        self.scrapers_label = QLabel("Número de Navegadores (1-16)")
        self.scrapers_input = QLineEdit()
        self.layout.addWidget(self.scrapers_label)
        self.layout.addWidget(self.scrapers_input)

        # Checkboxes Layout
        checkbox_layout = QHBoxLayout()
        # Phone, Website and Socials Checkbox
        self.phone_checkbox = QCheckBox("Celular")
        self.website_checkbox = QCheckBox("Sitio Web")
        # self.social_checkbox = QCheckBox("Redes Sociales")
        checkbox_layout.addWidget(self.phone_checkbox)
        checkbox_layout.addWidget(self.website_checkbox)
        # checkbox_layout.addWidget(self.social_checkbox)
        self.layout.addLayout(checkbox_layout)

        # Progress Bar
        # self.progress_bar = QProgressBar()
        # self.layout.addWidget(self.progress_bar)

        # Start Scraping Button
        self.scrape_button = QPushButton("Extraer Datos")
        self.scrape_button.clicked.connect(self.start_scraping)
        self.layout.addWidget(self.scrape_button)

        self.central_widget.setLayout(self.layout)

    def start_scraping(self):
        # Get user inputs
        cities = self.location_input.text().split(',')  # Split the input into a list of cities
        country = self.country_input.text()
        num_results = int(self.results_input.text())
        rating = float(self.rating_input.text())
        reviews = int(self.reviews_input.text())
        phone = self.phone_checkbox.isChecked()
        website = self.website_checkbox.isChecked()
        scrapers = int(self.scrapers_input.text())

        queries = []  # Create an empty list to store the queries

        # Create a query for each city
        for city in cities:
            keyword = f"{self.business_input.text()} en {city.strip()}, {country}"
            query = {
                "keyword": keyword,
                "select": ["title", "link", "main_category", "rating", "reviews", "website", "phone", "address"],
                "min_rating": rating,
                "min_reviews": reviews,
                "has_phone": phone,
                "has_website": website,
                "max_results": num_results,
            }
            queries.append(query)

        # Update the configuration in config.py
        config.queries = queries
        config.number_of_scrapers = scrapers

        # Save the updated configuration to config.py
        with open('src/config.py', 'w') as config_file:
            config_file.write(f'queries = {config.queries}\n')
            config_file.write(f'number_of_scrapers = {config.number_of_scrapers}\n')

        # Print the updated configuration
        print(config.queries)

        for idx, query in enumerate(config.queries):
            print(f"Query {idx + 1}: {query}")
        print("number of scrapers:", config.number_of_scrapers)

        # Start the scraping process
        launch_tasks(ScrapeGoogleMapsLinksTask)


def run_app():
    app = QApplication(sys.argv)
    main_window = GoogleMapsScraperApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()