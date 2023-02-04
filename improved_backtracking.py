from convert import *
from generate_input import *

N = int(input('Enter number of courses (N): '))
M = int(input('Enter number of classrooms (M): '))
generate_input(N, M, 1)

courses_info = dict()
professors_list = list()
classrooms_list = list(range(1, M + 1))
classroom_seats = list()

with open("input.txt", 'r') as fp:
    for index, line in enumerate(fp.readlines()):
        if index == 0: continue
        if index == N+1:
            classroom_seats = list(map(int, line.rstrip().split(' ')))
            continue
        t, g, s = tuple(map(int, line.rstrip().split(' ')))
        professors_list.append(g)
        courses_info[index] = (t, g, s)

def t(course): # number of periods
    return courses_info[course][0]
def g(course): # course professor
    if course == 0:
        return 0
    return courses_info[course][1]
def s(course): # number of students
    return courses_info[course][2]
def c(classroom): # classroom capacity
    return classroom_seats[classroom - 1]

# session: Monday morning to Friday afternoon. total of 10 sessions
all_slots = [(session, period, classroom) for classroom in classrooms_list for session in range(1,11) for period in range(1,7)]
timetable = [(None, None, None)] * N

def next_slot(slot, i):
    try:
        x = slot[1] + i
        return ((slot[0], x, slot[2]))
    except:
        return (None, None, None)

def print_timetable(timetable):
    timetable_sorted = list()
    for (index, slot) in enumerate(timetable):
        course = index + 1
        for i in range(t(course)):
            next = next_slot(slot,i)
            timetable_sorted.append((next[0], next[1], next[2], course))
    timetable_sorted.sort(key=lambda t: (t[0], t[2], t[1], t[3]))
    for (session, period, classroom, course) in timetable_sorted:
        if course == 0: continue
        print(convert_session(session) + " - Period " + str(period) + " - Classroom " + str(classroom) + \
            ' (' + str(c(classroom)) + ')' + ": Course " + str(course) + " " + str(courses_info[course]))

def export_timetable(timetable):
    with open("output.txt",'w') as fp:
        timetable_sorted = list()
        for (index, slot) in enumerate(timetable):
            course = index + 1
            timetable_sorted.append((slot[0], slot[1], slot[1]+t(course)-1, course, convert_prof(courses_info[course][1]), s(course), slot[2], c(slot[2])))
        timetable_sorted.sort(key=lambda t: (t[0], t[-2], t[1], t[3]))
        for index, entry in enumerate(timetable_sorted):
            entry_string = '-'.join(list(map(str, entry)))
            fp.write(entry_string)
            if index != len(timetable_sorted) - 1:
                fp.write('\n')

def update_all_slots(course):
    temp = all_slots[:]
    for i in range(M):        
        if c(i + 1) < s(course):
            for j in range(60):
                temp[j + 60*i] = None
    updated_all_slots = [x for x in temp if x != None]
    updated_all_slots.sort(key = lambda t: c(t[2]))
    return updated_all_slots

def Assign(course):

    if course == N+1:
        print_timetable(timetable)
        export_timetable(timetable)
        return True

    for slot in update_all_slots(course):
        
        # there are not enough periods left in a session to cover the entire class
        if (6 - slot[1] + 1) < t(course): 
            continue
        
        # slot is already taken
        is_taken = False
        for (index, assigned_slot) in enumerate(timetable[:(course-1)]): 
            assigned_course = index + 1
            for i in range(t(course)):
                for j in range(t(assigned_course)):
                    if next_slot(slot, i) == next_slot(assigned_slot, j): 
                        is_taken = True
                        break
        if is_taken:
            continue
        
        # there are not enough seats
        if c(slot[2]) < s(course):
            continue
        
        # one professor appears in two classrooms at once
        has_duplicated_prof = False
        for (index, assigned_slot) in enumerate(timetable[:(course-1)]): 
            assigned_course = index + 1
            if g(course) == g(assigned_course) and slot[0] == assigned_slot[0]:
                if len(set([(slot[1] + i) for i in range(t(course))]) & set([(assigned_slot[1] + j) for j in range(t(assigned_course))])) != 0:
                    has_duplicated_prof = True
                    break
        if has_duplicated_prof:
            continue
    
        timetable[course - 1] = slot

        if Assign(course + 1):
            return True
    
    return False

Assign(1)