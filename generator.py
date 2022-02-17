import random
import argparse

# constants
SAMPLE_RATE = 24    # number of data points per second
VAR_LIMIT = 0.05   # variance limit per data point

# parse command line for filename
parser = argparse.ArgumentParser(description="Generate plaintext Kinect body tracking data.")
parser.add_argument("filename", help="The name of the file to be generated")
args = parser.parse_args()

# write to file
def generate_text(filename):
    if filename is None:
        print("ERROR: Please specify a filename.")
        return
    
    try:
        # open file in write mode
        f = open("output/" + filename, 'w')
        print("Opened file.")

        # create set of strings to be written into file
        filetext = ["Start of generated Kinect data.\n"]
        # EXAMPLE
        filetext.extend(create_straight_line(0.0, 0.0, 5.0, 5.0, 6))
        filetext.extend(create_straight_line(5.0, 5.0, 5.0, 0.0, 4))

        f.writelines(filetext)
        f.close()
    except IOError:
        print("ERROR: problems writing to file.")
    
    print("File sucessfully generated.")

# returns a list of strings to be appended to the filetext
def create_straight_line(x1, y1, x2, y2, sec, sample_rate=SAMPLE_RATE, variance=True):
    print("Generating line from (" + str(x1) + ", " + str(y1) + ") to (" + str(x2) + ", " + str(y2) + ")")

    x_pos = x1
    y_pos = y1
    filetext = []

    for i in range(sec * SAMPLE_RATE):
        pos = "pos ( %2.4f, %2.4f, 1.50); " % (x_pos, y_pos)
        quat = "quat (-0.05, 0.00, 0.99 );\n"
        filetext.append(pos + quat)

        x_pos += (x2 - x1) / (sec * sample_rate)
        y_pos += (y2 - y1) / (sec * sample_rate)

        # add slight variance to each data point to emulate imprecision of real data
        if variance:
            x_pos += random.uniform(-VAR_LIMIT, VAR_LIMIT)
            y_pos += random.uniform(-VAR_LIMIT, VAR_LIMIT)

    return filetext


if __name__ == "__main__":
    generate_text(args.filename)