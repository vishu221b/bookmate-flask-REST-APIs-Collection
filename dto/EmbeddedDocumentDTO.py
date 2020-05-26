def generate_embedded_dto(obj) -> dict:
    response_dto = dict()
    try:
        response_dto.setdefault('user_id', obj.user_reference)
        response_dto.setdefault('user_email', obj.user_email)
        response_dto.setdefault('created_at', str(obj.created_at))
        response_dto.setdefault('last_updated_at', str(obj.last_updated_at))
        response_dto.setdefault('is_active', obj.is_active)
        response_dto.setdefault('version', obj.version)
        return response_dto
    except Exception as e:
        print("DEBUG: Exception - {} - occurred at EmbeddedDocumentDTO.".format(e))
        return response_dto
