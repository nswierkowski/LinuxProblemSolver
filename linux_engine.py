from experta import (
    Rule, 
    KnowledgeEngine,
    DefFacts, 
    Fact, 
    AND)
from facts.facts_classes import (
    UserProblemTopic, 
    UserProblemCategory, 
    UserSubProblemTopic)
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

def validate_user_tag(user_input: str, maximum_length: int) -> int:
    if not user_input.isdigit():
        return None
    
    user_value: int = int(user_input)
    if user_value < 1 or user_value > maximum_length:
        return None
    
    return user_value

class LinuxProblemSolverEngine(KnowledgeEngine):
    """Knowledge engine about linux errors"""

    @DefFacts()
    def init(self):
        print("Initialization...")
        yield Fact(action="general_categories")

    def __handle_user_input(self, enum_class: EnumMeta):
        for enum_value in enum_class:
            print(f'{enum_value.value}.{enum_value.name}')
        
        user_choice = validate_user_tag(
            input("Your choice: "),
            len(enum_class)
        )
        while not user_choice:
            user_choice = validate_user_tag(
                input("Your choice: "),
                len(enum_class)
            )
        
        return user_choice

    @Rule(Fact(action="general_categories"))
    def general_categories(self):
        """Ask user about general categories that relates to the error"""
        print("Which category is mostly related to your issue?")

        self.declare(
            UserProblemCategory(
                category = self.__handle_user_input(CommonQuestionTopic)
            )
        )

    @Rule(UserProblemCategory(category = CommonQuestionTopic.GENERAL_USAGE))
    def general_usage_topics(self):
        """Ask user about which general usage problem is related to his/her issue"""
        print("Choose your problem:")

        self.declare(
            UserProblemTopic(
                topic = self.__handle_user_input(GeneralUsage)
            )
        )

    @Rule(UserProblemCategory(category = CommonQuestionTopic.COMMON_PROBLEMS))
    def common_problems_topics(self):
        """Ask user about which common problem is related to his/her issue"""
        print("Choose your problem:")

        self.declare(
            UserProblemTopic(
                topic = self.__handle_user_input(CommonProblems)
            )
        )


    @Rule(UserProblemCategory(category = CommonQuestionTopic.DEALING_WITH_MULTIPLE_OLDER_KERNELS_IN_BOOT_MENU))
    def older_kernels_topic(self):
        """Ask user about which old kernel problem is related to his/her issue"""
        print("Choose your problem:")
        
        self.declare(
            UserProblemTopic(
                topic = self.__handle_user_input(DealingWithMultipleOlderKernelsInBootMenu)
            )
        )

    @Rule(UserProblemCategory(category = CommonQuestionTopic.UPGRADING_TO_A_NEW_RELEASE))
    def older_kernels_topic(self):
        """Ask user about which update problem is related to his/her issue"""
        print("Choose your problem:")
        
        self.declare(
            UserProblemTopic(
                topic = self.__handle_user_input(UpgradingToANewRelease)
            )
        )

    @Rule(UserProblemCategory(category = CommonQuestionTopic.DATABASES))
    def older_kernels_topic(self):
        """Ask user about which database problem is related to his/her issue"""
        print("Choose your problem:")
        
        self.declare(
            UserProblemTopic(
                topic = self.__handle_user_input(Databases)
            )
        )

    @Rule(UserProblemCategory(category = CommonQuestionTopic.DATABASES))
    def older_kernels_topic(self):
        """Ask user about which general usage problem is related to his/her issue"""
        print("Choose your problem:")
        
        self.declare(
            UserProblemTopic(
                topic = self.__handle_user_input(Databases)
            )
        )

    @Rule(
            AND(
                UserProblemCategory(category = CommonQuestionTopic.GENERAL_USAGE), 
                UserProblemTopic(topic = GeneralUsage.INSTALLING_SKYPE)
            )
        )
    def installing_skype_subtopic(self):
        """Ask user about what type of installing skype he/she is into"""
        print("Choose subtopic of your problem:")
        
        self.declare(
            UserSubProblemTopic(
                subtopic = self.__handle_user_input(InstallingSkype)
            )
        )

    @Rule(
            AND(
                UserProblemCategory(category = CommonQuestionTopic.GENERAL_USAGE), 
                UserProblemTopic(topic = GeneralUsage.INSTALLING_JAVA)
            )
        )
    def installing_java_subtopic(self):
        """Ask user about what type of installing java he/she is into"""
        print("Choose subtopic of your problem:")
        
        self.declare(
            UserSubProblemTopic(
                topic = self.__handle_user_input(InstallingJava)
            )
        )

    @Rule(
            AND(
                UserProblemCategory(category = CommonQuestionTopic.GENERAL_USAGE), 
                UserProblemTopic(topic = GeneralUsage.INSTALLING_REQUIRED_PACKAGES_TO_PLAY_MOVIES_AND_MUSIC)
            )
        )
    def installing_packages_for_movies_music_subtopic(self):
        """Show user how to install required packages for music/movies"""
        
        
        
    
