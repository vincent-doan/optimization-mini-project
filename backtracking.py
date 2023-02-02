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
        print(CONVERT_SESSION[session] + " - Period " + str(period) + " - Classroom " + str(classroom) + \
            ' (' + str(c(classroom)) + ')' + ": Course " + str(course) + " " + str(courses_info[course]))

solution_obtained = [False]

def Assign(course):

    for slot in all_slots:
        # only need one solution
        if solution_obtained[0] == True:
            continue
        
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

        if course == N:
            print_timetable(timetable)
            solution_obtained[0] = True
        else:
            Assign(course + 1)

Assign(1)