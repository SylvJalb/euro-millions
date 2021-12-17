import math

import pandas as pd

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
count_number = df['N1'].value_counts().add(df['N2'].value_counts(), fill_value=0).add(df['N3'].value_counts(),
                                                                                      fill_value=0).add(
    df['N4'].value_counts(), fill_value=0).add(df['N5'].value_counts(), fill_value=0)
count_additional_number = df['E1'].value_counts().add(df['E2'].value_counts(), fill_value=0)


# Get chance to win
def combination(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def get_chance_of_winning(numbers, additionalNumbers):
    """
    Calculate the chance of winning for a given set of numbers and additional numbers.
    Use combinations to calculate the chance of winning.
    """
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
        averageChanceAdditionalNumbers += 1 - (
                count_additional_number[number] - count_additional_number.mean()) / count_additional_number.sum()
    averageChanceAdditionalNumbers /= len(additionalNumbers)
    chanceOfWinningAdditionalNumbers *= averageChanceAdditionalNumbers
    # return the chance of winning for all numbers
    return chanceOfWinningNumbers * chanceOfWinningAdditionalNumbers
