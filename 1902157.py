import csv
import sys


def copyall(filename, datasetnumber):
    if datasetnumber == 1:
        ifile = open('co-curricular-activities-ccas.csv', "rb")
        reader = csv.DictReader(ifile)
        ofile = open(filename, "wb")
        writer = csv.DictWriter(ofile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            writer.writerow(row)

        ifile.close()
        ofile.close()

        print "The chosen dataset has been successfully exported to the following file:" + filename


    elif datasetnumber == 2:
        ifile = open('general-information-of-schools.csv', "rb")
        reader = csv.DictReader(ifile)
        ofile = open(filename, "wb")
        writer = csv.DictWriter(ofile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            writer.writerow(row)

        ifile.close()
        ofile.close()

        print "The chosen dataset has been successfully exported to the following file:" + filename

    elif datasetnumber == 3:
        ifile = open('subjects-offered.csv', "rb")
        reader = csv.DictReader(ifile)
        ofile = open(filename, "wb")
        writer = csv.DictWriter(ofile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            writer.writerow(row)

        ifile.close()
        ofile.close()

        print "The chosen dataset has been successfully exported to the following file:" + filename


def copycertain(filename, datasetnumber, schoolipt):
    s1 = schoolipt.upper()
    success = 0

    if datasetnumber == 1:
        with open("co-curricular-activities-ccas.csv", "rb") as f:
            reader = csv.DictReader(f, delimiter=',')
            with open(filename, "wb") as f_out:
                writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames, delimiter=",")
                writer.writeheader()
                for row in reader:
                    if row['school_name'] == s1:
                        writer.writerow(row)
                        success = len(row)

            if success == 0:
                print "The school you've entered is not found in our dataset."
                tryagain = int(input("Would you like to try again? 1 = Yes, 2 = No"))

                if tryagain == 1:
                    export()

                else:
                    sys.exit()

            else:
                print "The chosen dataset has been successfully exported to the following file:" + filename



    elif datasetnumber == 2:
        s1 = schoolipt.upper()
        success = 0

        with open("general-information-of-schools.csv", "rb") as f:
                reader = csv.DictReader(f, delimiter=',')
                with open(filename, "wb") as f_out:
                    writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames, delimiter=",")
                    writer.writeheader()
                    for row in reader:
                        if row['school_name'] == s1:
                            writer.writerow(row)
                            success = len(row)

                if success == 0:
                    print "The school you've entered is not found in our dataset."
                    tryagain = int(input("Would you like to try again? 1 = Yes, 2 = No"))

                    if tryagain == 1:
                        export()

                    else:
                        sys.exit()

                else:
                    print "The chosen dataset has been successfully exported to the following file:" + filename

    elif datasetnumber == 3:
        s1 = schoolipt.upper()
        success = 0

        with open("subjects-offered.csv", "rb") as f:
                reader = csv.DictReader(f, delimiter=',')
                with open(filename, "wb") as f_out:
                    writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames, delimiter=",")
                    writer.writeheader()
                    for row in reader:
                        if row['school_name'] == s1:
                            writer.writerow(row)
                            success = len(row)

                if success == 0:
                    print "The school you've entered is not found in our dataset."
                    tryagain = int(input("\nWould you like to try again? 1 = Yes, 2 = No\n"))

                    if tryagain == 1:
                        export()

                    else:
                        sys.exit()

                else:
                    print "The chosen dataset has been successfully exported to the following file:" + filename
                    sys.exit()

def export():

    print "\n1. Co-Curricular Activities \n2. General Information of Schools \n3. Subjects Offered from Schools "


    try:
        datasetnumber = int(input("\nWhich data set would you like to export from? "))


    except:
        print "\nYou have entered an invalid input. Please try again\n"
        export()

    if (datasetnumber == 1) or (datasetnumber == 2) or (datasetnumber == 3):

            fe = raw_input("\nSet the export filename: ")

            if set('[~!@#$%^&*()_+{}":;\']+$').intersection(fe):
                print "\nPlease enter only characters or numbers. The program will restart again.\n"
                export()

            else:
                filename = fe + '.csv'

                print "\n1. Entire Dataset \n2. Search By Specific School"

                try:
                    specificornah = int(input("\nWould you like to copy the entire dataset or only for a specific school?"))

                except:
                    print "\nYou have entered an invalid input. Please try again\n"
                    export()

                if specificornah == 1:
                    copyall(filename, datasetnumber)

                elif specificornah == 2:
                    schoolipt = raw_input("\nPlease type in the name of the school: \n")
                    copycertain(filename, datasetnumber, schoolipt)

                else:
                    print "\nYou have entered an invalid input. Please try again\n"
                    export()

    else:
        print "\nYou have entered an invalid input. Please try again\n"
        export()



export()
