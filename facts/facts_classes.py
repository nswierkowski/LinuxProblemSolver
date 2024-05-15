from experta import Fact

class UserProblemCategory(Fact):
    pass

class UserProblemTopic(Fact):
    pass

class UserSubProblemTopic(Fact):
    pass

class Tag(Fact):
    """The area that relates to error"""
    pass

class Error(Fact):
    """The occured error"""
    pass

class Command(Fact):
    """Command connected with error"""
    pass

class User(Fact):
    """User which make an error (root or default user)"""
    pass