import joblib
import random
import pandas as pd
import math

nbrLostRows = 5000

# Give the chance to win for a lottery ticket
def get_ml_stat(ticket):
    # Load the model from the file
    model = joblib.load('./model/random_forest.joblib')
    # Predict the result
    result = model.predict_proba([ticket])[0]
    # Return the result (chance to win)
    return result[1]

# fit model with one more wining ticket
def add_data(date, ticket, winner, gain):
    # Build datas
    generations = [ticket]
    for i in range(nbrLostRows):
        # generate a list of random numbers
        set = sorted(random.sample(range(1, 51), 5)).__add__(sorted(random.sample(range(1, 13), 2)))
        # check if the set is different from the wining set or is not already generated
        while (set in generations):
            set = sorted(random.sample(range(1, 51), 5)).__add__(sorted(random.sample(range(1, 13), 2)))
        generations.append(set)
    # Load the data file
    finalFile = open('../../datasource/euromillions_' + str(nbrLostRows+1) + '.csv', 'a+')
    # Write the winning ticket
    converted_ticket = [str(element) for element in ticket]
    finalFile.write(date + ';' + ';'.join(converted_ticket) + ';' + str(winner) + ';' + str(gain) + ';win\n')
    # Write all generated datas
    for generation in generations[1:]:
        converted_generation = [str(element) for element in generation]
        finalFile.write(date + ';' + ';'.join(converted_generation) + ';0;0;lose\n')
    finalFile.close()
    # Load the model from the file
    model = joblib.load('./model/random_forest.joblib')
    # Fit the model with the wining ticket
    model.fit([ticket], ['win'])
    # Fit the model with all lose tickets
    model.fit(generations[1:], ['lose'] * (nbrLostRows))
    # Save the model to the file
    joblib.dump(model, './model/random_forest.joblib')

def get_stat(ticket):
    """
    Calculate the chance of winning for a given set of numbers and additional numbers (in ticket).
    Use combinations to calculate the chance of winning.
    """
    # Get chance to win
    def combination(n, k):
        return math.factorial(n) // (math.factorial(k) * math.factorial(n-k))

    # Separate the numbers
    numbers, additionalNumbers = ticket[:5], ticket[5:]

    # import datas
    df = pd.read_csv('../../datasource/euromillions.csv', sep=";")
    # define types of numbers
    df['N1'] = df['N1'].astype(int)
    df['N2'] = df['N2'].astype(int)
    df['N3'] = df['N3'].astype(int)
    df['N4'] = df['N4'].astype(int)
    df['N5'] = df['N5'].astype(int)
    df['E1'] = df['E1'].astype(int)
    df['E2'] = df['E2'].astype(int)

    # Get apparitions times
    count_number = df['N1'].value_counts().add(df['N2'].value_counts(), fill_value=0).add(df['N3'].value_counts(), fill_value=0).add(df['N4'].value_counts(), fill_value=0).add(df['N5'].value_counts(), fill_value=0)
    count_additional_number = df['E1'].value_counts().add(df['E2'].value_counts(), fill_value=0)

    # calculate the chance of winning for the main numbers
    chanceOfWinningNumbers = 1 / combination(count_number.index.max(), len(numbers))
    averageChanceNumbers = 0
    for number in numbers:
        averageChanceNumbers += 1 - (count_number[number] - count_number.mean()) / count_number.sum()
    averageChanceNumbers /= len(numbers)
    chanceOfWinningNumbers *= averageChanceNumbers
    # calculate the chance of winning for the additional numbers
    chanceOfWinningAdditionalNumbers = 1 / combination(count_additional_number.index.max(), len(additionalNumbers))
    averageChanceAdditionalNumbers = 0
    for number in additionalNumbers:
        averageChanceAdditionalNumbers += 1 - (count_additional_number[number] - count_additional_number.mean()) / count_additional_number.sum()
    averageChanceAdditionalNumbers /= len(additionalNumbers)
    chanceOfWinningAdditionalNumbers *= averageChanceAdditionalNumbers
    # return the chance of winning for all numbers
    return chanceOfWinningNumbers * chanceOfWinningAdditionalNumbers