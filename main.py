from HandleRequests import RequestsHandler
from configparser import ConfigParser
import Roblox, time


def main():
    RobloxAcc = Roblox.RobloxAPIs(Cookie, Proxies=False)
    UserdID = RobloxAcc.getUserId()
    Inventory = RobloxAcc.getUserInventory(UserdID)
    with open("Ids.txt", "r") as File:
        data = File.read()
    for Item in eval(data):
        ItemID = Item["id"]
        ItemName = Item["name"]
        productId = Item["productId"]
        SellerID = Item["creatorTargetId"]
        ExpectedPrice = 0
        if ItemID not in Inventory:
            retries = 0
            max_retries = 10

            while retries < max_retries:
                Response = RobloxAcc.PurchaseItem(int(productId), 1, ExpectedPrice, int(SellerID))
                if Response is not None:
                    print("Bought", ItemName)
                    break
                else:
                    print("Couldnt buy", ItemName, "Trying again")
                    retries += 1
                    time.sleep(5)
        else:
            print("Already Own", ItemName)

if __name__ == "__main__":
    file = 'Settings.cfg'
    config = ConfigParser()
    config.read(file)
    Cookie = config['Authentication']['.ROBLOSECURITY Cookie']

    if config['Items']['RefreshIds'].lower() == 'true':
        Scraper = Roblox.RobloxAPIs(Proxies=True)
        Scraper.scanRobloxCatalog()

    main()
