import json
from bson import json_util
from flask import Blueprint, jsonify, request
import repositories.accidents_repository as accidents_repo
import services.statistics_service as statistics_service

statistics_blueprint = Blueprint("accidents/statistics", __name__)


@statistics_blueprint.route("/", methods=['GET'])
def get_all():
    accidents = list(accidents_repo.get_all())
    return jsonify(json.loads(json_util.dumps(accidents))), 200


@statistics_blueprint.route("/accidents_by_area/<int:beat_id>", methods=['GET'])
def get_accidents_by_area(beat_id: int):
    if not beat_id:
        return jsonify({"error": "beat ID is required"}), 400
    time_type = request.args.get('time-type')
    date = request.args.get('date')

    if (time_type and not date) or (not time_type and date):
        return jsonify({"error": "date params are required"}), 400

    res = statistics_service.get_accidents_by_area_and_time(beat_id, time_type, date)
    return jsonify(res), 200


