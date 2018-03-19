import json
from copy import deepcopy
from pprint import pprint

def create_new_json_template():
    new_json = {
        "thrusters": {
            "desired_thrust": [0, 0, 0, 0, 0, 0],
            "disabled_thrusters": [],
            "thruster_scales": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        },
        "claw": {
            "power": 0.0
        },
        "cameras": [
            { "port": 8080, "status": 1 }
        ]
    }

    return new_json

def generate_example_test():
    all_jsons = []

    for i in range(10):
        temp_json = create_new_json_template()
        temp_json['thrusters']['desired_thrust'] = [float(i) / 10 for _ in range(6)]

        all_jsons.append(deepcopy(temp_json))

    return all_jsons

if __name__ == "__main__":
    with open('testOutput.json', 'w') as outFile:

        # generate new json by writing new functions and then inserting them into the write
        new_output = generate_example_test()

        outFile.write(json.dumps(new_output, indent=3))
