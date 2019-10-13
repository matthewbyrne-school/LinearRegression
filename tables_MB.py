# Author: Matthew Byrne
# Date: 7/10/19
''' Table Handling '''

months = ["January", "Feburary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

#  Main Table Class
class table:
    def __init__(self, data_Dictionary):
        self.data = data_Dictionary

    def getItem(self, col = None, rowIndex = None):
        if col:
            if rowIndex:
                return self.data[col][rowIndex]

            else:
                x = []
                for j in self.data[col]:
                    x.append(j)
                return x

        else:
            if rowIndex != None:
                y = []
                for col in self.data:
                    if col != "reference":
                        y.append(self.data[col][0])
                return y

            else:
                return self.data

    def __str__(self):
        Keys = list(self.data.keys())

        output = f"\n\t\t"
        for i in range(1, len(Keys)):
            output += f"\t{Keys[i]}"


        output += "\n\n"

        for i, j in enumerate(self.data[Keys[1]]):
            output += f"{self.data[Keys[0]][i]}"
            if len(self.data["reference"][i]) < 8:
                output += "\t"            
            for k in range(1, len(Keys)):
                if Keys[k] != "information":
                   output += f"\t\t£{self.data[Keys[k]][i] * 1000}"


            output += f"\n"

        return output


if __name__ == "__main__":
    
    Data = table({"reference":["January", "Feburary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], "Previous":[6, 10, 12, 15, 19, 19, 0, 23, 25, 29, 34, 41], "Precicted":[5, 8, 11, 14, 17, 20, 24, 27, 30, 33, 36, 39]})

    print(Data)

    print(Data.getItem(rowIndex=0))