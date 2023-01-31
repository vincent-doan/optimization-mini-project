from collections import defaultdict

CONVERT_SESSION = {1:"Monday morning", 
2:"Monday afternoon", 
3:"Tuesday morning", 
4:"Tuesday afternoon",
5:"Wednesday morning",
6:"Wednesday afternoon",
7:"Thursday morning",
8:"Thursday afternoon",
9:"Friday morning",
10:"Friday afternoon"}

# input
N, M = tuple(map(int, input().split()))
courses_info = dict()
professors_list = list()
for i in range(1, N + 1):
    t, g, s = tuple(map(int, input().split()))
    professors_list.append(g)
    courses_info[i] = (t, g, s)

def t(course): # number of periods
    return courses_info[course][0]
def g(course): # course professor
    if course == 0:
        return 0
    return courses_info[course][1]
def s(course): # number of students
    return courses_info[course][2]

classrooms_list = list(range(1, M + 1))
classroom_seats = list(map(int, input().split()))
assert len(classroom_seats) == M

def c(classroom): # classroom capacity
    return classroom_seats[classroom - 1]

periods_list = [(session, period) for session in range(1,11) for period in range(1,7)] # session: Monday morning to Friday afternoon. total of 10 sessions

# a slot represents some time (time = session + period) and some classroom
all_slots = [(time, classroom) for classroom in classrooms_list for time in periods_list]
# boolean list to check whether a course has been assigned yet. N = total number of courses
check_added = [False] * N
# dictionary where key = slot (slot = time + classroom), value = course
filled_slots = defaultdict(int)

# format printing of filled_slots
def print_filled_slots(filled_slots):
    filled_slots_sorted = list()
    for (((session, period), classroom), course) in filled_slots.items():
        filled_slots_sorted.append((session, period, classroom, course))
    filled_slots_sorted.sort(key=lambda t: (t[0], t[2], t[1], t[3]))
    for (session, period, classroom, course) in filled_slots_sorted:
        if course == 0: continue
        print(CONVERT_SESSION[session] + " - Period " + str(period) + " - Classroom " + str(classroom) + ": Course " + str(course))

def Backtracking(course):
    for (time, classroom) in all_slots:
        if (6 - time[1] + 1) < t(course): # there are not enough periods left in a session to cover the entire class
            continue
        if (time, classroom) in filled_slots and filled_slots[(time, classroom)] != 0: # there already exists a class
            continue
        if c(classroom) < s(course): # there are not enough seats
            continue
        if sum([g(filled_slots[time, room]) == g(course) for room in classrooms_list]) > 0: # one professor appears in two classrooms at once
            continue
        if check_added[course - 1] == True: # a course has already been assigned
            continue

        index = periods_list.index(time)
        for i in range(t(course)):
            time = periods_list[index + i]
            filled_slots[(time, classroom)] = course
            check_added[course - 1] = True
        
        if course == N:
            print_filled_slots(filled_slots)
        else:
            Backtracking(course + 1)

Backtracking(1)