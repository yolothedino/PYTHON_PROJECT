import csv
Subjects_offered= {}
global recordcnt

def readfile(): #This function is to open the file and with read access
    #filename= input("Enter the file name: ")
    recordcnt = 0
    filename="subjects-offered.csv"
    infile = open(filename,"r")
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
    #print(recordcnt)
    
    
def displaysubjectoff(typesort):
    schcnt = 0
    if typesort == 0: 
        for key in sorted(Subjects_offered):
            schcnt += 1
            print ('%s:%s \n' % (key, Subjects_offered[key]))
        print ('Total School %d .'%(schcnt))
    elif typesort == 1:
        for key in sorted(Subjects_offered, reverse=True):
            schcnt += 1
            print ('%s:%s \n' % (key, Subjects_offered[key]))
        print ('Total School %d .'%(schcnt))
    else:
        print('You choose an invaild sort vaule !!! Either 0 or 1')

readfile()
typesort = input("Enter 0 (if you perfer sort A-Z) or 1 (if you perfer sort Z-A)")
displaysubjectoff(typesort)
