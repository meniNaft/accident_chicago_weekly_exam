import json

from bson import json_util
from flask import Blueprint, jsonify
import repositories.accidents_repository as accidents_repo

statistics_blueprint = Blueprint("accidents-statistics", __name__)


@statistics_blueprint.route("/", methods=['GET'])
def get_all():
    accidents = list(accidents_repo.get_all())
    return jsonify(json.loads(json_util.dumps(accidents))), 200


@statistics_blueprint.route("/", methods=['GET'])
def get_accidents_by_area():
    pass
