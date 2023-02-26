# -> Change Pages Dynamically
# -> Get All Categories Links Dynamically

import requests


class storeCategoryCrawl:
    def __init__(self, url):
        self.url = url

    def extract(self):
        request = requests.get(
            self.url)

        self.data = request.json()["data"]
        self.status = request.json()["status"]

        return [self.data, self.status]

    def extractProducts(self):
        self.extract()

        productsUrls = []
        if (self.status == 200):
            for i in self.data["products"]:
                productsUrls.append(
                    {"id": i["id"], "title": i["title_fa"], "url": i["url"]["uri"]})

        self.productsUrls = productsUrls
        return productsUrls

    def extractProductDetails(self):
        self.extractProducts()

        if (len(self.productsUrls) > 0):
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


storeCategoryData = storeCategoryCrawl(
    'CATEGORY_LINK')

storeCategoryData.extractProductDetails()
