from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, moons):
        self.id = id
        self.name = name
        self.description = description
        self.moons = moons

planets = [
    Planet(1, "Mercury", "Mercury's craters are named after famous artists, musicians and authors.", 0),
    Planet(2 , "Venus", "Venus is the hottest planet in the solar system.", 0),
    Planet(3, "Earth", "Is Hell. Is a prison for my weary bones to which I am condemned.", 1),
    Planet(4, "Mars", "There have been more missions to Mars than any other planet.", 2),
    Planet(5, "Jupiter", "Jupiter has more than double the mass of all the other planets combined.", 53),
    Planet(6, "Saturn", "Saturn has more moons than any other planet in the Solar System.", 53),
    Planet(7, "Uranus", "Uranus has only been visited by a single spacecraft, Voyager 2", 27),
    Planet(8, "Neptune", "It takes like more than 4 hours for light to reach Neptune from the Sun.", 14)
]

planets_bp = Blueprint("planets_bp",__name__,url_prefix="/planets")

@planets_bp.route("",methods=["GET"])
def get_planets():
    planets_response = []
    for planet in planets:
        planets_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "moons": planet.moons
        })
    return jsonify(planets_response), 200

@planets_bp.route("/<id>",methods=["GET"])
def get_planet(id):
    print(id)
    planet_response = {}
    for planet in planets:
        print(planet.id)
        if planet.id == int(id):
            planet_response["id"] = planet.id,
            planet_response["name"] = planet.name,
            planet_response["description"] = planet.description,
            planet_response["moons"] = planet.moons
        print(planet_response)
    return jsonify(planet_response), 200
    






# can we use name/other non-pk attribute instead of id/pk for endpoint?
# do we need to feed id argument into function?