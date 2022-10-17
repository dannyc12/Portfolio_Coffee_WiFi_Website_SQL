from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, URL
import secrets
from flask_bcrypt import Bcrypt

app = Flask(__name__)
SECRET_KEY = secrets.token_hex(16)  # create HEX key
bcrypt = Bcrypt(app)
SECRET_HASH_KEY = bcrypt.generate_password_hash(SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_HASH_KEY
Bootstrap(app)
# Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ------------Cafe TABLE Configuration ------------- #
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

# as of Flask 3.0, to run a db query outside an the 'app', open it with 'app.app_context()'

new_cafe = Cafe(
    name='Chris wild cafe',
    map_url='http://dans.com',
    img_url='http://picture.com',
    location='BV',
    seats=10,
    has_toilet=1,
    has_wifi=1,
    has_sockets=1,
    can_take_calls=1,
    coffee_price='$5'
    )

# db.session.add(new_cafe)
# cafe_erase = db.session.query(Cafe).get(22)
# db.session.delete(cafe_erase)
# db.session.commit()

class AddCafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Google Maps URL', validators=[DataRequired(), URL()])
    img_url = StringField('Google Image URL', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    seats = SelectField(u'Seating Available', choices=['0-10', '10-20', '20-30', '30-40', '40-50', '50+'],
                        validators=[InputRequired()])
    has_toilet = SelectField(u'Toilets', choices=['Yes', 'No'],
                             validators=[InputRequired()])
    has_wifi = SelectField(u'Free WiFi', choices=['Yes', 'No'],
                           validators=[InputRequired()])
    has_sockets = SelectField(u'Power Sockets', choices=['Yes', 'No'], validators=[InputRequired()])
    can_take_calls = SelectField(u'Allows Phone Calls', choices=['Yes', 'No'], validators=[InputRequired()])
    coffee_price = StringField(u'Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafes')
def show_cafes():
    cafe_columns = ['Cafe', 'Directions', 'Picture', 'Location', 'Seating', 'Toilets', 'WiFi', 'Power',
                    'Video/Audio Calls', 'Coffee Price']
    all_cafes = db.session.query(Cafe).all()
    # print(f'Length: {len(all_cafes)}')

    return render_template('cafes.html', cafe_columns=cafe_columns, all_cafes=all_cafes)


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        if form.has_toilet.data == 'Yes':
            form.has_toilet.data = True
        else:
            form.has_toilet.data = False
        if form.has_wifi.data == 'Yes':
            form.has_wifi.data = True
        else:
            form.has_wifi.data = False
        if form.has_sockets.data == 'Yes':
            form.has_sockets.data = True
        else:
            form.has_sockets.data = False
        if form.can_take_calls.data == 'Yes':
            form.can_take_calls.data = True
        else:
            form.can_take_calls = False

        cafe_to_add = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=form.coffee_price.data
        )
        db.session.add(cafe_to_add)
        db.session.commit()
        return redirect(url_for('show_cafes'))
    return render_template('add.html', form=form)

#TODO: add user authentication to this route
@app.route('/update/<cafe_id>', methods=['POST', 'GET'])
def update_cafe(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    # print(f'you have selected cafe: {cafe.name}')
    update_form = AddCafeForm(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        seats=cafe.seats,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        has_sockets=cafe.has_sockets,
        can_take_calls=cafe.can_take_calls,
        coffee_price=cafe.coffee_price
        )
    if update_form.validate_on_submit():
        if update_form.has_toilet.data == 'Yes':
            update_form.has_toilet.data = True
        else:
            update_form.has_toilet.data = False
        if update_form.has_wifi.data == 'Yes':
            update_form.has_wifi.data = True
        else:
            update_form.has_wifi.data = False
        if update_form.has_sockets.data == 'Yes':
            update_form.has_sockets.data = True
        else:
            update_form.has_sockets.data = False
        if update_form.can_take_calls.data == 'Yes':
            update_form.can_take_calls.data = True
        else:
            update_form.can_take_calls = False
        cafe.name = update_form.name.data
        cafe.map_url = update_form.map_url.data
        cafe.img_url = update_form.img_url.data
        cafe.location = update_form.location.data
        cafe.seats = update_form.seats.data
        cafe.has_toilet = update_form.has_toilet.data
        cafe.has_wifi = update_form.has_wifi.data
        cafe.has_sockets = update_form.has_sockets.data
        cafe.can_take_calls = update_form.can_take_calls.data
        cafe.coffee_price = update_form.coffee_price.data
        db.session.commit()
        return redirect(url_for('show_cafes'))
    return render_template('add.html', form=update_form, is_update=True)

#TODO: add user authentication to this route
@app.route('/delete/<cafe_id>', methods=['POST', 'GET'])
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('show_cafes'))

if __name__ == '__main__':
    app.run(debug=True)



