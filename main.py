# -> Get Categories Links Dynamically

import requests


class storeCategoryCrawl:
    def __init__(self, url):
        self.url = url

    def checkCategory(self):
        request = requests.get(
            self.url)

        if (request.json()["status"] != 200):
            self.status = 400

            return "Category Error"
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
        for i in range(commentsPagesCount):
            request = requests.get(
                "https://api.digikala.com/v1/product/" + str(productId) + "/comments/?page=" + str(commentsPagesCount))

            if (request.json()["status"] != 200):
                return "Comments Error"
            else:
                if "comments" in request.json()["data"]:
                    for j in request.json()["data"]["comments"]:
                        print(j["body"])

    def getDetails(self, productId):
        request = requests.get(
            "https://api.digikala.com/v1/product/" + str(productId) + "/")

        print(request.json()["data"]["product"]
              ["review"]["description"])

    def extractProductDetails(self):
        self.extractProducts()

        if (len(self.productsUrls) > 0 and self.status == 200):

            for i in self.productsUrls:
                print(str(i["id"]))

                # -> Product Details

                # self.getDetails(i["id"])

                # -> Comments

                self.getComments(i["id"], 1)


for i in range(1):
    storeCategoryData = storeCategoryCrawl(
        'CATEGORY_LINK' + str(i))

    storeCategoryData.extractProductDetails()
