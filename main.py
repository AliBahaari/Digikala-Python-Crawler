# -> Change Comment Pages Dynamically

import requests


class storeCategoryCrawl:
    def __init__(self, url):
        self.url = url

    def checkCategory(self):
        request = requests.get(
            self.url)

        if (request.json()["status"] != 200):
            self.status = 400

            return "Error"
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

    def extractProductDetails(self):
        self.extractProducts()

        if (len(self.productsUrls) > 0 and self.status == 200):
            for i in self.productsUrls:
                print(str(i["id"]))

                # -> Product Details

                request = requests.get(
                    "https://api.digikala.com/v1/product/" + str(i["id"]) + "/")

                print(request.json()["data"]["product"]
                      ["review"]["description"])

                # -> Comments

                request = requests.get(
                    "https://api.digikala.com/v1/product/" + str(i["id"]) + "/comments/?page=1")

                if "comments" in request.json()["data"]:
                    for j in request.json()["data"]["comments"]:
                        print(j["body"])


for i in range(10):
    storeCategoryData = storeCategoryCrawl(
        'CATEGORY_LINK' + str(i))

    print(storeCategoryData.checkCategory())
