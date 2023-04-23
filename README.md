# T6WeaponEdit
T6WeaponEdit: It is a program created to facilitate the creation of weapons for black ops2 zm.

it gives the possibility of you can put the name for purchases, price, purchase limit per round, round that will be unlocked, kills needed, kills hs needed, to can happen the purchase.

you can also create your own gsc script and ultilize as you wish, the app will give you a json file, you can do what you want with this file.

how to use it, you have to extract the gsc file and the program in your plutonium zm folder, when you use the app and create your weapon, remember to always export the json file so the script can find it, the rest is just start your server and the code will already be working. 

**obs:** this gsc script, will only work if you have the [t6-gsc-utils plugin](https://github.com/fedddddd/t6-gsc-utils).

**console commands:**
- wp_list on: ```is for the in case you have not exported the file but have already started your server, with this command the script will load the file in real time and will be working.```

* wp_list up: ```you can use this if you have deleted some weapon or modified, and exported the json, this command serves to update the list of weapons with their properties in real time in the game if your server is started.```

+ wp_list list: ```this command will show you on the console a list with the names of the weapons that will be in the current map.```

**commands in game:**
**.buy:** ```this command is for you to buy your weapon. to buy it you just have to type in game chat >>> ".buy m1911" and your weapon will be bought if you meet what is needed to buy it.```

**.list:** ```will show you the list of weapons and their prices.```
