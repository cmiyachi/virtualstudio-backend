def validate_studio(studio):
    if (studio.bizname == '' or studio.opening_date == ''):
        return False
    else:
        return True


def validate_instructor(instructor):
    if (instructor.name == '' or instructor.age == '' or instructor.gender == ''):
        return False
    else:
        return True
