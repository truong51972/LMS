def block_student(user):
    return user.role.role_name != 'Student'


def block_instructor(user):
    return user.role.role_name != 'Instructor'