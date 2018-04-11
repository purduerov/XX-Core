import os
import sys
import numpy as np
import argparse
import json
from pprint import pprint

def get_Directory():

    print ("Select the log you would like to access\n")
    for i in range(len(dir_list)):
        directory = str(i) + ": " + dir_list[i]                   #printing all the directories in a neat order
        print (directory)

    log_num = int(raw_input())                                    #user choosing a directory
    return log_num


                                                   #
def desired_thrust_parser(desired, desired_index):
    index = 1
    stop = desired.rfind(",") - 1                                 #the stopping point [0,0,0,0,0,0], and then accounting for the "]" so "stop -1"

    while index < stop:
        if (index > stop):
            break

        sub1 = desired.find(',', index)                           #looping through each number by using "," as seperators

        if (sub1==stop + 1):
            desired_num = desired[index:sub1 - 1]                 #if its the last one skip "]"
        else:
            desired_num = desired[index:sub1]

        desired_thrust[desired_index].append(int(desired_num))    #add to the array
        index = sub1+1



def frozen_thrust_parser(frozen,frozen_index):                    #same as the ones above
    index = 1
    stop = frozen.rfind(",")-1

    while index <(stop):

        if (index > stop):
            break

        sub2 = frozen.find(',', index)

        if (sub2==stop+1):
            frozen_num  = frozen[index:sub2 - 1]
        else:
            frozen_num  = frozen[index:sub2]

        frozen_thrust[frozen_index].append(int(frozen_num))
        index = sub2+1


def disabled_thrust_parser(disabled,disabled_index):
    index = 1
    stop = disabled.rfind(",")-1

    while index <(stop):

        if (index > stop):
            break

        sub = disabled.find(',', index)

        if (sub==stop+1):
            disabled_num  = disabled[index:sub - 1]
        else:
            disabled_num  = disabled[index:sub]

        disabled_thrust[disabled_index].append(float(disabled_num))
        index = sub+1


def thruster_scales_parser(scales,scales_index):
    index = 1
    stop = scales.rfind(",")-1

    while index <(stop):

        if (index > stop):
            break

        sub = scales.find(',', index)

        if (sub==stop+1):
            scales_num  = scales[index:sub - 2]                     #this is "-2" to account for "]}"
        else:
            scales_num  = scales[index:sub]

        thruster_scales[scales_index].append(float(scales_num))
        index = sub+1


def print_Neatly(toprint, label,times):
    print ("Time          " + label)

    toprint = np.column_stack((times,toprint))
    print('\n'.join([''.join(['{:14}'.format(item) for item in row])
                     for row in toprint]),end='\n\n')


def getAverage(thrusters):
    nparray = np.array(thrusters)
   # print nparray.std(axis=0,dtype=np.longfloat)
    ave = nparray.mean(axis=0,dtype=np.longfloat)
    return ave


def print_Neatly2d(toprint, label,times):
    print ("\n"+label+"\n"+"Time   ", end ='')
    i=0
    while (i< len(toprint[0])):
        print ("       Scale " + str(i),end='')
        i=i+1
    print ("")

    toprint = np.column_stack((times,toprint))

    print('\n'.join([''.join(['{:14}'.format(item) for item in row])
                     for row in toprint]),end='\n\n')




#dearflask: {thrusters: {desired_thrust: [0, 0, 0, 0, 0, 0 ],frozen: [0, 0, 0, 0, 0, 0 ],disabled_thrusters: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
# thruster_scales: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]},claw: {power: 0.0},cameras: {},leds: {bluetooth_led: false,camera_leds: false}},

def parse(lines,timefrom,timeto):
   # print (str(timefrom) + "----" + str(timeto))
    #print (len(lines))
    j=0
    for i in range(len(lines)):
     #   print (i)
        if ((i>=timefrom) & (i<timeto)):
            all_lines = lines[i].split(":")

            desired_thrust.append([])
            frozen_thrust.append([])
            disabled_thrust.append([])
            thruster_scales.append([])

            all_lines[4] = all_lines[4].replace(" ", "")
            all_lines[5] = all_lines[5].replace(" ", "")
            all_lines[6] = all_lines[6].replace(" ", "")
            all_lines[7] = all_lines[7].replace(" ", "")
            all_lines[9] = all_lines[9].replace(" ","")
            all_lines[12] = all_lines[12].replace(" ","")
            all_lines[13] = all_lines[13].replace(" ","")

            bluetooth = all_lines[12].split(",")
            camera = all_lines[13].split(",")
            power = all_lines[9].split(",")
            power[0] = power[0][0:len(power[0])-1]
            camera[0] = (camera[0])[0:len(camera[0])-2]


            all_time.append(all_lines[0])
            desired_thrust_parser(all_lines[4],j)
            frozen_thrust_parser(all_lines[5],j)
            disabled_thrust_parser(all_lines[6],j)
            thruster_scales_parser(all_lines[7],j)
            bluetooth_led.append(bluetooth[0])
            camera_led.append(camera[0])
            power_claw.append(power[0])

            j=j+1


def timeErrorCheck(timefrom,timeto):
    if (timefrom > len(lines)):
        sys.stderr.write('From exceeds total number of entries')
        exit(1)

    if (timefrom < 0):
        sys.stderr.write('From cannot be negative')
        exit(1)

    if (timeto > len(lines)):
        sys.stderr.write('To exceeds total number of entries')
        exit(1)

    if (timeto < 0):
        sys.stderr.write('To cannot be negative')
        exit(1)

    if (timeto - timefrom < 0):
        sys.stderr.write('Please enter valid time intervals')
        exit(1)



def printTime(alltimes):
    for i in alltimes:
        i=i.split(":")
        print ("Time: " + str(i[0]))


def getTime(lines,fro,to):

    timefromindex=0
    timetoindex=len(lines)
    j=0

    for i in lines:
        i=i.split(":")

        if (i[0]==fro):
            timefromindex = j
            break

        if (i[0]==to):
            timetoindex=j
            break
        j=j+1;

    return timefromindex,timetoindex




if __name__ == "__main__":

    dir_list = []
    LOG_DIR = "LOGDIR"
    env = os.environ[LOG_DIR]
    log_num = 0

    dir_list = next(os.walk(env))[1]
    env += dir_list[log_num]

    choice = 0
    file_list = os.listdir(env)
    env = [env + "/" + file_list[0], env + "/" + file_list[1]][choice == 1]  # setting the path to either dearflask or dearclient
    file_object = open(env, "r")
    lines = file_object.readlines()
    json_data = open(env).read()
    data= json.loads(json_data)



    #pr = json.loads(lines)
    pprint(data)

    desired_thrust = []
    frozen_thrust = []
    disabled_thrust = []
    thruster_scales = []
    bluetooth_led = []
    camera_led = []
    power_claw = []
    all_time = []


    timefrom =0
    timeto =0


    parser = argparse.ArgumentParser()
    parser.add_argument("-t", action='store_true',help="Prints out the times for all the logs")#print out all the times
    parser.add_argument("-des" , action='store_true', help="Prints out the logs for desired thrust")
    parser.add_argument("-dbt" , action='store_true', help="Prints out the logs for disabled thrust")
    parser.add_argument("-ft" , action='store_true', help="Prints out the logs for disabled thrust")
    parser.add_argument("-ts", action='store_true', help="Prints out the logs for thruster scales")
    parser.add_argument("-fr" , type=str, help="the starting point for the logs")
    parser.add_argument("-to" ,  type=str, help="The ending point of the logs")
    parser.add_argument("-cled", action='store_true',help="Prints out the camera LED's")
    parser.add_argument("-bled", action='store_true', help="Prints out the Bluetooth LED's")
    parser.add_argument("-pclw", action='store_true', help="Prints the power: Claw")
    args=parser.parse_args()




    if args.fr:
        timefrom = args.fr

    if args.to:
        timeto = args.to

    # timefrom,timeto = getTime(lines,timefrom,timeto)
    # timeErrorCheck(timefrom,timeto)
    # parse(lines, timefrom, timeto)

    if args.t:
        printTime(all_time)

    if args.des:
        print_Neatly2d(desired_thrust, "Desired Thrust",all_time)

    if args.dbt:
        print_Neatly2d(disabled_thrust,"Disabled Thrust",all_time)

    if args.ft:
        print_Neatly2d(frozen_thrust, "Frozen Thrust",all_time)

    if args.ts:
        print_Neatly2d(thruster_scales,"Thruster Scales",all_time)

    if args.cled:
        print_Neatly(camera_led,"Camera LED",all_time)

    if args.bled:
        print_Neatly(bluetooth_led,"Bluetooth LED",all_time)

    if args.pclw:
        print_Neatly(power_claw,"Power : Claw",all_time)