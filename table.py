from student import *
import copy

# load the existing saved record
def load_record():
    dictionary =  {}
    with open('db.txt', "r") as f:  # reading each line as string
        for line in f:
            # separate id and student_info
            s = line.strip().split(": ")
            id, student_info = int(s[0]), s[1]
            # separate student_info by comma to create Student object
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
            # final action to assign entry "ID: student" into dict
            dictionary[id] = student
        return dictionary

# global variables
student_table = load_record()
highest_id = max(student_table.keys()) if student_table else 0

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

# Performs sorting based on attribute and ascending/descending order
def sort_by_student(attribute, direction):
    global student_table
    rev = False if direction == 'ascending' else True
    to_sort = {}
    # isolate the key : attribute from the entire student_table dict
    for k in student_table:
        to_sort[k] = student_table[k].info[attribute]
    # sorts isolated dict into a list based on the key's value
    to_sort = sorted(to_sort.items(), key=lambda ts: (ts[1], ts[0]), reverse=rev)
    sorted_dict = {}
    # reads to_sort sequentially and recreates new sorted_dict
    for k in to_sort:
        sorted_dict[k[0]] = student_table[k[0]]
    return sorted_dict

# Performs search based on the attribute provided and keyword
def search_by_attribute(attribute, keyword):
    global student_table
    # first isolate key and attribute into separate dict
    to_find = {}
    for k in student_table:
        to_find[k] = student_table[k].info[attribute]
    # search entire to_find for the keyword provided and list all such matches
    found_items = {}
    for k in to_find:
        if to_find[k] == keyword:
            found_items[k] = student_table[k]
    return found_items

# Pushes changes to file in memory
def update_record():
    global student_table
    text = ''
    # creating line in the form
    # "id: last_name, first_name, email, phone_number, age, major, gpa"
    for k in student_table:
        text += str(k)+": "+str(student_table[k])
    f = open('db.txt', 'w')
    f.write(text)
    f.close()
