import os
import argparse
import json


def get_Directory():

    print ("Select the log you would like to access by using -run=<number>\n")
    for i in range(len(dir_list)):
        directory = "Run " + str(i) + ":  " + dir_list[i]                   #printing all the directories in a neat order
        print (directory)


#to get the all the keys .. not applicable right now

# def get_keys(d_or_l, keys_list):
#     if isinstance(d_or_l, dict):
#         for k, v in iter(sorted(d_or_l.items())):
#             if isinstance(v, list):
#                 get_keys(v, keys_list)
#             elif isinstance(v, dict):
#                 get_keys(v, keys_list)
#             keys_list.append(k)   #  Altered line
#     elif isinstance(d_or_l, list):
#         for i in d_or_l:
#             if isinstance(i, list):
#                 get_keys(i, keys_list)
#             elif isinstance(i, dict):
#                 get_keys(i, keys_list)
#     else:
#         print ('\n')
#         #print ("** Skipping item of type: {}".format(type(d_or_l)))
#     return keys_list

def getTimeIndex(dic,from_t,to_t):

    # gets the index of the from and to time from string to integers
    i = 0
    from_index = 0
    to_index = len(dic)
    while (i < len(dic)):
        if (str(dic[i]["last_update"]) >= from_t):
            if (i!=0):
                from_index = i
            else:
                from_index = i
            break

        i = i + 1

    i = 0
    while (i < len(dic)):
        if (str(dic[i]["last_update"]) >= to_t):
            if (i != 0):
                to_index = i
            else:
                to_index = i
            break

        i = i + 1
    return from_index, to_index


def print1dim( dic, key, label, starttime, endtime):
    # helper function for non nested keys i.e. 1 dimensional array haha
    print("\n"+label)

    while (starttime < endtime):
        print (dic[starttime]["last_update"]," : ",dic[starttime][key])
        starttime = starttime + 1


def print2dim(dic, key, key2, label, starttime, endtime):
    # helper function for nested keys i.e. 2 dimensional only
    # add similar helper function for more nested keys if need be
    print("\n" + label)

    while (starttime < endtime):
        print (dic[starttime]["last_update"]," : ",dic[starttime][key][key2])
        starttime = starttime + 1


if __name__ == "__main__":

    # if the enviroment variable for the directory path doesn't exist, print error
    try:
        LOG_DIR = "LOGDIR"
        env = os.environ[LOG_DIR]
    except:
        print ("error")
        exit(10)

    # PATTERN = DD_HH_MIN_SEC_USEC


    # keys_list = []                                        //to get all the keys.. not useable right now
    # data1 =""
    # env1= "C:/Users/Mudabbir/Desktop/Logfolder/2018_01_17__12_59_23/dearclientlog.txt"
    # with open(env1) as f:
    #     for line in f:
    #         data1 = json.loads(line)
    #         data1 = json.loads(data1)
    #         break
    #
    # get_keys(data1,keys_list)
    # print (data1,'\n\n')
    # print (keys_list)


    # sets up the argument parser
    # edit this to add more arguments or take out arguments

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true', help="Prints out all the runs")
    parser.add_argument("-run", type=int, help="Selects the run you want tot access")
    parser.add_argument("-t", action='store_true',help="Prints out the times for all the logs")

    parser.add_argument("-df", action='store_true', help="Prints out logs for dearflask")
    parser.add_argument("-des", action='store_true', help="Prints out the logs for desired thrust")
    parser.add_argument("-dbt", action='store_true', help="Prints out the logs for disabled thrust")
    parser.add_argument("-trs", action='store_true', help="Prints out the logs for thruster scales")

    parser.add_argument("-claw", action='store_true', help="Prints out all the contents in claw")
    parser.add_argument("-pow", action='store_true', help="Prints out the power component in claw")
    parser.add_argument("-led", action='store_true', help="Prints out all the contents in led")
    parser.add_argument("-cled", action='store_true', help="Prints out the Camera LED")
    parser.add_argument("-bled", action='store_true', help="Prints out the Bluetooth LED")

    parser.add_argument("-cam", action='store_true', help="Prints all the cameras")
    parser.add_argument("-thruster" ,action='store_true', help="Prints out all the contents in the thrusters")
    parser.add_argument("-frt", action='store_true', help="Prints out the logs for frozen/frozen thrusters")
    parser.add_argument("-logtime", action='store_true', help="Prints the times inside the selected log")

    parser.add_argument("-dc", action='store_true', help="Prints out the logs for dearclient")
    parser.add_argument("-IMU",action='store_true', help="Prints out the logs for dearflask")
    parser.add_argument("-pres", action='store_true', help="Prints out contests for pressure")
    parser.add_argument("-camnum", type=int, help='Which camera do u want to print?')

    # PATTERN = DD_HH_MIN_SEC_USEC
    parser.add_argument("-fr", type=str, help="the starting point for the logs")
    parser.add_argument("-to", type=str, help="The ending point of the logs")

    args = parser.parse_args()

    # gets all the directories i.e. the directories with time stamps for each run
    dir_list = next(os.walk(env))[1]


    # if a run is provided then access that run, else default to the most recent run
    if args.run != None:
        log_num = args.run
    else:
        log_num = 0 #default

    if (args.r):
        get_Directory()
        exit(10)


    # adding the directory path
    env += dir_list[log_num]

    choice = 0
    file_list = os.listdir(env)
    if (args.dc): # if dearclient is chosen; else if defaults to dearflask , however no error happens by defaulting
        choice = 1

    env = [env + "/" + file_list[0], env + "/" + file_list[1]][choice == 0]  # setting the path to either dearflask or dearclient

    data = []
    with open(env) as f:
        for line in f:
            data.append(json.loads(line))

    # PATTERN = DD_HH_MIN_SEC_USEC
    fromtime = data[0]["last_update"] #by default it goes from start to end
    totime = data[len(data)-1]["last_update"]

    if (args.fr != None):
        fromtime = str(args.fr)

    if (args.to != None):
        totime = args.to


    # gets the index of the times from strings for easier access
    fromtime, totime = getTimeIndex(data, fromtime, totime)
    print ("Please use this format for time inputs: 00_00_00_00_000000")

    # Printing all the arguments , whatever was asked for
    check = 0

    if (args.df):
        check =1
        if (args.t):
            print("Time Format: DD_HH_MIN_SEC_USEC \nstart time: ",data[0]["last_update"]+ '\n' + "end time: ",data[len(data)-1]["last_update"] )

        if (args.thruster):
            print1dim(data,'thrusters','Thrusters',fromtime,totime)

        if (args.des):
            print2dim(data, 'thrusters','desired_thrust', 'Desired Thrusters', fromtime, totime)

        if (args.dbt):
            print2dim(data, 'thrusters','disabled_thrusters', 'Disabled thrusters', fromtime, totime)

        if (args.trs):
            print2dim(data, 'thrusters','thruster_scales', 'Thruster scales', fromtime, totime)

        if (args.frt):
            print2dim(data, 'thrusters','frozen', 'Frozen', fromtime, totime)

        if (args.claw):
            print1dim(data,'claw','Claw',fromtime,totime)

        if (args.pow):
            print2dim(data, 'claw','power', 'Claw: Power', fromtime, totime)

        if (args.led):
            print1dim(data,'leds','LED\'s',fromtime,totime)

        if (args.cled):
            print2dim(data, 'leds','camera_leds', 'LED : Camera LED', fromtime, totime)

        if (args.bled):
            print2dim(data, 'leds','bluetooth_led', 'LED: Bluetooth LED', fromtime, totime)

        if (args.cam):
            print1dim(data,'cameras','Camera',fromtime,totime)

    if (args.dc):
        check =1
        if (args.t):
            print("Time Format: DD_HH_MIN_SEC_USEC \nstart time: ",data[0]["last_update"]+ '\n' + "end time: ",data[len(data)-1]["last_update"] )

        if (args.thruster):
            print1dim(data,'thrusters','Thrusters',fromtime,totime)

        if (args.IMU):
            print1dim(data,'IMU','IMU',fromtime,totime)

        if (args.pres):
            print1dim(data,'pressure','Pressure',fromtime,totime)

        if (args.logtime):
            print1dim(data,'cam_cur', 'Times',fromtime,totime)

        if (args.cam):
            if (args.camnum!=None):
                cam_num = args.camnum
                str = 'Cam_' + str(cam_num)

                try:
                    print2dim(data, 'cameras', str, 'Camera '+str, fromtime, totime)
                except:
                    print ("Camera Number out of range")

            else :
                print1dim(data,'cameras','Cameras',fromtime,totime)

    # if neither were selected, tell user to select one or the other
    if (check == 0):
        print ("Please choose either dearclient or dearflask\nUser -dc or -df")
        exit(0)