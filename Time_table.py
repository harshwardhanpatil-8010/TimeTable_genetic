import streamlit as st
import prettytable as prettytable
import random as rnd
from datetime import datetime, timedelta


POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 1
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

# professor Class
class professor:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

# Course Class
class Course:
    def __init__(self, number, name, professors, lectures_per_week, labs_per_week=0):
        self._number = number
        self._name = name
        self._professors = professors
        self._lectures_per_week = lectures_per_week
        self._labs_per_week = labs_per_week

    def get_number(self):
        return self._number

    def get_name(self):
        return self._name

    def get_professors(self):
        return self._professors

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
        self._class_times = []
        self._professors = []
        self._courses = []
        self._depts = []
        self._panels = []

    def add_room(self, room):
        self._rooms.append(room)

    def add_lab_room(self, room):
        self._lab_rooms.append(room)

    def add_class_time(self, class_time):
        self._class_times.append(class_time)

    def add_professor(self, professor):
        self._professors.append(professor)

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

    def get_class_times(self):
        return self._class_times

    def get_professors(self):
        return self._professors

    def get_courses(self):
        return self._courses

    def get_depts(self):
        return self._depts

    def get_panels(self):
        return self._panels

    def generate_class_times(self):
        class_time_id = 1
        for day in DAYS_OF_WEEK:
            current_time = UNIVERSITY_START_TIME
            while current_time < UNIVERSITY_END_TIME:
                if current_time < LUNCH_BREAK_START or current_time >= LUNCH_BREAK_END:
                    class_time = MeetingTime(f'MT{class_time_id}', day, current_time.strftime("%H:%M"), TIME_SLOT_DURATION)
                    self.add_class_time(class_time)
                    class_time_id += 1
                    if current_time + LAB_TIME_SLOT_DURATION <= UNIVERSITY_END_TIME:
                        class_time = MeetingTime(f'MT{class_time_id}', day, current_time.strftime("%H:%M"), LAB_TIME_SLOT_DURATION)
                        self.add_class_time(class_time)
                        class_time_id += 1
                current_time += TIME_SLOT_DURATION


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
                
                class_times = [mt for mt in self._data.get_class_times() if mt.get_duration() == TIME_SLOT_DURATION]
                rnd.shuffle(class_times)
                
                for i in range(course.get_lectures_per_week()):
                    if i < len(class_times) - 1:  # Ensure we have enough consecutive slots
                        class_time = class_times[i]
                        next_class_time = class_times[i + 1]

                       
                        if class_time.get_day() == next_class_time.get_day() and \
                                (datetime.strptime(next_class_time.get_time(), "%H:%M") - datetime.strptime(class_time.get_time(), "%H:%M")) == TIME_SLOT_DURATION:
                            room = rnd.choice(self._data.get_rooms())
                            professor = rnd.choice(course.get_professors()) if course.get_professors() else None
                            if professor:
                                self._classes.append({
                                    "panel": self._panel.get_name(),
                                    "department": dept.get_name(),
                                    "course": course.get_name(),
                                    "room": room.get_number(),
                                    "professor": professor.get_name(),
                                    "class_time": f"{class_time.get_day()} {class_time.get_time()} ({class_time.get_duration()})"
                                })
                        else:
                            class_time = rnd.choice(class_times)
                            room = rnd.choice(self._data.get_rooms())
                            professor = rnd.choice(course.get_professors()) if course.get_professors() else None
                            if professor:
                                self._classes.append({
                                    "panel": self._panel.get_name(),
                                    "department": dept.get_name(),
                                    "course": course.get_name(),
                                    "room": room.get_number(),
                                    "professor": professor.get_name(),
                                    "class_time": f"{class_time.get_day()} {class_time.get_time()} ({class_time.get_duration()})"
                                })

                for _ in range(course.get_labs_per_week()):
                    lab_class_times = [mt for mt in self._data.get_class_times() if mt.get_duration() == LAB_TIME_SLOT_DURATION]
                    rnd.shuffle(lab_class_times)
                    lab_class_time = lab_class_times[0]
                    lab_room = rnd.choice(self._data.get_lab_rooms())
                    professor = rnd.choice(course.get_professors()) if course.get_professors() else None
                    if professor:
                        self._classes.append({
                            "panel": self._panel.get_name(),
                            "department": dept.get_name(),
                            "course": f"{course.get_name()} (Lab)",
                            "room": lab_room.get_number(),
                            "professor": professor.get_name(),
                            "class_time": f"{lab_class_time.get_day()} {lab_class_time.get_time()} ({lab_class_time.get_duration()})"
                        })
        return self

    def get_fitness(self):
        if self._is_fitness_changed:
            self._fitness = self.calculate_fitness()
            self._is_fitness_changed = False
        return self._fitness

    def calculate_fitness(self):
        room_time_slots = set()
        professor_time_slots = set()

        for cls in self._classes:
            room_time_slot = (cls["room"], cls["class_time"])
            professor_time_slot = (cls["professor"], cls["class_time"])

            if room_time_slot in room_time_slots or professor_time_slot in professor_time_slots:
                return 0.0  # Penalize for conflicts

            room_time_slots.add(room_time_slot)
            professor_time_slots.add(professor_time_slot)

  
        return len(self._classes) / (len(self._data.get_rooms()) * len(DAYS_OF_WEEK))

# Population Class (Genetic Algorithm)
class Population:
    def __init__(self, size, data):
        
        self._schedules = [Schedule(data, panel).initialize() for panel in data.get_panels()]

    def get_schedules(self):
        return self._schedules
    
# Genetic Algorithm
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
            new_schedule = GeneticAlgorithm._crossover_schedule(schedule1, schedule2)
            crossover_pop.get_schedules().append(new_schedule)
        return crossover_pop

    @staticmethod
    def _crossover_schedule(schedule1, schedule2):
        new_schedule = Schedule(schedule1._data, schedule1._panel)
        new_classes = []

        classes1 = schedule1.get_classes()
        classes2 = schedule2.get_classes()

        all_classes = classes1 + classes2
        rnd.shuffle(all_classes)

        num_classes = min(len(classes1), len(classes2))
        new_classes = all_classes[:num_classes]

        new_schedule._classes = new_classes
        return new_schedule

    @staticmethod
    def _mutate_population(population):
        schedules = population.get_schedules()
        if not schedules:
            raise ValueError("Cannot perform mutation on an empty population.")
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            GeneticAlgorithm._mutate_schedule(schedules[i])
        return population

    @staticmethod
    def _mutate_schedule(schedule):
        classes = schedule.get_classes()
        if not classes:
            return
        
        # Choose a random class to mutate
        class_to_mutate = rnd.choice(classes)
        new_class = class_to_mutate.copy()
        
        # Example mutation: random change in room or professor
        new_class['room'] = rnd.choice(schedule._data.get_rooms()).get_number()
        if schedule._data.get_professors():
            new_class['professor'] = rnd.choice(schedule._data.get_professors()).get_name()

        # Replace the old class with the mutated class
        index = classes.index(class_to_mutate)
        classes[index] = new_class

        # Mark the fitness as changed
        schedule._is_fitness_changed = True

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
        table = prettytable.PrettyTable(['Panel', 'Department', 'Course', 'Room', 'Professor', 'Class Time'])
        for cls in schedule.get_classes():
            table.add_row([cls["panel"], cls["department"], cls["course"], cls["room"], cls["professor"], cls["class_time"]])
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
    data.generate_class_times()

    # Input for professors
    professor_count = st.number_input('Number of Professors:', min_value=1, max_value=10, value=5, key='professor_count')
    for i in range(professor_count):
        professor_name = st.text_input(f'professor {i + 1} Name:', key=f'professor_name_{i}')
        data.add_professor(professor(f'I{i + 1}', professor_name))

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
            professor_indices = st.multiselect(f'Assign Professors for {course_name}:', 
                     options=[prof.get_name() for prof in data.get_professors()], 
                     key=f'course_professors_{i}_{j}')
            selected_professors = [prof for prof in data.get_professors() if prof.get_name() in professor_indices]
            courses.append(Course(f'C{j + 1}', course_name, selected_professors, course_lectures, course_labs))
        data.add_dept(Department(dept_name, courses))


    st.subheader("Panels")
    panel_count = st.number_input('Number of Panels:', min_value=1, max_value=5, value=2, key='panel_count')
    for i in range(panel_count):
        panel_name = st.text_input(f'Panel {i + 1} Name:', key=f'panel_name_{i}')
        data.add_panel(Panel(panel_name))

    if st.button('Generate Timetable'):
        population = Population(POPULATION_SIZE, data)
        genetic_algorithm = GeneticAlgorithm()
        evolved_population = genetic_algorithm.evolve(population)


        sorted_schedules = sorted(evolved_population.get_schedules(), key=lambda x: x.get_fitness(), reverse=True)
        best_schedule = sorted_schedules[0]

        st.header(f"{panel_name}")
        display = PrettyTableDisplay()
        display.print_schedule_as_table(best_schedule)

if __name__ == '__main__':
    main()
