import streamlit as st
import prettytable as prettytable
import random as rnd
from datetime import datetime, timedelta


POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1

# University Time Constants
UNIVERSITY_START_TIME = datetime.strptime("08:30", "%H:%M")
UNIVERSITY_END_TIME = datetime.strptime("16:45", "%H:%M")
LUNCH_BREAK_START = datetime.strptime("12:45", "%H:%M")
LUNCH_BREAK_END = datetime.strptime("13:30", "%H:%M")
TIME_SLOT_DURATION = timedelta(hours=1)
LAB_TIME_SLOT_DURATION = timedelta(hours=2)  # Lab time slot is 2 hours
DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Room Class
class Room:
    def __init__(self, number):
        self._number = number

    def get_number(self):
        return self._number

# Instructor Class
class Instructor:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

# Course Class
class Course:
    def __init__(self, number, name, instructors, lectures_per_week, labs_per_week=0):
        self._number = number
        self._name = name
        self._instructors = instructors
        self._lectures_per_week = lectures_per_week
        self._labs_per_week = labs_per_week

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_instructors(self):
        return self._instructors

    def get_lectures_per_week(self):
        return self._lectures_per_week

    def get_labs_per_week(self):
        return self._labs_per_week

# Department Class
class Department:
    def __init__(self, name, courses):
        self._name = name
        self._courses = courses

    def get_name(self):
        return self._name

    def get_courses(self):
        return self._courses

# MeetingTime Class
class MeetingTime:
    def __init__(self, id, day, time, duration):
        self._id = id
        self._day = day
        self._time = time
        self._duration = duration

    def get_id(self):
        return self._id

    def get_day(self):
        return self._day

    def get_time(self):
        return self._time

    def get_duration(self):
        return self._duration

# Panel Class
class Panel:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name

# Data Class (Storage)
class Data:
    def __init__(self):
        self._rooms = []
        self._lab_rooms = []
        self._meeting_times = []
        self._instructors = []
        self._courses = []
        self._depts = []
        self._panels = []

    def add_room(self, room):
        self._rooms.append(room)

    def add_lab_room(self, room):
        self._lab_rooms.append(room)

    def add_meeting_time(self, meeting_time):
        self._meeting_times.append(meeting_time)

    def add_instructor(self, instructor):
        self._instructors.append(instructor)

    def add_course(self, course):
        self._courses.append(course)

    def add_dept(self, dept):
        self._depts.append(dept)

    def add_panel(self, panel):
        self._panels.append(panel)

    def get_rooms(self):
        return self._rooms

    def get_lab_rooms(self):
        return self._lab_rooms

    def get_meeting_times(self):
        return self._meeting_times

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

    def get_panels(self):
        return self._panels

    def generate_meeting_times(self):
        meeting_time_id = 1
        for day in DAYS_OF_WEEK:
            current_time = UNIVERSITY_START_TIME
            while current_time < UNIVERSITY_END_TIME:
                if current_time < LUNCH_BREAK_START or current_time >= LUNCH_BREAK_END:
                    meeting_time = MeetingTime(f'MT{meeting_time_id}', day, current_time.strftime("%H:%M"), TIME_SLOT_DURATION)
                    self.add_meeting_time(meeting_time)
                    meeting_time_id += 1
                    if current_time + LAB_TIME_SLOT_DURATION <= UNIVERSITY_END_TIME:
                        meeting_time = MeetingTime(f'MT{meeting_time_id}', day, current_time.strftime("%H:%M"), LAB_TIME_SLOT_DURATION)
                        self.add_meeting_time(meeting_time)
                        meeting_time_id += 1
                current_time += TIME_SLOT_DURATION

# Schedule Class (Genetic Algorithm)
class Schedule:
    def __init__(self, data, panel):
        self._data = data
        self._panel = panel
        self._classes = []
        self._fitness = 0
        self._is_fitness_changed = True

    def get_classes(self):
        self._is_fitness_changed = True
        return self._classes

    def initialize(self):
        self._classes = []
        for dept in self._data.get_depts():
            for course in dept.get_courses():
                # Schedule lectures consecutively
                meeting_times = [mt for mt in self._data.get_meeting_times() if mt.get_duration() == TIME_SLOT_DURATION]
                rnd.shuffle(meeting_times)
                
                for i in range(course.get_lectures_per_week()):
                    if i < len(meeting_times) - 1:  # Ensure we have enough consecutive slots
                        meeting_time = meeting_times[i]
                        next_meeting_time = meeting_times[i + 1]

                        # Check if the next time slot is consecutive
                        if meeting_time.get_day() == next_meeting_time.get_day() and \
                                (datetime.strptime(next_meeting_time.get_time(), "%H:%M") - datetime.strptime(meeting_time.get_time(), "%H:%M")) == TIME_SLOT_DURATION:
                            room = rnd.choice(self._data.get_rooms())
                            instructor = rnd.choice(course.get_instructors()) if course.get_instructors() else None
                            if instructor:
                                self._classes.append({
                                    "panel": self._panel.get_name(),
                                    "department": dept.get_name(),
                                    "course": course.get_name(),
                                    "room": room.get_number(),
                                    "instructor": instructor.get_name(),
                                    "meeting_time": f"{meeting_time.get_day()} {meeting_time.get_time()} ({meeting_time.get_duration()})"
                                })
                        else:
                            meeting_time = rnd.choice(meeting_times)
                            room = rnd.choice(self._data.get_rooms())
                            instructor = rnd.choice(course.get_instructors()) if course.get_instructors() else None
                            if instructor:
                                self._classes.append({
                                    "panel": self._panel.get_name(),
                                    "department": dept.get_name(),
                                    "course": course.get_name(),
                                    "room": room.get_number(),
                                    "instructor": instructor.get_name(),
                                    "meeting_time": f"{meeting_time.get_day()} {meeting_time.get_time()} ({meeting_time.get_duration()})"
                                })

                # Schedule labs similarly if needed
                for _ in range(course.get_labs_per_week()):
                    lab_meeting_times = [mt for mt in self._data.get_meeting_times() if mt.get_duration() == LAB_TIME_SLOT_DURATION]
                    rnd.shuffle(lab_meeting_times)
                    lab_meeting_time = lab_meeting_times[0]
                    lab_room = rnd.choice(self._data.get_lab_rooms())
                    instructor = rnd.choice(course.get_instructors()) if course.get_instructors() else None
                    if instructor:
                        self._classes.append({
                            "panel": self._panel.get_name(),
                            "department": dept.get_name(),
                            "course": f"{course.get_name()} (Lab)",
                            "room": lab_room.get_number(),
                            "instructor": instructor.get_name(),
                            "meeting_time": f"{lab_meeting_time.get_day()} {lab_meeting_time.get_time()} ({lab_meeting_time.get_duration()})"
                        })
        return self

    def get_fitness(self):
        if self._is_fitness_changed:
            self._fitness = self.calculate_fitness()
            self._is_fitness_changed = False
        return self._fitness

    def calculate_fitness(self):
        room_time_slots = set()
        instructor_time_slots = set()

        for cls in self._classes:
            room_time_slot = (cls["room"], cls["meeting_time"])
            instructor_time_slot = (cls["instructor"], cls["meeting_time"])

            if room_time_slot in room_time_slots or instructor_time_slot in instructor_time_slots:
                return 0.0  # Penalize for conflicts

            room_time_slots.add(room_time_slot)
            instructor_time_slots.add(instructor_time_slot)

        # Example fitness calculation: Higher if more classes are scheduled without conflicts
        return len(self._classes) / (len(self._data.get_rooms()) * len(DAYS_OF_WEEK))

# Population Class (Genetic Algorithm)
class Population:
    def __init__(self, size, data):
        self._schedules = [Schedule(data, panel).initialize() for panel in data.get_panels()]

    def get_schedules(self):
        return self._schedules

# GeneticAlgorithm Class (Genetic Algorithm)
class GeneticAlgorithm:
    @staticmethod
    def evolve(population):
        schedules = population.get_schedules()
        if not schedules:
            raise ValueError("Population is empty. Cannot evolve an empty population.")
        return GeneticAlgorithm._mutate_population(GeneticAlgorithm._crossover_population(population))

    @staticmethod
    def _crossover_population(population):
        schedules = population.get_schedules()
        if len(schedules) < 2:
            raise ValueError("Not enough schedules for crossover. Ensure population is large enough.")

        crossover_pop = Population(0, schedules[0]._data)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(schedules[i])
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            schedule1 = GeneticAlgorithm._select_tournament_population(population).get_schedules()[0]
            schedule2 = GeneticAlgorithm._select_tournament_population(population).get_schedules()[0]
            crossover_pop.get_schedules().append(GeneticAlgorithm._crossover_schedule(schedule1, schedule2))
        return crossover_pop

    @staticmethod
    def _mutate_population(population):
        schedules = population.get_schedules()
        if not schedules:
            raise ValueError("Cannot perform mutation on an empty population.")
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            GeneticAlgorithm._mutate_schedule(schedules[i])
        return population

    @staticmethod
    def _select_tournament_population(population):
        schedules = population.get_schedules()
        if len(schedules) < TOURNAMENT_SELECTION_SIZE:
            raise ValueError(f"Not enough schedules for tournament selection. Population needs at least {TOURNAMENT_SELECTION_SIZE} schedules.")
        tournament_pop = Population(0, schedules[0]._data)
        for i in range(TOURNAMENT_SELECTION_SIZE):
            tournament_pop.get_schedules().append(schedules[rnd.randrange(0, len(schedules))])
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


# PrettyTableDisplay Class
class PrettyTableDisplay:
    def print_schedule_as_table(self, schedule):
        table = prettytable.PrettyTable(['Panel', 'Department', 'Course', 'Room', 'Instructor', 'Meeting Time'])
        for cls in schedule.get_classes():
            table.add_row([cls["panel"], cls["department"], cls["course"], cls["room"], cls["instructor"], cls["meeting_time"]])
        st.text(table)

# Streamlit UI
def main():
    st.title('University Timetable Scheduling')
    st.header('Input Data')

    data = Data()

    # Input for Rooms
    room_count = st.number_input('Number of Rooms:', min_value=1, max_value=10, value=3, key='room_count')
    for i in range(room_count):
        room_number = st.text_input(f'Room {i + 1} Number:', key=f'room_number_{i}')
        data.add_room(Room(room_number))

    # Input for Lab Rooms
    lab_room_count = st.number_input('Number of Lab Rooms:', min_value=1, max_value=5, value=1, key='lab_room_count')
    for i in range(lab_room_count):
        lab_room_number = st.text_input(f'Lab Room {i + 1} Number:', key=f'lab_room_number_{i}')
        data.add_lab_room(Room(lab_room_number))

    # Input for Meeting Times
    st.subheader("Meeting Times")
    data.generate_meeting_times()

    # Input for Instructors
    instructor_count = st.number_input('Number of Instructors:', min_value=1, max_value=10, value=5, key='instructor_count')
    for i in range(instructor_count):
        instructor_name = st.text_input(f'Instructor {i + 1} Name:', key=f'instructor_name_{i}')
        data.add_instructor(Instructor(f'I{i + 1}', instructor_name))

    # Input for Courses and Departments
    st.subheader("Departments and Courses")
    dept_count = st.number_input('Number of Departments:', min_value=1, max_value=5, value=2, key='dept_count')
    for i in range(dept_count):
        dept_name = st.text_input(f'Department {i + 1} Name:', key=f'dept_name_{i}')
        course_count = st.number_input(f'Number of Courses in {dept_name}:', min_value=1, max_value=10, value=3, key=f'course_count_{i}')
        courses = []
        for j in range(course_count):
            course_name = st.text_input(f'Course {j + 1} Name:', key=f'course_name_{i}_{j}')
            course_lectures = st.number_input(f'Number of Lectures per Week for {course_name}:', min_value=1, max_value=5, value=3, key=f'course_lectures_{i}_{j}')
            course_labs = st.number_input(f'Number of Labs per Week for {course_name}:', min_value=0, max_value=3, value=1, key=f'course_labs_{i}_{j}')
            instructor_indices = st.multiselect(f'Instructors for {course_name}:', range(instructor_count), key=f'instructor_indices_{i}_{j}')
            selected_instructors = [data.get_instructors()[k] for k in instructor_indices]
            courses.append(Course(f'C{j + 1}', course_name, selected_instructors, course_lectures, course_labs))
        data.add_dept(Department(dept_name, courses))

    # Input for Panels
    panel_count = st.number_input('Number of Panels:', min_value=1, max_value=11, value=2, key='panel_count')
    for i in range(panel_count):
        panel_name = st.text_input(f'Panel {i + 1} Name:', key=f'panel_name_{i}')
        data.add_panel(Panel(panel_name))

    if st.button("Generate Timetable"):
        population = Population(POPULATION_SIZE, data)
        genetic_algorithm = GeneticAlgorithm()
        display = PrettyTableDisplay()

        # Evolve the population for multiple generations
        for _ in range(100):  # Example: evolve over 100 generations
            population = genetic_algorithm.evolve(population)
        
        best_schedule = population.get_schedules()[0]
        st.header("Best Timetable")
        display.print_schedule_as_table(best_schedule)

if __name__ == "__main__":
    main()
