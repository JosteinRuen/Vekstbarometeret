import csv
import pandas as pd
import requests
import json
from pyjstat import pyjstat


def kombiner_sporringer(df_1, df_2):
    print(df_1.describe)

    #Først rename alle ringerike(1977) til bare Ringerike etc
    for row_label, row in df_1.iterrows():
        if row['region'] == 'Ringerike (1977-2019)':
            df_1.loc[row_label, 'region'] = 'Ringerike'
        if row['region'] == 'Jevnaker (-2019)':
            df_1.loc[row_label, 'region'] = 'Jevnaker'
        if row['region'] == 'Hole (1977-2019)':
            df_1.loc[row_label, 'region'] = 'Hole'
        if row['region'] == 'Modum (-2019)':
            df_1.loc[row_label, 'region'] = 'Modum'


    dataframes = [df_1, df_2]
    sammensatt_frames = pd.concat(dataframes) #Concat dataframes til 1 dataframe

    return sammensatt_frames



def dataframe_to_linechart(df):  # Formaterer data til highchart formatet(år, Ringerike_verdi, Hole_verdi, Modum_verdi, Jevnaker_verdi)

    #Lag tomme lister med nettinnflytning som data
    ringerike_list = []
    hole_list = []
    modum_list = []
    jevnaker_list = []

    #Iterer over dataframe
    for row_label, row in df.iterrows():
        if row['region'] == 'Ringerike': #Hvis regionen er ringerike...
            # Legg til nettofinnflytnings verdien i listen
            ringerike_list.append([row['år'], row['value'], row['region']])
        if row['region'] == 'Hole':
            hole_list.append([row['år'], row['value'], row['region']])
        if row['region'] == 'Modum':
            modum_list.append([row['år'], row['value'], row['region']])
        if row['region'] == 'Jevnaker':
            jevnaker_list.append([row['år'], row['value'], row['region']])


    # Resultat_string bygger opp CSV filen som highcharts skal lese av
    resultat_string = "År, Ringerike, Hole, Modum, Jevnaker\n"

    # Iterer over alle elementer i ringerike listen
    for i in ringerike_list:
        resultat_string += i[0] + ', ' #Legger til året i csv filen
        resultat_string += str(i[1]) + ', ' #legger til ringerike sin netto-verdi

        # for hvert element i listen, iterer de andre listene og slå sammen til 1 CSV fil
        for x in hole_list:
            if(x[0] == i[0]): # Hvis ringerike-år er det samme som hole-år...
                resultat_string += str(x[1]) + ', ' # Legg til hole nettoverdi i CSV filen
                break

        for x in modum_list:
            if(x[0] == i[0]):
                resultat_string+= str(x[1]) + ', '
                break

        for x in jevnaker_list:
            if (x[0] == i[0]):
                resultat_string += str(x[1])
                break

        resultat_string+= '\n'

    with open('verdier.csv', 'w', encoding='UTF8') as f:
        skriver = csv.writer(f)
        f.write(resultat_string)


    # for col_label, col in df.items():
    #   print(col_label, col, sep='\n')
    #  if (col_label == 'år'):
    #     print()


    # print(newdf.describe)
    return df


def main():
    url = "https://data.ssb.no/api/v0/no/table/09588/"
    sporring_77 = {
        "query": [
            {
                "code": "Region",
                "selection": {
                    "filter": "agg_single:KommGjeldende",
                    "values": [
                        "0532",
                        "0605",
                        "0612",
                        "0623"
                    ]
                }
            },
            {
                "code": "ContentsCode",
                "selection": {
                    "filter": "item",
                    "values": [
                        "Netto"
                    ]
                }
            },
            {
                "code": "Tid",
                "selection": {
                    "filter": "item",
                    "values": [
                        "2004",
                        "2005",
                        "2006",
                        "2007",
                        "2008",
                        "2009",
                        "2010",
                        "2011",
                        "2012",
                        "2013",
                        "2014",
                        "2015",
                        "2016",
                        "2017",
                        "2018",
                        "2019"
                    ]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }
    sporring_20 = {
        "query": [
            {
                "code": "Region",
                "selection": {
                    "filter": "agg_single:Komm2020",
                    "values": [
                        "3007",
                        "3038",
                        "3047",
                        "3053"
                    ]
                }
            },
            {
                "code": "ContentsCode",
                "selection": {
                    "filter": "item",
                    "values": [
                        "Netto"
                    ]
                }
            },
            {
                "code": "Tid",
                "selection": {
                    "filter": "item",
                    "values": [
                        "2020",
                        "2021"
                    ]
                }
            }
        ],
        "response": {
            "format": "json-stat2"
        }
    }

    x = requests.post(url, json=sporring_77)
    response_77 = json.loads(x.text)

    dataset = pyjstat.Dataset.read(x.text)
    df_77 = dataset.write('dataframe')

    x = requests.post(url, json=sporring_20)
    response_20 = json.loads(x.text)

    dataset = pyjstat.Dataset.read(x.text)
    df_20 = dataset.write('dataframe')

    df_kombinert = kombiner_sporringer(df_77, df_20)

    print(df_kombinert.describe)
    newdf = dataframe_to_linechart(df_kombinert)

main()




