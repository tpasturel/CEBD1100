
import os, argparse, csv
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file")
args = parser.parse_args()

def is_there_an_input_file():
    # While building this function, I ran through the two errors where either
    # I provided the wrong input file name or no input file name at all
    # and looked for a way to address both
    if args.input_file is not None:
        input_file = os.path.join(os.getcwd(),args.input_file)
        try:
            with open(input_file) as data:
                read_data = data.read()
                return input_file
        except FileNotFoundError:
            print("Failed to open" + str(input_file) + \
            ". \nPlease look for a potential typo in your file name and/or file path.")
            exit()
    else:
        print("Please provide an input file.")
        exit()

# Setting the input file calling the function I created above
input_file = is_there_an_input_file()

def convert_type(element):
    # Case 2: is an emptry str, should be ignored
    if element == "": # len(element) == 0
        return None
    # Case 4: is a # with no ., should be int
    try:
        return int(element)
    except ValueError:
        # Case 3: has a . but is a #, should be float
        try:
            return float(element)
        except ValueError:
            # Case 1: is a string, should remain a string
            return element


# My weird way of dealing with either commas, single spaces or double spaces separators
def format_row(row):
    if "," in row:
        row = row
    else:
        # Shrinking multiples spaces separators into a single one and replacing them 
        # by a comma in each row
        row = " ".join(row.split())
        row = row.replace(" ", ",")
    return row

def populate_outer_list_orig():
    data=open(input_file, 'r')
    my_read_data = data.read()
    my_read_data1 = my_read_data.split('\n')    
    outer_list = []
    for row in my_read_data1:
        row = format_row(row)
        row_list = []
        for element in row.split(","):    
            new_element = convert_type(element)
            if new_element is not None:
                row_list += [new_element]
        if len(row_list) > 0:
            outer_list += [row_list]
    return outer_list

def populate_outer_list_csv():
    with open(input_file, 'r') as data:
        # Trying to read with comma separators, if csv.reader fails using commas, 
        # getting rid of the error and using default "one or more spaces" delimiter
        try:
            inputcsv = csv.reader(data, delimiter=',')
        except csv.Error:
            pass
        else:
            inputcsv = csv.reader(data)
            outer_list = []
            for row in inputcsv:
                row_list = []
                for (index,element) in enumerate(row):
                    new_element = convert_type(element)
                    if new_element is not None:
                        row_list += [new_element]
                if len(row_list) > 0:
                    outer_list += [row_list]
            return outer_list

def compare_outer_lists():
    outer_list_orig = populate_outer_list_orig()
    outer_list_csv = populate_outer_list_csv()
    try:
        assert sorted(outer_list_orig) == sorted(outer_list_csv)     
    except AssertionError:
        print("\nouter_list_orig and outer_list_csv are not identical :(" + "\n")
        print("And yet, these two lists seem to contain the same elements:")
        print("== First element of outer_list_orig == \n" + str(outer_list_orig[0]))
        print("== First element of outer_list_csv == \n" + str(outer_list_csv[0]))
        print("\nThis is because csv.reader returns strings by default while the elements in our original list were casted as either ints of floats.")
        #But then looking up online, I found out in https://docs.python.org/3/library/csv.html#csv.reader that csv.reader returns strings by default.")

def populate_dict():
    our_dictionary = {}
    outer_list = populate_outer_list_orig()
    for location, column_headings in enumerate(outer_list[0]):
        # Setting the dictionary's keys based on outer_list's indexes
        our_dictionary[location] = []
        for row in outer_list[1:]:
            our_dictionary[location] += [row[location]]
    print(our_dictionary)

# This function does not yet plot the data in a consistent way because I am not really sure 
# on how to plot together the values from each column of each list in outer_list_orig :(
def plot_data():
    outer_list_orig = populate_outer_list_orig()
    outer_list_csv = populate_outer_list_csv()
    plt.hist([[value for value in row] for row in outer_list_orig])
    plt.ylabel('not sure what the y value represent here')
    plt.savefig(str(input_file) + "_histogram.png")
    # I am commenting the following out to allow my CallScript.py not to hang after it runs
    # this script on the first file while plot displays the first histogram
    # plt.show()

def main():
    populate_outer_list_orig()
    #populate_dict()
    populate_outer_list_csv()
    compare_outer_lists()
    plot_data()

if __name__ == "__main__": 
    main()