from flask import Blueprint, jsonify
from repositories.csv_repository import init_accidents_db

csv_blueprint = Blueprint("csv", __name__)


@csv_blueprint.route('/start-csv-insert', methods=['POST'])
def start_csv_insert():
    try:
        init_accidents_db()
        return jsonify({"message": "CSV data insertion started"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500
