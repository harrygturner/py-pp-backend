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
   cur.execute("SELECT id, name FROM team;") 
   result = cur.fetchall() 
   new_format = []
   for i in result:
      to_add = {'id': i[0], 'name': i[1]}
      new_format.append(to_add)
   return jsonify({ 'Teams': new_format })

@app.route('/kickers', methods=['GET'])
def get_kickers():
   cur = db_connect.cursor()
   cur.execute("SELECT * FROM kicker;")
   result = cur.fetchall()
   new_format = []
   for i in result:
      to_add = {'id': i[0], 'name': i[1], 'position': i[2], 'team_id': i[3]}
      new_format.append(to_add)
   return jsonify({ 'Kickers': new_format })

if __name__ == '__main__':
   app.run(port='3000')
