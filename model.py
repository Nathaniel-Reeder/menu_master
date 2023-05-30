import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    '''A user with their username, email, and password'''
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    
    def __repr__(self):
        return f'<User user_id={self.id} username={self.username} email={self.email}>'
    
    @classmethod
    def create(cls, username, email, password):
        '''Create and return a new user'''
        return cls(username=username, email=email, password=generate_password_hash(password))
    
class Ingredient(db.Model):
    '''An ingredient for use in recipes or on-hand. Quantities are tracked in other tables.'''
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique = True, nullable = False)
    
    def __repr__(self):
        return f'<Ingredient id={self.id} name={self.name}>'
    
    @classmethod
    def create(cls, name):
        return cls(name=name)
    
class Recipe(db.Model):
    '''A recipe. Ingredients and quantites are stored in the recipe_ingredients association table.'''
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    instructions = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='recipes', lazy=False)
    
    def __repr__(self):
        return f'<Recipe id={self.id} name={self.name} user_id={self.user_id}>'
    
    @classmethod
    def create(cls, name, instructions, user):
        return cls(name=name, instructions=instructions, user=user)
    
class RecipeIngredient(db.Model):
    '''Association table for an individual recipe's ingredients and their quantities.'''
    __tablename__ = 'recipe_ingredients'
    
    id = db.Column(db.Integer, primary_key = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    quantity = db.Column(db.Integer, nullable = False)
    
    recipe = db.relationship('Recipe', backref='recipe_ingredients', lazy=False)
    ingredient = db.relationship('Ingredient', backref='recipe_ingredients', lazy=False)
    
    def __repr__(self):
        return f'<RecipeIngredient id={self.id} recipe_id={self.recipe_id} ingredient_id={self.ingredient_id} quantity={self.quantity}>'
    
    @classmethod
    def create(cls, recipe, ingredient, quantity):
        return cls(recipe=recipe, ingredient=ingredient, quantity=quantity)
        
class OnHand(db.Model):
    '''List of ingredients a user has available to them.'''
    __tablename__ = 'on_hand'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    quantity = db.Column(db.Integer, nullable = False)
    
    user = db.relationship('User', backref='on_hand', lazy=False)
    ingredient = db.relationship('Ingredient', backref='on_hand', lazy=False)
    
    def __repr__(self):
        return f'<OnHand id={self.id} user_id={self.user_id} ingredient_id={self.ingredient_id} quantity={self.quantity}>'
    
    @classmethod
    def create(cls, user, ingredient, quantity):
        return cls(user=user, ingredient=ingredient, quantity=quantity)

class Menu(db.Model):
    '''A menu item. One menu can have many days planned.'''
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    active = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # days = db.relationship('Day', backref='menus')
    user = db.relationship('User', backref='menus', lazy=False)
    
    def __repr__(self):
        return f'<Menu id={self.id} name={self.name} user_id={self.user_id}>'
    
    @classmethod
    def create(cls, name, user):
        return cls(name=name, user=user)
    
class Day(db.Model):
    '''A day item to be used in a menu. One day can have many recipes.'''
    __tablename__ = 'days'
    
    id = db.Column(db.Integer, primary_key = True)
    day_of_week = db.Column(db.Integer)
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    
    menu = db.relationship('Menu', backref='days', lazy=False)
    
    def __repr__(self):
        return f'<Day id={self.id} day_of_week={self.day_of_week} menu_id={self.menu_id}>'
    
    @classmethod
    def create(cls, day_of_week, menu):
        return cls(day_of_week=day_of_week, menu=menu)
    
class DaysRecipe(db.Model):
    '''An association table for recipes within a given day.'''
    __tablename__ = 'days_recipes'
    id = db.Column(db.Integer, primary_key = True)
    day_id = db.Column(db.Integer, db.ForeignKey('days.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    
    day = db.relationship('Day', backref='days_recipes', lazy=False)
    recipe = db.relationship('Recipe', backref='days_recipes', lazy=False)
    
    def __repr__(self):
        return f'<DaysRecipe id={self.id} day={self.day_id} recipe={self.recipe_id}>'
    
    @classmethod
    def create(cls, day, recipe):
        return cls(day=day, recipe=recipe)

class GroceryList(db.Model):
    '''A list of ingredients.'''
    __tablename__ = 'grocery_list'
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    active = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='grocery_list')
    
    def __repr__(self):
        return f'<GroceryList id={self.id} name={self.name} user_id={self.user_id}>'
    
    @classmethod
    def create(cls, name, user):
        return cls(name=name, user=user)
    
class GroceryIngredient(db.Model):
    '''Keeps track of ingredients and their quantities in a grocery list.'''
    __tablename__ = 'grocery_ingredients'
    
    id = db.Column(db.Integer, primary_key = True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    grocery_list_id = db.Column(db.Integer, db.ForeignKey('grocery_list.id'))
    quantity = db.Column(db.Integer, nullable = False)
    
    ingredient = db.relationship('Ingredient', backref='grocery_ingredients')
    grocery_list = db.relationship('GroceryList', backref=('grocery_ingredients'))
    
    def __repr__(self):
        return f'<GroceryIngredient id={self.id} ingredient_id={self.ingredient_id} grocery_list_id={self.grocery_list_id} quantity={self.quantity}>'
    
    @classmethod
    def create(cls, ingredient, grocery_list, quantity):
        return cls(ingredient=ingredient, grocery_list=grocery_list, quantity=quantity)

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['POSTGRES_URI']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    app.app_context().push()
    db.init_app(app)
    
