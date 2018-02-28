import os
import argparse
import json

# Time needs to be added
# While testing for me log_num=0 had all the file contents, that is what I tested with
# I did some cross tests and it seems to work
# DeerClient has not been added yet but it will just be same as what we have right now, wasn't added because
# I didn't have a sample at that time
# I will keep on working on this and provide a complete parser asap
# this works for deerflask and lays the outline of how I am approaching it for now


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


if __name__ == "__main__":

    #LOGDIR = "C:/Users/Mudabbir/Desktop/Logfolder/"


    #if the enviroment variable for the directory path doesn't exist, print error
    try:
        LOG_DIR = "LOGDIR"
        env = os.environ[LOG_DIR]
    except:
        print ("error")
        exit(10)



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
    #print (data1)




    #sets up the argument parser

    parser = argparse.ArgumentParser()
    parser.add_argument("-r", action='store_true', help="Prints out all the runs")
    parser.add_argument("-run", type=int, help="Selects the run you want tot access")
    parser.add_argument("-t", action='store_true',help="Prints out the times for all the logs")

    parser.add_argument("-thruster" ,action='store_true', help="Prints out all the contents in the thrusters")
    parser.add_argument("-des", action='store_true', help="Prints out the logs for desired thrust")
    parser.add_argument("-dbt", action='store_true', help="Prints out the logs for disabled thrust")
    parser.add_argument("-trs", action='store_true', help="Prints out the logs for thruster scales")
    parser.add_argument("-frt", action='store_true', help="Prints out the logs for frozen thrusters")

    parser.add_argument("-claw", action='store_true', help="Prints out all the contents in claw")
    parser.add_argument("-pow", action='store_true', help="Prints out the power component in claw")
    parser.add_argument("-led", action='store_true', help="Prints out all the contents in led")
    parser.add_argument("-cled", action='store_true', help="Prints out the Camera LED")
    parser.add_argument("-bled", action='store_true', help="Prints out the Bluetooth LED")
    parser.add_argument("-cam", action='store_true', help="Prints all the cameras")

    parser.add_argument("-fr", type=int, help="the starting point for the logs")
    parser.add_argument("-to", type=int, help="The ending point of the logs")
    args = parser.parse_args()

    #gets all the directories i.e. the directories with time stamps for each run
    dir_list = next(os.walk(env))[1]


    #if a run is provided then access that run, else default to the most recent run
    if args.run != None:
        log_num = args.run
    else:
        log_num = 0 #default

    if (args.r):
        get_Directory()
        exit(10)


   # log_num = 0      #for now because first directory is the only one with data
    env += dir_list[log_num]

    choice = 0      #because we only produced deerflask samples right now
    file_list = os.listdir(env)
    env = [env + "/" + file_list[0], env + "/" + file_list[1]][choice == 0]  # setting the path to either dearflask or dearclient
  #  print (env, "   ", log_num)


    data = []
    i=0

    with open(env) as f:
        for line in f:
            data.append(json.loads(line))
            data[i] = json.loads(data[i])
            i=i+1

    fromtime=0 #by default
    totime=len(data)

    if (args.fr!=None):       # we need to incorporate the time so this needs more work
        fromtime = args.fr

    if (args.to!=None):
        totime = args.to


    #Printing all the arguments , whatever was asked for
    if (args.thruster):
        i= fromtime
        print ("\nThrusters:")
        while (i<totime):
            print (data[i]['thrusters'])
            i = i + 1

    if (args.des):
        i = fromtime
        print ("\nThruster: Desired Thrusters")
        while (i<totime):
            print (data[i]['thrusters']['desired_thrust'])
            i = i + 1

    if (args.dbt):
        i = fromtime
        print ("\nThruster: Disabled Thrusters")
        while (i<totime):
            print (data[i]['thrusters']['disabled_thrusters'])
            i = i + 1

    if (args.trs):
        i = fromtime
        print ("\nThruster: Thruster Scales")
        while (i < totime):
            print (data[i]['thrusters']['thruster_scales'])
            i = i + 1


    if (args.frt):
        i = fromtime
        print ("\nThrusters: Frozen Thrusters")
        while (i<totime):
            print (data[i]['thrusters']['frozen'])
            i = i + 1


    if (args.claw):
        i = fromtime
        print ("\nClaw")
        while (i < totime):
            print (data[i]['claw'])
            i = i + 1


    if (args.pow):
        i = fromtime
        print ("\nClaw: Power")
        while (i < totime):
            print (data[i]['claw']['power'])
            i = i + 1

    if (args.led):
        i = fromtime
        print ("\nLED's")
        while (i < totime):
            print (data[i]['leds'])
            i = i + 1


    if (args.cled):
        i = fromtime
        print ("\nLED : Camera LED")
        while (i < totime):
            print (data[i]['leds']['camera_leds'])
            i = i + 1


    if (args.bled):
        i = fromtime
        print ("\nLED: Bluetooth LED")
        while (i < totime):
            print (data[i]['leds']['bluetooth_led'])
            i = i + 1


    if (args.cam):
        i = fromtime
        print ("\nCameras")
        while (i < totime):
            print (data[i]['cameras'])
            i = i + 1
