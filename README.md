# LicencePlateScraper
Système automatique pour constituer un dataset de plaque d'immatriculation de voiture par scraping et crawling



## Explications & contenu de ce dépôt
- Partie 1 :  [**Constitution du dataset de la plaque d’immatriculation**](https://deeplylearning.fr/cours-pratiques-deep-learning/radar-automatique-partie-1-constitution-du-dataset-de-la-plaque-dimmatriculation/ "Constitution du dataset de la plaque d’immatriculation")  
    - Constitution du dataset
    - Scraping & crawling via Scrapy



## Explications & contenu annexes
- Partie 2 : [**Détection & localisation de la plaque d’immatriculation**](https://deeplylearning.fr/cours-pratiques-deep-learning/radar-automatique-partie-2-detection-localisation-de-la-plaque-dimmatriculation/ "Détection & localisation de la plaque d’immatriculation")  
    - Premier réseau de neurones
    - Algorithme de détection & localisation d'objets

- Partie 3 : [**Reconnaissance optique des caractères de la plaque d’immatriculation**](https://deeplylearning.fr/cours-pratiques-deep-learning/radar-automatique-partie-2-detection-localisation-de-la-plaque-dimmatriculation/ "Reconnaissance optique des caractères de la plaque d’immatriculation")  
    - Second réseau de neurones 
    - Algorithme de reconnaissance de caractères sur une image (OCR) 

- Dépôt Github : [**Partie 2 & 3**](https://deeplylearning.fr/cours-pratiques-deep-learning/radar-automatique-partie-2-detection-localisation-de-la-plaque-dimmatriculation/ "Partie 2 & 3") 



## Technos & Framework
| Type  | Nom |
| ------------- | ------------- |
| Langage  | Python 3.7.6  |
| Crawling & Scraping  | Scrapy  |




## Scripts
Les scripts suivant doit être utiliser dans le projet Scrapy :

`$ cd DataScrapper/spiders`



### Réglage vitesse des spiders
- **settings.py** permet d'avoir des accès parralèles plus ou moins nombreux, et donc de gérer la vitesse de nos spiders pour récuperer les donneés.

Les plus importans : 
| Type  | Nom |
| ------------- | ------------- |
| BOT_NAME  | Nom de votre bot  |
| USER_AGENT  | Nom de votre agent  |
| CONCURRENT_REQUESTS  | Maximum de requêtes parallèles  |
| AUTOTHROTTLE_ENABLED  | Laisse à Scrapy le réglages du nombre de requêtes pour éviter de surcharger le site  |
| AUTOTHROTTLE_TARGET_CONCURRENCY  | Nombre de requête moyenne sur chaqun de nos serveur  |

Il est mieux vu de mettre sa vrai identité lorsque on utilise de telles solutions pour récuperer des données, d'un point de vue juridique.


### Scraping
Ce premier spider permet de récuperer des photos de voitures, avec leur 
Dans le dossier **/DataScrapper** :

Voici les données que l'on récupère :
| Type  | Nom |
| ------------- | ------------- |
| heure  | Heure de l'ajout de la voiture sur le site distant  |
| date | Date de l'ajout de la voiture sur le site distant  |
| voitureMarque | Marque de la voiture  |
| voitureModele | Modèle de la voiture  |
| imgGlobalName | Nom de l'image sauvegardé de la voiture globale  |
| imgPlaqueName | Nom de l'image sauvegardé de lla plaque d'immatriculation  |
| plateNumber | Numéro de la plaque  |

Pensez à régler dans les attributs de la classe du spider :
- csvFilepath : fichier CSV contenant l'ensemble des attributs précédents
- DIRECTORY_IMG_PLATE : dossier de destination pour les images des plaques
- DIRECTORY_IMG_GLOBAL : dossier de destination pour les images des voitures
- page & maxPage : c'est une fourchette d'interval à donner à notre spider concernant les pages à visiter

**Important :**
J'impose une version specifique à mon agent afin de le faire passer pour un vrai utilisateur et non un bot, permettant de bypass les erreurs 403 FORBIDDEN.

#### Lancement du spider
`$ scrapy runspider scraper.py`



### Génération de plaque via API
Le site contient une api pour générer à la volée des plaques d'immatriculations. Pour ce projet, je me suis concentré pour créer seulement des plaques françaises.

Voici les données que l'on récupère dans notre fichier .csv, en plus de l'image .jpg de la plaque :
| Type  | Nom |
| ------------- | ------------- |
| imgPlaqueName  | Nom de mon image de plaque dans mon dossier  |
| plateNumber  | Numéro de la plaque  |
| nation  | Nationalité de la plaque  |
| departement  | Département de la plaque  |

Pensez à régler dans les attributs de la classe du spider :
- csvFilepath : fichier CSV contenant l'ensemble des attributs précédents
- destinationFolderPlateGenerated : dossier de destination pour les images des plaques
- MAX_ITERATION : nombre de plaque généré souhaité

#### Lancement du spider
`$ scrapy runspider plateGenerator.py`



## Remerciement
Le tutoriel n'aurait pu être possible sans le site Platesmania. Pour préserver la stabilité du site, ne crawler/scraper qu'avec un nombre de requête et parallèles raisonable.