import os
from datetime import date
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from model import db, connect_to_db, User, OnHand, Ingredient, Menu, Day, DaysRecipe, Recipe, RecipeIngredient, GroceryIngredient, GroceryList
from werkzeug.security import check_password_hash
from forms import LoginForm, CreateUserForm, AddIngredientForm, CreateMenuForm, CreateRecipeForm, AddRecipeIngredientForm

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    '''View homepage'''
    
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Create a new user'''
    create_user_form = CreateUserForm()
    
    if create_user_form.validate_on_submit():
        if create_user_form.password.data != create_user_form.confirm_password.data:
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('register'))
        else:
            check_user = User.query.filter_by(username=create_user_form.username.data).first()
            check_email = User.query.filter_by(email=create_user_form.email.data).first()
            if check_email:
                flash("Sorry, a user with that email already exists.")
            elif check_user:
                flash("Sorry, a user with that username already exists.")
            else:
                new_user = User.create(create_user_form.username.data, create_user_form.email.data, create_user_form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash("New user created! Please Log In")
                return redirect(url_for('login'))
    
    return render_template('register.html', create_user_form=create_user_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user:
            if check_password_hash(user.password, login_form.password.data):
                login_user(user)
                flash('Login Successful')
                return redirect(url_for('dashboard'))
            else: 
                flash('Wrong Pasword - Try Again!')
        else:
            flash("That user does not exist.")
    
    return render_template('login.html', login_form=login_form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login'))

@app.route('/menus')
@login_required
def menus():
    user_menus = Menu.query.filter_by(user_id=current_user.id).all()
    active_menu = Menu.query.filter_by(user_id=current_user.id, active=True).first()
    
    return render_template('menus.html', user_menus=user_menus, active_menu=active_menu)

@app.route('/menus/active/<menu_id>')
@login_required
def make_menu_active(menu_id):
    active_menu = Menu.query.filter_by(id=menu_id).first()
    active_menu.active = True
    db.session.commit()
    flash(f'{active_menu.name} is now the active menu.')
    return redirect(url_for('menus'))

@app.route('/menus/deactivate/<menu_id>')
@login_required
def deactivate_menu(menu_id):
    active_menu = Menu.query.filter_by(id=menu_id).first()
    active_menu.active = False
    db.session.commit()
    flash(f'{active_menu.name} has been deactivated.')
    return redirect(url_for('menus'))

@app.route('/menus/delete/<menu_id>')
@login_required
def delete_menu(menu_id):
    menu = Menu.query.filter_by(id=menu_id).first()
    db.session.delete(menu)
    db.session.commit()
    flash(f'{menu.name} has been deleted.')
    return redirect(url_for('menus'))

@app.route('/menus/create', methods=["GET", "POST"])
@login_required
def create_menu():
    create_menu_form = CreateMenuForm()
    create_menu_form.update_recipe_choices(Recipe.query.filter_by(user_id=current_user.id).all())
    
    if create_menu_form.validate_on_submit():
        #Create a new menu
        new_menu = Menu.create(create_menu_form.name.data, current_user)
        db.session.add(new_menu)
        
        #Create days of the week for that menu, append to the list
        sunday = Day.create(1, new_menu)
        db.session.add(sunday)
        
        monday = Day.create(2, new_menu)
        db.session.add(monday)
        
        tuesday = Day.create(3, new_menu)
        db.session.add(tuesday)
        
        wednesday = Day.create(4, new_menu)
        db.session.add(wednesday)
        
        thursday = Day.create(5, new_menu)
        db.session.add(thursday)
        
        friday = Day.create(6, new_menu)
        db.session.add(friday)
        
        saturday = Day.create(7, new_menu)
        db.session.add(saturday)
        
        #Get the recipes from the form
        sunday_recipe = Recipe.query.filter_by(id=create_menu_form.sunday_recipe.data).first()
        print(sunday_recipe)
        monday_recipe = Recipe.query.filter_by(id=create_menu_form.monday_recipe.data).first()
        tuesday_recipe = Recipe.query.filter_by(id=create_menu_form.tuesday_recipe.data).first()
        wednesday_recipe = Recipe.query.filter_by(id=create_menu_form.wednesday_recipe.data).first()
        thursday_recipe = Recipe.query.filter_by(id=create_menu_form.thursday_recipe.data).first()
        friday_recipe = Recipe.query.filter_by(id=create_menu_form.friday_recipe.data).first()
        saturday_recipe = Recipe.query.filter_by(id=create_menu_form.saturday_recipe.data).first()
        
        #Create the DaysRecipes object for each day. 
        sunday_menu = DaysRecipe.create(sunday, sunday_recipe)
        db.session.add(sunday_menu)
        
        monday_menu = DaysRecipe.create(monday, monday_recipe)
        db.session.add(monday_menu)
        
        tuesday_menu = DaysRecipe.create(tuesday, tuesday_recipe)
        db.session.add(tuesday_menu)
        
        wednesday_menu = DaysRecipe.create(wednesday, wednesday_recipe)
        db.session.add(wednesday_menu)
        
        thursday_menu = DaysRecipe.create(thursday, thursday_recipe)
        db.session.add(thursday_menu)
        
        friday_menu = DaysRecipe.create(friday, friday_recipe)
        db.session.add(friday_menu)
        
        saturday_menu = DaysRecipe.create(saturday, saturday_recipe)
        db.session.add(saturday_menu)
        
        db.session.commit()
        flash('New Menu Created!')
        return redirect(url_for('menus'))
    
    return render_template('create_menu.html', create_menu_form=create_menu_form)

@app.route('/pantry', methods=['GET', 'POST'])
@login_required
def pantry():
    user_pantry = OnHand.query.filter_by(user_id=current_user.id).all()
    
    add_ingredient_form = AddIngredientForm()
    add_ingredient_form.update_ingredients(Ingredient.query.all())
    
    if add_ingredient_form.validate_on_submit():
        ing_id = add_ingredient_form.ingredient.data
        ing_to_add = Ingredient.query.filter_by(id=ing_id).first()
        qty_to_add = add_ingredient_form.quantity.data
        existing_pantry_item = OnHand.query.filter_by(ingredient=ing_to_add).first()
        if existing_pantry_item:
            existing_pantry_item.quantity = qty_to_add + existing_pantry_item.quantity
            db.session.commit()
            flash(f'Added {qty_to_add} of {existing_pantry_item.ingredient.name}. 1')
            return redirect(url_for('pantry'))
        else:
            new_pantry_item = OnHand.create(current_user, ing_to_add, qty_to_add)
            db.session.add(new_pantry_item)
            db.session.commit()
            flash(f'Added {new_pantry_item.quantity} of {new_pantry_item.ingredient.name}. 2')
            return redirect(url_for('pantry'))
    
    return render_template('pantry.html', user_pantry=user_pantry, add_ingredient_form=add_ingredient_form)
    
@app.route('/pantry/delfrom/<ingredient_id>')
def del_from_pantry(ingredient_id):
    to_delete = OnHand.query.filter_by(user_id=current_user.id, ingredient_id=ingredient_id).first()
    db.session.delete(to_delete)
    db.session.commit()
    flash("Ingredient deleted from pantry!")
    return redirect(url_for('pantry'))

@app.route('/lists')
@login_required
def lists():
    active_list = GroceryList.query.filter_by(user_id=current_user.id, active=True).first()
    previous_lists = GroceryList.query.filter_by(user_id=current_user.id, active=False).all()
    
    return render_template('lists.html', active_list=active_list, previous_lists=previous_lists)

@app.route('/lists/add_ingredient', methods=["GET", "POST"])
@login_required
def add_ing_to_list():
    active_list = GroceryList.query.filter_by(user=current_user, active=True).first()
    
    add_ing_form = AddIngredientForm()
    add_ing_form.update_ingredients(Ingredient.query.all())
    
    if add_ing_form.validate_on_submit():
        ing_id = add_ing_form.ingredient.data
        ing_to_add = Ingredient.query.filter_by(id=ing_id).first()
        qty_to_add = add_ing_form.quantity.data
        
        existing_list_item = GroceryIngredient.query.filter_by(ingredient=ing_to_add, grocery_list=active_list).first()
        
        if existing_list_item:
            existing_list_item.quantity = qty_to_add + existing_list_item.quantity
            db.session.commit()
            flash(f'Added {qty_to_add} of {existing_list_item.ingredient.name} to active list')
            return redirect(url_for('lists'))
        else:
            new_list_item = GroceryIngredient.create(ing_to_add, active_list, qty_to_add)
            db.session.add(new_list_item)
            db.session.commit()
            flash(f'Added {qty_to_add} of {ing_to_add.name} to active list')
            return redirect(url_for('lists'))
    
    return render_template('add_ing_to_list.html', add_ing_form=add_ing_form)

@app.route('/lists/remove/<grocery_ingredient_id>')
@login_required
def remove_from_list(grocery_ingredient_id):
    to_delete = GroceryIngredient.query.filter_by(id=grocery_ingredient_id).first()
    db.session.delete(to_delete)
    db.session.commit()
    flash("Deleted from grocery list!")
    return redirect(url_for('lists'))

@app.route('/lists/purchase')
@login_required
def purchase_list():
    active_list = GroceryList.query.filter_by(user=current_user, active=True).first()
    
    for grocery_ingredient in active_list.grocery_ingredients:
        ing_to_add = grocery_ingredient.ingredient
        qty_to_add = grocery_ingredient.quantity
        
        ing_in_pantry = OnHand.query.filter_by(ingredient=ing_to_add, user=current_user).first()
        
        if ing_in_pantry:
            ing_in_pantry.quantity = qty_to_add + ing_in_pantry.quantity
            db.session.commit()
        else:
            new_pantry_item = OnHand.create(current_user, ing_to_add, qty_to_add)
            db.session.add(new_pantry_item)
            db.session.commit()
    
    active_list.active = False
    db.session.commit()
    
    flash('Ingredients from list added to pantry!')
    return redirect(url_for('pantry'))

@app.route('/lists/generate')
@login_required
def generate_list():
    active_menu = Menu.query.filter_by(user_id=current_user.id, active=True).first()
    
    if not active_menu:
        flash("Sorry, we need an active menu. Set one in your menu page!")
        return redirect(url_for('lists'))
    else:
        today = date.today()
        new_grocery_list = GroceryList.create(str(today), current_user)
        new_grocery_list.active = True
        
        user_pantry = OnHand.query.filter_by(user_id=current_user.id).all()
        
        for day in active_menu.days:
            for day_recipe in day.days_recipes:
                for recipe_ingredient in day_recipe.recipe.recipe_ingredients:
                    
                    ingredient_in_pantry = OnHand.query.filter_by(ingredient_id=recipe_ingredient.ingredient.id, user_id=current_user.id).first()
                    
                    if ingredient_in_pantry:
                        qty_in_pantry = ingredient_in_pantry.quantity
                        qty_to_add = recipe_ingredient.quantity - qty_in_pantry
                        if qty_to_add > 0:
                            new_list_ingredient = GroceryIngredient.create(recipe_ingredient.ingredient, new_grocery_list, qty_to_add)
                            db.session.add(new_list_ingredient)
                    else:
                        new_list_ingredient = GroceryIngredient.create(recipe_ingredient.ingredient, new_grocery_list, recipe_ingredient.quantity)
                        db.session.add(new_list_ingredient)
        
        if not new_grocery_list.grocery_ingredients:
            flash("Can't create new list; ingredients for your menu are all in your pantry.")
            return redirect(url_for('lists'))
        db.session.add(new_grocery_list)
        db.session.commit()
        flash('New grocery list created from menu!')
        return redirect(url_for('lists'))

@app.route('/recipes')
@login_required
def recipes():
    user_recipes = Recipe.query.filter_by(user=current_user).all()
    
    return render_template('recipes.html', user_recipes=user_recipes)

@app.route('/recipe/delete/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    db.session.delete(recipe)
    flash(f'{recipe.name} deleted!')
    return redirect(url_for('recipes'))

@app.route('/recipe/add')
@login_required
def add_recipe():
    
    
    return render_template('add_recipe.html')

@app.route('/recipe/view/<recipe_id>')
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    recipe_ingredients = RecipeIngredient.query.filter_by(recipe=recipe).all()
    return render_template('view_recipe.html', recipe=recipe, recipe_ingredients=recipe_ingredients)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)