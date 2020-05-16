def user_dto(user):
    try:
        return {
            'id': str(user.pk),
            'first_name': user.first_name,
            'last_name': user.last_name if user.last_name else "",
            'date_of_birth': str(user.date_of_birth)[:10],
            'email': user.email,
            'phone_number': user.phone_number,
            'username': user.username,
            'is_active': user.is_active,
            'created_at': str(user.created_at),
            'password': str(user.password),
            'is_admin': bool(user.is_admin),
            'fav_books': list(user.fav_books),
        }
    except Exception as e:
        print("Error UDTO:2=>{}".format(e))
