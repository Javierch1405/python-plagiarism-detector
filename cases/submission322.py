def get_user_email(user_dict):
    try:
        return user_dict["email"]
    except KeyError:
        return "No Email"