import pandas as pd


data_collection = []


def dataParse():
    # read excel file
    df = pd.read_excel('comment_dataset.xlsx')
    #init variables
    global total_frequency
    global total_positive_prob
    global total_natural_prob
    global total_negative_prob
    global positive_frequency 
    global natural_frequency 
    global negative_frequency 
    total_frequency = 0
    total_positive_prob = 0
    total_natural_prob = 0
    total_negative_prob = 0
    positive_frequency = 0
    natural_frequency = 0
    negative_frequency = 0
    # Put all the letters in all rows in the first column into an array
    unique_chars = df.iloc[:, 0].str.cat(sep='').replace(' ', '').replace('\n', '').replace('\t', '')
    unique_chars = list(set(unique_chars))

  
    

    # Add data by calculating frequency for each unique_chars
    for char in unique_chars:
        char_data = {
            'Character': char,
            'Frequency_positive': sum(df[df.iloc[:, 1] == 1].iloc[:, 0].str.count(char)) + 1,
            'Frequency_natural': sum(df[df.iloc[:, 1] == 0].iloc[:, 0].str.count(char)) + 1,
            'Frequency_negative': sum(df[df.iloc[:, 1] == -1].iloc[:, 0].str.count(char)) + 1
        }
        data_collection.append(char_data)



    


    for data in data_collection:
        positive_frequency += data['Frequency_positive']

    for data in data_collection:
        natural_frequency += data['Frequency_natural']

    for data in data_collection:
        negative_frequency += data['Frequency_negative']  

    total_frequency = natural_frequency+positive_frequency+negative_frequency
    total_positive_prob = positive_frequency/total_frequency
    total_natural_prob = natural_frequency/total_frequency
    total_negative_prob = negative_frequency/total_frequency

    print(f"the prob of total positive : {total_positive_prob}")
    print(f"the prob of total natural : {total_natural_prob}")
    print(f"the prob of total negative : {total_negative_prob}")
    
    

def getStrPositiveProb(characters):
    positive_possibilities = []
    for char in characters:
        found = False
        for data in data_collection:
            if data['Character'] == char:
                positive_possibilities.append(data['Frequency_positive']/total_positive_prob)
                found = True
                break
        if not found:
            positive_possibilities.append(1/total_positive_prob)
    str_positive_prob = 0
    for prob in positive_possibilities:
        str_positive_prob += prob

    print(f"input string : {characters}")
    print(f"positive prob for every char : {positive_possibilities}")
    print(f"total positive prob for this sentance : {total_positive_prob*str_positive_prob}")
    return total_positive_prob*str_positive_prob


def getStrNaturalProb(characters):
    natural_possibilities = []
    for char in characters:
        found = False
        for data in data_collection:
            if data['Character'] == char:
                natural_possibilities.append(data['Frequency_natural']/total_natural_prob)
                found = True
                break
        if not found:
            natural_possibilities.append(1/total_natural_prob)
    str_natural_prob = 0
    for prob in natural_possibilities:
        str_natural_prob += prob

    print(f"input string : {characters}")
    print(f"natural_prob for every char : {natural_possibilities}")
    print(f"total natural_prob for this sentance : {total_natural_prob*str_natural_prob}")
    return total_natural_prob*str_natural_prob

def getStrNegativeProb(characters):
    negative_possibilities = []
    for char in characters:
        found = False
        for data in data_collection:
            if data['Character'] == char:
                negative_possibilities.append(data['Frequency_negative']/total_negative_prob)
                found = True
                break
        if not found:
            negative_possibilities.append(1/total_negative_prob)
    str_negative_prob = 0
    for prob in negative_possibilities:
        str_negative_prob += prob

    print(f"input string : {characters}")
    print(f"nagative_prob for every char : {negative_possibilities}")
    print(f"total nagative_prob for this sentance : {total_negative_prob*str_negative_prob}")
    return total_negative_prob*str_negative_prob

dataParse()
string = "很棒"
characters = []


for char in string:
    characters.append(char)


getStrPositiveProb(characters)
getStrNaturalProb(characters)
getStrNegativeProb(characters)

