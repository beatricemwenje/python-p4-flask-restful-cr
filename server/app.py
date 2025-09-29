#!/usr/bin/env python3

from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Root route
class Index(Resource):
    def get(self):
        return {"message": "Welcome to the Newsletter RESTful API"}, 200

api.add_resource(Index, '/')

# Collection route (all newsletters, create new newsletter)
class Newsletters(Resource):
    def get(self):
        newsletters = [n.to_dict() for n in Newsletter.query.all()]
        return newsletters, 200

    def post(self):
        if not request.form.get("title") or not request.form.get("body"):
            return {"error": "Both title and body are required"}, 400

        new_record = Newsletter(
            title=request.form["title"],
            body=request.form["body"],
        )

        db.session.add(new_record)
        db.session.commit()

        return new_record.to_dict(), 201

api.add_resource(Newsletters, '/newsletters')

# Single newsletter route (retrieve one by ID)
class NewsletterByID(Resource):
    def get(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return {"error": f"Newsletter with id {id} not found"}, 404
        return record.to_dict(), 200

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
