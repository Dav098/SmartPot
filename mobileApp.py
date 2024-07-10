from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.textfield import MDTextField
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import threading
import socket
import os
import shutil
import sqlite3

screen = Screen(name = 'main')
screen2 = Screen(name = 's2')
screen3 = Screen(name = 's3')
screen4 = Screen(name = 's4')
sm = ScreenManager()
error = Label(size_hint =(.5, .15),
                    pos_hint ={'top':.75, 'right':1},
                    color=(0,0,0,1),
                    text ='',
                    )    
        
def download_db(message):
    if(message !='q'):
        try:
            host='192.168.1.8' #client ip
            port = 4005
            
            server = ('192.168.1.3', 4000)
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            s.bind((host,port))
            
            s.sendto(message.encode('utf-8'), server)
            file = open("measure.db", 'wb')
            data, addr = s.recvfrom(99999)
        
            file.write(bytes(data))
            file.close()
            
            

        except:
            error.text = "No connection"
            


class data():
    air_temp = []
    air_hum = []
    soil_moisture = []
    led = []
    n=0
    def load_data():
        path = 'measure.db'
        isFile = os.path.isfile(path)
        
        if(isFile==False):
            return('', '', '', '','')
        
        if(isFile==True):
            
            con = sqlite3.connect('measure.db')
            cursor = con.cursor()
            cursor.execute("select count(*) from measurement")
            results = cursor.fetchone()
            data.n=(results[0])
            
            for row in cursor.execute('SELECT air_temp FROM measurement'):
                data.air_temp.append(row)
            
            for row in cursor.execute('SELECT air_hum FROM measurement'):
                data.air_hum.append(row)
                
            for row in cursor.execute('SELECT soil_moisture_d FROM measurement'):
                data.soil_moisture.append(row)
                
            for row in cursor.execute('SELECT led FROM measurement'):
                data.led.append(row)
                
            con.close()
            return (data.n, data.air_temp, data.air_hum, data.soil_moisture, data.led)
        
def save_config(plant_name, min_air_temp, max_air_temp, min_air_hum, max_air_hum, min_soil_moisture, max_soil_moisture):
    f = open("plants.txt", "w")
    f.write("nazwa_r{}\n".format(plant_name))
    f.write("min_air_temp{}\n".format(min_air_temp))
    f.write("max_air_temp{}\n".format(max_air_temp))
    f.write("min_air_hum{}\n".format(min_air_hum))
    f.write("max_air_hum{}\n".format(max_air_hum))
    f.write("min_soil_moisture{}\n".format(min_soil_moisture))
    f.write("min_soil_moisture{}\n".format(min_soil_moisture))
    f.close()


def read_config():
    f = open("plants.txt", "r")

    while True:
        lines = f.readline()
        if not lines:
            break

        for i in range(7):
            
            if(lines.strip()[:5]=="plant_name"):
                string = lines.strip()
                MainApp.plant_name = (str(string[5:]))
                
            if(lines.strip()[:7]=="min_air_temp"):
                string = lines.strip()
                MainApp.min_air_temp = (int(string[7:]))
                    
            if(lines.strip()[:7]=="max_air_temp"):
                string = lines.strip()
                MainApp.max_air_temp = (int(string[7:]))
                
            if(lines.strip()[:7]=="min_air_hum"):
                string = lines.strip()
                MainApp.min_air_hum = (int(string[7:]))
                    
            if(lines.strip()[:7]=="max_air_hum"):
                string = lines.strip()
                MainApp.max_air_hum = (int(string[7:]))
                    
            if(lines.strip()[:7]=="min_soil_moisture"):
                string = lines.strip()
                MainApp.min_soil_moisture = (int(string[7:]))
                    
            if(lines.strip()[:7]=="max_soil_moisture"):
                string = lines.strip()
                MainApp.max_soil_moisture = (int(string[7:]))
    f.close()

def save_record(filename):
    src = "measure.db"
    isFile = os.path.isfile(src)
    
    if(isFile==True):
        dst =  filename+".db"
        shutil.copyfile(src, dst)

class archives():
    air_temp = []
    air_hum = []
    soil_moisture = []
    led = []
    n=0
    def select(nazwa):
        con = sqlite3.connect(nazwa)
        cursor = con.cursor()
        cursor.execute("select count(*) from measurement")
        results = cursor.fetchone()
        archives.n=(results[0])
        
        for row in cursor.execute('SELECT air_temp FROM measurement'):
            archives.air_temp.append(row)
        
        for row in cursor.execute('SELECT air_hum FROM measurement'):
            archives.air_hum.append(row)
            
        for row in cursor.execute('SELECT soil_moisture_d FROM measurement'):
            archives.soil_moisture.append(row)
            
        for row in cursor.execute('SELECT led FROM measurement'):
            archives.led.append(row)
            
        con.close()
        return (archives.n, archives.air_temp, archives.air_hum, archives.soil_moisture, archives.led)


con = sqlite3.connect('measure.db')
cursor = con.cursor()

def create_table():
    cursor.execute('''CREATE TABLE IF NOT EXISTS measurement(
                    air_temp TEXT,
                    air_hum TEXT,
                    soil_moisture_d TEXT,
                    soil_moisture_a TEXT,
                    led TEXT )''')
    con.commit()
    
def insert(air_temp, air_hum, soil_moisture_d, soil_moisture_a, led):
    cursor.execute("INSERT INTO measurement VALUES (?, ?, ?, ?, ?)",
                   (air_temp, air_hum, soil_moisture_d,soil_moisture_a, led))
    con.commit()
    
def drop_table():
    cursor.execute('''DROP TABLE measurement''')

class MainApp(MDApp):
    
    plant_name=""
    min_air_temp = 0
    max_air_temp = 0
    min_air_hum = 0
    max_air_hum = 0
    min_soil_moisture = 0
    max_soil_moisture = 0
    
    def build(self):
        
        (n, air_temp, air_hum, soil_moisture, led )=(0,'','','','')
        
        
        # Function to update the table
        
        def update_table():
            
            download_db('1') 
            (n, air_temp, air_hum, soil_moisture, led )=(data.load_data())
            if(air_temp!=''):
                table.row_data=[
                    (air_temp[n-i-1][0]+'°C', air_hum[n-i-1][0]+'%',  soil_moisture[n-i-1][0], led[n-i-1][0]) for i in range(n+1)
                    ]
            
            screen.remove_widget(table)
            screen.add_widget(table)
            
            
        def refresh_app(instance):
            isFile = os.path.isfile("measure.db")
            
            if(isFile==True):
                read_config()
                update_table()
                note.text = ""
                if((float(data.air_temp[-1][0])) < MainApp.min_air_temp):
                    note.text += "The plant is too cold.\n"
                    
                if((float(data.air_temp[-1][0])) > MainApp.max_air_temp):
                    note.text += "The plant is too hot.\n"
                    
                if((float(data.air_hum[-1][0])) < MainApp.min_air_hum):
                    note.text += "The air is too dry for the plant.\n"
                    
                if((float(data.air_hum[-1][0])) > MainApp.max_air_hum):
                    note.text += "The air is too humid for the plant.\n"
                    
                if((float(data.soil_moisture[-1][0])) < MainApp.min_soil_moisture):
                    note.text += "The plant has too little water.\n"
                  
                if((float(data.soil_moisture[-1][0])) > MainApp.max_soil_moisture):
                    note.text += "The plant has too much water.\n"
                
                if(data.n>13):
                    if(str(data.led[:12]) == "["+"('Led On',), "*11+"('Led On',)"+"]"):
                        note.text += "The plant has too little natural light."
            
        
       
        def add_plant(instance):
            dropdown.dismiss()
            sm.switch_to(screen2) 
            
        def save_history(instance):
            dropdown.dismiss()
            sm.switch_to(screen3) 
            
        def open_archives(instance):
            dropdown.dismiss()
            sm.switch_to(screen4) 
            
        def reset(instance):
            create_table()
            drop_table()
            create_table()
            insert("0.00", "0", "0","0","0")
            dropdown.dismiss()
        ##########################################################
    
            
        # dropdown buttons
        
        dropdown = DropDown()
        
        add = Button(text='Add plant manually', size_hint_y=None, height=80)
        add.bind(on_press=add_plant)
        dropdown.add_widget(add)
        
        add = Button(text='Save plant history', size_hint_y=None, height=80)
        add.bind(on_press=save_history)
        dropdown.add_widget(add)
        
        add = Button(text='Plant archives', size_hint_y=None, height=80)
        add.bind(on_press=open_archives)
        dropdown.add_widget(add)
        
        add = Button(text='Reset application', size_hint_y=None, height=80)
        add.bind(on_press=reset)
        dropdown.add_widget(add)
        
        

        menu = Button(size_hint =(.4, .1),
                    pos_hint ={'top':.8, 'right':0.8},
                    background_color =(0, 1, 1, 1), 
                    text ="Menu")
        
        menu.bind(on_press=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(menu, 'text', x))
       
        ##########################################################
        
        #reset button
        
        refresh = Button(size_hint =(.2, .1),
                    pos_hint ={'top':.8, 'right':1},
                    background_color =(0, 1, 1, 1), 
                    text ="Refresh")
        
        refresh.bind(on_press=refresh_app)
        
        ##########################################################
        
        #note
        anchor = AnchorLayout(anchor_x='left', anchor_y='top')       
        
        note = Label(size_hint =(None, None),
                    pos_hint ={'top':.5, 'left':.5},
                    size = (700,400),
                    color=(0,0,0,1),
                    text ='notatka',

                    )
        anchor.add_widget(note)
        
        ##########################################################
        
        
		#table
        table = MDDataTable(
			pos_hint = {'center_x': 0.5, 'center_y': 0.3},
			size_hint =(0.9, 0.65),
            use_pagination=True,
			column_data = [
				("Air\ntemperature", dp(30)),
				("Air\nhumidity", dp(30)),
				("Soil\nmoisture", dp(30)),
                ("Light", dp(30))
			],
			row_data = [
				
                # (air_temp[i], air_hum[i], soil_moisture_d[i], soil_moisture_a[i], led[i]) for i in range(n)
			]
			)
		
        

        
        
        screen.add_widget(refresh)
        screen.add_widget(error)
        screen.add_widget(anchor) 
        screen.add_widget(menu)
        ##########################################################
        
        ####        add plant screen
        
        def submit(instance):
            if((min_air_temp.text).isnumeric() and (max_air_temp.text).isnumeric()
               and (min_air_hum.text).isnumeric() and (max_air_hum.text).isnumeric() 
               and (min_soil_moisture.text).isnumeric() and (max_soil_moisture.text).isnumeric()):
                save_config(plant_name.text, min_air_temp.text,
                            max_air_temp.text, min_air_hum.text, 
                            max_air_hum.text, min_soil_moisture.text, max_soil_moisture.text)
                download_db("2")
                sm.switch_to(screen)
        
        def cancel(instance):
            sm.switch_to(screen)
        
        warning = Label(size_hint =(None, None),
                    pos_hint ={'center_x':.5, 'y':.85},
                    size = (300,100),
                    color=(0,0,0,1),
                    text ='Adding a plant will result in the removal of the current database',

                    )
        screen2.add_widget(warning)
            
        plant_name = MDTextField(hint_text="plant name", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .8})
        screen2.add_widget(plant_name)
        
        min_air_temp = MDTextField(hint_text="minimum air temperature", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .7})
        screen2.add_widget(min_air_temp)
        
        max_air_temp = MDTextField(hint_text="maximum air temperature", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .6})
        screen2.add_widget(max_air_temp)
        
        min_air_hum = MDTextField(hint_text="minimum air humidity", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .5})
        screen2.add_widget(min_air_hum)
        
        max_air_hum = MDTextField(hint_text="maximum air humidity", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .4})
        screen2.add_widget(max_air_hum)
        
        min_soil_moisture = MDTextField(hint_text="minimum soil moisture", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .3})
        screen2.add_widget(min_soil_moisture)
        
        max_soil_moisture = MDTextField(hint_text="maximum soil moisture", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .2})
        screen2.add_widget(max_soil_moisture)
        
        btn = Button(text='save', size_hint=(.3, .1), pos_hint={'left': 1, 'y': .05})
        btn.bind(on_press=submit)
        screen2.add_widget(btn)
        btn = Button(text='cancel', size_hint=(.3, .1), pos_hint={'right': 1, 'y': .05})
        btn.bind(on_press=cancel)
        screen2.add_widget(btn)
        
        ##########################################################
        
        
        ## saving archive screen
        def save_plant_history(instance):
            save_record(str(name.text))
            sm.switch_to(screen)
            
        name = MDTextField(hint_text="Name of archives", size_hint=(.45, .1), pos_hint={'center_x': .5, 'y': .3})
        screen3.add_widget(name)
        
        btn = Button(text='save', size_hint=(.3, .1), pos_hint={'left': 1, 'y': .05})
        btn.bind(on_press=save_plant_history)
        screen3.add_widget(btn)
        btn = Button(text='cancel', size_hint=(.3, .1), pos_hint={'right': 1, 'y': .05})
        btn.bind(on_press=cancel)
        screen3.add_widget(btn)
        
        
        ##########################################################
        #archives screen
        
        
        def cancel(instance):
            screen4.remove_widget(table2)
            sm.switch_to(screen)
            

        
        def setname(instance):
            nazwa = instance.text
            (n, air_temp, air_hum, soil_moisture, led )=(archives.select(nazwa))
            if(air_temp!=''):
                table2.row_data=[
                    (air_temp[n-i-1][0]+'°C', air_hum[n-i-1][0]+'%',  soil_moisture[n-i-1][0], led[n-i-1][0]) for i in range(n+1)
                    ]
                
                screen4.add_widget(table2)
                
                
        layout = GridLayout(cols=1, spacing=3, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        path = os.getcwd()
        dir_list = os.listdir(path)
        for file in dir_list:
            if((file[-3:]) == '.db'):
                layout.add_widget(
                    OneLineListItem(text=f"{file}",on_press = setname)
                    )
        root = ScrollView(size_hint=(None, None), size=(400, 200),
            pos_hint={'top':1, 'right':1})
        
        
        
        table2 = MDDataTable(
			pos_hint = {'center_x': 0.5, 'center_y': 0.3},
			size_hint =(0.9, 0.65),
            use_pagination=True,
			column_data = [
				("Air\ntemperature", dp(30)),
				("Air\nhumidity", dp(30)),
				("Soil\nmoisture", dp(30)),
                ("Light", dp(30))
			],
			row_data = [
				
                # (air_temp[i], air_hum[i], soil_moisture_d[i], soil_moisture_a[i], led[i]) for i in range(n)
			]
			)
        
            
        back = Button(size_hint =(.15, .1),
                    pos_hint ={'top':.8, 'left':0.8},
                    background_color =(0, 1, 1, 1), 
                    text ="Back")
        
        back.bind(on_press=cancel)
        
        
        root.add_widget(layout)
        screen4.add_widget(root)
        screen4.add_widget(back)
        
        ##################################################
        
        
        sm.add_widget(screen4)
        sm.add_widget(screen3)
        sm.add_widget(screen2)
        sm.add_widget(screen)
        sm.current = 'main'
        return sm
    
    
	
	

if __name__ == '__main__':
    MainApp().run()

