import Tkinter
import csv

root = Tkinter.Tk()

# open file
with open("testData.csv") as fileName:  # testData is a very simple and useless csv
   reader = csv.reader(fileName)
# r and c to grid it out
   r = 0
   for col in reader:
      c = 0
      for row in col:
         label = Tkinter.Label(root, width = 20, height = 2, text = row, relief = Tkinter.RIDGE)
         label.grid(row = r, column = c)
         c += 1
      r += 1

root.mainloop()