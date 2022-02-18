import json
import random
import os, os.path
import re
from cairosvg import svg2png

        
class NFTbuilder():
    def __init__(self) -> None:
        self.idx = 10 # Number of NFTs to generate
        # SVG template
        self.template = '''
            <svg width="256" height="256" viewBox="0 0 256 256" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <!-- bg -->
                <!-- chest -->
                <!-- head --> 
                <!-- eyes -->
                <!-- nose -->    
                <!-- beard -->
                <!-- mouth -->
                <!-- hair -->
            </svg>
        '''

        # Names, this will be randomly selected and added to a large json file.
        self.adjectives = ("skinny", "fat", "tall", "muscular", "virgin", "jacked", "stubborn", "simple", "smart", 
                    "tiny", "stupid", "mean", "hardcore", "drunk" , "chaotic", "lawful", "boring", "crazy", "obese", 
                    "hot", "cringy", "dirty", "filthy", "sad", "funny", "poor", "rich")
        self.name = ("Pete", "Bob", "Chad", "Fred", "Jeff", "Paul", "Steve", "Tom", "Brian", "Frank", "Jack",
                "Quinten", "Eugene", "Steven", "Dennis", "Seamus", "Ryan", "Henry", "Sam", "Tim", "Moe", "Aaron",
                "Gary", "Kyle", "Joe", "Peter", "Ivan", "Dale", "Richard", "Mortimer", "Jake", "Brad")
        
        self.cards = self.GetJson("carddata") # Get large NFT json file --> this will store NFT name and rarity
        self.ids, self.names = self.fetchdata() # Generate IDs and names

        for i in range(self.idx): # Generate all NFTs
            self.createImage() # create NFT

    def createImage(self):
        #bg = len([name for name in os.listdir(f"{os.getcwd()}\layers\bg") if os.path.isfile(name)])
        beard = random.randint(0, len(next(os.walk(f"{os.getcwd()}\\layers\\beard"))[2])-1) # For each layer of the NFT, select a random index from their respective folders
        chest = random.randint(0, len(next(os.walk(f"{os.getcwd()}\\layers\\chest"))[2])-1)
        eyes = random.randint(0, len(next(os.walk(f"{os.getcwd()}\\layers\\eyes"))[2])-1)
        hair = random.randint(0, len(next(os.walk(f"{os.getcwd()}\\layers\\hair"))[2])-1)
        head = random.randint(0, len(next(os.walk(f"{os.getcwd()}\\layers\\head"))[2])-1)
        mouth = random.randint(0, len(next(os.walk(f"{os.getcwd()}\\layers\\mouth"))[2])-1)
        nose = random.randint(0, len(next(os.walk(f"{os.getcwd()}\\layers\\nose"))[2])-1)

        
        id = f"{beard}.{chest}.{eyes}.{hair}.{head}.{mouth}.{nose}" # These indexes will make up the NFT id, that is separated by periods
        print(id) 

        if id in self.ids: # we check if this ID is already existing
            self.createImage() # the function will call again to generate a new ID
        else:
            
            self.developimg(id) # develop the image if the ID does not exist
            

    def developimg(self, id): # One of the main parameters is the ID of the NFT.
        name = self.getRandName() # Generate a name for this NFT
        arr = list(map(int, id.split("."))) # Extract the layer indexes from the ID
        sum_of_digits = sum(int(digit) for digit in arr) # Sum the layers: we will use this to calculate the rarity 
        rarity = self.getrarity(sum_of_digits) # get rarity from sum
        
        # Now add each layer item to the template.
        finaltemplate = self.template.replace('<!-- beard -->', self.getLayer(f'beard\\{arr[0]}.svg')) \
            .replace('<!-- chest -->', self.getLayer(f'chest\\{arr[1]}.svg')) \
                .replace('<!-- eyes -->', self.getLayer(f'eyes\\{arr[2]}.svg')) \
                    .replace('<!-- hair -->', self.getLayer(f'hair\\{arr[3]}.svg')) \
                        .replace('<!-- head -->', self.getLayer(f'head\\{arr[4]}.svg')) \
                            .replace('<!-- mouth -->', self.getLayer(f'mouth\\{arr[5]}.svg')) \
                                .replace('<!-- nose -->', self.getLayer(f'nose\\{arr[6]}.svg')) \
                                    .replace('<!-- bg -->', self.getLayer(f'bg\\{rarity}.svg')) 

        # Write card metadata to the central json file
        cardmeta = self.GetJson("template")
        cards = self.GetJson("carddata")
        cardmeta["faceID"] = id
        cardmeta["Name"] = name
        cardmeta["rarity"] = rarity

        cards["cards"].append(cardmeta) 

        # add this data to the array of names + ids
        self.ids.append(id)
        self.names.append(name)

        # save this data
        try:
            with open(f"{os.getcwd()}\json\carddata.json", "w") as data:
                json.dump(cards, data, indent=4, separators=(',',': '))
        except Exception as e:
            print(f"error {e}")
            return

        
        # convert SVG to PNG
        svg2png(bytestring=finaltemplate,write_to=f"{os.getcwd()}\output\{id}.png")
            
        
        
        

        




        



    def getrarity(self, sum):
        # 130 max total 
        # middle = 65 
        # using Normal distribution and Z-scores, we can gauge the rarity of the card
        st = 10 # Standard deviation. --> this was mostly trial and error
        z = (sum - 65)/st # Calcualte z score
        print(sum)

        # extreme low or high sums are considered very rare. Most cards land close to the median.
        if (abs(z) < 1.5):
            return "common"
        elif (abs(z) >= 1.5 and abs(z) < 2):
            return "uncommon"
        elif (abs(z) >= 2 and abs(z) < 3):
            return "rare"
        elif (abs(z) >= 3 and abs(z) < 3.5):
            return "epic"
        elif (abs(z) >= 3.5 and abs(z) < 4):
            return "legendary"
        elif (abs(z) > 4):
            return "mythic"




    def getLayer(self, name): 
        with open(f"{os.getcwd()}\\layers\\{name}", 'r') as file:
            data = file.read().replace('\n', '')
            #print(data)

            try:
                regex = r"<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"256\" height=\"256\" viewBox=\"0 0 256 256\">(.*?)</svg>" # very bad regex
                layer = re.findall(regex, data)[0]
                #print(layer)
                return layer
            except Exception as e:
                #print(f"empty {e}")
                return ''
                

 



    
    def fetchdata(self):
        ids = []
        names = []
        for item in self.cards["cards"]:
            ids.append(item["faceID"])
            names.append(item["Name"])

        return ids, names

        

    def GetJson(self, filename):
        try:
            with open(f"{os.getcwd()}\\json\\{filename}.json", encoding='utf8') as data:
                return json.load(data)
        except FileNotFoundError:
            try:
                with open(f"{os.getcwd()}/json/{filename}.json", encoding='utf8') as data:
                    return json.load(data)
            except:
                raise FileNotFoundError("JSON file wasn't found")    

    def getRandName(self):
        name = f"{random.choice(self.adjectives)} {random.choice(self.name)}"
        # Check if name is taken
        
        while name in self.names:
            name = f"{random.choice(self.adjectives)} {random.choice(self.name)}"
        return name


ntf = NFTbuilder()
