from pywebio.input import *
from pywebio.output import *
from pywebio import start_server, config
from pywebio.session import run_js
import table
from functools import partial


@config(theme='dark')
def app():
    display_table()

def add_entry_page():
    clear()
    info = input_group('Add New Student Entry', [
                input(label='Last Name', name='last_name'),
                input(label='First Name', name='first_name'),
                input(label='Email', name='email'),
                input(label='Phone Number', name='phone_number'),
                input(label='Age', type=NUMBER, name='age'),
                input(label='Major', name='major'),
                input(label='GPA', name='gpa'),
                ], cancelable = True)
    table.add_new_entry(info)
    table.update_record()
    clear()
    display_table()


def btn_click(choice, key=None):
    if choice == 'delete':
        table.delete_entry(key)
        table.update_record()
        clear()
        display_table()
    elif choice == 'edit':
        edit_entry_form(key)
    elif choice == 'add':
        add_entry_page()
    elif choice == 'view':
        view_student_info(key)
    elif choice == 'back':
        clear()
        display_table()
    elif choice == 'sort':
        clear()
        sort_table_form()

def edit_entry_form(key):
    clear()
    student = table.student_table[key]
    info = input_group('Edit Student Info for {} {} (ID: {})'.format(student.info['first_name'],student.info['last_name'],key), [
                input(label='Last Name', value=student.info['last_name'], name='last_name'),
                input(label='First Name', value=student.info['first_name'], name='first_name'),
                input(label='Email', value=student.info['email'], name='email'),
                input(label='Phone Number', value=student.info['phone_number'], name='phone_number'),
                input(label='Age', value=student.info['age'], type=NUMBER, name='age'),
                input(label='Major', value=student.info['major'], name='major'),
                input(label='GPA', value=student.info['gpa'], name='gpa'),
                ], cancelable = True)
    student.edit(info)
    table.update_record()
    clear()
    display_table()

def sort_table_form():
    sorted_dict = {}
    display = []
    info = input_group("Choose attribute and direction to sort by:",[
                select(label='Attribute:',
                       options=[{'label': 'Student ID', 'value':'student_id'},
                                {'label': 'Last Name', 'value':'last_name'},
                                {'label': 'First Name', 'value':'first_name'},
                                {'label': 'Email', 'value':'email'},
                                {'label': 'Phone Number', 'value':'phone_number'}],
                       name='attribute', value = 'student_id'),
                select(label='Direction:',
                       options=[{'label':'Ascending', 'value':'ascending'},
                                {'label':'Descending', 'value':'descending'}],
                       name='direction', value='Ascending')])
    if info == None:
        return
    if info['attribute'] == 'student_id':
        rev = False if info['direction'] == 'ascending' else True
        sorted_dict = sorted(student_table.keys(), reverse=rev)
    else:
        sorted_dict = table.sort_by_student(info['attribute'],info['direction'])
    put_markdown("# Student Table (Sorted by: {} in {} order)".format(info['attribute'],info['direction']))
    put_button(label='Go Back', color='warning', onclick=lambda: btn_click('back'))
    for s in sorted_dict:
        row = []
        row.append(s)
        student_info = sorted_dict[s].info
        for k in student_info:
            if not(k=='age' or k=='gpa' or k=='major'):
                row.append(student_info[k])
        row.append(put_buttons([{'label':'View', 'value':'view', 'color':'info'},
                                {'label':'Edit', 'value':'edit', 'color':'warning'},
                                {'label':'Delete', 'value':'delete', 'color':'danger'}], onclick=partial(btn_click, key=s)))
        display.append(row)
    put_table(display, header=["Student ID", "Last Name", "First Name", "Email", "Phone Number", "Action"])

def display_table():
    put_markdown("# Student Table")
    put_button(label='Add +', color='success', onclick=lambda: btn_click('add'))
    put_button(label='Sort', onclick=lambda: btn_click('sort'))
    display = []
    for s in table.student_table:
        row = []
        row.append(s)
        student_info = table.student_table[s].info
        for k in student_info:
            if not(k=='age' or k=='gpa' or k=='major'):
                row.append(student_info[k])
        row.append(put_buttons([{'label':'View', 'value':'view', 'color':'info'},
                                {'label':'Edit', 'value':'edit', 'color':'warning'},
                                {'label':'Delete', 'value':'delete', 'color':'danger'}], onclick=partial(btn_click, key=s)))
        display.append(row)
    put_table(display, header=["Student ID", "Last Name", "First Name", "Email", "Phone Number", "Action"])

def view_student_info(id):
    clear()
    student = table.student_table[id].info
    put_grid([
        [span(put_markdown("# Viewing Student Info for {} {} (ID: {})".format(student['first_name'],student['last_name'],id)),col=2)],
        [put_button(label='Go Back', color='warning', onclick=lambda: btn_click('back')),None],
        [put_scope('student_left'), put_scope('student_right')],
    ],cell_widths='50% 50%')
    with use_scope('student_left'):
        put_markdown("### Full Name (last, first): {}, {}".format(student['last_name'], student['first_name']))
        put_markdown("### Student ID#: {}".format(id))
        put_markdown("### Email: {}".format(student['email']))
        put_markdown("### Phone: {}".format(student['phone_number']))
    with use_scope('student_right'):
        put_markdown("### Age: {}".format(student['age']))
        put_markdown("### Major: {}".format(student['major']))
        put_markdown("### GPA: {}".format(student['gpa']))

if __name__ == '__main__':
    start_server(app, port=8080, debug=True)
