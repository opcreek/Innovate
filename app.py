import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Project, Team
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # db_drop_and_create_all()
    # Set up CORS. Allow '*' for origins.b_
    CORS(app, resources={'/': {'origins': '*'}})

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # setup endpoint decorators
    # welcome page endpoint
    @app.route('/')
    def welcome():
        return "Welcome to the Innovation App"

    # Create an endpoint to handle GET requests
    # for all projects.
    @app.route('/projects')
    def get_projects():
        projects = Project.query.all()
        projects_list = []
        for proj in projects:
            projects_list.append(proj.title)

        # abort 404 error handler
        if (len(projects_list) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'projects': json.dumps(projects_list),
            'total_projects': len(projects_list)
        })

    # Create an endpoint to retrieve a project detail
    @app.route('/projects/<int:proj_id>/details')
    def get_project_detail(proj_id):
        project = Project.query.filter_by(id=proj_id).one_or_none()

        try:
            project_dict = {
                'title': project.title,
                'start date': project.startDate,
                'end date': project.endDate,
                'description': project.description,
                'completed': project.completed
            }

            # abort 404 error handler
            if (len(project_dict) == 0):
                abort(404)

            return jsonify({
                'success': True,
                'id': project.id,
                'project': project_dict
            })

        except Exception:
            abort(422)

    # Create an endpoint to handle GET requests for all
    # team members and their corresponding projects
    # This endpoint should return a list of names,
    # and project involved with.
    @app.route('/members')
    @requires_auth('get:team-members')
    def get_members(payload):
        try:
            # selection = Team.query.all()
            # total_questions = len(selection)
            # current_questions = paginate_questions(request, selection)
            # upcoming_shows_filter = db.session.query(Shows).join(Artist)\
            # .filter(Shows.venue_id==venue_id).filter(Shows.start_time>datetime.now()).all()
            members = Team.query.all()
            member_list = []
            for item in members:
                for member in item.members:
                    member_list.append(member)

            member_list = list(set(member_list))
            # abort 404 error handler
            if (len(member_list) == 0):
                abort(404)

            return jsonify({
                'success': True,
                'members': member_list,
                'total_members': len(member_list)
            })
        except AuthError:
            abort(AuthError)

    # Create an endpoint to DELETE a project using a project ID.
    @app.route('/projects/<int:proj_id>', methods=['DELETE'])
    @requires_auth('delete:project')
    def delete_project(payload, proj_id):
        try:
            # retrieve the project to be deleted
            project = Project.query.filter_by(id=proj_id).one_or_none()

            # abort 422 error handler
            if project is None:
                abort(422)

            # delete the question
            project.delete()

            return jsonify({
                'success': True
                # 'deleted': id
            })

        except AuthError:
            # abort 422 error handler
            abort(AuthError)

    # Create an endpoint to POST a new project,
    # which will require a start date, end date,
    # and description
    @app.route('/projects', methods=['POST'])
    @requires_auth('post:project')
    def submit_project(payload):
        body = request.get_json()
        # retrieve new data
        new_title = body.get('title')
        new_startDate = body.get('startDate')
        new_endDate = body.get('endDate')
        new_description = body.get('description')
        new_completed = False

        # check if data exists
        if ((new_title is None) or (new_startDate is None)
                or (new_endDate is None) or (new_description is None)):
            abort(422)

        try:
            # insert project
            project = Project(title=new_title,
                              startDate=new_startDate,
                              endDate=new_endDate,
                              description=new_description,
                              completed=new_completed)
            project.insert()

            return jsonify({
                'success': True,
                'id': project.id,
                'title': project.title,
                'project_created': project.startDate,
                'project_end': project.endDate,
                'description': project.description,
                'completed': project.completed,
                'total_projects': len(Project.query.all())
            })

        except AuthError:
            # abort 422 error handler
            abort(AuthError)

    # Create a PATCH endpoint to edit an existing project.
    # The following can be edited - end date, description,
    # and completed status
    @app.route('/projects/<int:proj_id>', methods=['PATCH'])
    @requires_auth('patch:project')
    def update_project(payload, proj_id):
        body = request.get_json()

        updated_project = Project.query.filter_by(id=proj_id).one_or_none()

        if updated_project is None:
            abort(404)

        try:
            updated_endDate = body.get('endDate', None)
            updated_description = body.get('description', None)
            updated_completed = body.get('completed', False)

            if updated_endDate:
                updated_project.endDate = body['endDate']

            if updated_description:
                updated_project.description = body['description']

            if updated_completed:
                updated_project.completed = body['completed']

            updated_project.update()

            return jsonify({
                'success': True,
                'id': updated_project.id,
                'title': updated_project.title,
                'project_created': updated_project.startDate,
                'project_end': updated_project.endDate,
                'description': updated_project.description,
                'completed': updated_project.completed,
            })
        except AuthError:
            # abort AuthError error handler
            print('Exception has occurred')
            abort(AuthError)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }, 404)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }, 400)

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Authorization header is expected"
        }, 400)

    @app.errorhandler(403)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Permission not found"
        }, 403)

    @app.errorhandler(AuthError)
    def authentification_failure(error):
        print(error.status_code)
        error_code = error.status_code
        if error_code == 403:
            return jsonify({
                "success": False,
                "error": 403,
                "message": "Permission not found"
            }, 403)
        elif error_code == 401:
            return jsonify({
                "success": False,
                "error": 401,
                "message": "Unauthorized"
            }, 401)
        else:
            return jsonify({
                "success": False,
                "error": 400,
                "message": "Bad Request"
            }, 400)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
