class EntityDoesNotExist(Exception):
    """
    Throw an exception when the data does not exist in the database.
    """


class EntityAlreadyExists(Exception):
    """
    Throw an exception when the data already exist in the database.
    """

class EmailAlreadyExists(Exception):
    """
    Throw an exception when the email already exist in the database.
    """

class UsernameAlreadyExists(Exception):
    """
    Throw an exception when the username already exist in the database.
    """
