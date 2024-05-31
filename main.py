from HandleRequests import RequestsHandler
from configparser import ConfigParser
import Roblox, time
print("Made by Flaried")

def main():
    RobloxAcc = Roblox.RobloxAPIs(Cookie, Proxies=False) 
    UserdID = RobloxAcc.getUserId()
    Inventory = RobloxAcc.getUserInventory(UserdID)
    with open("Ids.txt", "r") as File:
        data = File.read()
    for count, Item in enumerate(eval(data)):
        ItemID = Item["id"]
        ItemName = Item["name"]
        productId = Item["productId"]
        SellerID = Item["creatorTargetId"]
        ExpectedPrice = 0
        count = count +1
        # We have streak and sleep system to not flood the purchase API (Its a slow API that will error 500)
        streak = 0

        if ItemID not in Inventory:
            retries = 0
            max_retries = 5
            while retries < max_retries:
                Response = RobloxAcc.PurchaseItem(int(productId), 1, ExpectedPrice, int(SellerID))
                streak+=1
                
                if Response is not None:
                    print(f"[DoggoBuyer ({count} of {len(eval(data))})] Bought", ItemName)
                    time.sleep(float(Timesleep)*streak)  
                    if streak >= 25:
                        streak = 0

                    break
                else:
                    print(f"[DoggoBuyer ({count} of {len(eval(data))})] Couldnt buy", ItemName, "\nTrying again in 55 secs")
                    retries += 1
                    time.sleep(55)
        else:
            print(f"[DoggoBuyer ({count} of {len(eval(data))})] Already Own", ItemName)

if __name__ == "__main__":
    file = 'Settings.cfg'
    config = ConfigParser()
    config.read(file)
    Cookie = config['Authentication']['.ROBLOSECURITY Cookie']
    Timesleep= config['Items']['PurchaseTimeCooldown']
    if config['Items']['RefreshIds'].lower() == 'true':
        Scraper = Roblox.RobloxAPIs(Proxies=True)
        Scraper.scanRobloxCatalog()

    main()
    print("Done buying Items.")
