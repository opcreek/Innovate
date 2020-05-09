import os
from sqlalchemy import Column, String, Integer, create_engine, Date
from flask_sqlalchemy import SQLAlchemy
import json

# database_name = "inno"
# database_path = "postgres://rey@localhost:5432/inno"

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
Project

'''


class Project(db.Model):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    startDate = Column(Date)
    endDate = Column(Date)
    description = Column(String)
    completed = Column(db.Boolean, default=False)

    def __init__(self, title, startDate, endDate, description, completed):
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.description = description
        self.completed = completed

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self)


'''
Team

'''


class Team(db.Model):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    members = Column(db.ARRAY(String))
    project = Column(Integer, db.ForeignKey(Project.id))

    def __init__(self, members, project):
        self.members = members
        self.project = project

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self)
