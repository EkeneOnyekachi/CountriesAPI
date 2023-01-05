from sqlalchemy import Column, String, Integer, Date, Text
from flask_sqlalchemy import SQLAlchemy
from os import getenv


from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".", ".env")
load_dotenv(dotenv_path=env_path)


DB_USER = getenv("db_user")
DB_PASSWORD = getenv("db_pass")
DB_HOST = getenv("db_host")

database_name = "countries"
database_path = "postgresql://{}:{}@{}/{}".format(
    DB_USER, DB_PASSWORD, DB_HOST, database_name
)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

"""
 countries
 
"""
class Countries(db.Model):
    __tablename__ = "Countries"
    countryID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    continent = db.Column(db.String(50), nullable=False)
    population  = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    CCA3 = db.Column(db.String(50), nullable=False)
    Official_Language = db.Column(db.String(50), nullable=False)

    def __init__(self, name, continent, population, currency, CCA3, Official_Language):
        self.name = name
        self.continent = continent
        self.population = population
        self.currency = currency
        self.CCA3 = CCA3
        self.Official_Language = Official_Language
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "name": self.name,
            "continent": self.continent,
            "population": self.population,
            "currency": self.currency,
            "CCA3": self.CCA3,
            "Official_Language": self.Official_Language
        }
