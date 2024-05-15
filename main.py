from linux_engine import LinuxProblemSolverEngine

program_name_str = """
  _      _                    _____           _     _                   _____       _                
 | |    (_)                  |  __ \         | |   | |                 / ____|     | |               
 | |     _ _ __  _   ___  __ | |__) | __ ___ | |__ | | ___ _ __ ___   | (___   ___ | |_   _____ _ __ 
 | |    | | '_ \| | | \ \/ / |  ___/ '__/ _ \| '_ \| |/ _ \ '_ ` _ \   \___ \ / _ \| \ \ / / _ \ '__|
 | |____| | | | | |_| |>  <  | |   | | | (_) | |_) | |  __/ | | | | |  ____) | (_) | |\ V /  __/ |   
 |______|_|_| |_|\__,_/_/\_\ |_|   |_|  \___/|_.__/|_|\___|_| |_| |_| |_____/ \___/|_| \_/ \___|_|
"""



def print_menu():
    print(program_name_str)
    print("---------------------------------------------------------------------------------------------------------")
    print("| Description | A simple semantic web for analyzing and troubleshooting the Linux Fedora issues         |")
    print("---------------------------------------------------------------------------------------------------------")
    print("| Source      | https://discussion.fedoraproject.org/t/this-is-a-list-of-commonly-asked-questions/76986 |")
    print("---------------------------------------------------------------------------------------------------------")
    print('| Author      | Nikodem "Starsky" Swierkowski                                                           |')
    print("-------------------------------------------------------------------------------------------------------\n")

    engine = LinuxProblemSolverEngine()
    engine.reset()
    engine.run()


if __name__=="__main__":
    print_menu()