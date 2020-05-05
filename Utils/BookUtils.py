from Constants.BookConstants import MANDATORY_FIELDS_FOR_CREATION, REQUEST_FIELDS_FOR_CREATION
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


def book_dto(book):
    try:
        return {
            'id': str(book.pk),
            'book_name': book.name,
            'summary': book.summary if book.summary else "",
            'author': book.author,
            'book_genre': book.genre,
            'barcode': book.barcode,
            'created_at': str(book.created_at),
            'created_by': book.created_by,
            'last_updated_at': str(book.last_updated_at),
            'last_updated_by': book.last_updated_by,
            'is_active': book.is_active
        }
    except Exception as e:
        print("Error at book_dto=>{}".format(e))
