from flask import Blueprint, jsonify, make_response, abort, request
from app.models.planet import Planet
from app import db

# class Planet:
#     def __init__(self, id, name, description, moons):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.moons = moons

# planets = [
#     Planet(1, "Mercury", "Mercury's craters are named after famous artists, musicians and authors.", 0),
#     Planet(2 , "Venus", "Venus is the hottest planet in the solar system.", 0),
#     Planet(3, "Earth", "Is Hell. Is a prison for my weary bones to which I am condemned.", 1),
#     Planet(4, "Mars", "There have been more missions to Mars than any other planet.", 2),
#     Planet(5, "Jupiter", "Jupiter has more than double the mass of all the other planets combined.", 53),
#     Planet(6, "Saturn", "Saturn has more moons than any other planet in the Solar System.", 53),
#     Planet(7, "Uranus", "Uranus has only been visited by a single spacecraft, Voyager 2", 27),
#     Planet(8, "Neptune", "It takes like more than 4 hours for light to reach Neptune from the Sun.", 14)
# ]

planets_bp = Blueprint("planets_bp",__name__,url_prefix="/planets")

# standard webdev guidelines: try to limit to 3 otherwise consider more routes - it's ok to type more if it makes it more secure!
@planets_bp.route("",methods=["GET"])
def get_planets():
    params = request.args
    if len(params) == 0:
        planets = Planet.query.all()
    else:
        command_str = "Planet.query"
        for k,v in params.items():
            command_str += f".filter_by({k}='{v}')"
        planets = eval(command_str)
    planets_response = []
    if planets:
        for planet in planets:
            planets_response.append({
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "order_from_sun": planet.order_from_sun,
                "moons": planet.moons
            })
    return jsonify(planets_response), 200

@planets_bp.route("", methods=["POST"])
def add_planet():
    request_body = request.get_json()
    new_planet = Planet(
        name = request_body["name"],
        description = request_body["description"],
        order_from_sun = request_body["order_from_sun"],
        moons = request_body["moons"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return make_response(f"Planet {new_planet.name} successfully created.", 201)

@planets_bp.route("/<id>",methods=["GET"])
def get_planet(id):
    planets = Planet.query.all()
    planet = handle_id_errors(id,planets)
    planet_response = {
        "id":planet.id,
        "name":planet.name,
        "description":planet.description,
        "order_from_sun":planet.order_from_sun,
        "moons":planet.moons
        }
    return jsonify(planet_response), 200

@planets_bp.route("/<id>", methods=["PATCH"])
def update_planet(id):
    request_body = request.get_json()
    planets = Planet.query.all()
    planet = handle_id_errors(id,planets)
    valid_input = False
    if "name" in request_body:
        planet.name = request_body["name"]
        valid_input = True
    if "description" in request_body:
        planet.description = request_body["description"]
        valid_input = True
    if "order_from_sun" in request_body:
        planet.order_from_sun = request_body["order_from_sun"]
        valid_input = True
    if "moons" in request_body:
        planet.moons = request_body["moons"]
        valid_input = True
    if not valid_input:
        return jsonify({"unsuccessful": "no valid input given"}), 400
    db.session.commit()
    return jsonify({"successful": f"{planet.id} updated"}), 200

@planets_bp.route("/<id>",methods=["PUT"])
def replace_planet(id):
    request_body = request.get_json()
    planets = Planet.query.all()
    planet = handle_id_errors(id,planets)
    try:
        planet.name = request_body["name"],
        planet.description = request_body["description"],
        planet.order_from_sun = request_body["order_from_sun"],
        planet.moons = request_body["moons"]
    except KeyError:
        return {
            "unsuccessful": "name, description, order_from_sun, moons are all required fields"
        }
    db.session.commit()
    planet_response = {
        "id":planet.id,
        "name":planet.name,
        "description":planet.description,
        "order_from_sun":planet.order_from_sun,
        "moons":planet.moons
    }
    return jsonify(planet_response),200

@planets_bp.route("/<id>",methods=["DELETE"])
def delete_planet(id):
    planets = Planet.query.all()
    planet = handle_id_errors(id,planets)
    db.session.delete(planet)
    db.session.commit()
    return {"successful": f"planet #{id} is successfully deleted"},200


def handle_id_errors(id,planets):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"unsuccessful":f"id {id} is invalid"}, 400))
    for planet in planets:
        if planet.id == id:
            return planet
    abort(make_response({"unsuccessful":f"id {id} does not exist"}, 404)) 



# can we use name/other non-pk attribute instead of id/pk for endpoint?
# do we need to feed id argument into function?