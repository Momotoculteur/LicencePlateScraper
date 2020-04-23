import scrapy
from scrapy import FormRequest
from scrapy.http import Request
import pandas as pd
import urllib.request
from scrapy import signals
from pydispatch import dispatcher
from random import choice
from string import ascii_uppercase
from random import randint
from tqdm import tqdm
import random

# BYPASS du 403 forbidden :)
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"


class PlateGenerator(scrapy.Spider):
    name = 'plateGenerator'
    allowed_domains = ['platesmania.com']
    start_urls = [
        "http://platesmania.com/fr/informer"
    ]
    destinationFolderPlateGenerated = 'D:\\DeeplyLearning\\Github\\LicencePlateScaper\\data\\image\\plateGenerated\\'
    csvFilepath = 'D:\\DeeplyLearning\\Github\\LicencePlateScaper\\data\\text\\plateGenerated.csv'
    GLOBAL_DATA = None
    pbar = None

    MAX_ITERATION = 3000



    def __init__(self):
        dispatcher.connect(self.end, signals.spider_closed)
        dispatcher.connect(self.start, signals.spider_opened)

    def start_requests(self):
        i = 0
        self.pbar = tqdm(total=self.MAX_ITERATION, initial=i)
        while i < self.MAX_ITERATION:
            url = "http://platesmania.com/fr/informer"

            imatPartOne = self.generateRandomChar(2)
            imatPartTwo = self.generateRandomNumber(3)
            imatPartThree = self.generateRandomChar(2)

            imatDepartementPart = self.generateDepartementNumber()

            globalPlateGenerated = imatPartOne + imatPartTwo + imatPartThree

            frmdata = {
                "ctype": "1",
                "b1": imatPartOne,
                "digit2": imatPartTwo,
                "b2": imatPartThree,
                "region1": imatDepartementPart,
                "fon": "1",
                "posted": "1"
            }
            data = {
                "plate": globalPlateGenerated,
                "departement": imatDepartementPart
            }
            yield FormRequest(url, callback=self.parse, formdata=frmdata, meta=data)
            i += 1



    def parse(self, response):
        self.pbar.update(1)
        urlPlateGenerated = response.xpath('.//div[@class="container content"]//div[@class="row blog-page"]//div[@class="col-md-9 col-xs-12"]//div[@class="row margin-bottom-20 bg-grey"]//div[1]//img//@src').get()

        imgPlateName = urlPlateGenerated.split('/')[-1]
        imgPlateName = imgPlateName.split('/')[-1]


        row = {
            'imgPlaqueName': imgPlateName,
            'plateNumber': response.meta['plate'],
            'nation': 'F',
            'departement': response.meta['departement']
        }

        isUnique = self.GLOBAL_DATA[
            (self.GLOBAL_DATA['imgPlaqueName'] == imgPlateName) &
            (self.GLOBAL_DATA['plateNumber'] == response.meta['plate']) &
            (self.GLOBAL_DATA['nation'] == 'F') &
            (self.GLOBAL_DATA['departement'] == response.meta['departement'])
        ]

        if isUnique.empty:
            destinationFolderPlateGeneratedFinal = self.destinationFolderPlateGenerated + imgPlateName
            self.GLOBAL_DATA = self.GLOBAL_DATA.append(row, ignore_index=True)
            urllib.urlopener.retrieve(urlPlateGenerated, destinationFolderPlateGeneratedFinal)


    def start(self, spider):
        self.GLOBAL_DATA = pd.read_csv(self.csvFilepath)

    def end(self, spider):
        self.GLOBAL_DATA.to_csv(self.csvFilepath, encoding='utf-8', index=False)
        print(self.GLOBAL_DATA)

    def generateRandomNumber(self, length):
        return ''.join(["{}".format(randint(0, 9)) for num in range(0, length)])

    def generateRandomChar(self, length):
        return ''.join(choice(ascii_uppercase) for i in range(length))

    def generateDepartementNumber(self):
        departement = [
            '01',
            '02',
            '03',
            '04',
            '05',
            '06',
            '07',
            '08',
            '09',
            '10',
            '11',
            '12',
            '13',
            '14',
            '15',
            '16',
            '17',
            '18',
            '19',
            '21',
            '22',
            '23',
            '24',
            '25',
            '26',
            '27',
            '28',
            '29',
            '2A',
            '2B',
            '30',
            '31',
            '32',
            '33',
            '34',
            '35',
            '36',
            '37',
            '38',
            '39',
            '40',
            '41',
            '42',
            '43',
            '44',
            '45',
            '46',
            '47',
            '48',
            '49',
            '50',
            '51',
            '52',
            '53',
            '54',
            '55',
            '56',
            '57',
            '58',
            '59',
            '60',
            '61',
            '62',
            '63',
            '64',
            '65',
            '66',
            '67',
            '68',
            '69',
            '70',
            '71',
            '72',
            '73',
            '74',
            '75',
            '76',
            '77',
            '78',
            '79',
            '80',
            '81',
            '82',
            '83',
            '84',
            '85',
            '86',
            '87',
            '88',
            '89',
            '90',
            '91',
            '92',
            '93',
            '94',
            '95',
            '971',
            '972',
            '973',
            '974',
            '976',
            '987',
        ]
        return random.choice(departement)