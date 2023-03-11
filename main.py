# Fix Redundant Fetching

import requests
from time import sleep
import json


class storeCategoryCrawl:
    def __init__(self, url):
        self.url = url

    def checkCategory(self):
        request = requests.get(
            self.url)

        if (request.json()["status"] != 200):
            self.status = 400
            print("Category Error: " + request.json()["status"])
        else:
            self.data = request.json()["data"]
            self.status = 200

            return [self.data, self.status]

    def extractProducts(self):
        self.checkCategory()

        productsUrls = []
        if (self.status == 200):
            for i in self.data["products"]:
                productsUrls.append(
                    {"id": i["id"], "title": i["title_fa"], "url": i["url"]["uri"]})

        self.productsUrls = productsUrls

        return productsUrls

    def getComments(self, productId, commentsPagesCount):
        allComments = []
        for i in range(commentsPagesCount):
            request = requests.get(
                "https://api.digikala.com/v1/product/" + str(productId) + "/comments/?page=" + str(commentsPagesCount))

            if (request.json()["status"] != 200):
                print("Comments: " + request.json()["status"])
            else:
                allComments.append(request.json()["data"])

        return allComments

    def getDetails(self, productId):
        request = requests.get(
            "https://api.digikala.com/v1/product/" + str(productId) + "/")

        if (request.json()["status"] != 200):
            print("Product: " + request.json()["status"])
        else:
            return request.json()["data"]

    def extractProductDetails(self):
        self.extractProducts()

        if (len(self.productsUrls) > 0 and self.status == 200):

            for i in self.productsUrls:
                sleep(3)

                # -> Product Details
                productDetails = self.getDetails(i["id"])

                # -> Comments
                productComments = self.getComments(i["id"], 1)

                productDetails["comments"] = productComments

                with open(str(i["id"]) + ".json", "w", encoding='utf-8') as productFile:
                    json.dump(productDetails, productFile,
                              ensure_ascii=False, indent=4)

                print(str(i["id"]) + " - Completed")


allCategoriesLinks = ["CATEGORY_LINK"]

for i in allCategoriesLinks:
    for j in range(10):
        storeCategoryData = storeCategoryCrawl(
            i + str(j))

        storeCategoryData.extractProductDetails()
