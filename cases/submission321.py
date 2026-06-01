def get_user_email(user_dict):
    if "email" in user_dict:
        return user_dict["email"]
    return "No Email"