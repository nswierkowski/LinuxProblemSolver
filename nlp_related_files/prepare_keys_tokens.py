import nltk
from typing import Dict, Set, Iterable, List, Tuple
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import re
from dataclasses import dataclass

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("stopwords")
nltk.download("omw-1.4")
nltk.download("wordnet")

stopword = stopwords.words('english')
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def __lemmatize_and_stemm_word(word: str):
    return stemmer.stem(
        lemmatizer.lemmatize(word)
    )

def process_words_nltk(words: List[str]):
    """
    Processing given words using lemmatize, stopwords and stemming technique
    """
    return [__lemmatize_and_stemm_word(word) for word in words if word not in stopword]


def convert_folder_name_to_words(filenames: Iterable[str]) -> Dict[str, List[str]]:
    """
    Converts directories names from docs folder to valid form
    """
    result: Dict[str, List[str]] = {}
    for filename in filenames:
        if filename == "Index":
            continue
        result[filename] = process_words_nltk(re.split(r'[-_]', filename.lower().replace("?", "")))
        

    return result
        

def print_iterable(collection: Iterable[str]):
    for element in collection:
        print(element)


@dataclass
class MatchProblemTextPercentage:
    category_percentage: float
    problem_percentage: float
    matched_word_count: int


@dataclass
class MatchHeaderTextPercentage:
    header_percentage: float
    matched_word_count: int


def match_description_to_problem_comparator(match_problem_text_percentage: MatchProblemTextPercentage) -> float:
    """
    """
    compare_value: float = match_problem_text_percentage.matched_word_count + match_problem_text_percentage.problem_percentage
    if compare_value == 0:
        return match_problem_text_percentage.category_percentage
    return compare_value


def match_description_to_header_comparator(match_problem_text_percentage: MatchHeaderTextPercentage) -> float:
    """
    """
    return match_problem_text_percentage.matched_word_count + match_problem_text_percentage.header_percentage


class UserInputHandler:
    def __init__(self, category_to_problems: Dict[str, str], problem_to_headers: Dict[str, str]) -> None:
        self.category_to_problems: Dict[str, str] = category_to_problems
        self.problem_to_headers: Dict[str, str] = problem_to_headers

        self.problems: Dict[str, List[str]] = convert_folder_name_to_words(problem_to_headers.keys())
        self.headers: Dict[str, List[str]] = convert_folder_name_to_words([header for headers in problem_to_headers.values() for header in headers])

    def try_to_match_problem_description_to_docs(self, problem_description: str) -> List[Tuple[str, MatchProblemTextPercentage]]:
        """
        Try to match user problem description to existing category, problem and header
        """
        self.processed_problem_description: Set[str] = set(process_words_nltk(problem_description.lower().split(" ")))

        result: List[Tuple[str, MatchProblemTextPercentage]] = []
        for filename, filenames_words in self.problems.items():
                category = filenames_words[0]

                percent_of_existing_considered_category = 1 if category in self.processed_problem_description else 0
                percent_of_existing_considered_problem = 0
                if len(filenames_words) <= 1:
                    percent_of_existing_considered_problem = percent_of_existing_considered_category
                
                for word in filenames_words[1:]:
                    if word in self.processed_problem_description:
                        percent_of_existing_considered_problem += 1

                if percent_of_existing_considered_problem != 0 or percent_of_existing_considered_category != 0:
                    result.append((
                        filename, MatchProblemTextPercentage(percent_of_existing_considered_category, percent_of_existing_considered_problem/max(1, len(filenames_words)-1), percent_of_existing_considered_problem)
                    ))

        return sorted(result, key= lambda record: match_description_to_problem_comparator(record[1]), reverse=True)
    
    def try_to_match_header_by_description(self, problem: str):
        """
        """
        if len(self.problem_to_headers[problem]) <= 1:
            return []
            #return [(self.problem_to_headers[problem][0], MatchHeaderTextPercentage(1, 1))]
        
        result: List[Tuple[str, MatchHeaderTextPercentage]] = []
        for header in self.problem_to_headers[problem]:

            if header == 'Index':
                continue
            
            percent_of_existing_considered_header = 0
            for headers_word in self.headers[header]:
                if headers_word in self.processed_problem_description:
                        percent_of_existing_considered_header += 1

            if percent_of_existing_considered_header != 0:
                result.append((
                    header, MatchHeaderTextPercentage(percent_of_existing_considered_header/(len(self.headers[header])-1), percent_of_existing_considered_header)
                ))

        return sorted(result, key= lambda record: match_description_to_header_comparator(record[1]), reverse=True)
