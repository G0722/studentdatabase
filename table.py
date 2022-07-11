from student import *

# load the existing saved record
def load_record():
    dictionary =  {}
    with open('db.txt', "r") as f:
        for line in f:
            s = line.strip().split(": ")
            id, student_info = int(s[0]), s[1]
            student_info = student_info.split(', ')
            info = {'last_name': student_info[0],
                    'first_name': student_info[1],
                    'email': student_info[2],
                    'phone_number': student_info[3],
                    'age': student_info[4],
                    'major': student_info[5],
                    'gpa': student_info[6]
            }
            student = Student(info)
            dictionary[id] = student
        return dictionary

# global variables
student_table = load_record()
highest_id = max(student_table.keys())

# Allows creation of new entry in table with unique primary key
def add_new_entry(info):
    global highest_id, student_table
    if info == None:
        return
    highest_id += 1
    student_table[highest_id] = Student(info)

# Deletes entry from dictionary by key
def delete_entry(key):
    global student_table
    del student_table[key]


# Pushes changes to file in memory
def update_record():
    global student_table
    text = ''
    for k in student_table:
        text += str(k)+": "+str(student_table[k])
    f = open('db.txt', 'w')
    f.write(text)
    f.close()
