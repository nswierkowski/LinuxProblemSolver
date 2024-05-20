from experta import Fact, Field
from typing import Dict, List
from nlp_related_files.prepare_keys_tokens import MatchProblemTextPercentage, UserInputHandler

class Category(Fact):
    category_to_problems = Field(dict, mandatory=True)
    pass

class Problem(Fact):
    problem_to_headers = Field(dict, mandatory=True)
    pass

class UserProblemCategory(Fact):
    category = Field(str, mandatory=True)
    pass

class UserProblemTopic(Fact):
    topic = Field(str, mandatory=True)
    pass

class UserTopicsHeader(Fact):
    header = Field(str, mandatory=True)
    pass