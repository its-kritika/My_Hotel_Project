from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   
'''see here, we didn't mention (template_folder = 'template') bcoz by default render_template searches in 'templates'
   folder, which we have already created but in app.py it was 'template' folder and not 'templates', remember that s  '''

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3307/hotel_management' 
#this line is mainly to connect to the mysql, similar to we do in python by providing username, password, etc.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  #initialisation

class Hotels(db.Model):
    HotelId = db.Column(db.String(8), primary_key = True)
    HotelName = db.Column(db.String(50), nullable = False)
    Location = db.Column(db.String(20), nullable = False)
    NoOfRooms = db.Column(db.Integer, nullable = False)
    RoomsAvail = db.Column(db.Integer)
    LuxuryRoomAvai = db.Column(db.Integer)
    ExecutiveSuiteAvai = db.Column(db.Integer)
    DeluxeSuiteAvai = db.Column(db.Integer)
    SignatureSuiteAvai = db.Column(db.Integer)
    PriceRange = db.Column(db.String(30), nullable = False)
    NoOfEmployees = db.Column(db.Integer, nullable = False)

@app.route('/personal_info', methods = ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Adding entry to database
        F_name = request.form.get('FirstName')
        L_name = request.form.get('LastName')
        gen = request.form.get('gender')
        passw = request.form.get('password')
        branch = request.form.get('--SELECT--')
        hobbies = request.form.getlist('hobby')
        address = request.form.get('add')
        date = request.form.get('dob')    #quotes include 'name' of input from form in index.html
        entry = Contact(Fname = F_name, Lname = L_name, Gender = gen, Password = passw, Branch = branch, \
        Hobbies = ','.join(hobbies), Address = address, DOB = date)
        db.session.add(entry)
        db.session.commit()
        return 'Inserted'

@app.route('/get_options', methods=['GET'])
def get_options():
    query = request.args.get('query', '')  # Get the user's search query from the request
    items = Hotels.query.filter(Hotels.HotelName.ilike(f'%{query}%')).all()
    options_data = [item.HotelName for item in items]
    return jsonify(options_data)

@app.route('/')
def home_page():
    return render_template('my_template.html')

@app.route('/our_hotels')
def hotel():
    return render_template('hotels.html')

@app.route('/confirm-booking')
def confirmation():
    return render_template('confirmation_page.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/awards')
def awards():
    return render_template('awards.html')

@app.route('/booking-details')
def booking():
    return render_template('booking.html')

@app.route('/select-your-room')
def press():
    return render_template('rooms.html')
    
@app.route('/enter-your-details')
def details():
    return render_template('guest_details.html')

@app.route('/welcome')
def products():
    return 'This is something so amazing!!'

@app.route('/our_newsletter')
def subscribed():
    return 'Welcome!! You have subscribed the channel'

if __name__ == '__main__':
    app.run(debug = True)
    