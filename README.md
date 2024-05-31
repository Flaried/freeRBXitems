Roblox Bot that buys every free item thats in catalog thats sold by the Offical Roblox account.

## Files
Roblox.py - Manages Roblox APIs

HandleRequest.py - Manages status codes and other errors

main.py - main program to buy the Items

## [PROCESS THE BOT TAKES]
1. Get userinventory so you dont try to POST the API to buy something you already own.
2. Scans the catalog for new free items. (OPTIONAL IN SETTINGS.CFG)
3. Adds every item found in the catalog API to Ids.txt.
4. The bot will go through Ids.txt and try to buy them all for 0 robux.


