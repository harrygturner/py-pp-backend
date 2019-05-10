from server import conn
from flask import Flask, request
from flask_restful import Api, Resource
from json import dumps
from flask_jsonpify import jsonify

from pdb import set_trace as bp

db_connect = conn
app = Flask(__name__)
api = Api(app)

# from routes.kicker import *
# from routes.team import *

@app.route('/teams', methods=['GET'])
def get_teams():
   cur = db_connect.cursor()
   cur.execute( "SELECT id, name FROM team;" ) 
   result = cur.fetchall() 
   new_format = []
   for i in result:
      team_kickers = get_team_kickers(i[0])
      to_add = {'id': i[0], 'name': i[1], 'kickers': team_kickers}
      new_format.append(to_add)

   response = jsonify(new_format)
   response.status_code = 200
   return response

@app.route('/teams/<id>', methods=['GET'])
def get_team(id):
   cur = db_connect.cursor()
   cur.execute( "SELECT * FROM team WHERE id = " + str(id) )
   result = cur.fetchall() 
   team_kickers = get_team_kickers(id)
   for i in result:
      new_format = { 'id': i[0], 'name': i[1], 'league_id': i[2], 'kickers': team_kickers }

   response = jsonify(new_format)
   response.status_code = 200
   return response

def get_team_kickers(team_id):
   cur = db_connect.cursor()
   cur.execute( "SELECT name, position FROM kicker WHERE team_id = " + str(team_id) )
   result = cur.fetchall()
   new_format = []
   for i in result:
      to_add = { 'name': i[0], 'position': i[1] }
      new_format.append(to_add)

   return new_format

@app.route('/kickers', methods=['GET'])
def get_kickers():
   cur = db_connect.cursor()
   cur.execute("SELECT * FROM kicker;")
   result = cur.fetchall()
   new_format = []
   for i in result:
      to_add = {'id': i[0], 'name': i[1], 'position': i[2], 'team_id': i[3]}
      new_format.append(to_add)
   response = jsonify(new_format)
   response.status_code = 200
   return response

if __name__ == '__main__':
   app.run(port='3000')
