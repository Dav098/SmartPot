import serial
import sqlite3
import socket
import threading
 
        #baza danych
 
con = sqlite3.connect('measure.db', check_same_thread = False)
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
                   (air_temp, air_hum, soil_moisture_d, soil_moisture_a, led))
    con.commit()
 
def drop_table():
    cursor.execute('''DROP TABLE measurement''')
 
 
        #send and receive data
 
air_temp=""
air_hum=""
soil_moisture_d=""
soil_moisture_a=""
led=""
end=False
host = '192.168.1.3' #Server ip
port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
 
 
 
 
def snd_dwn(air_temp, air_hum, soil_moisture_d, soil_moisture_a, led):
 
    data, addr = s.recvfrom(1024)
    data = data.decode('utf-8')
    print("Message from: " + str(addr))
    print("From connected user: " + data)      
    if(data == "2"):
        drop_table()
        create_table()
 
    print("Sending...")
    file = open("measure.db", 'rb')
    filedata = file.read(99999)
    s.sendto(bytes(filedata), addr)
 
 
 
class download(threading.Thread):
    def __init__(self, air_temp, air_hum, soil_moisture_d, soil_moisture_a, led):
        threading.Thread.__init__(self)
        self.air_temp = air_temp
        self.air_hum = air_hum
        self.soil_moisture_d = soil_moisture_d
        self.soil_moisture_a = soil_moisture_a
        self.led = led
    def run(self):
        snd_dwn(self.air_temp, self.air_hum, self.soil_moisture_d, self.soil_moisture_a, self.led)
        print("Sent")
 
 
 
        #main code
 
print("Server Started")
create_table()
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=0.01)
 
while True:
    data_arduino = str(arduino.readline())
 
    if data_arduino!="b''":                     #we receive: b'(data)'
        data_arduino = (data_arduino[2:-1])     
        print(data_arduino) 
        if data_arduino[0] == 't':
            air_temp = data_arduino[1:]
        if data_arduino[0] == 'h':
            air_hum = data_arduino[1:]
        if data_arduino[0] == 'd':
            soil_moisture_d = data_arduino[1:]
        if data_arduino[0] == 'a':
            soil_moisture_a = data_arduino[1:]
        if data_arduino[0] == 'L':
            led = data_arduino[1:]
            end = True
 
 
        if end == True:
            insert(air_temp, air_hum, soil_moisture_d, soil_moisture_a, led)
            end = False
 
            #sending and receiving data from the client
            download(air_temp, air_hum, soil_moisture_d, soil_moisture_a, led).start()
 
            for row in cursor.execute('SELECT * FROM measurement'):
                print(row)
 
c.close()