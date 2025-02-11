
import sys
from PySide6 import QtCore, QtWidgets

#things to do:
#add column and add row functions
#make headers editable and have them in the first row of the .txt file (maybe)
#add an initial pop up that explains the program + buttons + warns that save is final. 

class Inventory(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory! :3")

        self.data = self.readDataFromFile() #add in test data


        self.table = QtWidgets.QTableWidget(self) #creates table
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(len(self.data[0]))

        #button to press that saves the table data and rewrites the saved text file. 
        self.saveButton = QtWidgets.QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveData) #connects to "saveData" function that saves the table data to text file

        #refresh button: Sort of like an undo but only visually. When the user clicks save button they will be told changes cannot be made after the file has been saved.
        self.refreshButton = QtWidgets.QPushButton("Undo", self)
        self.refreshButton.clicked.connect(self.refreshTable)

        #when clicked displays information about the program and a quick walk through including tips and limits.
        self.helpButton = QtWidgets.QPushButton("Help", self)
        self.helpButton.clicked.connect(self.helpFunction)


        self.table.setHorizontalHeaderLabels(["Name", "Cost", "Color"]) ##placeholder for sample data. 

        #function to populate the table with the inital data given in self.data
        self.insertData()





        #adds table
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignRight)
        self.layout.addWidget(self.table) #adds table to self
        #spacer to change the positioning of the table
        tableSpacer = QtWidgets.QSpacerItem(20,40, QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Maximum)
        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.refreshButton)
        self.layout.addWidget(self.helpButton)
        self.layout.addItem(tableSpacer)





       
 
    @QtCore.Slot()
    def insertData(self):
        for row in range(len(self.data)):
            for column in range(len(self.data[row])): #[row] so that it iterates over all columns
                self.table.setItem(row, column, QtWidgets.QTableWidgetItem(self.data[row][column]))

    #takes data from datafile.txt in order to display inventory.
    def readDataFromFile(self):
        data = []
        file = open('datafile.txt', 'r')
        text = file.readlines()
        for line in text:
            rowData = [string.strip() for string in line.split(',')] #splits the line data using , as a barrier string.strip() gets rid of \n that are after the final data value and spaces
            if (len(rowData)) == 3: # since there are three attributes in the table this function waits till it sees three then appends them to data. Ensuring everything is seen before returning #set as 3 for sample data
                data.append(rowData)

        return data
    
    def refreshTable(self):
        self.data = self.readDataFromFile()
        self.table.setRowCount(len(self.data))
        #self.table.setColumnCount(len(self.data)) #removed because it was adding extra columns. 
        self.insertData()

    def saveData(self):
        file = open('datafile.txt', 'w')

        for row in range(self.table.rowCount()):
            newData = [] #Each row has its own data list
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column) # gets data at row x column and puts it in item
                newData.append(item.text())

                if(len(newData)) == 3:
                    file.write(",".join(newData) + "\n") #writes the data back into the file in the proper format (data, data, data \n)


    def helpFunction(self):
        message = QtWidgets.QMessageBox(self) #creates the message box
        message.setWindowTitle("Program Information")
        message.setText("Hello! This is a simple inventory managment system!\n"
                        "Here are some tips to help get you started!\n"
                        "You can double click on the boxes to directly edit the information within the table.\n"
                        "When you are finished editing press the button labeled Save in order to save your changes.\n"
                        "Be aware that save cannot be undone. It is final.\n"
                        "If you wish to revert the changes that you made to the table you can press undo and it will reset the table back to its saved state.\n")

        #executes the message box
        message.exec()






if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Inventory()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())
