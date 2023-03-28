import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import json
from dateutil import parser

from models import setup_db, Movie, Actor, Cast
from auth.auth import AuthError, requires_auth, AUTH0_DOMAIN, API_AUDIENCE, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  return app

APP = create_app()
db = setup_db(APP)

@APP.route('/')
def index():
  return { 'HelloWorld' : 'Welcome to FSND capstone project...' }

@APP.route('/auth')
def authenticate():
  return jsonify({ 'auth-url': f'https://{AUTH0_DOMAIN}/authorize?audience={API_AUDIENCE}&response_type=token&client_id={AUTH0_CLIENT_ID}&redirect_uri={AUTH0_CALLBACK_URL}' })

@APP.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
   movies = Movie.query.all()
   if movies is None:
      formatted_movies = []
   else:
      formatted_movies = [movie.short() for movie in movies]       
   return jsonify({ 'success': True, 'movies': formatted_movies })

@APP.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
   actors = Actor.query.all()
   if actors is None:
      formatted_actors = []
   else:
      formatted_actors = [actor.short() for actor in actors]       
   return jsonify({ 'success': True, 'actors': formatted_actors })

@APP.route('/movies/<int:id>', methods= ['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, id):
     try:
          movie = Movie.query.filter(Movie.id == id).one_or_none()
          if movie is None:
               abort(404)
          else:
             movie.delete()
             return jsonify({ 'success': True, 'delete': id})
     except:
          abort(422)  

@APP.route('/actors/<int:id>', methods= ['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, id):
     try:
          actor = Actor.query.filter(Actor.id == id).one_or_none()
          if actor is None:
               abort(404)
          else:
             actor.delete()
             return jsonify({ 'success': True, 'delete': id})
     except:
          abort(422)  

@APP.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movie(payload):
    body = request.get_json()
    try:
         title = body.get('title', None)
         date = body.get('release_date', None)
         release_date = parser.parse(date).date()
         movie = Movie(title = title, release_date = release_date)  
         movie.insert()     
         filtered_movie = Movie.query.filter(Movie.id == movie.id).one_or_none()
         if filtered_movie is None:
            abort(404)     
         return jsonify({ 'success': True, 'movies': [filtered_movie.format()] })
    except:
         abort(422)

@APP.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actor(payload):
    body = request.get_json()
    try:
         name = body.get('name', None)
         age = body.get('age', None)
         gender = body.get('gender', None)
         actor = Actor(name = name, age = age, gender = gender)  
         actor.insert()
         filtered_actor = Actor.query.filter(Actor.id == actor.id).one_or_none()
         if filtered_actor is None:
            abort(404)     
         return jsonify({ 'success': True, 'actors': [filtered_actor.format()] })
    except:
         abort(422)

@APP.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(payload, id):
     try:
          movie = Movie.query.filter(Movie.id == id).one_or_none()
          if movie is None:
               abort(404)
          else:
             body = request.get_json()
             title = body.get('title', None)
             date = body.get('release_date', None)
             release_date = parser.parse(date).date()

             movie.title = title
             movie.release_date =  release_date
             movie.update()

             filtered_movie = Movie.query.filter(Movie.id == movie.id).one_or_none() 
             if filtered_movie is None:
                abort(404)       
             return jsonify({ 'success': True, 'movies': [filtered_movie.format()] })
     except:
          abort(422)

@APP.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(payload, id):
     try:
          actor = Actor.query.filter(Actor.id == id).one_or_none()
          if actor is None:
               abort(404)
          else:
             body = request.get_json()
             name = body.get('name', None)
             age = body.get('age', None)
             gender = body.get('gender', None)

             actor.name = name
             actor.age =  age
             actor.gender = gender
             actor.update()

             filtered_actor = Actor.query.filter(Actor.id == actor.id).one_or_none() 
             if filtered_actor is None:
                abort(404)       
             return jsonify({ 'success': True, 'actors': [filtered_actor.format()] })
     except:
          abort(422)

#CORS headers
@APP.after_request
def after_request(response):
   response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
   response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
   return response

# Error Handling
@APP.errorhandler(400)
def bad_request(error):
        return jsonify({ "success": False,  "error": 400, "message": "bad request" }), 400

@APP.errorhandler(401)
def unauthorized_error(error):
        return jsonify({ "success": False, "error": 401, "message": "unAuthorized" }), 401

@APP.errorhandler(403)
def forbidden_error(error):
        return jsonify({ "success": False, "error": 403, "message": "forbidden access" }), 403

@APP.errorhandler(404)
def not_found_error(error):
        return jsonify({ "success": False, "error": 404, "message": "not found" }), 404

@APP.errorhandler(405)
def method_not_error(error):
        return jsonify({ "success": False, "error": 405, "message": "method not allowed" }), 405

@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({ "success": False, "error": 422, "message": "unprocessable" }), 422

@APP.errorhandler(500)
def internal_error(error):
        return jsonify({ "success": False, "error": 500, "message": "internal server error" }), 500

@APP.errorhandler(AuthError)
def authorization_error(error):
     print(error)
     return jsonify({ "success": False, "error": error.status_code, "message": error.error['description'] }), error.status_code

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)