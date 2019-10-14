# import os
# filepath = os.path.join("/", "Users", "gkiar",
#                         "Desktop", "diabetes.rwrite1.txt")
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


# I am could not manage to use the .names files to collect the headers but
# I still put the two filenames and only used the .data one
filename = ['housing.data', 'any_file.names']

file= "/home/tpasturel/Desktop/IntroductionToPythonAndDataAnalysis/20191015_Assignment/hwk4_data/"+filename[0]
data=open(file, 'r')

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

def populate_dict():
    our_dictionary = {}
    for location, column_headings in enumerate(outer_list[0]):
        # Setting the dictionary's keys based on outer_list's indexes
        our_dictionary[location] = []
        for row in outer_list:
            our_dictionary[location] += [row[location]]
    print(our_dictionary)

populate_dict()