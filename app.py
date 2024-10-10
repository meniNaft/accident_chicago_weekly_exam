from flask import Flask
from controllers.csv_controller import csv_blueprint
from controllers.statistics_contrtoller import statistics_blueprint

app = Flask(__name__)
if __name__ == '__main__':
    app.register_blueprint(statistics_blueprint, url_prefix="/api/accidents-statistics")
    app.register_blueprint(csv_blueprint, url_prefix="/api/csv")
    app.run()
