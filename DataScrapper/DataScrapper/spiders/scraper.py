# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import pandas as pd
import urllib.request


# BYPASS du 403 forbidden :)
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.69 Safari/537.36"


class ScrapperSpider(scrapy.Spider):
    baseUrl = "http://platesmania.com/fr/gallery-"
    name = 'licenceScraper'
    allowed_domains = ['platesmania.com']
    start_urls = [
        "http://platesmania.com/fr/gallery-0"
    ]
    csvFilepath = 'D:\\DeeplyLearning\\Github\\LicencePlateScaper\\data\\text\\data.csv'

    page = 0
    maxPage = 5

    DIRECTORY_IMG_PLATE = 'D:\\DeeplyLearning\\Github\\LicencePlateScaper\\data\\image\\plate\\'
    DIRECTORY_IMG_GLOBAL = 'D:\\DeeplyLearning\\Github\\LicencePlateScaper\\data\\image\\car\\'

    lastUpdatedDate = ''
    urllib.urlopener = AppURLopener()

    def parse(self, response):

        csvData = pd.read_csv(self.csvFilepath)

        imgContenerAll = response.xpath('.//div[@class="panel panel-grey"]')

        for imgContener in imgContenerAll:
            panelBody = imgContener.xpath('div[@class="panel-body"]')

            carType = panelBody.xpath('.//h4/a/text()').get().split(' ')
            dateType = panelBody.xpath('.//p/small/text()').get().split(' ')

            voitureMarque = carType[0]
            voitureModele = carType[1]

            # car l'arg 0 est un espace
            dateAjout = dateType[1]
            heureAjout = dateType[2]

            subContenerImgGlobal = imgContener.xpath('.//div[@class="row"]')[1]
            subContenerImgPlate = imgContener.xpath('.//div[@class="row"]')[2]

            urlImgGlobal = subContenerImgGlobal.xpath('.//a//img/@src').get()
            urlImgPlate = subContenerImgPlate.xpath('.//a//img/@src').get()
            plateNumber = subContenerImgPlate.xpath('.//a//img/@alt').get()

            imgGlobalName = urlImgGlobal.split('/')[-1]
            imgPlateName = urlImgPlate.split('/')[-1]

            destinationFolderImgPlate = self.DIRECTORY_IMG_PLATE + imgPlateName
            destinationFolderImgGlobal = self.DIRECTORY_IMG_GLOBAL + imgGlobalName



            row = {
                'date': dateAjout,
                'heure': heureAjout,
                'voitureMarque': voitureMarque,
                'voitureModele': voitureModele,
                'imgGlobalName': imgGlobalName,
                'imgPlaqueName': imgPlateName,
                'plateNumber': plateNumber
            }

            isUnique = csvData[
                (csvData['date'] == dateAjout) &
                (csvData['heure'] == heureAjout) &
                (csvData['voitureMarque'] == voitureMarque) &
                (csvData['voitureModele'] == voitureModele) &
                (csvData['imgGlobalName'] == imgGlobalName) &
                (csvData['imgPlaqueName'] == imgPlateName) &
                (csvData['plateNumber'] == plateNumber)

            ]

            if isUnique.empty:
                urllib.urlopener.retrieve(urlImgGlobal, destinationFolderImgGlobal)
                urllib.urlopener.retrieve(urlImgPlate, destinationFolderImgPlate)

                csvData = csvData.append(row, ignore_index=True)




        csvData.to_csv(self.csvFilepath, encoding='utf-8', index=False)

        self.page += 1
        if self.page < self.maxPage:
            yield Request(url=self.baseUrl+str(self.page), callback=self.parse)