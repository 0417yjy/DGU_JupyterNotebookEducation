import ipywidgets as widgets
import subprocess
from IPython import get_ipython
from IPython.display import display
from IPython.display import clear_output
from IPython.core.display import HTML

# Global path constants
cd = get_ipython().run_line_magic('pwd', '')
exercise_directory = '.\\exercises\\'

# Global variables used in achievement rate
question_list = []
questions_num = 0
achievement_rate = 0
achieve_checkbox_list = []
achieve_label = widgets.Label('Participation: 0%')

class CompileOutputOnly():
    exercise_name = ""
    text = widgets.Textarea()
    outputtext = widgets.Textarea()
    compile_run_btn = widgets.Button()
    box = widgets.VBox()
    
    # Functions for compile widgets (output only)
    def run_code_clicked_o(self, b):
        usr_src_fname = exercise_directory + self.exercise_name + '.c'
        with open(usr_src_fname, 'w') as f:
            f.write(self.text.value)
        cmd_command = 'gcc ' + usr_src_fname + ' -o ' + exercise_directory + self.exercise_name
        result = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # compile the source program
        compile_error = result.communicate()[1]
        if compile_error == '':
            cmd_command = exercise_directory + self.exercise_name
            result = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # run the program
            output = result.communicate()[0]
            self.outputtext.value = output
        else:
            self.outputtext.value = compile_error

    def __init__(self, exercise_name):
        self.exercise_name = exercise_name
        src_fname = exercise_directory + exercise_name + '_src.c'
        with open(src_fname, 'r') as f:
            prewritten_src = f.read()
        self.text = widgets.Textarea(
            value=prewritten_src,
            placeholder='',
            disabled=False,
            layout=widgets.Layout(width='99%', height='200px'),
        )
        self.outputtext = widgets.Textarea(
            value='',
            placeholder='',
            disabled=True,
            layout=widgets.Layout(width='99%', height='100px'),
        )
        
        self.compile_run_btn = widgets.Button(
            description='Run Code',
            disabled=False,
            button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='',
            icon='check'
        )
        self.box = widgets.VBox(
            [widgets.Label('Write your own code:'), self.text, widgets.Label('Output:'), self.outputtext, self.compile_run_btn],
            layout = widgets.Layout(border='solid 2px', padding='1rem')
            )
        display(self.box)
        self.compile_run_btn.on_click(self.run_code_clicked_o) # Bind button event handler


# Functions for compile widgets (with input and output)
class CompileInputOuput():
    exercise_name = ""
    text = widgets.Textarea()
    outputtext = widgets.Textarea()
    inputtext = widgets.Textarea()
    compile_run_btn = widgets.Button()
    box = widgets.VBox()
    
    def run_code_clicked_io(self, b): # button event handler
        usr_src_fname = exercise_directory + self.exercise_name + '.c'
        with open(usr_src_fname, 'w') as f:
            f.write(self.text.value)
        cmd_command = 'gcc ' + usr_src_fname + ' -o ' + exercise_directory + self.exercise_name
        result = subprocess.Popen(cmd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # compile the source program
        compile_error = result.communicate()[1]
        if compile_error == '':
            cmd_command = exercise_directory + self.exercise_name
            result = subprocess.Popen(cmd_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) # run the program
            output = result.communicate(input=self.inputtext.value)[0]
            self.outputtext.value = output
        else: # compile error occured
            cmd_command = self.inputtext.value
            self.outputtext.value = compile_error

    def __init__(self, exercise_name):
        self.exercise_name = exercise_name
        src_fname = exercise_directory + self.exercise_name + '_src.c'
        with open(src_fname, 'r') as f:
            prewritten_src = f.read()
        self.text = widgets.Textarea(
            value=prewritten_src,
            placeholder='',
            disabled=False,
            layout=widgets.Layout(width='99%', height='200px'),
        )
        source_box = widgets.VBox([widgets.Label('Write your own code:'), self.text], layout = widgets.Layout(width='100%'))

        self.inputtext = widgets.Textarea(
            value='',
            placeholder='',
            disabled=False,
            layout=widgets.Layout(width='250px', height='100px'),
        )
        i_box = widgets.VBox([widgets.Label('Input:'), self.inputtext])

        self.outputtext = widgets.Textarea(
            value='',
            placeholder='',
            disabled=True,
            layout=widgets.Layout(width='250px', height='100px'),
        )
        o_box = widgets.VBox([widgets.Label('Output: '), self.outputtext])
        io_box = widgets.HBox(
            [i_box, o_box],
        )

        self.compile_run_btn = widgets.Button(
            description='Run Code',
            disabled=False,
            button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='',
            icon='check'
        )
        self.box = widgets.VBox(
            [widgets.Label('Write your own code:'), self.text, io_box, self.compile_run_btn],
            layout = widgets.Layout(border='solid 2px', padding='1rem')
            )
        display(self.box)
        
        self.compile_run_btn.on_click(self.run_code_clicked_io) # bind event handler

def convert_str2html(src_str):
    src_str = src_str.replace("\n", '<br>')
    return src_str

# Superclass for question widgets
class QuestionWidgets:
    idx = 0
    box = widgets.VBox()

    def __init__(self):
        global questions_num
        self.idx = questions_num
        questions_num = questions_num + 1

    def update_rate(self):
        global achieve_label
        global question_list
        achieved_num = 0

        # Count correct answers
        for i in question_list:
            if i.is_achieved == True:
                achieved_num += 1
        
        # Calculate achievement rate
        achievement_rate = int(achieved_num / questions_num * 100)
        # Update achievement rate label
        achieve_label.value = 'Participation: ' + str(achievement_rate) + '%'
        # Update achievement checkbox of its index
        achieve_checkbox_list[self.idx].value = True

# Class for short answer question widget
class ShortAnswerQuestion(QuestionWidgets):
    question_str=""
    answer_strs=['']
    wrong_description=""
    correct_description=""
    user_answer_text=widgets.Text()
    after_description=widgets.HTML()
    check_answer_btn=widgets.Button()
    box=widgets.VBox()
    is_achieved = False

    def s_check_clicked(self, b):
        answer_is_correct = False
        for i in self.answer_strs: # Check if the answer is correct
            if self.user_answer_text.value == i:
                answer_is_correct = True 
                break

        if answer_is_correct == True:
            self.is_achieved = True # Mark this question is completed
            self.update_rate()

            b.description='Correct'
            b.button_style='success'
            self.after_description.value = "<font color='green'>" + convert_str2html(self.correct_description)
        else:
            b.description='Incorrect'
            b.button_style='danger'
            self.after_description.value = "<font color='red'>" + convert_str2html(self.wrong_description)


    def __init__(self, question_str, answer_strs, wrong_description='', correct_description='', html_inserted=False):
        super().__init__()
        self.question_str = question_str
        self.answer_strs = answer_strs
        self.wrong_description = wrong_description
        self.correct_description = correct_description

        self.user_answer_text = widgets.Text(
            disabled=False,
        )
        self.check_answer_btn = widgets.Button(
            description='Check',
            disabled=False,
            button_style='warning',
            tooltip='',
            icon='check',
            layout=widgets.Layout(width='90px')
        )
        
        self.after_description = widgets.HTML('')

        if html_inserted == False: # If the question isn't in HTML format, convert it to HTML
            self.question_str = convert_str2html(self.question_str)

        self.box = widgets.VBox( # pack components into a VBox
            [widgets.HTML(self.question_str), self.user_answer_text, self.check_answer_btn, self.after_description],
            layout = widgets.Layout(border='solid 2px', padding='1rem')
            )
        display(self.box)
        self.check_answer_btn.on_click(self.s_check_clicked)
        global question_list # Add this object into widget list
        question_list.append(self)

    
# Class for choie question widget
class ChoiceQuestion(QuestionWidgets):
    question_str = ""
    choices = ['']
    answer_idx = 0
    wrong_description = ''
    correct_description = ''
    after_description=widgets.HTML()
    radio = widgets.RadioButtons()
    check_answer_btn = widgets.Button()
    is_achieved = False
    
    def c_check_clicked(self, b):
        if self.radio.index == self.answer_idx:
            self.is_achieved = True # Mark this question is completed
            self.update_rate()

            b.description='Correct'
            b.button_style='success'
            self.after_description.value = "<font color='green'>" + convert_str2html(self.correct_description)
        else:
            b.description='Incorrect'
            b.button_style='danger'
            self.after_description.value = "<font color='red'>" + convert_str2html(self.wrong_description)

    def __init__(self, question_str, choices, answer_idx, wrong_description='', correct_description='', html_inserted=False):
        super().__init__()
        self.question_str = question_str
        self.choices = choices
        self.answer_idx = answer_idx
        self.wrong_description = wrong_description
        self.correct_description = correct_description

        self.radio = widgets.RadioButtons(
            options = choices,
            disabled = False
        )
        self.check_answer_btn = widgets.Button(
            description='Check',
            disabled=False,
            button_style='warning',
            tooltip='',
            icon='check',
            layout=widgets.Layout(width='90px')
        )
        self.after_description = widgets.HTML('')
        if html_inserted == False:
            self.question_str = convert_str2html(question_str)
        self.box = widgets.VBox(
            [widgets.HTML(self.question_str), self.radio, self.check_answer_btn, self.after_description],
            layout = widgets.Layout(border = 'solid 2px', padding='1rem')
            )
        display(self.box)
        self.check_answer_btn.on_click(self.c_check_clicked)
        global question_list # Add this object into widget list
        question_list.append(self)

class AchieveRate:
    box = widgets.VBox()

    def __init__(self):
        # Using global variables
        global question_list
        global achieve_checkbox_list
        global achieve_label

        checks_box = widgets.HBox(layout = widgets.Layout(border='solid 1px'))
        for i in range(len(question_list)):
            c = widgets.Checkbox(
                value=False,
                description='',
                disabled=True
            )
            achieve_checkbox_list.append(c)
            checks_box.children += (c,)
        
        self.box = widgets.VBox(
            [checks_box, achieve_label],
            layout = widgets.Layout(border='ridge 2px', padding='1rem')
            )
        display(self.box)

def add_link_buttons(mod=0, prevlink='', nextlink=''):
    html_str = """
<style>
.button {
  background-color: orange;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}
.grid-container {
  display: grid;
  grid-template-columns: 100px auto 100px;
  grid-template-rows: auto;
}
</style>

<div class="grid-container">"""
    if mod == 0: # Previous and next links are inserted (default)
        html_str += "\n<div class=\"grid-item\"><a href=\"" + prevlink + """\" class="button">Previous</a></div>
<div class="grid-item"></div>
<div class="grid-item"><a href=\"""" + nextlink + """\" class=\"button\">Next</a></div>
</div>
"""
        display(HTML(html_str))
    elif mod == 1: # Only Previous link is inserted
        html_str += "\n<div class=\"grid-item\"><a href=\"" + prevlink + """\" class="button">Previous</a></div>
<div class="grid-item"></div>
<div class="grid-item"></div>
</div>
"""
        display(HTML(html_str))
    elif mod == 2: # Only next link is inserted
        html_str += "<div class=\"grid-item\"></div><div class=\"grid-item\"></div><div class=\"grid-item\"><a href=\"" + nextlink + """\" class=\"button\">Next</a></div>
</div>
"""
        display(HTML(html_str))  