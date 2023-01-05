from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random


from models import setup_db, Countries


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    #DEBUG = True
    with app.app_context():
        setup_db(app)
    CORS(app)


# CORS Headers

    @app.after_request
    def after_request(response):

        try:
            response.headers.add(
                "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
            )
            response.headers.add(
                "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
            )
            return response
        except Exception as erro:
            print(erro)


    #Post country
    @app.route("/countries", methods=["POST"])
    def insert_countries():
        
        try:
            body = request.get_json()

            new_name = body.get("name")
            new_continent = body.get("continent")
            new_population = body.get("population")
            new_currency = body.get("currency")
            new_CCA3 = body.get("CCA3")
            new_official_language = body.get("Official_Language")

            try:

                country = Countries(
                        name=new_name,
                        continent=new_continent,
                        population=new_population,
                        currency=new_currency,
                        CCA3=new_CCA3,
                        Official_Language=new_official_language
                    )

                country.insert()

                return jsonify(
                        ({
                            "success": True,
                            "massage": "country created",
                            "created": country.countryID,
                        }),200
                )

            except Exception as erro:
                print(erro)
                abort(422)

        except Exception as erro:
            print(erro)
            abort(400)


    #Get all countries 
    @app.route("/countries")
    def return_countries():

        try:
            #Get all countries by name in ascending order
            countries = Countries.query.order_by(Countries.name).all()
            
            if len(countries) == 0:
                abort(404)
            else:
                return jsonify(
                    ({
                        "success": True, 
                        "countries": [country.format() for country in countries],
                    }),200
                )
        except Exception as error:
            print(error)
            abort(500)

    @app.route("/countries/<country_name>")
    def get_country(country_name):

        try:
            #Get country by name used ilike to make it case insensitive
            country = Countries.query.filter(Countries.name.ilike(country_name)).one_or_none()

            if country is None:
                abort(404)
            else:
                return jsonify(
                    ({
                        "success": True, 
                        "country": country.format()
                    }),200
                )
        except Exception as error:
            print(error)
            abort(422)


    # Error handling

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource Not Found"}),
            404,
        )


    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
            422,
        )


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400


    @app.errorhandler(500)
    def Internal_Server_Error(error):
        return jsonify({"success": False, "error": 500, "message": "Internal Server Error"}), 500
            

    return app