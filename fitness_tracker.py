import sys

GOALS = {
    "marathon run": {"sport": "run", "distance_km": 42},
    "marathon swim": {"sport": "swim", "distance_km": 10},
    "century": {"sport": "cycle", "distance_km": 100},
    "5 minute mile": {"sport": "run", "speed_kmh": 19.31}, # 12 mph
    "ironman": {
        "swim": 4,
        "cycle": 180,
        "run": 42
    }
}

class Exercise:
    def __init__(self, name, distance, duration, date):
        self.name = name
        self.distance = float(distance)
        self.duration = int(duration)
        self.date = date
        
    def get_name(self):
        return self.name

    def get_distance(self):
        return self.distance
    
    def get_duration(self):
        return self.duration

    def get_date(self):
        return self.date 

class User: 
    def __init__(self, username: str):
        self.username = username
        self.exercises = []
          
    def get_username(self):
        return self.username
        
    def get_exercises(self):
        return self.exercises
        
    def read_data(self):
        try:
            user_file = f"{self.username}.txt"
            with open(user_file, "r") as person_file:
                for line in person_file.readlines():
                    if not line.strip():
                        continue
                    
                    line_split = line.split(",")
                    if len(line_split) != 4:
                        continue
                        
                    name, distance, duration, date = line_split
                    
                    try:
                        exercise = Exercise(name.strip(), distance.strip(), duration.strip(), date.strip())
                        self.exercises.append(exercise)
                    except ValueError:
                        continue
            return True
        except FileNotFoundError:
            print(f"No data file found for {self.username}. A new file will be created when you log an activity.")
            return True 
        except Exception as e:
            print(f"An error occurred reading data: {e}")
            return False
            
    def _calculate_stat_for_month(self, exercise_name, month, stat_getter):
        total_stat = 0
        parametermonth = ""
        parameteryear = ""

        if month != "all" and month is not None:
            try:
                parametermonth, parameteryear = month.split("/")
                parametermonth = parametermonth.strip()
                parameteryear = parameteryear.strip()
            except ValueError:
                return 0

        for exercise in self.exercises:
            if exercise.get_name() != exercise_name:
                continue

            if month == "all":
                total_stat += stat_getter(exercise)
                continue

            try:
                recordedmonth, recordedyear = exercise.get_date().split("/")
                if (recordedmonth.strip() == parametermonth and 
                    recordedyear.strip() == parameteryear):
                    total_stat += stat_getter(exercise)
            except ValueError:
                continue
                
        return total_stat

    def _calculate_max_stat(self, exercise_name, stat_getter):
        max_stat = 0
        for exercise in self.exercises:
            if exercise.get_name() == exercise_name:
                max_stat = max(max_stat, stat_getter(exercise))
        return max_stat

    def calculate_distance(self, exercise_name, month): 
        return self._calculate_stat_for_month(exercise_name, month, lambda ex: ex.get_distance())

    def calculate_max_distance(self, exercise_name):
        return self._calculate_max_stat(exercise_name, lambda ex: ex.get_distance())

    def calculate_duration(self, exercise_name, month):
        return self._calculate_stat_for_month(exercise_name, month, lambda ex: ex.get_duration())
    
    def calculate_max_duration(self, exercise_name): 
        return self._calculate_max_stat(exercise_name, lambda ex: ex.get_duration())


def welcome_screen():
    string_star_dash = ("*" + "-") * 13
    string_star_dash += "*"
    print(string_star_dash)
    print("| WELCOME TO FITNESS CLUB |")
    print(string_star_dash)
    print("*    LOGS YOUR WORKOUT    *")
    print("*   TRACKS YOUR FITNESS   *")
    print("*    GET FIT & HEALTHY    *")
    print(string_star_dash)

def get_username():
    while True:
        username = str(input("Login with your username: ")).strip()
        if len(username) > 20:
            print("Your username is too long (max 20 characters).")
            continue
        if not username:
             print("Username cannot be empty.")
             continue
        if " " in username or not username.isalnum():
            print("Username must be alphanumeric with no spaces.")
            continue
        else:
            return username

def display_menu(username):
    topline = "~"*27
    print("\n" + topline)
    number_of_whitespace = (len(topline) - 6) - len(username)
    if number_of_whitespace < 0:
        number_of_whitespace = 0
    print(f"| Hi {username}" + " "*number_of_whitespace + "|")
    print(topline)
    print("| [1] Log an activity     |")
    print("| [2] Track your fitness  |")
    print("| [3] Plan your health    |")
    print("| [4] Exit                |") 
    print(topline)
    
def is_valid_date(date_string):
    try:
        month_str, year_str = date_string.split('/')
        month = int(month_str)
        year = int(year_str)
        
        if len(month_str) != 2:
            print("Month must be two digits (e.g., 05).")
            return False
        if not (1 <= month <= 12):
            print("Please enter a valid month (01-12).")
            return False
        if not (2000 <= year <= 2026):
            print("Please enter a valid year (2000-2026).")
            return False
            
        return True
    except ValueError:
        print("Invalid format. Please use 'mm/yyyy'.")
        return False
    except Exception:
        print("An unexpected error occurred with the date.")
        return False

def log_workout(username):
    while True:
        exercise = input("What exercise would you like to log (swim, cycle or run): ")
        exercise_lower = exercise.lower()
        if exercise_lower in ["swim", "cycle", "run"]:
            break
        else:
            print(f"Sorry, {exercise} is not supported. Please choose swim, cycle, or run.")
            
    while True:
        date = input(f"What month did you {exercise} (mm/yyyy)? ")
        if is_valid_date(date):
            break

    while True:
        distance = input(f"What distance did you {exercise} (e.g., '10 km' or '5 miles')? ")
        distance_split = distance.split()
        try:
            value_str = distance_split[0]
            unit = "km"
            if len(distance_split) > 1:
                unit = distance_split[1].lower()
            
            value = float(value_str)
            if value < 0:
                print("Distance cannot be negative.")
                continue

            if unit == "miles":
                new_distance = value * 1.60934
                break
            elif unit == "km":
                new_distance = value
                break
            else:
                print("Invalid unit. Please use 'km' or 'miles'.")
        except (ValueError, IndexError):
            print("Invalid format. Please enter as '10 km' or '5 miles'.")

    while True:
        time = input(f"How long did you {exercise} (minutes)? ")
        try:
            time_val = int(time)
            if time_val > 0:
                break
            else:
                print("Duration must be a positive number of minutes.")
        except ValueError:
            print("Please enter a valid whole number for minutes.")
    
    file_name = f"{username}.txt"
    try:
        with open(file_name, "a") as myfile:
            myfile.write(f"{exercise_lower},{new_distance:.1f},{time},{date}\n")
        print(f"Successfully logged {new_distance:.1f}km {exercise_lower} for {date}.")
    except Exception as e:
        print(f"An error occurred while saving your workout: {e}")

def number_of_activities(username, exercise_name, month):
    user_file = f"{username}.txt"
    count = 0
    parametermonth = ""
    parameteryear = ""

    if month != "all":
        try:
            parametermonth, parameteryear = month.split("/")
            parametermonth = parametermonth.strip()
            parameteryear = parameteryear.strip()
        except (IndexError, AttributeError, ValueError):
            return 0
            
    try:
        with open(user_file, "r") as person_file:
            for line in person_file.readlines():
                if not line.strip():
                    continue
                
                try:
                    name, _, _, date = line.split(",")
                    name_stripped = name.strip()
                    date_stripped = date.strip()
                    
                    if name_stripped != exercise_name:
                        continue

                    if month == "all":
                        count += 1
                    else:
                        recordmonth, recordyear = date_stripped.split("/")
                        if (recordmonth.strip() == parametermonth and 
                            recordyear.strip() == parameteryear):
                            count += 1
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        return 0
        
    return count

def track_activity(username):
    userinfo = User(username)
    if not userinfo.read_data():
        return
    
    if not userinfo.get_exercises():
        print("You haven't logged any activities yet. Log one first!")
        return

    while True:
        exercise_name = input("What exercise would you like to track (swim, cycle, or run)? ").lower()
        if exercise_name in ["swim", "cycle", "run"]:
            break
        else:
            print(f"Sorry, {exercise_name} is not supported. Please choose swim, cycle, or run.")

    while True:
        month = input("What month would you like to track (mm/yyyy or 'all')? ").lower()
        if month == "all":
            break
        elif is_valid_date(month):
            break
            
    total_distance = userinfo.calculate_distance(exercise_name, month)
    print(f"Total distance: {total_distance:.1f}km")

    count = number_of_activities(username, exercise_name, month)
    
    if count > 0:
        average_distance = total_distance / count
        print(f"Average distance: {average_distance:.1f}km")

        total_duration = userinfo.calculate_duration(exercise_name, month)
        print(f"Total duration: {total_duration} mins")
        average_duration = total_duration / count
        print(f"Average duration: {average_duration:.0f} mins")
        
        converted_hours = average_duration / 60
        if converted_hours > 0:
            average_speed = average_distance / converted_hours
            print(f"Average speed (km/h): {average_speed:.2f}km/h")
        else:
            print("Average speed (km/h): N/A (duration is zero)")
    else:
        print("No activities found for this sport and period.")


def plan_health(username):
    userinfo = User(username)
    if not userinfo.read_data():
        return
        
    valid_goals = list(GOALS.keys())
    while True:
        print("\nSupported goals: " + ", ".join(valid_goals))
        goal = input("What goal would you like to achieve? ").lower()
        if goal in valid_goals:
            break
        else:
            print("Sorry, that goal is not supported.")
            
    while True:
        weeks = input("How many weeks do you have to achieve it? ")
        try:
            weeks_int = int(weeks)
            if weeks_int > 0:
                break
            else:
                print("Please enter a positive number of weeks.")
        except ValueError:
            print("Please enter a valid whole number for weeks.")

    print(f"To achieve the {goal} challenge in {weeks} weeks you need to:")

    if goal != "ironman" and goal != "5 minute mile":
        goal_data = GOALS[goal]
        exercise_name = goal_data["sport"]
        goal_dist = goal_data["distance_km"]
        
        max_distance = userinfo.calculate_max_distance(exercise_name)
        distance_todo = goal_dist - max_distance
        
        perweek_work = 0.0
        if distance_todo > 0.0:
            perweek_work = distance_todo / weeks_int
        
        print(f"    Increase your max {exercise_name} by {perweek_work:.1f}km per week.")
    
    elif goal == "ironman":
        goal_data = GOALS[goal]
        for sport, goal_dist in goal_data.items():
            max_distance = userinfo.calculate_max_distance(sport)
            distance_todo = goal_dist - max_distance
            
            perweek_work = 0.0
            if distance_todo > 0.0:
                perweek_work = distance_todo / weeks_int
            print(f"    Increase your max {sport} by {perweek_work:.1f}km per week.")

    elif goal == "5 minute mile":
        list_of_speeds = []
        test_exercise = GOALS[goal]["sport"]
        goal_speed = GOALS[goal]["speed_kmh"]
        
        for ex in userinfo.get_exercises():
            if ex.get_name() == test_exercise:
                total_distance = ex.get_distance()
                total_duration = ex.get_duration()
                if total_duration > 0:
                    speed_kmh = (total_distance / total_duration) * 60
                    list_of_speeds.append(speed_kmh)

        max_speed = 0.0
        if list_of_speeds:
            max_speed = max(list_of_speeds)
            
        speed_todo = goal_speed - max_speed
        
        perweek_work = 0.0
        if speed_todo > 0.0:
            perweek_work = speed_todo / weeks_int
        
        print(f"    Increase your max {test_exercise} speed by {perweek_work:.2f}km/h per week.")
        print(f"    (Your current max speed is {max_speed:.2f}km/h. Goal is {goal_speed:.2f}km/h)")


def main():
    welcome_screen()
    username = get_username()

    while True:
        display_menu(username)
        user_option = input("Choose an option (1-4): ")
        
        if user_option == "1":
            log_workout(username)
        elif user_option == "2":
            track_activity(username)
        elif user_option == "3":
            plan_health(username)
        elif user_option == "4":
            print(f"\nGoodbye, {username}!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")
        
        input("\nPress Enter to return to the menu...")

if __name__ == '__main__':
    main()

