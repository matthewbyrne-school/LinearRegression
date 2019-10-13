''' A Level Computer Science Project 2019 '''
# Author: Matthew Byrne
# Date: 11/10/19

# Imports
import linear_regression_MB
import tables_MB
import math

try:
    import matplotlib.pyplot as plt # This module is the only one that requires external installation, and so if not present you must be instructed to install it
except ImportError:
    raise ImportError("\n\nInstall the matplotlib library before attempting to run\n\n")

import json
import otp
from tkinter import filedialog, Tk, Label, Button


# Main data class
class SalesData():
    def __init__(self, previousYear):
        if type(previousYear) is list:
            self.Data = previousYear # takes the data from the previous year

        elif type(previousYear) is dict:
            try:
                self.previous = previousYear["information"]["previous year"]
            except:
                self.previous = "2018"

            self.Data = previousYear[self.previous]
            self.z = list(range(len(self.Data)+1, len(self.Data)*2+1))

            for i in range(1,20):
                num = str(2018 - i)

                try:
                    exec(f"self.year{num} = previousYear[num]")                
                
                except KeyError:
                    pass

            try:
                self.xLabel = previousYear["information"]["x label"]

            except:
                self.xLabel = "Time (Months)"

            try:
                self.yLabel = previousYear["information"]["y label"]

            except:
                self.yLabel = "Sales (£1000)"

        self.__equation = self.getEquation() # forming the equation as well as some key variables
        self.predictions, self.__r2 = self.predictResults()

    def getEquation(self): # formulating an equation
        self.x = list(range(1, len(self.Data)+1))

        self.__m, self.__c, self.__xBar, self.__yBar = linear_regression_MB.FormEquation(self.x, self.Data)
        equation = linear_regression_MB.Equation(f"y = {self.__m}x + {self.__c}")

        return equation
        
    def predictResults(self): # predicting the next year of sales
        initial_prediction = self.__equation.predict(self.x)
        r2 = linear_regression_MB.Rsquare(self.Data, self.__yBar, initial_prediction)

        predicted_equation = linear_regression_MB.optimise(self.x, self.Data, self.__equation, self.__yBar, self.__m, self.__c, r2)

        predictions = predicted_equation.predict(self.z)

        r2 = linear_regression_MB.Rsquare(self.Data, self.__yBar, predictions)

        for i, I in enumerate(predictions):
            predictions[i] = round(I)

        return predictions, r2

    def plot(self): # plotting the data into a graph
        equations = []

        plt.title(f"Data Approximation Using Linear Regression\nR² of approximately {round(self.__r2, 3)}")
        self.__equation.plot()
        equations.append("2019 Prediction")

        linear_regression_MB.plot(self.x, self.Data)
        equations.append(self.previous)

        for i in range(1,10):
            num = str(2018 - i)
            
            try:
                equations.append(num)
                exec(f"plt.plot(self.x, self.year{num}, dashes=[5, 5])")

            except AttributeError:
                pass

        plt.legend(equations, loc=2)
        
        plt.ylabel(self.yLabel)
        plt.xlabel(self.xLabel)

        plt.savefig("output.png")

    def __str__(self):
         return f"\nPrevious Year:\n\t{self.Data}\n\nApproximations:\n\t{self.predictions}\n"


# Main Interfacing
def interface(openJsonFile):
    root = Tk()
    root.title("Linear Regression Data Approximation")
    root.geometry("400x300")
    root.configure(background="white")
    label1 = Label(root, font="arial", background="white", activebackground="white", borderwidth=0, width=40, height=10, foreground="black", text="Select a JSON with the data you would like to import")
    label1.pack()
    button = Button(root, background="white", activebackground="white", borderwidth=2, text="Import", foreground="black", command=(lambda: openJsonFile(root)))
    button.pack()
    root.mainloop()


# File Opening Subroutine and JSON Parsing
def openJsonFile(root):
    global dataFile
    filename = filedialog.askopenfilename(parent=root, filetypes = [("JSON Files", "*.json")], initialdir = "/")
    root.destroy()
    with open(filename) as file:
        contents = file.read()

    dataFile = json.loads(contents)
    

def i2bArray(array): # Integer Array --> Binary Array

    outputArray = []
    for i in array:
        x = '{0:08b}'.format(i)
        outputArray.append(x)

    return outputArray

def encryptArray(array): # Encrypt and entire array at once
    
    k = otp.eightBitKeyGen()

    outputArray = []
    for i in array:
        c = otp.encryptString(k, i)
        outputArray.append(c)

    return outputArray, k

# Main Bit
if __name__ == "__main__":    
    dataFile = None
    interface(openJsonFile) # Reading the JSON file and parsing it into a readable format

    data = SalesData(dataFile) # Formatting the input
    data.plot() # Plotting the results and saving the figure
    output = data.predictions # Saving the predicted results

    print(output)

    newTable = tables_MB.table({"reference":tables_MB.months, "Previous":data.Data, "Predicted":output})
    print(newTable)

    binaryArray = i2bArray(output) # Converting every element of the list into binary, ready to be encrypted
    encryptedArray, key = encryptArray(binaryArray)

    print(f"\n\nThe file was encrypted with key '{key}'.\nDecrypt every item with this key to view the predictions.\n\nAlternatively, view the graph that has been saved to the directory containing the file to see the predicted trend.\n\n\n\nInfo:\n\tMade by Matthew Byrne\n\tUses linear regression to make a rough estimate of sales\n\tThis is a rough draft made on 11/10/19\n\n")

    with open("output.json", "w") as h:
        json.dump(encryptedArray, h)
