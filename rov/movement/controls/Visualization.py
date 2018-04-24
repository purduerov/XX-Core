import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import pandas as pd
import subprocess
import webbrowser
import sys

from Algorithm_Handler import Master_Algorithm_Handler


def create_window():
    window = tk.Tk()

def generate_data():
    from random import *
    
    buffer = 0.005
    # last time
    lt = time.time()
    
    data = {'sensors':
            {
                'imu' :
                {
                    'linear-acceleration' :
                    {
                        'x' : 1,
                        'y' : 1
                        },
                    'euler' :
                    {
                        'roll': 1,
                        'pitch': 1,
                        'yaw': 1
                    }
                },
                'pressure' :
                {
                    'pressure': 1
                }
            }
        }
    
    def rand():
        return (random() / 5.0) + 0.9
    
    def rand2():
        return random() * 0.001 - 0.0005
    
    def update_data(user_input, data, lt):
        dt = time.time() - lt
        lt = time.time()
        data['sensors']['imu']['linear-acceleration']['x'] += user_input[0] * dt * rand() + rand2()
        data['sensors']['imu']['linear-acceleration']['y'] += user_input[1] * dt * rand() + rand2()
        data['sensors']['pressure']['pressure'] += user_input[2] * dt * rand() + rand2()
        data['sensors']['imu']['euler']['roll'] += user_input[3] * dt * rand() + rand2()
        data['sensors']['imu']['euler']['pitch'] += user_input[4] * dt * rand() + rand2()
        data['sensors']['imu']['euler']['yaw'] += user_input[5] * dt * rand() + rand2()
        if data['sensors']['imu']['euler']['roll'] > 360:
            data['sensors']['imu']['euler']['roll'] -= 360
        elif data['sensors']['imu']['euler']['roll'] < 0:
            data['sensors']['imu']['euler']['roll'] += 360
    
    def position(data):
        position = [0,0,0,0,0,0]
        
        position[0] = data['sensors']['imu']['linear-acceleration']['x']
        position[1] = data['sensors']['imu']['linear-acceleration']['y']
        position[2] = data['sensors']['pressure']['pressure']
        position[3] = data['sensors']['imu']['euler']['roll']
        position[4] = data['sensors']['imu']['euler']['pitch']
        position[5] = data['sensors']['imu']['euler']['yaw']
    
        return position
    
    def sensor_data():
        return data['sensors']
    
    # initializes a control algorithm with the desired position of 4 for the z parameter
    assert 0 == 0
    
    # initializes a control algorithm with the desired position of 4 for the z parameter
    frozen = [1,2,1,2,1,2]
    user_input = [0,0,0,0,0,0]
    mah = Master_Algorithm_Handler(frozen, sensor_data())
    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    time.sleep(buffer)
    
    user_input = [0.5, 0.1, 0.2, 0.3, 0.4, 0.5]
    mah = Master_Algorithm_Handler(frozen, sensor_data())
    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    for i in range(6):
        time.sleep(buffer)
    
    frozen = [2,1,2,1,2,1]
    user_input = [0.5, 0.1, 0.2, 0.3, 0.21, 0.14]
    
    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    for i in range(6):
        time.sleep(buffer)
        mah.master(user_input, frozen)[i]
    
    frozen = [1,2,1,2,1,2]
    user_input = [0.5, 0.1, 0.2, 0.3, 0.21, 0.14]
    
    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    for i in range(6):
        time.sleep(buffer)
        mah.master(user_input, frozen)[i]
    
    frozen = [3,3,3,3,3,3]
    user_input = [0.5, 0.1, 0.2, 0.3, 0.21, 0.14]
    
    for i in range(100):
        time.sleep(buffer)
        update_data(mah.master(user_input, frozen), data, lt)
    for i in range(6):
        time.sleep(buffer)
        mah.master(user_input, frozen)[i]   
    

root = tk.Tk()
tk.Label(root, text='File Path').grid(row=0, column=0)
v = tk.StringVar()
entry = tk.Entry(root, textvariable=v).grid(row=0, column=1)



tk.Button(root, text='Browse Data Set',command=mah.plot_data).grid(row=1, column=0)
tk.Button(root, text='Close',command=root.destroy).grid(row=1, column=1)

tk.Button(root, text='Graph 1', command=graph_1).grid(row=3, column=0) # Call the graph_1 function
tk.Button(root, text='Graph 2', command=doNothing).grid(row=3, column=1)
tk.Button(root, text='Graph 3', command=doNothing).grid(row=3, column=2)
tk.Button(root, text='Graph 4', command=doNothing).grid(row=3, column=3)


menu =  Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="New", command=create_window)
subMenu.add_command(label="Open", command=doNothing)
subMenu.add_command(label="Restart", command=doNothing)
subMenu.add_command(label="Exit", command=doNothing)
editMenu = Menu(menu)
menu.add_cascade(label = "Help", menu=editMenu)
editMenu.add_command(label="Help", command=doNothing)

root.mainloop()
