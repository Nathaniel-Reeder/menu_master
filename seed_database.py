'''Script to seed the database'''

import os
import json
from random import choice, randint

import model
import server

os.system('dropdb menu_master')
os.system('createdb menu_master')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/recipes.json') as f:
    recipe_data = json.loads(f.read())
    
    for recipe in recipe_data:
        name_to_add = recipe['name']
        instruction_to_add = recipe['instructions']
        ingredients_to_add = recipe['ingredients']