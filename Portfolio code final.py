from tkinter import *              #importing all the libraries I'll need for the code
from tkinter.messagebox import *
from tkinter import messagebox
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from sqlite3 import*
from tkinter import ttk
import smtplib
from PIL import Image, ImageTk



#creating the main window; Landing page - the first Toplevel window you see when you run the code, background picture (made in Canva) is placed using PIL library to fit fullscreen window
t = Tk()
screen_width = t.winfo_screenwidth()
screen_height = t.winfo_screenheight()
t.attributes('-fullscreen', True)
pil_image = Image.open('LandingPage.png')

resized_image = pil_image.resize((screen_width, screen_height))
background_image = ImageTk.PhotoImage(resized_image)

background_label = Label(t, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

points=0



def next_question(current_question, t4): #defining next question function which is used everytime you click on the 'Next question' button in the quiz
    current_question.withdraw()
    if current_question == q1t:   
        q2(t4)                       #opens the next window with questions and withdraws the previous one
    elif current_question == q2t:    
        q3(t4)                         

    elif current_question == q3t:
        q4(t4)

    elif current_question == q4t:
        q5(t4)

    elif current_question == q5t:
        q6(t4)

    return





#defining the first window, collecting data that will later be used to calculate bmi  
def q1(t4):
    global q1t
    global weight
    global q2t
    global height

    q1t = Toplevel(t4)
    q1t.attributes('-fullscreen', True)
    q1t.config(bg='pink')

    def store_data():       #creating a function that stores data into corresponding database for question 1
        gender = uno.get()
        selected_weight = weight.get()
        selected_height = height.get()
        conn = connect('data.db', timeout = 10)    #tables in the database correspond to the question number (question 1 -> table1)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS table1 (
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        gender TEXT NOT NULL,
                        weight INTEGER NOT NULL,
                        height INTEGER NOT NULL)''')
        c.execute("INSERT INTO table1 (gender, weight, height) VALUES (?, ?, ?)", (gender, selected_weight, selected_height))
        conn.commit()
        conn.close()



    #designing the toplevel window for question 1
    s = ttk.Style()
    s.configure("my.TCombobox", font=('Poppins', 17), width=10, scrollbarwidth=20)

    l = Label(q1t, text='Please choose your weight', font=('Poppins', 25))
    l.place(x=550, y=50)
    weight = ttk.Combobox(q1t, style="my.TCombobox", values=(list(range(30, 200))), font=('Poppins', 25)) #setting the values the user chooses their weight from
    weight.place(x=550, y=100)
    l1 = Label(q1t, text='kg', font=('Poppins', 25))
    l1.place(x=940, y=100)
    l = Label(q1t, text='Please choose your height', font=('Poppins', 25))
    l.place(x=550, y=300)
    height = ttk.Combobox(q1t, style="my.TCombobox", values=(list(range(120, 301))), font=('Poppins', 25))
    height.place(x=550, y=350)
    l1 = Label(q1t, text='cm', font=('Poppins', 25))
    l1.place(x=940, y=350)
    b3 = Button(q1t, text='Next question', font=('Poppins', 20), command=lambda: [store_data(), next_question(q1t, t4)])
    button_height = int(screen_height * 0.1)  # calculate the height of the button as 10% of the screen height
    b3.place(relx=0.5, rely=1.0, anchor='s', y=-button_height)
    q1t.attributes("-topmost", True)
    q1t.transient(t4)
    l2 = Label(q1t, text='Please choose your gender', font=('Poppins', 25))
    l2.place(x=550, y=550)
    uno = ttk.Combobox(q1t, values=["Male", "Female", "Other", "I prefer not to say"], font=('Poppins', 25))
    uno.place(x=550, y=600) 

    return q1t




#defining window
def q2(t4):
    global q2t, var1, var2
    q2t = Toplevel(t4)
    q2t.attributes('-fullscreen', True)
    q2t.config(bg='pink')
    var1 = IntVar()
    var2 = IntVar() #setting 2 integer variables for 2 groups of radiobuttons 

    def add_p2(var1, var2): #defining the function that adds points to global variable points; based on what option user selects 
        global points
        if var1.get()==1:
            points += 1
        elif var1.get()==2:
            points += 2
        elif var1.get()==3:
            points += 3
        elif var1.get()==4:
            points += 4
        elif var1.get()==5:
            points += 5
        if var2.get()==1:
            points += 1
        elif var2.get()==2:
            points += 2
        elif var2.get()==3:
            points += 3
        elif var2.get()==4:
            points += 4
        elif var2.get()==5:
            points += 5
        


    def store_data2():   #collecting inputs based on user selection for from question 2        
        conn = connect('data.db', timeout = 10)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS table2 (
                    id2 INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_number INTEGER NOT NULL,
                    work_setting TEXT NOT NULL,
                    free_time TEXT NOT NULL,
                    FOREIGN KEY(id2) REFERENCES table1(ID))''')

        #defining label_dict dictionary so data will be stored as 'TEXT' , not Int (integer value)
        label_dict = {
        1: 'Physical/manual job',
        2: 'Mainly on my feet',
        3: 'It varies',
        4: 'Office job',
        5: 'Work from home'
        }
        work_setting = label_dict.get(var1.get())   
        
        label_dict2 = {
        1: 'Flexible',
        2: 'Evenings and weekends',
        3: 'Only evenings',
        4: 'Only weekends',
        5: 'None'
        }
        free_time = label_dict2.get(var2.get())

        c.execute("INSERT INTO table2 (question_number, work_setting, free_time) VALUES (?, ?, ?)",
                      (2, work_setting, free_time))
         
        conn.commit()
        conn.close()


    
    #first group of radiobuttons
    l = Label(q2t, text='Choose what work setting fits you the most currently:', font=('Poppins', 22))
    l.place(x=screen_width / 3, y=50)
    r1 = Radiobutton(q2t, text='Office job', variable=var1, value=4,
                     bg='pink', font=("Poppins", 20))  
    r1.place(x=screen_width / 3, y=90)
    r2 = Radiobutton(q2t, text='Mainly on my feet', variable=var1, value=2,
                     bg='pink', font=("Poppins", 20))
    r2.place(x=screen_width / 3, y=140)
    r3 = Radiobutton(q2t, text='Physical/manual job', variable=var1, value=1,
                     bg='pink', font=("Poppins", 20))
    r3.place(x=screen_width / 3, y=190)
    r4 = Radiobutton(q2t, text='Work from home', variable=var1, value=5,
                     bg='pink', font=("Poppins", 20))
    r4.place(x=screen_width / 3, y=240)
    r5 = Radiobutton(q2t, text='It varies', variable=var1, value=3,
                     bg='pink', font=("Poppins", 20))
    r5.place(x=screen_width / 3, y=290)
    q2t.attributes("-topmost", True)
    q2t.transient(t4)
    
    #second group of radiobuttons
    l1 = Label(q2t, text=' How much free time do you have weekly?', font=('Poppins', 22))
    l1.place(x=screen_width / 3, y=360)
    r11 = Radiobutton(q2t, text='Only weekends ', variable=var2, value=4,
                      bg='pink', font=("Poppins", 20))
    r11.place(x=screen_width / 3, y=410)
    r22 = Radiobutton(q2t, text='Only evenings', variable=var2, value=3,
                      bg='pink', font=("Poppins", 20))
    r22.place(x=screen_width / 3, y=460)
    r33 = Radiobutton(q2t, text='Evenings and weekends', variable=var2, value=2,
                     bg='pink', font=("Poppins", 20))
    r33.place(x=screen_width / 3, y=510)
    r44 = Radiobutton(q2t, text='Flexible', variable=var2, value=1,
                      bg='pink', font=("Poppins", 20))
    r44.place(x=screen_width / 3, y=560)
    r55 = Radiobutton(q2t, text='None', variable=var2, value=5, bg='pink',
                      font=("Poppins", 20))
    r55.place(x=screen_width / 3, y=610)
    b = Button(q2t, text='Next question', font=('Poppins', 22),
               command=lambda: [store_data2(), add_p2(var1, var2), next_question(q2t, t4)]) #by clicking on the button you automatically go to the next question, points based on your answers are added to global variable 'points' and data is stored into database
    button_height = int(screen_height * 0.1)  
    b.place(relx=0.5, rely=1.0, anchor='s', y=-button_height)

    return q2t




        
#defining window 3
def q3(t4):
    global q3t, var1, var2
    q3t = Toplevel(t4)
    q3t.attributes('-fullscreen', True)
    q3t.config(bg='pink')
    var1 = IntVar()
    var2 = IntVar() #using two variables for 2 groups of radiobuttons
    
    def add_p3(var1, var2):
        global points
        if var1.get()==1:
            points += 1
        elif var1.get()==2:
            points += 2
        elif var1.get()==3:
            points += 3
        elif var1.get()==4:
            points += 4
        elif var1.get()==5:
            points += 5
        elif var1.get()==6:
            points += 6
        if var2.get()==1:
            points += 1
        elif var2.get()==2:
            points += 2
        elif var2.get()==3:
            points += 3
        elif var2.get()==4:
            points += 4
        

    
    def store_data3():   
        conn = connect('data.db', timeout = 10)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS table3 (
                    id3 INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_number INTEGER NOT NULL,
                    average_steps TEXT NOT NULL,
                    exercise_time TEXT NOT NULL,
                    FOREIGN KEY(id3) REFERENCES table2(id2))''')
        
        label_dict = {
        1: 'More than 15000',
        2: '10000-15000',
        3: '7500-10000',
        4: '5000-7500',
        5: '2000-5000',
        6: 'Less than 2000'
        }
        average_steps = label_dict.get(var1.get())
        
        label_dict2 = {
        1: 'Yes, more than 5 hours per week',
        2: 'Yes, between 2 and 5 hours per week',
        3: 'Yes, about 2 hours per week',
        4: 'No'
        }
        exercise_time = label_dict2.get(var2.get())

        c.execute("INSERT INTO table3 (question_number, average_steps, exercise_time) VALUES (?, ?, ?)",
                      (3, average_steps, exercise_time))
        conn.commit()
        conn.close()

    #designing layout for question 3
    l = Label(q3t, text='How many steps do you average per day?', font=('Poppins', 20))
    l.place(x=screen_width / 3, y=50)
    r1 = Radiobutton(q3t, text='Less than 2000', variable=var1, value=6,
                     bg='pink', font=("Poppins", 18))
    r1.place(x=screen_width / 3, y=90)
    r2 = Radiobutton(q3t, text='2000-5000', variable=var1, value=5,
                     bg='pink', font=("Poppins", 18))
    r2.place(x=screen_width / 3, y=140)
    r3 = Radiobutton(q3t, text='5000-7500', variable=var1, value=4, 
                     bg='pink', font=("Poppins", 18))
    r3.place(x=screen_width / 3, y=190)
    r4 = Radiobutton(q3t, text='7500-10000', variable=var1, value=3, 
                     bg='pink', font=("Poppins", 18))
    r4.place(x=screen_width / 3, y=240)
    r5 = Radiobutton(q3t, text='10000-15000', variable=var1, value=2, 
                     bg='pink', font=("Poppins", 18))
    r5.place(x=screen_width / 3, y=290)
    r6 = Radiobutton(q3t, text='More than 15000', variable=var1, value=1,
                     bg='pink', font=("Poppins", 18))
    r6.place(x=screen_width / 3, y=340)

    l1 = Label(q3t, text='Do you currently spend time exercising?', font=('Poppins', 20))
    l1.place(x=screen_width / 3, y=410)
    r11 = Radiobutton(q3t, text='Yes, more 5 hours per week', variable=var2, value=1,
                       bg='pink', font=("Poppins", 18))
    r11.place(x=screen_width / 3, y=460)
    r22 = Radiobutton(q3t, text='Yes, between 2 and 5 hours per week', variable=var2, value=2,
                       bg='pink', font=("Poppins", 18))
    r22.place(x=screen_width / 3, y=510)
    r33 = Radiobutton(q3t, text='Yes, about 2 hours per week', variable=var2, value=3,
                      bg='pink', font=("Poppins", 18))
    r33.place(x=screen_width / 3, y=560)
    r44 = Radiobutton(q3t, text='No', variable=var2, value=4, bg='pink',
                      font=("Poppins", 18))
    r44.place(x=screen_width / 3, y=610)

    b = Button(q3t, text='Next question', font=('Poppins', 20),
               command=lambda: [next_question(q3t, t4), add_p3(var1, var2), store_data3()])
    button_height = int(screen_height * 0.1)  
    b.place(relx=0.5, rely=1.0, anchor='s', y=-button_height)
    q3t.attributes("-topmost", True)
    q3t.transient(t4)

    return q3t


#defining window 4 as a window with non-scoring question. It collects data on preferred and disliked type of exercise
def q4(t4):
    global q4t, selected_var1, selected_var3
    q4t = Toplevel(t4)
    q4t.attributes('-fullscreen', True)
    q4t.config(bg='pink')

    selected_var1 = StringVar(value='')

    selected_var3 = StringVar(value='')
    selected_var1.set(None)
    selected_var3.set(None)

    preferred_type = ''
    disliked_type = ''

    def get_selected():  #collecting inputs based on user selection in question 4; preferred and disliked type of exercise
        global preferred_type, disliked_type
        preferred_type = selected_var1.get()
        disliked_type = selected_var3.get()
        if preferred_type and disliked_type:   #storing data into database
            conn = connect('data.db', timeout = 10)
            c = conn.cursor()
            inquires='''CREATE TABLE IF NOT EXISTS table4 (
                    id4 INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_num INTEGER NOT NULL,
                    preferred_type TEXT NOT NULL,
                    disliked_type TEXT NOT NULL,
                    FOREIGN KEY(id4) REFERENCES table3(id3))'''
            c.execute(inquires)
            c.execute('''INSERT INTO table4 (question_num, preferred_type, disliked_type)
                         VALUES (?, ?, ?)''', (4, preferred_type, disliked_type))
            conn.commit()
            conn.close()
    

    #designing the layout for question 4
    l = Label(q4t, text='What is your preferred type of exercise?', font=('Poppins', 17))
    l.place(x=screen_width / 6, y=50)
    r1 = Radiobutton(q4t, text='Walking & Hiking', variable=selected_var1,
                     value='Walking & Hiking', bg='pink', font=("Poppins", 16))
    r1.place(x=screen_width / 6, y=90)
    r2 = Radiobutton(q4t, text='HIIT & Crossfit', variable=selected_var1, value='HIIT & Crossfit',
                     bg='pink', font=("Poppins", 16))
    r2.place(x=screen_width / 6, y=140)
    r3 = Radiobutton(q4t, text='Aerobic & Cardio', variable=selected_var1, 
                     value='Aerobic & Cardio', bg='pink', font=("Poppins", 16))
    r3.place(x=screen_width / 6, y=190)
    r4 = Radiobutton(q4t, text='Yoga & Pilates', variable=selected_var1, value='Yoga & Pilates',
                     bg='pink', font=("Poppins", 16))
    r4.place(x=screen_width / 6, y=240)
    r5 = Radiobutton(q4t, text='Strength Training', variable=selected_var1,
                     value='Strength Training', bg='pink', font=("Poppins", 16))
    r5.place(x=screen_width / 6, y=290)
    r6 = Radiobutton(q4t, text='Sports Training (group sports)', variable=selected_var1,
                     value='Sports Training (group sports)', bg='pink', font=("Poppins", 16))
    r6.place(x=screen_width / 6, y=340)
    r7 = Radiobutton(q4t, text='Swimming', variable=selected_var1, value='Swimming', bg='pink',
                     font=("Poppins", 16))
    r7.place(x=screen_width / 6, y=390)
    r8 = Radiobutton(q4t, text='Tennis', variable=selected_var1, value='Tennis', bg='pink',
                     font=("Poppins", 16))
    r8.place(x=screen_width / 6, y=440)

    l2 = Label(q4t, text='Which type of exercise do you dislike?', font=('Poppins', 17))
    l2.place(x=(screen_width - (screen_width / 12) * 5), y=50)
    r12 = Radiobutton(q4t, text='Walking & Hiking', variable=selected_var3,
                      value='Walking & Hiking', bg='pink', font=("Poppins", 16))
    r12.place(x=(screen_width - (screen_width / 12) * 5), y=90)
    r23 = Radiobutton(q4t, text='HIIT & Crossfit', variable=selected_var3,
                      value='HIIT & Crossfit', bg='pink', font=("Poppins", 16))
    r23.place(x=(screen_width - (screen_width / 12) * 5), y=140)
    r32 = Radiobutton(q4t, text='Aerobic & Cardio', variable=selected_var3, 
                      value='Aerobic & Cardio', bg='pink', font=("Poppins", 16))
    r32.place(x=(screen_width - (screen_width / 12) * 5), y=190)
    r42 = Radiobutton(q4t, text='Yoga & Pilates', variable=selected_var3, value='Yoga & Pilates',
                      bg='pink', font=("Poppins", 16))
    r42.place(x=(screen_width - (screen_width / 12) * 5), y=240)
    r52 = Radiobutton(q4t, text='Strength Training', variable=selected_var3,
                      value='Strength Training', bg='pink', font=("Poppins", 16))
    r52.place(x=(screen_width - (screen_width / 12) * 5), y=290)
    r62 = Radiobutton(q4t, text='Sports Training (group sports)', variable=selected_var3,
                      value='Sports Training (group sports)', bg='pink', font=("Poppins", 16))
    r62.place(x=(screen_width - (screen_width / 12) * 5), y=340)
    r72 = Radiobutton(q4t, text='Swimming', variable=selected_var3, value='Swimming', bg='pink',
                      font=("Poppins", 16))
    r72.place(x=(screen_width - (screen_width / 12) * 5), y=390)
    r82 = Radiobutton(q4t, text='Tennis', variable=selected_var3, value='Tennis', bg='pink',
                      font=("Poppins", 16))
    r82.place(x=(screen_width - (screen_width / 12) * 5), y=440)
    r92 = Radiobutton(q4t, text='There is nothing I dislike', variable=selected_var3,
                      value='There is nothing I dislike', bg='pink', font=("Poppins", 16))
    r92.place(x=(screen_width - (screen_width / 12) * 5), y=490)

    b = Button(q4t, text='Next question', font=('Poppins', 20), command=lambda: [next_question(q4t, t4), get_selected()])  
    button_height = int(screen_height * 0.1)  
    b.place(relx=0.5, rely=1.0, anchor='s', y=-button_height)
    q4t.attributes("-topmost", True)
    q4t.transient(t4)

    return q4t


#defining window 5, similar to window 2 but it has a dropdown option
def q5(t4):
    global q5t, var, add_points_q5
    q5t = Toplevel(t4)
    q5t.attributes('-fullscreen', True)
    q5t.config(bg='pink')
    var = IntVar()
    
    def add_p5(var):
        global points
        if var.get()==1:
            points += 1
        elif var.get()==2:
            points += 2
        elif var.get()==3:
            points += 3
       

    def store_data5():
        conn = connect('data.db', timeout = 10)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS table5 (
                id5 INTEGER PRIMARY KEY AUTOINCREMENT,
                question_number INTEGER NOT NULL,
                physical_activity TEXT NOT NULL,
                meals TEXT NOT NULL,
                FOREIGN KEY(id5) REFERENCES table4(id4))''')
        
        label_dict = {
        1: 'Balanced: mix of carbohydrates, proteins and fats',
        2: 'Planned: mix of carbohydrates, proteins and fats along\n with micrunutrients like vitamins and minerals',
        3: 'Hectic: mostly simple carbohydrates with little else',
        }
        meals = label_dict.get(var.get())
        physical_activity=active.get() #gets the value you have selected in dropdown option
        
        c.execute("INSERT INTO table5 (question_number, physical_activity, meals) VALUES (?, ?, ?)",
                      (5, physical_activity, meals))
        conn.commit()
        conn.close()

    #designing the layout for window 5   
    l = Label(q5t, text='Do you currently track your progress\n for overall physical activity?', font=('Poppins', 20))
    l.place(x=screen_width / 3, y=60)
    active = ttk.Combobox(q5t, values=['Yes', 'No'], font=('Poppins', 25)) #dropdown option
    active.place(x=screen_width / 3, y=150)
   

    l1 = Label(q5t, text='What type of meals do you usually consume?', font=('Poppins', 20))
    l1.place(x=screen_width / 3, y=250)
    r11 = Radiobutton(q5t, text='Balanced: mix of carbohydrates, proteins and fats', variable=var, value=1, bg='pink',
                      font=("Poppins", 18))
    r11.place(x=screen_width / 3, y=310)
    r22 = Radiobutton(q5t, text='Planned: mix of carbohydrates, proteins and fats along \nwith micrunutrients like vitamins and minerals', variable=var, value=2, bg='pink',
                      font=("Poppins", 18), justify="left")
    r22.place(x=screen_width / 3, y=360)
    r3 = Radiobutton(q5t, text='Hectic: mostly simple carbohydrates with little else', variable=var, value=3, bg='pink',
                     font=("Poppins", 18))
    r3.place(x=screen_width / 3, y=430)
    

    b = Button(q5t, text='Next question', font=('Poppins', 20),
               command=lambda: [next_question(q5t, t4), add_p5(var), store_data5()]) #adding points, going to the next question and storing data
    button_height = int(screen_height * 0.1)
    b.place(relx=0.5, rely=1.0, anchor='s', y=-button_height)
    q5t.attributes("-topmost", True)
    q5t.transient(t4)

    return q5t


    

#defining window 6; the last one
def q6(t4):
    global q6t, var1, var2, add_points_q6
    q6t = Toplevel(t4)
    q6t.attributes('-fullscreen', True)
    q6t.config(bg='pink')
    var1 = IntVar()
    var2 = IntVar()
    

    def add_p6(var1, var2):
        global points
        if var1.get()==1:
            points += 1
        elif var1.get()==2:
            points += 2
        elif var1.get()==3:
            points += 3
        elif var1.get()==4:
            points += 4
        if var2.get()==1:
            points += 1
        elif var2.get()==2:
            points += 2

    def store_data6():
        conn = connect('data.db', timeout = 10)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS table6 (
                     id6 INTEGER PRIMARY KEY AUTOINCREMENT,
                     question_number INTEGER NOT NULL,
                     sleep_hours TEXT NOT NULL,
                     bedtime TEXT NOT NULL,
                     other_inputs TEXT,
                     FOREIGN KEY(id6) REFERENCES table5(id5))''')
        
        label_dict = {
        1: 'Between 8 and 9 hours',
        2: '10 hours or more',
        3: 'Between 5 and 7 hours',
        4: 'Less than 5 hours'
        }
        sleep_hours = label_dict.get(var1.get())
        
        label_dict2 = {
        1: 'Yes',
        2: 'No',
        }
        bedtime = label_dict2.get(var2.get())
        other_inputs = entry.get()
        c.execute("INSERT INTO table6 (question_number, sleep_hours, bedtime, other_inputs) VALUES (?, ?, ?, ?)",
                      (6, sleep_hours, bedtime, other_inputs))
        conn.commit()
        conn.close()

    #designing the layout for window 6
    l = Label(q6t, text='How many hours of sleep do you get on average?', font=('Poppins', 23))  
    l.place(x=screen_width / 3, y=60)
    r1 = Radiobutton(q6t, text='Less 5 hours ', variable=var1, value=4, bg='pink',
                     font=("Poppins", 20))
    r1.place(x=screen_width / 3, y=100)
    r2 = Radiobutton(q6t, text='Between 5 and 7 hours', variable=var1, value=3,
                     bg='pink', font=("Poppins", 20))
    r2.place(x=screen_width / 3, y=150)
    r3 = Radiobutton(q6t, text='Between 8 and 9 hours', variable=var1, value=1,
                     bg='pink', font=("Poppins", 20))
    r3.place(x=screen_width / 3, y=200)
    r4 = Radiobutton(q6t, text='10 hours or more', variable=var1, value=2, bg='pink',
                     font=("Poppins", 20))
    r4.place(x=screen_width / 3, y=250)

    l2 = Label(q6t, text='Do you have a consistent bedtime?', font=('Poppins', 23))
    l2.place(x=screen_width / 3, y=310)
    y = Radiobutton(q6t, text='Yes', variable=var2, value=1, bg='pink',
                    font=("Poppins", 20))
    y.place(x=screen_width / 3, y=350)
    n = Radiobutton(q6t, text='No', variable=var2, value=2, bg='pink',
                    font=("Poppins", 20))
    n.place(x=screen_width / 3, y=400)

    label=Label(q6t, text='*Any other relevant inputs to share? \n(health limitations, lifestyle factors, personal habits etc.)', font=('Poppins', 23), justify="left")
    label.place(x=screen_width / 3, y=470)
    entry=Entry(q6t, font=("Poppins", 23), width=44)
    entry.place(x=screen_width/3, y=560)

    b = Button(q6t, text='Finish', font=('Poppins', 20),
               command=lambda: [calculate_bmi(t4), add_p6(var1, var2), store_data6(), firstrec(t4)]) #'Finish' button is adding points to the last question, runs the calculate_bmi(t4) function which also adds points to the global points variable, stores data for questin 6 and opens first reccomondation with function firstrec() (both defined below)
    button_height = int(screen_height * 0.1)
    b.place(relx=0.5, rely=1.0, anchor='s', y=-button_height)
    q6t.attributes("-topmost", True)
    q6t.transient(t4)

    return q6t


#defining the function that opens second toplevel window 
def new():
    global t4
    t2 = Toplevel(t)
    t2.title('Improve')
    t2.attributes('-fullscreen', True)
    t2.config(bg='beige')
    image_files = ["w1.png", "w2.png", "w3.png", "w4.png"] #accessing the images that I'll be using as 4 buttons later in this function
    labels = [
        "LOSE WEIGHT",
        "GET TONED",
        "GAIN WEIGHT",
        "IMPROVE WELLBEING"]  #labeling the images for easier managing later on

    def nw(label):
        global selected_label
        t4 = Toplevel(t2)
        t4.attributes('-fullscreen', True)
        t4.config(bg='pink')
        Label(t4, text=label).pack()
        q1t = q1(t4)
        q1t.lift()

        selected_label = label  #remembering assigned labels for images(buttons) as selected_label which will be used later on in display_recommonedation
        t4.mainloop()

    for i, image_file in enumerate(image_files):  #placing images so they are perfectly alligned when using for loop
        image = PhotoImage(file=image_file)
        b3 = Button(t2, image=image, command=lambda i=i: nw(labels[i])) #setting images as buttons which open the quiz as you click on them
        b3.image = image
        b3.grid(row=i // 2, column=i % 2, sticky="nsew")

    for i in range(2):
        t2.columnconfigure(i, weight=1) #placing them into 2 columns
        t2.rowconfigure(i, weight=1)  #placing them into 2 rows

    t2.update()


  
 
button = Button(t, text='Take the quiz', font=('Poppins', 13), height=3, width=40,
                command=lambda: [(messagebox.showinfo('message', 'Choose an option', default=messagebox.OK), new())]) #opening dialog window that opens when you click 'take the quiz' on Landing page (first toplevel window)
button_height = int(screen_height * 0.85)
button.place(x=screen_width/30, y=button_height)


#defining the function that gives first recommendation in a new toplevel window based on points you have scored in the quiz and selected_label
def firstrec(t4):   
    global selected_label
    f = Toplevel(t4)
    f.attributes('-fullscreen', True)
    f.config(bg='pink')
    pil_image = Image.open('Back1.png')  #using another picture (made with Canva) as a fullscreen background

    resized_image = pil_image.resize((screen_width, screen_height))  
    background_image = ImageTk.PhotoImage(resized_image)

    background_label = Label(f, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)


    message = display_recommendation() #displaying the message you got based on total score and selected_label (defined below)

    centered_message = message.split('\n\n\n')[0]  #message consists of the title and the recommendation
    left_message = message.split('\n\n\n')[1]

    centered_label = Label(f, text=centered_message,  bg='pink', font=('Helvetica', 18), justify=CENTER)
    centered_label.pack(pady=50)
    left_label = Label(f, text=left_message, font=('Helvetica', 15), justify=LEFT, wraplength=900)

    left_label.pack(pady=30, padx=50, anchor="w")

    #defining the function that opens when user click on the 'find out more' button; it opens a new fullscreen window that has 3 options(plans) you can choose from: Standard, Guided and Custom
    def prices(f):
        p = Toplevel(f)
        p.attributes('-fullscreen', True)
        p.config(bg='white')

        img1 = PhotoImage(file="Plann1.png")
        img2 = PhotoImage(file="Plann2.png")
        img3 = PhotoImage(file="Plann3.png")

        # displaying the images on the canvas
        label1 = Label(p, text="Standard")
        label2 = Label(p, text="Guided")
        label3 = Label(p, text="Custom")

        label1.config(image=img1)
        label2.config(image=img2)
        label3.config(image=img3)

        label1.grid(row=1, column=0, padx=10, pady=10)
        label2.grid(row=1, column=1, padx=10, pady=10)
        label3.grid(row=1, column=2, padx=10, pady=10)

        # creating 3 buttons for plans; when the user clicks on a button, a new toplevel window opens. It is defined with login function (name and email entered, defined below)
        button1 = Button(p, text='Sign up for Standard', font=('Poppins', 15),command=lambda: login(p, "Standard"))
        button2 = Button(p, text='Sign up for Guided', font=('Poppins', 15), command=lambda: login(p, "Guided"))
        button3 = Button(p, text='Sign up for Custom', font=('Poppins', 15), command=lambda: login(p, "Custom"))


        button1.grid(row=2, column=0, padx=10, pady=10)
        button2.grid(row=2, column=1, padx=10, pady=10)
        button3.grid(row=2, column=2, padx=10, pady=10)

        p.grid_rowconfigure(0, weight=1)
        p.grid_columnconfigure(0, weight=1)
        p.grid_columnconfigure(1, weight=1)
        p.grid_columnconfigure(2, weight=1)

        p.grid_rowconfigure(1, weight=1)

        p.grid_rowconfigure(2, weight=1)

        p.attributes("-topmost", True)
        p.transient(f)
        p.mainloop()

    b = Button(f, text='Find out more', command=lambda: prices(f), font=('Poppins', 19)) #button to kick off 'prices' function which offering 3 plans
    button_height = int(screen_height * 0.1)
    b.place(relx=0.5, rely=1.0, anchor='s', y=-button_height)
    f.attributes("-topmost", True)
    f.transient(t4)
    f.mainloop()

#defining the function that calculates bmi
def calculate_bmi(t4):
    global weight1, height1, selected_label, points

    weight1 = int(weight.get())
    height1 = int(height.get())

    global bmi

    bmi = weight1 / (height1 / 100) ** 2

    if 18.5 < bmi < 25:   #based on their weight and height selectin, the user's BMI is calculated. The user is assigned a number of points added to the other points scored in the quiz 
        points += 1 
    elif 24.99 < bmi < 27.5:
        points += 2
    elif 27.49 < bmi < 30:
        points += 3
    else:
        points += 4



#defining the function that displays the first recommendation based on points and the option the user chooses in the second toplevel window (selected_label)
def display_recommendation():
    global points
    global selected_label #label (button you clicked on) in the second toplevel window
    #for every selected label there are 4 options: minor improvements, improvements needed, major improvements and complete overhaul. This is based on user's total score(points) throught the quiz. Higher the score, bigger 'changes' needed
    #based on your points and selected label, message is formed and displayed in 'f' toplevel window defined by firstrec(t4) function
    if selected_label == "LOSE WEIGHT":
        if 13 >= points > 0:
            message = "Habits to implement to improve your weight loss process:\n\n\n"

            message += "• Be mindful of your sleep. Consistent bedtime and sleeping 8-9 hours each night can significantly help you with your overall efforts to lose weight.\n"
            message += "• Think about whether incorporating a new practice could benefit your body - it could be a new sport or a new type of exercise to work your muscles in a completely different way.\n"
            message += "• Make sure you hit the daily 10,000 step count consistently throughout the week.\n"
            message += "• Stay hydrated and focus on making healthy food choices\n"
            message += "• Look into increasing your daily activity by adding short workouts and check whether reducing your calorie intake is possible by replacing unhealthy snacks with healthier options.\n"

        elif 14 <= points <= 19:
            message = "Habits to implement to improve your weight loss process\n\n\n"

            message += "• Start with being honest with yourself and setting specific goals for weight loss.\n"
            message += "• Be mindful of your sleep. Consistent bedtime and sleeping 8-9 hours each night can significantly help you with your overall efforts to lose weight.\n"
            message += "• Increase the frequency and intensity of workouts you currently do. Consider incorporating a new practice as it could benefit your body significantly.\n Either introduce a new sport into your schedule or try a new type of exercise to work your muscles in a different way.\n"
            message += "• Make sure you are tracking your calorie intake and reduce it by making healthier food choices.\n"
            message += "• Make sure you hit the daily 10,000 step count consistently throughout the week."
        elif 20 <= points <= 25:
            message = "Habits to implement to improve your weight loss process\n\n\n"

            message += "• Consult with a healthcare professional or a registered dietitian if you feel like there is a potential there are any health concerns that should be addressed first.\n"
            message += "• Be strict when it comes to sleep. Consistent bedtime and sleeping 8-9 hours each night can significantly help you with your overall efforts to lose weight.\n"
            message += "• Watch your calorie intake more closely. You may not be aware of how much you're eating until you start tracking your food intake every meal. \n"
            message += "• Limit or try to eliminate at least half of the current rota of processed and sugary foods you eat.\n"
            message += "• It is crucial you find some time to introduce a new activity into your schedule. It can be a new sport or a new type of exercise. Either will get you to new activity levels which will help you burn calories more consistently. \n"
        else:
            message = "Habits to implement to improve your weight loss process:\n\n\n"

            message += "• Address any underlying health conditions that may be contributing to weight gain.\n"
            message += "• Be strict when it comes to sleep. Consistent bedtime and sleeping 8-9 hours each night can significantly help you with your overall efforts to lose weight.\n"
            message += "• Start watching your calorie intake. You may not be aware of how much you're eating until you start tracking your food intake every meal.\n"
            message += "• It is crucial you find some time to introduce a new activity into your schedule. It can be a new sport or a new type of exercise. Either will get you to new activity levels which will help you burn calories more consistently.\n"
            message += "• Make sure you hit the daily 10,000 - 15,000 step count consistently throughout the week. You can start by walking less and increase it to the 15,000 count once you feel ready.\n"
            message += "• Try incorporating strength training exercises into your workout routine, as building muscle can boost your metabolism and help with weight loss.\n"
            message += "• Stay hydrated by drinking enough water throughout the day, as dehydration can lead to false feelings of hunger and unnecessary snacking."

    elif selected_label == "GET TONED":
        if 13 >= points > 0:
            message = "Habits to implement that will help you feel more fit & toned:\n\n\n"

            message += "• Make sure you get enough sleep each night - consistently sleeping 8-9 hours can do wonders for your overall wellness.\n"
            message += "• Look more closely at your meals. Is there an opportunity to introduce more variety into your meals and snacks to ensure you're getting all the necessary nutrients? It could be something small yet significant. \n"
            message += "• Take regular breaks throughout the day to stretch your body and ease any tension you may be holding. Simple 10-minute stretches throughout the day or a quick yoga session can boost your feeling of wellbeing. \n"
            message += "• Drink enough water throughout the day to stay hydrated. Tracking your water intake can help understand whether you are drinking 2-3 litres of water each day. \n"
            message += "• Make sure you hit the daily 10,000 step count consistently throughout the week."

        elif 14 <= points <= 19:
            message = "Habits to implement that will help you feel more fit & toned: \n\n\n"

            message += "• Set specific goals for yourself and identify areas of your life where you can make healthier choices.\n"
            message += "• Make sure you get enough sleep each night - consistently sleeping 8-9 hours can do wonders for your overall wellness.\n"
            message += "• Incorporate more physical activity into your daily routine - this could be as simple as going for a walk or taking a yoga class.\n"
            message += "• Make sure you hit the daily 10,000 step count consistently throughout the week.\n"
            message += "• Pay attention to your mental health and take steps to manage stress, such as practising meditation or deep breathing exercises.\n"
            message += "• Introduce more variety into your meals and snacks to ensure you're getting all the necessary nutrients."

        elif 20 <= points <= 25:
            message = "Habits to implement that will help you feel more fit & toned: \n\n\n"

            message += "• Start with being honest with yourself and setting specific goals for improving your wellness. If you have any underlying health concerns, consult with a healthcare professional to address them.\n"
            message += "• Make sure you prioritise getting enough sleep each night - consistently sleeping 8-9 hours can do wonders for your overall wellness.\n"
            message += "• Incorporate more challenging physical activities into your routine to challenge yourself and boost your fitness levels. This could be anything you like, it’s not limited to a specific practice.\n"
            message += "• Make sure you hit the daily 10,000 step count consistently throughout the week.\n"
            message += "• Pay attention to your mental health and take steps to manage stress, such as introducing a mindfulness practice, meditating, and potentially seeking therapy or joining a support group.\n"
            message += "• Evaluate your current diet and make necessary changes to ensure you're getting all the necessary nutrients."
        else:
            message = "Habits to implement that will help you feel more fit & toned: \n\n\n"

            message += "• If you have any underlying health concerns, consult with a healthcare professional to address them. \n"
            message += "• Be strict when it comes to sleep. Consistent bedtime and sleeping 8-9 hours each night can significantly help you with your overall efforts to improve your wellness.\n"
            message += "• Incorporate regular physical activity into your routine, aiming for at least 30 minutes of moderate-to-vigorous exercise most days of the week. Pair this with making sure you hit the daily 10,000 step count consistently throughout the week. \n"
            message += "• Pay attention to your mental health and make it a priority. If you feel like you need it, seek support. \n"
            message += "• Make sure you're fueling your body with whole, nutrient-dense foods and avoiding heavily processed or sugary foods. \n"

    elif selected_label == "IMPROVE WELLNESS":
        if 13 >= points > 0:
            message = "Habits to implement that will raise your wellness levels: \n\n\n"

            message += "• Incorporate more strength training exercises into your routine to help build muscle and tone your body. You can use weights, resistance bands, or bodyweight exercises. \n"
            message += "• Look more closely at your meals. Is there an opportunity to introduce more protein-rich foods and nutrient-dense carbohydrates to support muscle growth and repair? It could be something small yet significant.\n"
            message += "• Take regular breaks throughout the day to stretch your body and ease any tension you may be holding. Simple 10-minute stretches throughout the day or a quick yoga session can boost your feeling of wellbeing and flexibility.\n"
            message += "• Drink enough water throughout the day to stay hydrated. Tracking your water intake and drinking 2-3 litres of water each day can help you reach your fitness goals. \n"
            message += "• Make sure you get enough sleep each night - sleeping 8-9 hours each night can do wonders for your overall fitness and muscle recovery. \n"
            message += "• Make sure you hit the daily 10,000 step count consistently throughout the week to improve your cardiovascular health and support your overall fitness levels. \n"
        elif 14 <= points <= 19:
            message = "Habits to implement that will raise your wellness levels: \n\n\n"

            message += "• Set specific goals for yourself and identify areas of your life where you can make healthier choices, such as incorporating more strength training exercises into your routine.\n"
            message += "• Incorporate more protein-rich foods and nutrient-dense carbohydrates into your diet to support muscle growth and repair, while limiting highly processed foods and added sugars.\n"
            message += "• Incorporate more challenging strength training exercises into your routine to challenge yourself and build muscle mass. Aim to increase weight or reps over time.\n"
            message += "• Make sure you hit the daily 10,000 step count consistently throughout the week to improve your cardiovascular health and support your overall fitness levels.\n"
            message += "• Pay attention to your mental health and take steps to manage stress, such as practising meditation or deep breathing exercises.\n"
            message += "• Make sure you get enough sleep each night - sleeping 8-9 hours each night can do wonders for your overall fitness and muscle recovery.\n"

        elif 20 <= points <= 25:
            message = "Habits to implement that will raise your wellness levels: \n\n\n"

            message += "• Start with being honest with yourself and setting specific goals for improving your fitness levels and building muscle. If you have any underlying health concerns, consult with a healthcare professional to address them.\n "
            message += "• Make strength training a priority in your workout routine, focusing on compound exercises that work multiple muscle groups at once. Aim to increase weight or reps over time to challenge yourself and continue to see progress.\n"
            message += "• Make sure you hit the daily 10,000 step count consistently throughout the week to improve your cardiovascular health and support your overall fitness levels.\n"
            message += "• Pay attention to your mental health and make it a priority. If you feel like you need it, seek support.\n"
            message += "• Evaluate your current diet and make necessary changes to ensure you're getting enough protein and nutrient-dense carbohydrates to support muscle growth and repair, while limiting highly processed foods and added sugars.\n"
            message += "• Be strict when it comes to sleep. Consistent bedtime and sleeping 8-9 hours each night can significantly help you with your overall efforts to improve your fitness levels and build muscle mass."
        else:
            message = "Habits to implement that will raise your wellness levels: \n\n\n"

            message += "• If you have any underlying health concerns, consult with a healthcare professional to address them and create a workout and nutriton plan that is safe and effective for you.\n"
            message += "• Make strength training a priority in your workout routine, focusing on compound exercises that work multiple muscle groups at once. Aim to increase weight or reps over time to challenge yourself and continue to see progress.\n"
            message += "• Incorporate both strength training and cardio into your routine, aiming for at least 30-60 minutes of exercise most days of the week. \n"
            message += "• Make sure you hit the daily 10,000 step count consistently throughout the week to improve your cardiovascular health and support your overall fitness levels.\n"
            message += "• Pay attention to your mental health and make it a priority. If you feel like you need it, seek assistance in addressing your mental health concerns.\n"
    else:
        if 13 >= points > 0:
            message = "Habits to implement to improve your weight & wellness: \n\n\n"

            message += "• Track your caloric intake to ensure you are eating enough to support weight gain. Eat more frequent meals throughout the day to ensure that you're consuming enough calories. \n"
            message += "• Focus on adding more healthy fats and nutrient-dense foods to your diet. Include sources of protein in every meal. Increase your caloric intake by adding healthy snacks throughout the day such as nuts, seeds, fruits, and vegetables, to help with weight gain.\n"
            message += "• Avoid consuming empty calories from processed foods, sugary drinks, and snacks as they provide little nutritional value and can lead to weight gain in an unhealthy way.\n"
            message += "• Get enough sleep each night - consistently sleeping 8-9 hours can help with muscle recovery and overall well being.\n"

        elif 14 <= points <= 19:
            message = "Habits to implement to improve your weight & wellness: \n\n\n"

            message += "• Focus on resistance training exercises to build muscle mass and strength, and pair this with cardiovascular exercise for overall fitness.\n"
            message += "• Make sure you're eating enough calories to support your weight gain goals, and consider tracking your food intake to ensure that you're meeting your daily calorie needs.\n"
            message += "• Focus on adding more healthy fats and nutrient-dense foods to your diet. Include sources of protein in every meal. \n"
            message += "• Avoid consuming empty calories from processed foods, sugary drinks, and snacks as they provide little nutritional value and can lead to weight gain in an unhealthy way.\n"
            message += "• Get enough sleep each night - consistently sleeping 8-9 hours can help with muscle recovery and overall well being.\n"
        elif 20 <= points <= 25:
            message = "Habits to implement to improve your weight & wellness: \n\n\n"

            message += "• Consult with a healthcare professional to ensure that there are no underlying health concerns that could be affecting your ability to gain weight.\n"
            message += "• When it comes to gaining weight and building muscle, strength training exercises are essential. Resistance training, whether with weights or bodyweight exercises, stimulates the muscles to grow in size and strength. It is recommended to do strength training exercises with a focus on compound exercises that work multiple muscle groups at once.\n"
            message += "• It is also important to progressively increase the weight or resistance used in your strength training exercises over time to continue challenging the muscles and stimulating growth. \n"
            message += "• Prioritise consuming nutrient-dense foods such as lean proteins, whole grains, and healthy fats. Include sources of protein in every meal - consider incorporating protein shakes or weight-gain shakes into your diet to increase calorie and protein intake.\n"
            message += "• Increase your caloric intake by adding healthy snacks throughout the day, such as nuts, seeds, fruits, and vegetables, to help with weight gain.\n It is crucial you track your caloric intake and ensure you are consuming more calories than you are burning each day to promote weight gain.\n"
            message += "• Avoid consuming empty calories from processed foods, sugary drinks, and snacks as they provide little nutritional value lead to weight gain in an unhealthy way.\n"
            message += "• Get enough sleep each night - consistently sleeping 8-9 hours can help with muscle recovery and overall well being."
        else:
            message = "Habits to implement to improve your weight & wellness: \n\n\n"

            message += "• Consult with a healthcare professional to ensure that there are no underlying health concerns that could be affecting your ability to gain weight.\n"
            message += "• Incorporate a combination of strength training and cardiovascular exercise into your workout routine to improve overall fitness and increase muscle mass.\n"
            message += "• When it comes to gaining weight and building muscle, strength training exercises are essential. Resistance training, whether with weights or bodyweight exercises, stimulates the muscles to grow in size and strength. It is recommended to do strength training exercises with a focus on compound exercises that work multiple muscle groups at once.\n"
            message += "• It is also important to progressively increase the weight or resistance used in your strength training exercises\n over time to continue challenging the muscles and stimulating growth.\n"
            message += "• Prioritise consuming nutrient-dense foods such as lean proteins, whole grains, and healthy fats. Include sources of protein in every meal - consider incorporating protein shakes or weight-gain shakes into your diet to increase calorie and protein intake.\n"
            message += "• Increase your caloric intake by adding healthy snacks throughout the day, such as nuts, seeds, fruits, and vegetables, to help with weight gain. It is crucial you track your caloric intake and ensure you are consuming more calories than you are burning each day to promote weight gain.\n"
            message += "• Avoid consuming empty calories from processed foods, sugary drinks, and snacks as they provide little nutritional value and can lead to weight gain in an unhealthy way.\n"
    return message


#defining the function that sends email user's email address based on the plan (button) the user select in 'p' toplevel window which is defined by prices() function
def login(p, plan):
    def send_email(name, email, plan):

        server = smtplib.SMTP('smtp.gmail.com', 587)   #server and safety port I'll be using to send you an email

        server.starttls()

        server.login('achieve.goals234@gmail.com', 'vehczbtetqjekmup')
        
        message = MIMEMultipart()

        #outlining the contets of the email sent to the user usim html based on the plan user selected
        #this is the standard plan
        if plan == "Standard":  
            subject = 'Improve Your Life - Standard Plan'
            body = f"""\
                <html>
                    <body>
                    <p>Hi {name},</p>
                    <p>Mia from Improve Your Life here. Thank you for filling out the questionnaire on my website, I appreciate the time it took you to do this.<br>
    <               Your answers will help me improve my program and currently outlined recommendations, and allow me to develop more advanced iterations of Improve Your Life.</p>
                    <p>As you already feel like you've got a great grip on your fitness, here are some things to keep in mind on your further fitness journey!<br>
                       Remember, there is always room for improvement, even if it means making sure you're checking all the things off the list!</p>
                    <img src="cid:image1">
                    
                        <ol>
                          <li>Aim to walk at least 10,000 steps a day to stay active and improve cardiovascular health.</li>
                          <li>Drink at least 2.5 liters of water each day to stay hydrated and support overall health.</li>
                          <li>Consider taking supplements if you feel tired or fatigued. It's best to consult a healthcare professional and get a blood test to determine what supplements your body needs.</li>
                          <li>Establish a consistent bedtime routine to improve sleep quality and overall health.</li>
                          <li>Aim to sleep at least 7 hours each night to support recovery and overall health.</li>
                          <li>Listen to your body and adjust your workout routine or diet accordingly to prevent injuries, overtraining, or nutrient deficiencies.</li>
                          <li>Stay motivated and accountable by tracking progress and celebrating achievements.</li>
                          <li>Avoid comparing yourself to others and focus on your own progress and goals.</li>
                          <li>Incorporate stress-reducing practices such as meditation, yoga, or deep breathing to support overall health.</li>
                          <li>Incorporate flexibility exercises to improve mobility and prevent injuries.</li>
                        </ol>

                        <p>Good luck and I will keep in touch with news on Improve Your Life once we fully take it live!</p>

                        <p>Best regards,<br>
                        Mia</p>
                    </body>
                </html>
                """
            #putting the image of a plan you have chosen in the email
            with open('Plann1.png', 'rb') as f:
                img_data = f.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '<image1>')
            message.attach(img)

            message['Subject'] = subject
            message.attach(MIMEText(body, 'html'))

        #this is the guided plan
        elif plan == "Guided":
            subject = 'Improve Your Life - Guided Plan'
            body = f"""\
                <html>
                    <body>
                        <p>Hi {name},</p>
                        <p>Mia from Improve Your Life here. Thank you for filling out the questionnaire on my website, I appreciate the time it took you to do this.<br>
                        Your answers will help me improve my program and currently outlined recommendations, and allow me to develop more advanced iterations of Improve Your Life.</p>
                        <img src="cid:image1">
                        <ol>
                            <li>Aim to walk at least 10,000 steps a day to stay active and improve cardiovascular health.</li>
                            <li>Drink at least 2.5 liters of water each day to stay hydrated and support overall health.</li>
                            <li>Consider taking supplements if you feel tired or fatigued. It's best to consult a healthcare professional and get a blood test to determine what supplements your body needs.</li>
                            <li>Establish a consistent bedtime routine to improve sleep quality and overall health.</li>
                            <li>Aim to sleep at least 7 hours each night to support recovery and overall health.</li>
                            <li>Listen to your body and adjust your workout routine or diet accordingly to prevent injuries, overtraining, or nutrient deficiencies.</li>
                            <li>Stay motivated and accountable by tracking progress and celebrating achievements.</li>
                            <li>Avoid comparing yourself to others and focus on your own progress and goals.</li>
                            <li>Incorporate stress-reducing practices such as meditation, yoga, or deep breathing to support overall health.</li>
                            <li>Incorporate flexibility exercises to improve mobility and prevent injuries.</li>
                        </ol>
                        <p>Good luck and I will keep in touch with news on Improve Your Life once we fully take it live!</p>
                        <p>Best regards,<br>
                        Mia</p>
                    </body>
                </html>
            """
            with open('Plann2.png', 'rb') as f:
                img_data = f.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '<image1>')
            message.attach(img)

            message['Subject'] = subject
            message.attach(MIMEText(body, 'html'))

        #this is the custom plan
        elif plan == 'Custom':
            subject = 'Improve Your Life - Custom Plan'
            body = f"""\
                <html>
                    <body>
                    <p>Hi {name},</p>
                    <p>Mia from Improve Your Life here. Thank you for filling out the questionnaire on my website. Your answers have provided valuable insights into your fitness goals and abilities, and I am excited to work with you to develop a fully custom plan tailored to your needs.</p>
                    <p>Based on the data analysis, we can focus on specific areas including sleep, nutrition, walking, exercise, and mindfulness. Together, we can work towards achieving your fitness goals and improving your overall health.</p>
                    <p>Here are a few things to start with as we begin this journey:</p>
                    <img src="cid:image1">
                    <ol>
                        <li>Aim to prioritize sleep by establishing a consistent bedtime routine and aiming to get at least 7 hours of sleep each night.</li>
                        <li>Incorporate walking into your daily routine to stay active and improve cardiovascular health.</li>
                        <li>Incorporate mindfulness practices such as meditation, deep breathing, or yoga to reduce stress and improve overall well-being.</li>
                    </ol>
                    <p>I am excited to work with you to develop a fully custom plan that will help you achieve your fitness goals and improve your overall health.</p>
                    <p>Please feel free to share any additional information with me, and I will use the questionnaire you already filled out to develop a personalized plan just for you.</p>
                    <p>Thank you for choosing Improve Your Life as your partner on this journey. I look forward to working with you!</p>
                    <p>Best regards,<br>Mia</p>
                    </body>
                </html>
            """
            with open('Plann3.png', 'rb') as f:
                img_data = f.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '<image1>')
            message.attach(img)

            message['Subject'] = subject
            message.attach(MIMEText(body, 'html'))


        #sending the email from email address I have created for this program
        server.sendmail('achieve.goals234@gmail.com', email, message.as_string())
        server.quit()


    #designing the toplevel window where the user enters their name and email (a pop-up window)
    tm = Toplevel(p)
    tm.config(bg='white')
    tm.geometry('450x150')

    l1 = Label(tm, text='Name and Surname', bg='white', font=('Poppins', 12))
    l1.grid(row=0, column=0, pady=10, padx=20)

    #collecting the data the user has provided which is stored into the database. The program uses the name for the opening of the email: 'Hi [insert name],...'. It also serves as the link to recognise the receiving email address
    name_entry = Entry(tm, font=('Poppins', 12), width=50)
    name_entry.grid(row=0, column=1, padx=20, pady=10)
    l2 = Label(tm, text='Enter Email', bg='white', font=('Poppins', 12))
    l2.grid(row=1, column=0, pady=10, padx=20)

    email_entry = Entry(tm, font=('Poppins', 12), width=50)
    email_entry.grid(row=1, column=1, padx=20, pady=10)

    #creating function that stores the user's name and email information into the database 
    def store_data_mail():
        conn = connect('data.db', timeout = 10)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS table7 (
                     id7 INTEGER PRIMARY KEY AUTOINCREMENT,
                     question_number INTEGER NOT NULL,
                     name_surname TEXT NOT NULL,
                     email TEXT NOT NULL,
                     FOREIGN KEY(id7) REFERENCES table6(id6))''')
        
        name_surname = name_entry.get()
        email = email_entry.get()
        c.execute("INSERT INTO table7 (question_number, name_surname, email) VALUES (?, ?, ?)",
                      (7, name_surname, email))
        conn.commit()
        conn.close()

    #creating the final toplevel window
    def final(p):
        def closet(): #function that closes all toplevel windows when run
            t.destroy()

        h = Toplevel(p)
        h.attributes('-fullscreen', True)
        h.attributes('-topmost', True)
        pil_image = Image.open('Last.png')
        resized_image = pil_image.resize((screen_width, screen_height))
        background_image = ImageTk.PhotoImage(resized_image)

        background_label = Label(h, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1,anchor=NW)
        quit_button = Button(h, text='EXIT', command=closet, bg='red', font=('Poppins', 16)) #closing all toplevel windows 
        quit_button.pack(side=TOP, anchor='ne')

        h.lift()
        h.transient(p)
        h.mainloop()

    #button in email entry pop-up that sends email to email address provided, stores data and opens the final window
    bb = Button(tm, text='Sign up', font=('Poppins', 11), bg='#4CAF50', fg='white',
                command=lambda: [(send_email(name_entry.get(), email_entry.get(), plan), store_data_mail(), final(tm))])
    bb.grid(row=2, columnspan=2, pady=20, padx=20)
    bb.grid(row=2, columnspan=2, pady=20, padx=20)
    tm.transient(p)
    tm.mainloop()


t.title('Improve your life!')
t.mainloop()  #putting mainloop at the end of the code so everything runs smoothly
