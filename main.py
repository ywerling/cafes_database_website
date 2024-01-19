from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, URL, NumberRange

# creates the flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = '62136423sWFS3fdfdfs3f3fgH3'
Bootstrap5(app)

# connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


# create table in the database
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    city = db.Column(db.String(50), nullable=True)
    website = db.Column(db.String(500), nullable=True)
    map_location = db.Column(db.String(500), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    overall_rating = db.Column(db.Float, nullable=True)
    coffee = db.Column(db.Integer, nullable=True)
    tea = db.Column(db.Integer, nullable=True)
    wifi = db.Column(db.Integer, nullable=True)
    cake = db.Column(db.Integer, nullable=True)
    work = db.Column(db.Integer, nullable=True)
    breakfast = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(2500), nullable=True)

class EditCafeForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    city = StringField("City")
    website = StringField("Website URL", [URL()])
    map_location = StringField("Online Map url")
    description = StringField("Description")
    overall_rating = FloatField("Overall Rating", [NumberRange(min=0, max=5)])
    coffee = IntegerField("Coffee Rating", [NumberRange(min=0, max=5)])
    tea = IntegerField("Tea Rating", [NumberRange(min=0, max=5)])
    cake = IntegerField("Cake Rating", [NumberRange(min=0, max=5)])
    breakfast = IntegerField("Breakfast Rating", [NumberRange(min=0, max=5)])
    wifi = IntegerField("Wifi Rating", [NumberRange(min=0, max=5)])
    work = IntegerField("Suitability for work Rating", [NumberRange(min=0, max=5)])
    review = StringField("Your Review")

    submit = SubmitField("Done")


# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()

# first entry in the database in order to test the display
# new_cafe = Cafe(
#     name="Moja Sredcovka",
#     city="Bratislava",
#     website="https://www.mojasrdcovka.sk/",
#     map_location="https://en.mapy.cz/zakladni?source=osm&id=136382968&ds=1&x=17.1058352&y=48.1411637&z=17",
#     description="Cafe with a wide choice of cakes",
#     overall_rating=5,
#     coffee=4,
#     tea=4,
#     wifi=4,
#     cake=5,
#     work=3,
#     breakfast=3,
#     review="Excellent service and great cakes."
# )

# with app.app_context():
#     db.session.add(new_cafe)
#     db.session.commit()


# start page of the webapplicatiop
@app.route("/")
def home():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.overall_rating))
    # Use .scalars() to get the elements rather than entire rows from the database
    all_cafes = result.scalars().all()
    return render_template('index.html', cafes=all_cafes)

@app.route("/view", methods=["GET", "POST"])
def view():
    cafe_id = request.args.get("id")
    cafe = db.get_or_404(Cafe, cafe_id)
    return render_template('view.html', cafe=cafe)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditCafeForm()
    cafe_id = request.args.get("id")
    cafe = db.get_or_404(Cafe, cafe_id)
    #pre populate the form with data from from the cafe
    if request.method == 'GET':
        form.name.data = cafe.name
        form.city.data = cafe.city
        form.website.data = cafe.website
        form.map_location.data = cafe.map_location
        form.description.data = cafe.description
        form.overall_rating.data = cafe.overall_rating
        form.coffee.data = cafe.coffee
        form.tea.data = cafe.tea
        form.wifi.data = cafe.wifi
        form.cake.data = cafe.cake
        form.work.data = cafe.work
        form.breakfast.data = cafe.breakfast
        form.review.data = cafe.review
    if request.method == "POST":
        if form.validate_on_submit():
            cafe.name = form.name.data
            cafe.city = form.city.data
            cafe.website = form.website.data
            cafe.map_location = form.map_location.data
            cafe.description = form.description.data
            cafe.overall_rating = form.overall_rating.data
            cafe.coffee = form.coffee.data
            cafe.work = form.work.data
            cafe.breakfast = form.breakfast.data
            cafe.review = form.review.data
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('edit.html', cafe=cafe, form=form)

@app.route("/add", methods=["GET", "POST"])
def add():
    form = EditCafeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            cafe_name = form.name.data
            print(f"Cafe to be added: {cafe_name}.")
            new_cafe = Cafe(
                name = form.name.data,
                city = form.city.data,
                website = form.website.data,
                map_location = form.map_location.data,
                description = form.description.data,
                overall_rating = form.overall_rating.data,
                coffee = form.coffee.data,
                tea = form.tea.data,
                wifi = form.wifi.data,
                cake = form.cake.data,
                work = form.work.data,
                breakfast = form.breakfast.data,
                review = form.review.data
            )
            db.session.add(new_cafe)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        print("Entry not valid")

    return render_template('add.html', form=form)

@app.route('/delete')
def delete():
    cafe_id = request.args.get('id')

    # DELETE A RECORD BY ID
    cafe_to_delete = db.get_or_404(Cafe, cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/search')
def search():
    #TODO: imnplement a search function for cafes
    return render_template('search.html')

# ensures that the application keeps running
if __name__ == "__main__":
    # remove the debug=True statement before deploment
    app.run(debug=True)
