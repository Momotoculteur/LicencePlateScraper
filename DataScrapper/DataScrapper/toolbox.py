import pandas as pd

'''
SCRIPT
Permet de récup les données bruts issu de notre bot
Et de les séparer en deux data distinctes
D'un côté les voitures, et l'autre les plaques seulement
Et de supprimer les espaces et tiret dans les numéros de plaques
'''


allData = pd.read_csv('D:\\DeeplyLearning\\Github\\LicencePlateRecognizer\\data\\text\\data.csv')
allData['plateNumber'] = allData['plateNumber'].str.replace('-* *', '')

plateOnly = allData.copy()
globalOnly = allData.copy()


plateOnly = plateOnly.drop(columns=['voitureModele', 'voitureMarque', 'imgGlobalName', 'date', 'heure'])
globalOnly = globalOnly.drop(columns=['imgPlaqueName', 'date', 'heure'])

plateOnly.to_csv('D:\\DeeplyLearning\\Github\\LicencePlateRecognizer\\data\\text\\plate.csv', encoding='utf-8', index=False)
globalOnly.to_csv('D:\\DeeplyLearning\\Github\\LicencePlateRecognizer\\data\\text\\car.csv', encoding='utf-8', index=False)

print(globalOnly)