import ipywidgets as widgets
import functools
import subprocess
from IPython import get_ipython
from IPython.display import display
from IPython.display import clear_output
cd = get_ipython().run_line_magic('pwd', '')
exercise_directory = '.\\exercises\\'
#change Label to html would work I think

# Functions for compile widgets (output only) (adding exercise direcotires)
def run_code_clicked_o(b, rs_="", text=widgets.Textarea(), outputtext=widgets.Textarea()): # button event handler
    usr_src_fname = exercise_directory + rs_ + '.c'
    with open(usr_src_fname, 'w') as f:
        f.write(text.value)
    cmd_command = 'gcc ' + usr_src_fname + ' -o ' + exercise_directory + rs_
    result = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # compile the source program
    compile_error = result.communicate()[1]
    if compile_error == '':
        cmd_command = exercise_directory + rs_
        result = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # run the program
        output = result.communicate()[0]
        outputtext.value = output
    else:
        outputtext.value = compile_error

def add_compile_widgets_o(exercise_name):
    src_fname = exercise_directory + exercise_name + '_src.c'
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
    compile_run_btn.on_click(functools.partial(run_code_clicked_o, rs_=exercise_name, text=text, outputtext=outputtext)) # bind event handler

# Functions for compile widgets (with input and output) (working)
def run_code_clicked_io(b, rs_="", text=widgets.Textarea(), outputtext=widgets.Textarea(), inputtext=widgets.Textarea()): # button event handler
    usr_src_fname = exercise_directory + rs_ + '.c'
    with open(usr_src_fname, 'w') as f:
        f.write(text.value)
    cmd_command = 'gcc ' + usr_src_fname + ' -o ' + exercise_directory + rs_
    result = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # compile the source program
    compile_error = result.communicate()[1]
    if compile_error == '':
        cmd_command = exercise_directory + rs_
        result = subprocess.Popen(cmd_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # run the program
        output = result.communicate(input=inputtext.value)[0]
        outputtext.value = output
    else: # compile error occured
        cmd_command = inputtext.value
        outputtext.value = compile_error

def add_compile_widgets_io(exercise_name):
    src_fname = exercise_directory + exercise_name + '_src.c'
    with open(src_fname, 'r') as f:
        prewritten_src = f.read()
    text = widgets.Textarea(
        value=prewritten_src,
        placeholder='',
        disabled=False,
        layout=widgets.Layout(width='99%', height='200px'),
    )

    inputtext = widgets.Textarea(
        value='',
        placeholder='',
        disabled=False,
        layout=widgets.Layout(width='250px', height='100px'),
    )
    i_box = widgets.VBox([widgets.Label('Input:'), inputtext])

    outputtext = widgets.Textarea(
        value='',
        placeholder='',
        disabled=True,
        layout=widgets.Layout(width='250px', height='100px'),
    )
    o_box = widgets.VBox([widgets.Label('Output: '), outputtext])
    io_box = widgets.HBox(
        [i_box, o_box],
        #layout=widgets.Layout(max_width='100%', height='150px'),
    )
    boxes = widgets.VBox([widgets.Label('Write your own code:'), text, io_box])

    compile_run_btn = widgets.Button(
        description='Run Code',
        disabled=False,
        button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='',
        icon='check'
    )
    display(boxes, compile_run_btn)
    compile_run_btn.on_click(functools.partial(run_code_clicked_io, rs_=exercise_name, text=text, outputtext=outputtext, inputtext=inputtext)) # bind event handler

# Functions for short answer question widgets
def s_check_clicked(b, answer_strs=[''], wd_str='', cd_str='', user_answer_text=widgets.Text(), after_description=widgets.Label()):
    answer_is_correct = False
    for i in answer_strs:
        if user_answer_text.value == i:
            answer_is_correct = True 
            break

    if answer_is_correct == True:
        b.description='Correct'
        b.button_style='success'
        after_description.layout = widgets.Layout(border='solid 1px')
        after_description.value = cd_str
    else:
        b.description='Incorrect'
        b.button_style='danger'
        after_description.layout = widgets.Layout(border='solid 1px')
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
        layout=widgets.Layout(width='90px')
    )
    after_description = widgets.Label('')
    qa_box = widgets.VBox([widgets.Label(question_str), user_answer_text, check_answer_btn, after_description])
    display(qa_box)
    check_answer_btn.on_click(functools.partial(s_check_clicked, answer_strs=answer_strs, wd_str=wrong_description, cd_str=correct_description, user_answer_text=user_answer_text, after_description=after_description))

    
#Functions for choice question widgets
def c_check_clicked(b, answer_idx=0, cd_str='', wd_str='', radio=widgets.RadioButtons(), after_description=widgets.Label()):
    if radio.index == answer_idx:
        b.description='Correct'
        b.button_style='success'
        after_description.layout = widgets.Layout(border='solid 1px')
        after_description.value = cd_str
    else:
        b.description='Incorrect'
        b.button_style='danger'
        after_description.layout = widgets.Layout(border='solid 1px')
        after_description.value = wd_str

def add_choice_question(question_str, choices, answer_idx, wrong_description='', correct_description=''):
    radio = widgets.RadioButtons(
        options = choices,
        disabled = False
    )
    check_answer_btn = widgets.Button(
        description='Check',
        disabled=False,
        button_style='warning',
        tooltip='',
        icon='check',
        layout=widgets.Layout(width='90px')
    )
    after_description = widgets.Label('')
    choice_box = widgets.VBox([widgets.Label(question_str), radio, check_answer_btn, after_description])
    display(choice_box)
    check_answer_btn.on_click(functools.partial(c_check_clicked, answer_idx=answer_idx, cd_str=correct_description, wd_str=wrong_description, radio=radio, after_description=after_description))