import pandas as pd
import random
from tqdm import tqdm, tqdm_notebook
import sys

# How many losed rows have to been generated for each existing win row
nbrLostRows = int(sys.argv[1])

df = pd.read_csv('./euromillions.csv', sep=";")

allPosibFile = open('./all_euromillions_combi_possible.csv', 'r')
allPosib = allPosibFile.readlines()
maxPosib = len(allPosib)
allPosibFile.close()

finalFile = open('./euromillions_' + str(nbrLostRows+1) + '.csv', 'a')
finalFile.write("Date;N1;N2;N3;N4;N5;E1;E2;Winner;Gain;Result\n")

# for each row in the dataframe, we create losed rows and save it to the final dataframe
for index, row in tqdm(df.iterrows(), total=len(df)):
    rowString = str(row['N1']) + ';' + str(row['N2']) + ';' + str(row['N3']) + ';' + str(row['N4']) + ';' + str(row['N5']) + ';' + str(row['E1']) + ';' + str(row['E2'])
    finalFile.write(row['Date'] + ';' + rowString + ';' + str(row['Winner']) + ';' + str(row['Gain']) + ';win\n')
    generations = []
    for i in range(nbrLostRows):
        # generate a list of random numbers
        randomNumber = random.randint(0, maxPosib-1)
        randomList = allPosib[randomNumber][:-1]
        # check if randomList is different from the current row
        while (randomList == rowString or randomNumber in generations):
            randomNumber = random.randint(0, maxPosib-1)
            randomList = allPosib[randomNumber][:-1]
        generations.append(randomNumber)
        finalFile.write(row['Date'] + ";" + randomList + ";0;0;lose" + '\n')
finalFile.close()