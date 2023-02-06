from generate_input import *
from convert import *

N = int(input('Enter number of courses (N): '))
M = int(input('Enter number of classrooms (M): '))
generate_input(N, M, 1)

classrooms = [] # list of dictionaries, one corresponding to a classroom
classes = [] # list of dictionaries, one corresponding to a class
with open("input.txt", 'r') as fp:
    for index, line in enumerate(fp.readlines()):
        if index == 0: continue
        if index == N+1:
            for id, capacity in enumerate(list(map(int, line.rstrip().split(' ')))):
                classrooms.append({
                        'classroom_name': id + 1, 
                        'capacity': capacity
                        })
            continue
        t, g, s = tuple(map(int, line.rstrip().split(' ')))
        classes.append({'class_name': index, 
                        'duration': t, 
                        'professor': g, 
                        'no_students': s, 
                        'domain': list()
                        })

all_slots = [(session, period, classroom) for classroom in classrooms for session in range(1,11) for period in range(1,7)]

# decision variables are the classes (N)
# we want to assign a tuple (session, period, classroom) to a class

# first, we generate the initial domains for these N variables,
# based on the constraint of classroom capacity and no_students
# and based on the constraint of a class completed in a session
# we also sort the domains based on classroom capacity
for class_ in classes:
    temp = all_slots[:]
    for id, classroom in enumerate(classrooms):
        if classroom['capacity'] < class_['no_students']:
            for i in range(60):
                temp[i + 60*id] = None
    sorted_domain = [slot for slot in temp if slot != None]
    sorted_domain = [slot for slot in sorted_domain if slot[1] + class_['duration'] - 1 <= 6]
    sorted_domain.sort(key = lambda t: t[2]['capacity'])
    class_['domain'] = sorted_domain

def next_slot(slot, i):
    return (slot[0], slot[1] + i, slot[2])

def print_timetable(assignments):
    timetable_sorted = list()
    for (index, slot) in enumerate(assignments):
        for i in range(classes[index]['duration']):
            next = next_slot(slot,i)
            timetable_sorted.append((next[0], next[1], next[2]['classroom_name'], classes[index]['class_name']))
    timetable_sorted.sort(key=lambda t: (t[0], t[2], t[1], t[3]))
    for (session, period, classroom, course) in timetable_sorted:
        if course == 0: continue
        (t, g, s) = (classes[course - 1]['duration'], classes[course - 1]['professor'], classes[course - 1]['no_students'])
        print(convert_session(session) + " - Period " + str(period) + " - Classroom " + str(classroom) + \
            ' (' + str(classrooms[classroom - 1]['capacity']) + ')' + ": Course " + str(course) + ' ' + str((t,g,s)))

def export_timetable(assignments):
    with open("output_forward_checking.txt",'w') as fp:
        timetable_sorted = list()
        for (index, slot) in enumerate(assignments):
            course = index + 1
            timetable_sorted.append((slot[0], slot[1], slot[1] + classes[index]['duration'] - 1, course, convert_prof(classes[index]['professor']), classes[index]['no_students'], slot[2]['classroom_name'], slot[2]['capacity']))
        timetable_sorted.sort(key=lambda t: (t[0], t[-2], t[1], t[3]))
        for index, entry in enumerate(timetable_sorted):
            entry_string = '-'.join(list(map(str, entry)))
            fp.write(entry_string)
            if index != len(timetable_sorted) - 1:
                fp.write('\n')

def forward_checking(current_index, assigned_slot):
    deleted = [[]]*N
    for index, class_ in enumerate(classes):
        if index <= current_index: continue
        for possible_slot in class_['domain']:
            # use the current assignment to update the domains of assigned variables
            # first, the slots taken (computed by duration of a class) are removed
            # from the remaining domains
            if possible_slot in [next_slot(assigned_slot, i) for i in range(classes[current_index]['duration'])]:
                if possible_slot not in deleted[index]:
                    deleted[index].append(possible_slot)
            # second, slots at the same time, in different classrooms, cannot be assigned
            # to the same professor
            if class_['professor'] == classes[current_index]['professor']:
                for slot in [(assigned_slot[0], assigned_slot[1], classroom) for classroom in classrooms]:
                    for i in range(classes[current_index]['duration']):
                        if next_slot(slot, i) not in deleted[index]:
                            deleted[index].append(next_slot(slot, i))
        # remove slots from domains
        for slot in deleted[index]:
            if slot in class_['domain']:
                class_['domain'].remove(slot)
    return deleted

assignments = list()

def assign(current_index):
    if current_index == N:
        return True
    
    for slot in classes[current_index]['domain']:
        for class_ in classes:
            if len(class_['domain']) == 0:
                return False
        assignments.append(slot)
        deleted = forward_checking(current_index, slot)
        if assign(current_index + 1):
            return True
        # reverting changes to the unassigned domains once the algorithm backtracks
        for index in range(current_index + 1, N):
            classes[index]['domain'].extend(deleted[index])
            classes[index]['domain'].sort(key = lambda t: t[2]['capacity'])
    
    return False

if assign(0) == False:
    print('No solution')
else:
    print_timetable(assignments)
    export_timetable(assignments)