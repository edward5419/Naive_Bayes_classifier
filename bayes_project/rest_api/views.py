
from django.http.response import JsonResponse
from rest_api.models import *
from rest_api.serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.http import  JsonResponse
from django.db import transaction
import json
import pandas as pd



    
@csrf_exempt
def dataUpload(request):
    # Read Excel file
    df = pd.read_excel(request.FILES['file'], dtype={0: str, 1: int})

    # Initialize variables
    data_collection = []
    total_frequency = 0
    positive_frequency = 0
    natural_frequency = 0
    negative_frequency = 0

    # Put all the letters in all rows in the first column into an array
    unique_chars = df.iloc[:, 0].astype(str).str.cat(sep='').replace(' ', '').replace('\n', '').replace('\t', '')
    unique_chars = list(set(unique_chars))

    # Add data by calculating frequency for each unique_chars
    for char in unique_chars:
        positive_frequency = sum(df[df.iloc[:, 1] == 1].iloc[:, 0].str.count(char))
        natural_frequency = sum(df[df.iloc[:, 1] == 0].iloc[:, 0].str.count(char))
        negative_frequency = sum(df[df.iloc[:, 1] == -1].iloc[:, 0].str.count(char))
        char_data = {
            'Character': char,
            'Frequency_positive': positive_frequency + 1 if pd.notnull(positive_frequency) else 1, #laplace smoothing, add one to every char frequency
            'Frequency_natural': natural_frequency + 1 if pd.notnull(natural_frequency) else 1,
            'Frequency_negative': negative_frequency + 1 if pd.notnull(negative_frequency) else 1
        }
        data_collection.append(char_data)

    # Calculate totals
    for data in data_collection:
        positive_frequency += data['Frequency_positive']
        natural_frequency += data['Frequency_natural']
        negative_frequency += data['Frequency_negative']

    total_frequency = natural_frequency + positive_frequency + negative_frequency

    # Upload data to MySQL
    with transaction.atomic():
        for data in data_collection:
            char = data['Character']
            positive_prob = data['Frequency_positive'] / positive_frequency
            negative_prob = data['Frequency_negative'] / negative_frequency
            natural_prob = data['Frequency_natural'] / natural_frequency

            # Create or update DataProb object in mysql
            obj, created = DataProb.objects.update_or_create(char=char, defaults={'positive_prob': positive_prob, 'negative_prob': negative_prob, 'natural_prob': natural_prob})

    # Calculate total probabilities
    total_positive_prob = positive_frequency / total_frequency
    total_negative_prob = negative_frequency / total_frequency
    total_natural_prob = natural_frequency / total_frequency

    print(f"The probability of total positive: {total_positive_prob}")
    print(f"The probability of total natural: {total_natural_prob}")
    print(f"The probability of total negative: {total_negative_prob}")

    #store the metadata to mysql
    meta_data = MetaData.objects.get_or_create(pk=1)
    meta_data.total_positive_freq = positive_frequency
    meta_data.total_negative_freq = negative_frequency
    meta_data.total_natural_freq = natural_frequency
    meta_data.total_freq = total_frequency
    meta_data.total_positive_prob = total_positive_prob
    meta_data.total_negative_prob = total_negative_prob
    meta_data.total_natural_prob = total_natural_prob
    meta_data.save()
    
    #response to client
    return JsonResponse('data upload succesfully', safe=False)

@csrf_exempt
def output(request):
    #array to store probabilities of each sentance, at the and of this code, compares these three data and give result.
    datalistPositiveProb = []
    datalistNegativeProb = []
    datalistNaturalProb = []
    
    data_str = request.POST.get('data')  # Get the array of strings from the request as a string
    datalist = json.loads(data_str)

    #get the metaData from mysql
    metadata = MetaData.objects.first()
    total_positive_freq = metadata.total_positive_freq
    total_negative_freq = metadata.total_negative_freq
    total_natural_freq = metadata.total_natural_freq
    total_positive_prob = metadata.total_positive_prob
    total_negative_prob = metadata.total_negative_prob
    total_natural_prob = metadata.total_natural_prob

    for data in datalist:
        # arrays to store probability of each letters
        dataPositiveProb = []
        dataNegativeProb = []
        dataNaturalProb = []
        
        for char in data:
            try:
                #get the each hanzi's probabilities from mysql
                char_prob = DataProb.objects.get(char=char)
                positive_prob = char_prob.positive_prob
                negative_prob = char_prob.negative_prob
                natural_prob = char_prob.natural_prob
            except DataProb.DoesNotExist:
                positive_prob = 1 / (total_positive_freq+1) # laplace smoothing, if input char is not in database, prob = 1/total positive frequency+1
                negative_prob = 1 / (total_negative_freq +1)
                natural_prob = 1 / (total_natural_freq +1)
            
            dataPositiveProb.append(positive_prob)
            dataNegativeProb.append(negative_prob)
            dataNaturalProb.append(natural_prob)
        #multiply all probs for each letter in a sentance
        multiPositive = 1
        multiNegative = 1
        multiNatural = 1
        
        for prob in dataPositiveProb:
            multiPositive *= prob
        for prob in dataNegativeProb:
            multiNegative *= prob
        for prob in dataNaturalProb:
            multiNatural *= prob
        #add to array
        datalistPositiveProb.append(multiPositive * total_positive_prob)
        datalistNegativeProb.append(multiNegative * total_negative_prob)
        datalistNaturalProb.append(multiNatural * total_natural_prob)
    
    print(datalistPositiveProb)
    print(datalistNegativeProb)
    print(datalistNaturalProb)
    print(len(datalistPositiveProb))
    #get the number of sentences, if client send 40 sentance, then 40
    maxListNum = len(datalistPositiveProb)
    #array for store result
    finalOutcome = []
    #compares each sentence's positive, negative, natural probability 
    for i in range(maxListNum):
        positive_prob = datalistPositiveProb[i]
        negative_prob = datalistNegativeProb[i]
        natural_prob = datalistNaturalProb[i]
    
        if positive_prob > negative_prob and positive_prob > natural_prob:
            finalOutcome.append(1)
        elif negative_prob > positive_prob and negative_prob > natural_prob:
            finalOutcome.append(-1)
        else:
            finalOutcome.append(0)
    print('final outcome')
    print(finalOutcome)

        
    # return result to client
    return JsonResponse(finalOutcome, safe=False)

