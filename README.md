# Fitness club, backend interface
A Python-based command-line fitness tracker that lets users log, track, and plan workouts.
All user data is saved locally in individual .txt files, making it simple.

## Features
### User Authentication: 
- Simple username-based login system.
- Each user’s data is stored in a unique file (e.g., john.txt). 

### Log workouts:
Users can log Running, Swimming, or Cycling sessions, including:
- Date (mm/yyyy)
- Distance (in km or miles)
- Duration (in minutes)
- Automatic conversion: Miles are converted to kilometers before saving.

### Track fitness:
View performance statistics by sport and time period (monthly or all-time):
- Total & average distance
- Total & average duration
- Average speed (km/h)

### Plan Health Goals
Generate simple weekly plans for major fitness targets:
- Marathon (42 km run)
- Marathon Swim (10 km)
- Century Ride (100 km cycle)
- Ironman (4 km swim, 180 km cycle, 42 km run)
- 5-Minute Mile (run at 19.31 km/h)

## How to Use
Run the application:
python fitness_tracker.py

Login:
- Enter your username when prompted.
- If the user exists, their data is loaded.
- If not, a new file (<username>.txt) is created once you log your first activity.

Main Menu:
After logging in, you will see the main menu:
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~
| Hi <username>           |
~~~~~~~~~~~~~~~~~~~~~~~~~~~
| [1] Log an activity     |
| [2] Track your fitness  |
| [3] Plan your health    |
| [4] Exit                |
~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

- Log an activity → Enter sport, date, distance, duration
- Track fitness → Choose sport + time period (e.g., 05/2024 or all)
- Plan health goal → Choose goal + training weeks
- Exit the program

File Structure
fitness_tracker.py: The main Python script containing all the application logic.
<username.txt>: User data file storing workouts as: sport,distance_km,duration_minutes,mm/yyyy