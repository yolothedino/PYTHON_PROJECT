import csv

cca_offeredAll = {}
cca_offeredPri = {}
cca_offeredSec = {}
cca_offeredJc = {}

def readAll(): #This function is to open the file and with read access
    #filename= input("Enter the file name: ")
    recordcnt = 0
    filename="co-curricular-activities-ccas.csv"
    infile = open(filename,"r")
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for data in csv_reader:
            if data[0] != 'school_name':
                recordcnt += 1
                if data[0] in cca_offeredAll.keys():           #Checking if the School is inside the Dictionary Already
                    cca_offeredAll[data[0]].append(data[3])    #If yes, append the new CCA to the List
                else:
                    cca_offeredAll[data[0]] = [data[3]]        #If not, create a new Key and assign the CCA as a List to it
    return cca_offeredAll
    infile.close

def displayPrimary():
    recordcnt = 0
    filename = "co-curricular-activities-ccas.csv"
    infile = open(filename, "r")
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for data in csv_reader:
            if data[0] != 'school_name':
                if data[1] == 'PRIMARY':
                    recordcnt += 1
                    if data[0] in cca_offeredPri.keys():  # Checking if the School is inside the Dictionary Already
                        cca_offeredPri[data[0]].append(data[3])  # If yes, append the new CCA to the List
                    else:
                        cca_offeredPri[data[0]] = [data[3]]  # If not, create a new Key and assign the CCA as a List to it
    infile.close
    schcnt = 0

    for key in sorted(cca_offeredPri):
        schcnt += 1
        print ('%s:%s \n' % (key, cca_offeredPri[key]))
    print ('Total School %d .\n' % (schcnt))  # Display all Primary Schools and their CCAs

def displaySecondary():
    recordcnt = 0
    filename = "co-curricular-activities-ccas.csv"
    infile = open(filename, "r")
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for data in csv_reader:
            if data[0] != 'school_name':
                if data[1] == 'SECONDARY':
                    recordcnt += 1
                    if data[0] in cca_offeredSec.keys():  # Checking if the School is inside the Dictionary Already
                        cca_offeredSec[data[0]].append(data[3])  # If yes, append the new CCA to the List
                    else:
                        cca_offeredSec[data[0]] = [data[3]]  # If not, create a new Key and assign the CCA as a List to it
    infile.close
    schcnt = 0

    for key in sorted(cca_offeredSec):
        schcnt += 1
        print ('%s:%s \n' % (key, cca_offeredSec[key]))
    print ('Total School %d .\n' % (schcnt))  # Display all Primary Schools and their CCAs

def displayJC():
    recordcnt = 0
    filename = "co-curricular-activities-ccas.csv"
    infile = open(filename, "r")
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for data in csv_reader:
            if data[0] != 'school_name':
                if data[1] == 'JUNIOR COLLEGE':
                    recordcnt += 1
                    if data[0] in cca_offeredJc.keys():  # Checking if the School is inside the Dictionary Already
                        cca_offeredJc[data[0]].append(data[3])  # If yes, append the new CCA to the List
                    else:
                        cca_offeredJc[data[0]] = [data[3]]  # If not, create a new Key and assign the CCA as a List to it
    infile.close
    schcnt = 0

    for key in sorted(cca_offeredJc):
        schcnt += 1
        print ('%s:%s \n' % (key, cca_offeredJc[key]))
    print ('Total School %d .\n' % (schcnt))  # Display all Primary Schools and their CCAs


while True:
    try:
        selection = input("1) Display All Schools and their CCAs \n"
                          "2) Display all the Primary Schools and CCAs Offered \n"
                          "3) Display all the Secondary Schools and CCAs Offered \n"
                          "4) Display all the Junior College and CCAs Offered \n"
                          "5) Display CCAs offered in selected school \n"
                          "6) End Program \n"
                          "Key in the option number to continue: ")


        if selection == 1:
            readAll()
            schcnt = 0
            for key in sorted(cca_offeredAll):
                schcnt += 1
                print ('%s:%s \n' % (key, cca_offeredAll[key]))
            print ('Total School %d .\n' % (schcnt))

        elif selection == 2:
            displayPrimary()

        elif selection == 3:
            displaySecondary()

        elif selection == 4:
            displayJC()

        elif selection == 5:
            readAll()
            schoolname = raw_input("Enter School Name: ")
            CAPSschoolname = schoolname.upper()
            try:
                print "CCAs offered are: " + str(cca_offeredAll[CAPSschoolname]) + '\n'
            except KeyError:
                print "Please enter a valid school!\n"

        elif selection == 6:
            break

        else:
            print "Please choose an valid option\n\n"
    except NameError:
        print "Please choose an valid option\n\n"
    except SyntaxError:
        print "Please choose an valid option\n\n"