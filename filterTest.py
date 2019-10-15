#   base code derived from derrick's

import csv

Subjects_offered = {}
global recordcnt


def readfile():  # This function is to open the file and with read access
    # filename= input("Enter the file name: ")
    recordcnt = 0
    filename = "subjects-offered.csv"
    infile = open(filename, "r")
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for data in csv_reader:
            if data[0] != 'school_name':
                recordcnt += 1
                if data[0] in Subjects_offered.keys():
                    Subjects_offered[data[0]].append(data[1])
                else:
                    Subjects_offered[data[0]] = [data[1]]
    infile.close
    # print(recordcnt)

def filterByString(str):
    schcnt = 0
    filterCount = 0
    str = str.upper()

    for key in sorted(Subjects_offered):
        schcnt += 1
        if str in key:
            print('%s:%s \n' % (key, Subjects_offered[key]))
            filterCount += 1
    print('Total schools (after filter) %d .' % (filterCount))

def filterByLevel(typesort):
    schcnt = 0
    filterCount = 0

    print(typesort)

    if typesort == 1:
        for key in sorted(Subjects_offered):
            schcnt += 1
            if "PRIMARY SCHOOL" in key:
                print('%s:%s \n' % (key, Subjects_offered[key]))
                filterCount +=1
        print('Total schools (after filter) %d .' % (filterCount))
    if typesort == 2:
        for key in sorted(Subjects_offered):
            schcnt += 1
            if "SECONDARY SCHOOL" in key:
                print('%s:%s \n' % (key, Subjects_offered[key]))
                filterCount += 1
        print('Total schools (after filter) %d .' % (filterCount))
    else:
        print('You chose an invalid sort value.')


readfile()

#print("Enter the following for their respective filters:")
#print("1 - Primary Schools")
#print("2 - Secondary Schools")

typesort = raw_input("Enter text to filter by:")
filterByString(typesort)    #'typesort' is the filter text
#filterbyLevel(typesort)

