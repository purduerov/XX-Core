import os
import numpy as np
import argparse

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


def getAverage(thrusters):
    nparray = np.array(thrusters)
   # print nparray.std(axis=0,dtype=np.longfloat)
    ave = nparray.mean(axis=0,dtype=np.longfloat)
    return ave


def print_Neatly2d(toprint, label):
    print (label)
    i=0
    print "    ",
    while (i< len(toprint[0])):
        print (" Scale " + str(i)),
        i=i+1;
    print ("")

    print('\n'.join([''.join(['{:9}'.format(item) for item in row])
                     for row in toprint]))
    print ("")




#dearflask: {thrusters: {desired_thrust: [0, 0, 0, 0, 0, 0 ],frozen: [0, 0, 0, 0, 0, 0 ],disabled_thrusters: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
# thruster_scales: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]},claw: {power: 0.0},cameras: {},leds: {bluetooth_led: false,camera_leds: false}},

def parse(lines):

    for i in range(len(lines)):
        all_lines = lines[i].split(":")

        desired_thrust.append([])
        frozen_thrust.append([])
        disabled_thrust.append([])
        thruster_scales.append([])

        all_lines[4] = all_lines[4].replace(" ", "")
        all_lines[5] = all_lines[5].replace(" ", "")
        all_lines[6] = all_lines[6].replace(" ", "")
        all_lines[7] = all_lines[7].replace(" ", "")

        desired_thrust_parser(all_lines[4],i)
        frozen_thrust_parser(all_lines[5],i)
        disabled_thrust_parser(all_lines[6],i)
        thruster_scales_parser(all_lines[7],i)




def main():
      # getting the value from the environment variable


    # print "0-DeerFlask\n1-DeerLog"
    # choice = int(raw_input())

    # parse(lines)
    #
    # print_Neatly2d(desired_thrust, "Desired Thrust")
    # print ("Average of Desired: " + str(getAverage(desired_thrust)) + "\n")
    #
    # print_Neatly2d(frozen_thrust, "Frozen Thrust")
    # print ("Average of Frozen: " + str(getAverage(frozen_thrust)) + "\n")
    #
    # print ("Disabled Thrust: " + str(disabled_thrust))
    # print ("Thruster Scales: " + str(thruster_scales))

    print ("A")



def printTime(lines):
    for i in lines:
        i=i.split(":")
        print ("Time: " + str(i[0]))

if __name__ == "__main__":

    LOG_DIR = "LOGDIR"
    env = os.environ[LOG_DIR]
    log_num = 0

    dir_list = next(os.walk(env))[1]
    env += dir_list[log_num]

    choice = 0
    file_list = os.listdir(env)
    env = [env + "/" + file_list[0], env + "/" + file_list[1]][
        choice == 0]  # setting the path to either dearflask or dearclient
    file_object = open(env, "r")
    lines = file_object.readlines()


    desired_thrust = []
    frozen_thrust = []
    disabled_thrust = []
    thruster_scales = []
    claw = []
    dir_list = []




    print_time = False
    dbt_thr = False
    froz_thr = False
    des_thr = False
    thr_sca = False
    timefrom =0
    timeto =0



    parser = argparse.ArgumentParser()
    parser.add_argument("-t", action='store_true',help="Prints out the times for all the logs")#print out all the times
    parser.add_argument("-des" , action='store_true', help="Prints out the logs for desired thrust")
    parser.add_argument("-dbt" , action='store_true', help="Prints out the logs for disabled thrust")
    parser.add_argument("-ft" , action='store_true', help="Prints out the logs for disabled thrust")
    parser.add_argument("-ts", action='store_true', help="Prints out the logs for thruster scales")
    parser.add_argument("-fr" , type=int, help="the starting point for the logs")
    parser.add_argument("-to" ,  type=int, help="The ending point of the logs")
    args=parser.parse_args()



   # print (lines)
    parse(lines)


    #print ("Average of Desired: " + str(getAverage(desired_thrust)) + "\n")


    #print ("Average of Frozen: " + str(getAverage(frozen_thrust)) + "\n")

    #print ("Disabled Thrust: " + str(disabled_thrust))
    print ("Thruster Scales: " + str(thruster_scales))
    print_Neatly2d(thruster_scales, "Thruster Scales")

    if args.t:
        printTime(lines)

    if args.des:
        print_Neatly2d(desired_thrust, "Desired Thrust")

    if args.dbt:
        print_Neatly2d(disabled_thrust,"Disabled Thrust")

    if args.ft:
        print_Neatly2d(frozen_thrust, "Frozen Thrust")

    if args.ts:
        print_Neatly2d(thruster_scales,"Thruster Scales")

    if args.fr:
        timefrom=args.fr
        
    if args.to:
        timeto = args.to



    #print ("print time = " + str(print_time))
    #print ("Desired thrust = " + str(des_thr))
    #print ("Disabled thrust = " + str(dbt_thr))
    #print ("Frozen thrust = " + str(froz_thr))
    #print ("Thruster scales = " + str(thr_sca))
    #print ("time from = " + str(timefrom) + " time to = " + str(timeto))

