from Constants.BookConstants import MANDATORY_FIELDS_FOR_CREATION
import Models
import json


def convert_new_book_request_object_for_persistence(aa: dict, bb: Models.Book):
    for field in MANDATORY_FIELDS_FOR_CREATION:
        if field not in aa.keys():
            return f"Required field {field} is missing"
    return bb.from_json(json.dumps(aa))  # returns a dictionary


def validate_incoming_request_dto(request: dict):
    for key in MANDATORY_FIELDS_FOR_CREATION:
        if key not in request.keys() or not request[key]:
            return {'error': f" '{key}' field is a required field."}, 400
    return None
