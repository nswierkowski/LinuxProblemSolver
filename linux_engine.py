import collections
import os
import re
from experta import (
    Rule, 
    KnowledgeEngine,
    DefFacts, 
    Fact, 
    AND,
    MATCH,
    NOT)
from facts.facts_classes import (
    UserProblemTopic, 
    UserProblemCategory, 
    UserTopicsHeader,
    Category,
    Problem)
from constants import *
# (
#     CommonQuestionTopic, 
#     GeneralUsage, 
#     CommonProblems, 
#     DealingWithMultipleOlderKernelsInBootMenu, 
#     UpgradingToANewRelease, 
#     Databases,
#     InstallingSkype)
from enum import Enum, EnumMeta
from data_cleaner.cleaner import prepare_data
from typing import Dict, Iterable, List, Optional, Tuple
from nlp_related_files.prepare_keys_tokens import MatchProblemTextPercentage, UserInputHandler
from queue import PriorityQueue

def validate_user_tag(user_input: str, maximum_length: int) -> int:
    if not user_input.isdigit():
        return None
    
    user_value: int = int(user_input)
    if user_value < 1 or user_value > maximum_length:
        return None
    
    return user_value


def handle_user_input(options: Iterable):
    for index, option in enumerate(options):
        print(f'{index+1}.{option}')
        
    user_choice = validate_user_tag(
            input("Your choice: "),
        len(options)
    )
    while not user_choice:
        print("The input must be a digit and in range")
        user_choice = validate_user_tag(
            input("Your choice: "),
            len(options)
        )
        
    return options[user_choice-1]


def print_file(filename: str) -> None:
    if not os.path.exists(filename):
        print(f"File: {filename} not found")
        return

    print(f"#################################################################################################################################################################\n")
    with open(filename, 'r') as file:
        for line in file:
            print(line, end='')
    print(f"#################################################################################################################################################################")


def print_default_problem_description(category: str, problem: str) -> None:
    filename = f"{os.getcwd()}/docs/{category}/{problem}/Index.adoc"
    print_file(filename)


def get_problems_category(problem: str) -> str:
    return re.split(r'[-_]', problem)[0]


class LinuxProblemSolverEngine(KnowledgeEngine):
    """Knowledge engine about linux errors"""

    @DefFacts()
    def init(self):
        print("Initialization...")
        category_to_problems, problem_to_headers = prepare_data()
        yield Category(category_to_problems = category_to_problems)
        yield Problem(problem_to_headers = problem_to_headers)


    @Rule(
            AND(
                Category(category_to_problems = MATCH.category_to_problems),
                Problem(problem_to_headers = MATCH.problem_to_headers)
            )
    )
    def get_user_problem_description(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str]):
        """Ask user to enter his/her problem description"""
        problem_description = input("Describe your problem (if you prefer to review the documentation yourself type 'docs')\n")
        
        if problem_description == 'docs':
            self.declare(
                Fact(
                    action = problem_description
                )
            )
            return
        
        print("Converting...")
        self.nlp_handler = UserInputHandler(category_to_problems, problem_to_headers)
        matching_problems_to_input_result: List[Tuple[str, MatchProblemTextPercentage]] = self.nlp_handler.try_to_match_problem_description_to_docs(problem_description)
        
        found_problem: Optional[str] = None
        if matching_problems_to_input_result:
            for problem in matching_problems_to_input_result:
                if problem[1].problem_percentage > MIN_ACCEPTABLE_PERCENTAGE_MATCH_PROBLEM_INPUT:
                    self.declare(UserProblemTopic(topic=problem[0]))
                    found_problem = problem[0]
                    if problem[1].category_percentage > 0:
                        self.declare(UserProblemCategory(category=get_problems_category(problem[0])))
                    return

        if not found_problem:
            for problem in matching_problems_to_input_result:
                if problem[1].category_percentage > 0:
                    self.declare(UserProblemCategory(category=re.split(r'[-_]', problem[0])[0]))
                    return
        
        self.declare(Fact(status=0))
        

    
    @Rule(
            AND(
                Category(category_to_problems = MATCH.category_to_problems),
                Problem(problem_to_headers = MATCH.problem_to_headers),
                NOT(UserProblemCategory(category = MATCH.category)),
                Fact(action="docs")
            )
    )
    def choose_category(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str]):
        """Ask user about category that relates to the error"""
        print("Which category is mostly related to your issue?")

        self.declare(
            UserProblemCategory(
                category = handle_user_input(list(category_to_problems))
            )
        )

    @Rule(
            AND(
                Category(category_to_problems = MATCH.category_to_problems),
                Problem(problem_to_headers = MATCH.problem_to_headers),
                UserProblemCategory(category = MATCH.category),
                NOT(UserTopicsHeader()),
                Fact(action="docs")
            )
    )
    def choose_problem(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str], category: str):
        """Ask user about general categories that relates to the error"""
        print("Select your issues?")

        self.declare(
            UserProblemTopic(
                topic = handle_user_input(category_to_problems[category])
            )
        )

    @Rule(
            AND(
                Category(category_to_problems = MATCH.category_to_problems),
                Problem(problem_to_headers = MATCH.problem_to_headers),
                UserProblemCategory(category = MATCH.category),
                UserProblemTopic(topic = MATCH.problem),
                Fact(action="docs")
            )
    )
    def choose_header(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str], category: str, problem: str):
        """Ask user about general categories that relates to the error"""
        print_default_problem_description(category, problem)
        print("Select header most related to you issue:")

        self.declare(
            UserTopicsHeader(
                header = handle_user_input(problem_to_headers[problem])
            )
        )

    @Rule(
            AND(
                Category(category_to_problems = MATCH.category_to_problems),
                Problem(problem_to_headers = MATCH.problem_to_headers),
                UserProblemCategory(category = MATCH.category),
                UserProblemTopic(topic = MATCH.problem),
                UserTopicsHeader(header = MATCH.header)
            )
    )
    def show_result(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str], category: str, problem: str, header: str):
        """Ask user about general categories that relates to the error"""
        
        print("--------------------------------------------------------------------------------------------------------")
        print("| Result                                                                                               |")
        print("--------------------------------------------------------------------------------------------------------")
        print_file(f"{os.getcwd()}/docs/{category}/{problem}/{header}.adoc")
        

    @Rule(
            AND(
                Category(category_to_problems = MATCH.category_to_problems),
                Problem(problem_to_headers = MATCH.problem_to_headers),
                UserProblemCategory(category = MATCH.category),
                UserProblemTopic(topic = MATCH.problem),
                NOT(UserTopicsHeader())
            )
    )
    def find_matching_header(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str], problem: str, category: str):
        """Find matching header from user input"""
        headers = self.nlp_handler.try_to_match_header_by_description(problem)

        if headers:
            for header in headers:
                if header[1].header_percentage > MIN_ACCEPTABLE_PERCENTAGE_MATCH_PROBLEM_INPUT:
                    print_default_problem_description(category, problem)
                    self.declare(
                        UserTopicsHeader(
                            header = header[0]
                        )
                    )
                    return

        self.declare(
            Fact(action="docs")
        )
        
    @Rule(
            AND(
                Category(category_to_problems = MATCH.category_to_problems),
                Problem(problem_to_headers = MATCH.problem_to_headers),
                UserProblemCategory(category = MATCH.category),
                NOT(UserTopicsHeader()),
            )
    )
    def choose_problem(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str], category: str):
        """Ask user which problem connected with category he/she is interested into"""
        print("Select your issues?")

        self.declare(
            UserProblemTopic(
                topic = handle_user_input(category_to_problems[category])
            )
        )
    

    @Rule(
            AND(
                Category(category_to_problems = MATCH.category_to_problems),
                Problem(problem_to_headers = MATCH.problem_to_headers),
                UserProblemTopic(topic = MATCH.problem),
                NOT(UserProblemCategory())
            )
    )
    def ask_user_category_valid(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str], problem: str):
        """Ask user which problem connected with category he/she is interested into"""
        print(f"Problem: {problem}")
        potential_category = get_problems_category(problem)
        print(f"Category: {potential_category}")
        user_answer = input("Can your issue be in this category? [y/n]").lower()

        if user_answer == "y":
            self.declare(
                UserProblemCategory(
                    category = potential_category)
                )
        else:
            self.declare(
                Fact(
                    action = "docs")
            )   
        

    @Rule(
            AND(
                Category(category_to_problems = MATCH.category_to_problems),
                Problem(problem_to_headers = MATCH.problem_to_headers),
                NOT(UserProblemTopic()),
                NOT(UserProblemCategory()),
                Fact(status=MATCH.status)
            )
    )
    def find_header_to_problem(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str], status: int):
        """Ask user which problem connected with category he/she is interested into"""
        
        queue: PriorityQueue = PriorityQueue()
        for problem in problem_to_headers.keys():
            for header, match_header_text_percentage in self.nlp_handler.try_to_match_header_by_description(problem):
                queue.put((match_header_text_percentage.matched_word_count + match_header_text_percentage.header_percentage, (problem, header, match_header_text_percentage)))


        while not queue.empty():
            problem, header, match_header_text_percentage = queue.get()[1]
            if match_header_text_percentage.header_percentage > MIN_ACCEPTABLE_PERCENTAGE_MATCH_PROBLEM_INPUT:
                self.declare(UserProblemTopic(topic=problem))
                self.declare(UserTopicsHeader(header=header))
                return

        print("Unfortunately I did not found anything related to entered text in documantation. Try to found it yourself!")
        self.declare(
                Fact(
                    action = "docs")
            ) 
        
    
