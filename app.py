import os
from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from models import setup_db, db, studio, instructor
from auth import AuthError, requires_auth
from utils import *


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def welcome():
        return 'Welcome to studios Hub!'

    @app.route('/studios')
    @requires_auth('get:studios')
    def get_studios(jwt):
        studios = studio.query.all()
        return jsonify({
            'success': True,
            'studios': [studio.format() for studio in studios],
        }), 200

    @app.route('/studios/<int:id>')
    @requires_auth('get:studios')
    def get_studio_by_id(jwt, id):
        studios = studio.query.get(id)

        if studios is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'studio': studios.format(),
            }), 200

    @app.route('/studios', methods=['POST'])
    @requires_auth('post:studios')
    def post_studio(jwt):
        data = request.get_json()
        bizname = data.get('bizname', '')
        date = data.get('opening_date', '')

        studios = studio(bizname=bizname, opening_date=date)
        if validate_studio(studios) is False:
            abort(400)
        try:
            studios.insert()
            return jsonify({
                'success': True,
                'message': 'studio added',
                'studio': studios.format()
            }), 201
        except:
            abort(500)

    @app.route('/studios/<int:id>', methods=['PATCH'])
    @requires_auth('patch:studios')
    def edit_studio(jwt, id):
        data = request.get_json()
        bizname = data.get('bizname', '')
        date = data.get('opening_date', '')

        studios = studio.query.get(id)

        if studios is None:
            abort(404)

        studios.bizname = bizname
        studios.opening_date = date
        if validate_studio(studios) is False:
            db.session.rollback()
            abort(400)
        try:
            studios.update()
            return jsonify({
                'success': True,
                'message': 'studio updated',
                'studio': studios.format()
            }), 200
        except:
            db.session.rollback()
            abort(500)

    @app.route('/studios/<int:id>', methods=['DELETE'])
    @requires_auth('delete:studios')
    def delete_studio(jwt, id):
        studios = studio.query.get(id)

        if studios is None:
            abort(404)
        try:
            studios.delete()
            return jsonify({
                'success': True,
                'message': 'studio deleted',
                'studio': studios.id
            })
        except:
            db.session.rollback()
            abort(500)

    '''
    instructorS ENDPOINTS
    '''
    @app.route('/instructors')
    @requires_auth('get:instructors')
    def get_instructors(jwt):
        instructors = instructor.query.all()
        return jsonify({
            'success': True,
            'instructors': [instructor.format() for instructor in instructors],
        }), 200

    @app.route('/instructors/<int:id>')
    @requires_auth('get:studios')
    def get_instructor_by_id(jwt, id):
        instructors = instructor.query.get(id)

        if instructors is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'instructor': instructors.format(),
            }), 200

    @app.route('/instructors', methods=['POST'])
    @requires_auth('post:instructors')
    def post_instructor(jwt):
        data = request.get_json()
        name = data.get('name', '')
        age = data.get('age', '')
        gender = data.get('gender', '')
        class_type = data.get('class_type', '')

        instructors = instructor(name=name, age=age, gender=gender, class_type=class_type)
        if validate_instructor(instructors) is False:
            abort(400)
        try:
            instructors.insert()
            return jsonify({
                'success': True,
                'message': 'instructor added',
                'instructor': instructors.format()
            }), 201
        except:
            abort(500)

    @app.route('/instructors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:instructors')
    def edit_instructor(jwt, id):
        data = request.get_json()
        name = data.get('name', '')
        age = data.get('age', '')
        gender = data.get('gender', '')
        class_type = data.get('class_type', '')

        instructors = instructor.query.get(id)

        if instructors is None:
            abort(404)

        instructors.name = name
        instructors.age = age
        instructors.gender = gender
        instructors.class_type = class_type
        if validate_instructor(instructors) is False:
            db.session.rollback()
            abort(400)
        try:
            instructors.update()
            return jsonify({
                'success': True,
                'message': 'instructor updated',
                'instructor': instructors.format()
            }), 200
        except:
            db.session.rollback()
            abort(500)

    @app.route('/instructors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:instructors')
    def delete_instructor(jwt, id):
        instructors = instructor.query.get(id)

        if instructors is None:
            abort(404)
        try:
            instructors.delete()
            return jsonify({
                'success': True,
                'message': 'instructor deleted',
                'instructor': instructors.id
            })
        except:
            db.session.rollback()
            abort(500)

    '''
    Create error handlers for all expected errors
    '''
    # handle bad request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Bad Request, pls check your inputs"
        }), 400

    # handle unauthorized request errors
    @app.errorhandler(401)
    def unathorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": error.description,
        }), 401

    # handle forbidden requests
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "You are forbidden from accessing this resource",
        }), 403

    # handle resource not found errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    # handle bad request
    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Something went wrong, please try again"
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
