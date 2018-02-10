import os

desired_thrust =[]
frozen_thrust = []
disabled_thrust = []
thruster_scales = []
claw = []


env = os.environ["LOGDIR"] #getting the value from the environment variable
log_num=0
dir_list = next(os.walk(env))[1]


def get_Directory():

    print "Select the log you would like to access\n"
    for i in range(len(dir_list)):
        directory = str(i) + ": " + dir_list[i]                   #printing all the directories in a neat order
        print directory

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



env += dir_list[log_num]


                                                            #print "0-DeerFlask\n1-DeerLog"
                                                            #choice = int(raw_input())
choice =0
file_list = os.listdir(env)
env = [env+"/"+file_list[0],env+"/"+file_list[1]][choice==0] #setting the path to either dearflask or dearclient


file_object = open(env,"r")
lines = file_object.readlines();

#dearflask: {thrusters: {desired_thrust: [0, 0, 0, 0, 0, 0 ],frozen: [0, 0, 0, 0, 0, 0 ],disabled_thrusters: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
# thruster_scales: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]},claw: {power: 0.0},cameras: {},leds: {bluetooth_led: false,camera_leds: false}},


for i in range(len(lines)):

    all_lines = lines[i].split(":")
    index=1

    desired_thrust.append([])
    frozen_thrust.append([])
    disabled_thrust.append([])
    thruster_scales.append([])

    all_lines[3] = all_lines[3].replace(" ", "")
    all_lines[4] = all_lines[4].replace(" ", "")
    all_lines[5] = all_lines[5].replace(" ", "")
    all_lines[6] = all_lines[6].replace(" ", "")

    desired_thrust_parser(all_lines[3],i)
    frozen_thrust_parser(all_lines[4],i)
    disabled_thrust_parser(all_lines[5],i)
    thruster_scales_parser(all_lines[6],i)



print desired_thrust
print frozen_thrust
print disabled_thrust
print thruster_scales
