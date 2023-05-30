from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SelectField, SubmitField, EmailField, Form
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class CreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class AddIngredientForm(FlaskForm):
    ingredient = SelectField("Ingredient", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
    def update_ingredients(self, ingredients):
        self.ingredient.choices = [(item.id, item.name) for item in ingredients]
        
class CreateMenuForm(FlaskForm):
    name = StringField("Menu Name", validators=[DataRequired()])
    sunday_recipe = SelectField("Sunday Recipe")
    monday_recipe = SelectField("Monday Recipe")
    tuesday_recipe = SelectField("Tuesday Recipe")
    wednesday_recipe = SelectField("Wednesday Recipe")
    thursday_recipe = SelectField("Thursday Recipe")
    friday_recipe = SelectField("Friday Recipe")
    saturday_recipe = SelectField("Saturday Recipe")
    submit = SubmitField("Submit")
    
    def update_recipe_choices(self, recipes):
        recipe_choices = [(recipe.id, recipe.name) for recipe in recipes]
        self.sunday_recipe.choices = recipe_choices
        self.monday_recipe.choices = recipe_choices
        self.tuesday_recipe.choices = recipe_choices
        self.wednesday_recipe.choices = recipe_choices
        self.thursday_recipe.choices = recipe_choices
        self.friday_recipe.choices = recipe_choices
        self.saturday_recipe.choices = recipe_choices
        
class CreateRecipeForm(FlaskForm):
    name = StringField("Recipe Name", validators=[DataRequired()])
    instructions = TextAreaField("Instructions", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class AddRecipeIngredientForm(Form):
    ingredient = SelectField("Ingredient", validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    
    def update_recipe_ingredients(self, ingredients):
        self.ingredient.choices = [(item.id, item.name) for item in ingredients]