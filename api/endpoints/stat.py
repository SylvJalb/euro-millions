import pandas as pd
import math

# import datas
df = pd.read_csv('../../datasource/EuroMillions_numbers.csv', sep=";")

# Get apparitions times
count_number = df['N1'].value_counts() + df['N2'].value_counts() + df['N3'].value_counts() + df['N4'].value_counts() + df['N5'].value_counts()
count_additional_number = df['E1'].value_counts() + df['E2'].value_counts()

# Get chance to win
def combination(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n-k))

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
        averageChanceAdditionalNumbers += 1 - (count_additional_number[number] - count_additional_number.mean()) / count_additional_number.sum()
    averageChanceAdditionalNumbers /= len(additionalNumbers)
    chanceOfWinningAdditionalNumbers *= averageChanceAdditionalNumbers
    # return the chance of winning for all numbers
    return chanceOfWinningNumbers * chanceOfWinningAdditionalNumbers
