from conjugFR.views import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dbadmin:89Rhs33EmG@localhost:3306/conjugDB'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

SECRET_KEY = '4e074c033785b0ec6cc2ce3a7b4efc1a2796090ac4de3f9eb123af0adafb7387'
