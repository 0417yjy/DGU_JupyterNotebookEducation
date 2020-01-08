import ipywidgets as widgets
import functools
import subprocess
from IPython import get_ipython
from IPython.display import display
from IPython.display import clear_output
cd = get_ipython().run_line_magic('pwd', '')

# Functions for compile widgets
def print_result(exercise_name, cmd_result): # used for parsing the actual result (not used anymore)
    cmd_result = cmd_result.replace(exercise_name, 'X', 2).replace(cd, 'X', 3)
    cmd_result = cmd_result[cmd_result.find(exercise_name)+6:cmd_result.find(cd)-2]
    print(cmd_result)

def run_code_clicked(b, rs_="", text=widgets.Textarea(), outputtext=widgets.Textarea()): # button event handler
    usr_src_fname = rs_ + '.c'
    with open(usr_src_fname, 'w') as f:
        f.write(text.value)
    usr_src_fname = rs_ + '.c'
    cmd_command = 'gcc ' + usr_src_fname + ' -o ' + rs_
    result = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # compile the source program
    compile_error = result.communicate()[1]
    if compile_error == '':
        cmd_command = rs_
        result = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # run the program
        output = result.communicate()[0]
        outputtext.value = output
    else:
        outputtext.value = compile_error

def add_compile_widgets(exercise_name):
    src_fname = exercise_name + '_src.c'
    with open(src_fname, 'r') as f:
        prewritten_src = f.read()
    text = widgets.Textarea(
        value=prewritten_src,
        placeholder='',
        disabled=False,
        layout=widgets.Layout(width='99%', height='200px'),
    )
    outputtext = widgets.Textarea(
        value='',
        placeholder='',
        disabled=True,
        layout=widgets.Layout(width='99%', height='100px'),
    )
    boxes = widgets.VBox([widgets.Label('Write your own code:'), text, widgets.Label('Output:'), outputtext])

    compile_run_btn = widgets.Button(
        description='Run Code',
        disabled=False,
        button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='',
        icon='check'
    )
    display(boxes, compile_run_btn)
    compile_run_btn.on_click(functools.partial(run_code_clicked, rs_=exercise_name, text=text, outputtext=outputtext)) # bind event handler

# Functions for short answer quesetion widgets
def check_clicked(b, answer_strs=[''], wd_str='', cd_str='', user_answer_text=widgets.Text(), after_description=widgets.Label()):
    answer_is_correct = False
    for i in answer_strs:
        if user_answer_text.value == i:
            answer_is_correct = True 
            break

    if answer_is_correct == True:
        b.description='Correct'
        b.button_style='success'
        after_description.value = cd_str
    else:
        b.description='Wrong'
        b.button_style='danger'
        after_description.value = wd_str


def add_short_question(question_str, answer_strs, wrong_description='', correct_description=''):
    user_answer_text = widgets.Text(
        disabled=False,
    )
    check_answer_btn = widgets.Button(
        description='Check',
        disabled=False,
        button_style='warning',
        tooltip='',
        icon='check',
        layout=widgets.Layout(width='80px')
    )
    after_description = widgets.Label('')
    qa_box = widgets.VBox([widgets.Label(question_str), user_answer_text, check_answer_btn, after_description])
    display(qa_box)
    check_answer_btn.on_click(functools.partial(check_clicked, answer_strs=answer_strs, wd_str=wrong_description, cd_str=correct_description, user_answer_text=user_answer_text, after_description=after_description))

    

def add_choice_question(question_str, choices, answer_idx):
    print('not yet implemented')