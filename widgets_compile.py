import ipywidgets as widgets
import functools
import subprocess
from IPython import get_ipython
from IPython.display import display
cd = get_ipython().run_line_magic('pwd', '')

def print_result(exercise_name, cmd_result): # used for parsing the actual result (not used anymore)
    cmd_result = cmd_result.replace(exercise_name, 'X', 2).replace(cd, 'X', 3)
    cmd_result = cmd_result[cmd_result.find(exercise_name)+6:cmd_result.find(cd)-2]
    print(cmd_result)

def on_button_clicked(b, rs_=""): # button event handler
    usr_src_fname = rs_ + '.c'
    with open(usr_src_fname, 'w') as f:
        f.write(text.value)
    usr_src_fname = rs_ + '.c'
    cmd_command = 'gcc ' + usr_src_fname + ' -o ' + rs_
    subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # compile the source program
    cmd_command = rs_
    result = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # run the program
    output = result.communicate()[0]
    print(output)

def add_exercise_widgets(exercise_name):
    src_fname = exercise_name + '_src.c'
    with open(src_fname, 'r') as f:
        prewritten_src = f.read()
    global text
    text = widgets.Textarea(
        value=prewritten_src,
        placeholder='',
        description='Write your own code:',
        disabled=False
    )
    compile_run_btn = widgets.Button(
        description='Run Code',
        disabled=False,
        button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='',
        icon='check'
    )
    display(text, compile_run_btn)
    compile_run_btn.on_click(functools.partial(on_button_clicked, rs_=exercise_name)) # bind event handler