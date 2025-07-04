import json

value = 1
value2 = 2

data = {
    "name": "Bob",
    "value": value,
    "value2": value2
}

data2 = {
    "name": "alice",
    "value": value,
    "value2": value2
}

with open('Python_Game_Files/Data/SavedAttributes.json', 'w') as file:
    json.dump(data, file, indent=4)

with open('Python_Game_Files/Data/SavedAttributes.json', 'r') as file:
    fileData = json.load(file)

print(fileData)