import requests, HandleRequests, time

class RobloxAPIs():
    def __init__(self, Cookie=None, Proxies=False) -> None:
        self.Session = requests.Session() if Cookie else None
        if Cookie:
            self.Session.cookies[".ROBLOSECURITY"] = Cookie

        self.Account = HandleRequests.RequestsHandler(self.Session, Proxies)

        
    def PurchaseItem(self, AssetID:int, expectedCurrency:int, expectedPrice:int, SellerID:int) -> requests.Response:
        """
        Got server error retrying 5 times.. {"errors":[{"code":0,"message":"InternalServerError"}]} Payload: {'expectedCurrency': 1, 'expectedPrice': 0, 'expectedSellerId': 1}
        Couldnt buy {'id': 945, 'itemType': 'Bundle', 'bundleType': 4, 'name': 'Dylan Default', 'description': 'A look that never goes out of style.', 'productId': 1303995044, 'itemStatus': [], 'itemRestrictions': ['Live'], 'creatorHasVerifiedBadge': True, 'creatorType': 'User', 
        'creatorTargetId': 1, 'creatorName': 'Roblox', 'price': 0, 'priceStatus': 'Free', 'purchaseCount': 0, 'favoriteCount': 241643, 'offSaleDeadline': None, 'saleLocationType': 'NotApplicable'}

        Bundles might need another API
        
        """
        url = f"https://economy.roblox.com/v1/purchases/products/{int(AssetID)}"
        data = {
            'expectedCurrency': int(expectedCurrency),
            'expectedPrice': int(expectedPrice),
            'expectedSellerId': int(SellerID),
        }
        return self.Account.requestAPI(url, "post", data)





    def getUserInventory(self, userID):
        """
        Doesnt Need cookie unless private inventory (scraping API)
        Of course roblox gotta fucking have asset type sorting for inventory API
        
        https://roblox.fandom.com/wiki/Asset
        https://www.roblox.com/users/inventory/list-json?assetTypeId=24&cursor=&itemsPerPage=100&pageNumber=1&userId=3054007
        """
        UsefulAssetTypes = [2, 8,11, 12, 17, 18, 24, 32, 41, 42, 43, 44, 45, 46, 47, 61, 64, 65, 66, 67, 68, 69, 70, 71, 72]
        
        Inventory = []
        for AssetType in UsefulAssetTypes:
            nextPage = ""
            while nextPage is not None:
                url = f"https://www.roblox.com/users/inventory/list-json?assetTypeId={AssetType}&cursor=&{nextPage}itemsPerPage=100&pageNumber=1&userId={userID}"
                Response = self.Account.requestAPI(url)
                try:
                    nextPage = Response.json()['Data']['nextPageCursor']

                    for ItemData in Response.json()['Data']['Items']:
                        Inventory.append(ItemData['Item']['AssetId'])
                except:
                    print("Got error:", Response.json())
                    time.sleep(30)
        Inventory.extend(self.getBundleInventory(userID))
        print(len(Inventory), "Items in inventory")
        return Inventory

    def getBundleInventory(self, userID):
        UsefulBundleTypes = [1, 2, 3, 4]
        
        BundleInv = []
        for BundleType in UsefulBundleTypes:
            nextPage = ""
            while nextPage is not None:
                url = f"https://catalog.roblox.com/v1/users/{userID}/bundles/{BundleType}?cursor={nextPage}&limit=100&sortOrder=Desc"
                Response = self.Account.requestAPI(url)
                if Response is None:
                    print(BundleType)
                    nextPage = None
                    continue
                nextPage = Response.json()['nextPageCursor']

                for ItemData in Response.json()['data']:
                    BundleInv.append(ItemData['id'])

        return BundleInv
   
    def getUserId(self):
        login = self.Session.get("https://users.roblox.com/v1/users/authenticated")#, headers=headers)
        if login.status_code==200:
            userid = login.json()['id']
            return userid
        else:
            print("Invalid Cookie")
            return None


    def scanRobloxCatalog(self):
        """
        This function retrieves all item IDs from the Roblox catalog.

        The search APIs return a maximum of 1000 hats, so we need to get all the
        categories and subcategories to bypass this limit.

        Note: No cookies are needed for this operation.
        """

        Categories = {
            11: [54, 21, 22, 23, 24, 25, 26, 5],
            4: [66, 20, 15, 10],
            12: [27, 38, 39],
            3: [58, 59, 62, 61, 60, 63, 65, 64, 56, 55, 57],
            17: [""]
        }

        listOfIds = []
        
        # Loop through each category and its subcategories
        for category, subcategories in Categories.items():
            for subcategory in subcategories:
                nextPage = ""
                
                while nextPage is not None:
                    print("Getting Page for category: ", category, "subcategory:", (subcategory))
                    #url = f"https://catalog.roblox.com/v1/search/items?category={category}&subcategory={subcategory}&limit=120&maxPrice=0&cursor={nextPage}&salesTypeFilter=1"
                    url = f"https://catalog.roblox.com/v1/search/items/details?Category={category}&MaxPrice=0&Subcategory={subcategory}&cursor={nextPage}&CreatorTargetId=1&SortType=0&SortAggregation=5&Limit=30"
                    Response = self.Account.requestAPI(url)
                    data = Response.json()
                    
                    nextPage = data['nextPageCursor']

                    
                    for item in data['data']:
                        if item not in listOfIds:
                            listOfIds.append(item)
                    
                    print("[DoggoBuyer] Appending to item to list",len(listOfIds))
        
        # Write the collected IDs to a file
        with open("Ids.txt", "w") as File:
            File.write(str(listOfIds))
        
        return listOfIds
