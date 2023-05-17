'''Script to seed the database'''

import os
import json

import model
import server

os.system('dropdb menu_master')
os.system('createdb menu_master')

model.connect_to_db(server.app)
model.db.create_all()

#Create and add a test user to own our test recipes
user = model.User.create('test', 'test@test.test', 'test')
model.db.session.add(user)

with open('data/recipes.json') as f:
    #Get the data from the JSON file
    recipe_data = json.loads(f.read())
    recipes_in_db = []
    
    for recipe in recipe_data:
        name_to_add = recipe['name']
        # print(name_to_add)
        instruction_to_add = recipe['instructions']
        
        #Create the Recipe entry to be referenced later
        new_recipe = model.Recipe.create(name_to_add, instruction_to_add, user)
        model.db.session.add(new_recipe)
        
        #Get the list of Ingredients
        ingredients_to_add = recipe['ingredients']
        # print(ingredients_to_add)
        
        #Iterate over the ingredients and add them to the Ingredient table
        for ingredient in ingredients_to_add:
            # print(ingredient["name"])
            # print(ingredient["qty"])
            existing_ingredient = model.Ingredient.query.filter_by(name=ingredient['name']).first()
            qty = ingredient["qty"]
            if not existing_ingredient:
                #If the ingredient does not exist, create an entry for it.
                ingredient_new = model.Ingredient.create(ingredient['name'])
                model.db.session.add(ingredient_new)
                
                #Link the ingredient to its recipe and get the quantity
                recipe_ingredient = model.RecipeIngredient.create(new_recipe, ingredient_new, qty)
                model.db.session.add(recipe_ingredient)
                model.db.session.commit()
            else:
                #If the ingredient already exists, link it to the recipe.
                recipe_ingredient = model.RecipeIngredient.create(new_recipe, existing_ingredient, qty)
                model.db.session.add(recipe_ingredient)
                model.db.session.commit()

#Create an on_hand inventory for our user
with open('data/on_hand.json') as f:
    on_hand_data = json.loads(f.read())
    
    for ingredient in on_hand_data:
        ingredient_obj = model.Ingredient.query.filter_by(name=ingredient['name']).first()
        qty = ingredient['qty']
        new_on_hand = model.OnHand.create(user, ingredient_obj, qty)
        model.db.session.add(new_on_hand)
        model.db.session.commit()
        
#Create an example menu for our user
menu = model.Menu.create('Example', user)
model.db.session.add(menu)

#Create days for the menu
for n in range(7):
    #Get a day of the week number using the range function
    new_day = model.Day.create(n+1, menu)
    model.db.session.add(new_day)
    #Get a recipe out of the database and add it to the day.
    recipe = model.Recipe.query.filter_by(id=n).first()
    new_day_recipe = model.DaysRecipe.create(new_day, recipe)

model.db.session.commit()