import csv
import pandas as pd
import requests
import json
from pyjstat import pyjstat

"""
def kombiner_sporringer(df_1, df_2):  # Formaterer og kombinerer 2 dataframes
    print(df_1.describe)

    # Først rename alle ringerike(1977) til bare Ringerike etc
    for row_label, row in df_1.iterrows():
        if row['region'] == 'Ringerike (1977-2019)':
            df_1.loc[row_label, 'region'] = 'Ringerike'
        if row['region'] == 'Jevnaker (-2019)':
            df_1.loc[row_label, 'region'] = 'Jevnaker'
        if row['region'] == 'Hole (1977-2019)':
            df_1.loc[row_label, 'region'] = 'Hole'
        if row['region'] == 'Modum (-2019)':
            df_1.loc[row_label, 'region'] = 'Modum'
        #Legg til flere regioner her etter behov

    dataframes = [df_1, df_2]
    sammensatt_frames = pd.concat(dataframes)  # Concat dataframes til 1 dataframe

    return sammensatt_frames # Returner den samensatte dataframen som inneholder 2004-2020
"""


def kombiner_sporringer(df_1, df_2):  # Tar 2 dataframes, kombinerer 1 kombinert dataframe
    # Agnostisk ovenfor region, vil sammenslå enhver tabell fra 2004 - 2020

    print(df_1.describe)

    # Først rename alle ringerike(1977) til bare Ringerike etc
    for row_label, row in df_1.iterrows():  # For alle rader i dataframen
        if "(1977-2019)" in str(row['region']):  # Hvis raden er fra -2019 dataframen...
            df_1.loc[row_label, 'region'] = str(
                row['region'].replace(' (1977-2019)', ''))  # Fjern -2019 identifikatoren
        if "(-2019)" in str(row['region']):
            df_1.loc[row_label, 'region'] = str(row['region'].replace(' (-2019)', ''))

    dataframes = [df_1, df_2]

    sammensatt_frames = pd.concat(dataframes)  # Concat dataframes til 1 dataframe

    return sammensatt_frames  # Returner den samensatte dataframen som inneholder 2004-2020


def dataframe_to_linechart(df, r_list):  # Formaterer data til highchart formatet(år, Ringerike, Hole, Modum, Jevnaker)
    dict = {}

    for x in r_list:
        dict[x] = []

    for row_label, row in df.iterrows():
        # print(row['år'])
        for x in r_list:
            if row['region'] == x:
                dict[row['region']] += [row['år'], row['value'], row['region']]

    # df = df.pivot(index='år',columns='region')
    # df.drop('statistikkvariabel', axis=1)
    # df = df.pivot_table(df, values='value', index='år', columns='region')

    resultat_string = "År "
    for x in range(0, len(r_list)):
        if x == len(r_list) - 1:
            resultat_string += str(r_list[x]) + '\n'
        else:
            resultat_string += str(r_list[x]) + ", "

    for key in dict.keys():
        for element in dict[key]:
            print(element)

    # print(resultat_string)
    for key, value in dict.items():
        # print("Key: " , key)

        for x in dict[key]:
            # print(x)

            for z in dict[key]:
                s = 1
                # print("x: " , x, "Z; ", z)
            for i in range(0, len(value)):
                s = 1

            # print(dict[key][0])
            if x == value[0]:
                s = 1
                # resultat_string += str(value[1]) + ", "

    print(resultat_string)


def dataframe_til_linechart_01(df,
                               r_list):  # Formaterer data til highchart formatet(år, Ringerike, Hole, Modum, Jevnaker)
    # Denne funksjonen
    # Lag tomme lister med nettinnflytning som data, trenger flere lister ved større spørringer
    liste_1 = []
    liste_2 = []
    liste_3 = []
    liste_4 = []

    #  Leser gjennom hvor mange regioner som skal inkluderes, endrer csv fil dynamisk
    # Resultat_string bygger opp CSV filen som highcharts skal lese av
    resultat_string = "År, "
    for x in range(0, len(r_list)):
        if x == len(r_list) - 1:
            resultat_string += str(r_list[x]) + '\n'
        else:
            resultat_string += str(r_list[x]) + ", "

    # Iterer over dataframe
    for row_label, row in df.iterrows():
        if row['region'] == r_list[0]:  # Hvis regionen er ringerike...
            # Legg til nettofinnflytnings verdien i listen
            liste_1.append([row['år'], row['value'], row['region']])
        if row['region'] == r_list[1]:
            liste_2.append([row['år'], row['value'], row['region']])
        if row['region'] == r_list[2]:
            liste_3.append([row['år'], row['value'], row['region']])
        if row['region'] == r_list[3]:
            liste_4.append([row['år'], row['value'], row['region']])

    # Iterer over alle elementer i første liste
    for i in liste_1:
        resultat_string += i[0] + ', '  # Legger til året i csv filen
        resultat_string += str(i[1]) + ', '  # legger til ringerike sin netto-verdi

        # for hvert element i listen, iterer de andre listene og slå sammen til 1 CSV fil
        for x in liste_2:
            if (x[0] == i[0]):  # Hvis ringerike-år er det samme som hole-år...
                resultat_string += str(x[1]) + ', '  # Legg til hole nettoverdi i CSV filen
                break

        for x in liste_3:
            if (x[0] == i[0]):
                resultat_string += str(x[1]) + ', '
                break

        for x in liste_4:
            if (x[0] == i[0]):
                resultat_string += str(x[1])
                break

        resultat_string += '\n'

    return resultat_string


def skriv_til_fil(filnavn, stringen):  # Skriver en gitt string til CSV, filnavn som parameter
    with open(filnavn, 'w', encoding='UTF8') as f:
        f.write(stringen)


def lag_dataframes(sporring, url):  # returnerer en dataframe av en gitt spørring
    response = requests.post(url, json=sporring)
    dataset = pyjstat.Dataset.read(response.text)
    df = dataset.write('dataframe')
    return df


def main():
    #Spørringer og url
    url = "https://data.ssb.no/api/v0/no/table/09588/"
    sporring_netto_77 = {
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
    sporring_netto_20 = {
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
    sporring_inn_ut_77 = {
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
                        "Innflytting",
                        "Utflytting"
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
    sporring_inn_ut_20 = {
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
                        "Innflytting",
                        "Utflytting"
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

    #Lag dataframes ut av spørringene
    df_netto_77 = lag_dataframes(sporring_netto_77, url)
    df_netto_20 = lag_dataframes(sporring_netto_20, url)
    df_inn_ut_77 = lag_dataframes(sporring_inn_ut_77, url)
    df_inn_ut_20 = lag_dataframes(sporring_inn_ut_20, url)

    #Kombiner og formater netto dataframene
    df_kombinert = kombiner_sporringer(df_netto_77, df_netto_20)

    #Kombiner og formater inn/ut dataframene
    df_inn_ut_kombinert = kombiner_sporringer(df_inn_ut_77, df_inn_ut_20)

    print(df_kombinert.describe)
    print(df_inn_ut_kombinert.describe)

    #les dataframe og omformater til riktig highcharts format
    csv_string = dataframe_til_linechart_01(df_kombinert, ['Ringerike', 'Hole', 'Modum', 'Jevnaker'])

    #Lagre nettoinnflytting resultatet i en CSV fil som leses av Highcharts
    skriv_til_fil('verdier.csv', csv_string)

    #lagre Inn og utflytting data i en CSV fil som leses av Highcharts
    df_inn_ut_kombinert.to_csv('inn_ut.csv', index=False)

    print("========================================= \n")
    print("Programmet ble utført og verdier.csv har blitt lagd")
    print("Du kan nå åpne Highcharts_resultat.html for å se resultatet")


main()
