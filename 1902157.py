import csv,\
    sys, re

Subjects_offered, Subjectsls = {}, []
Menu = {0: "Exit", 1: "Read data info from dataset", 2: "Show all the result", 3: "Search by exact school name",
        4: "Search school that contains the following word",
        5: "Display all the subject offer", 6: "Search school that offer the subject search"}


def displaymenu():  # This function display the item in menu
    for i in range(1, len(Menu) + 1):
        if i == len(Menu):
            i = 0
            print(i, Menu[i])
            return
        else:
            print(i, Menu[i])


def readfile():  # This function is to open the file and with read access
    # filename= input("Enter the file name: ")
    filename = "subjects-offered.csv"
    datasetsubjectoffer(filename)


def datasetsubjectoffer(filename):
    recordcnt = 0
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for data in csv_reader:
            if data[0] != 'school_name':
                recordcnt += 1
                if data[0] in Subjects_offered.keys():
                    Subjects_offered[data[0]].append(data[1])
                else:
                    Subjects_offered[data[0]] = [data[1]]
                if data[1] not in Subjectsls:
                    Subjectsls.append(data[1])
    print('%s %d' % ('Total record: ', recordcnt))


def sortAZZA(dic, typesort):  # Print subject offer by the order A-Z or Z-A
    schcnt = 0
    if typesort == 0:
        for key in sorted(dic):
            schcnt += 1
            print ('%s:%s \n' % (key, dic[key]))
        print ('Total School %d .' % (schcnt))
    elif typesort == 1:
        for key in sorted(dic, reverse=True):
            schcnt += 1
            print ('%s:%s \n' % (key, dic[key]))
        print ('Total School %d .' % (schcnt))
    else:
        print('You choose an invaild sort vaule !!! Either 0 or 1')


def SearchSchool(dic, school):
    if school in dic.keys():
        print ('%s:%s \n' % (school, dic[school]))
    else:
        print ('No result found.')


def SearchSchoolContainSubString(dic, patten):
    schcnt = 0
    # patten = 'SECONDARY SCHOOL'
    for key in dic.keys():
        if re.findall(patten, key):
            schcnt += 1
            print ('%s:%s \n' % (key, dic[key]))
    print ('Total School found %d base on your search.' % (schcnt))


def SearchSubject(dic, subject):
    Subjectcnt = 0
    # patten = 'SECONDARY SCHOOL'
    for key in sorted(dic):
        # print Subjects_offered[key]
        if subject in dic[key]:
            Subjectcnt += 1
            print ('%s \n' % key)
    print ('Total School found %d base on your search subject offer.' % (Subjectcnt))


def displaysubject():
    for i in Subjectsls:
        print (i)

def export(filename,list):
    with open("output.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(list)



while True:
    displaymenu()
    option = int(input('Enter your option:'))
    if option == 0:
        exit()
    elif option == 1:
        readfile()
    elif option == 2:
        typesort = input('Enter 0 (if you perfer sort A-Z) or 1 (if you perfer sort Z-A)')
        sortAZZA(Subjects_offered, typesort)
    elif option == 3:
        school = raw_input('Enter the exactly school name you wish to search: ')
        SearchSchool(Subjects_offered, school.upper())
    elif option == 4:
        patten = raw_input('Enter anything contain in school name: ')
        SearchSchoolContainSubString(Subjects_offered, patten.upper())
    elif option == 5:
        displaysubject()
    elif option == 6:
        subject = raw_input('Enter the subject wish to search: ')
        SearchSubject(Subjects_offered, subject.upper())
    else:
        print('Invaild option')
