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

# --------------------- team routes ----------------------
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

# --------------- kicker routes -----------------------
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


# --------------- game_week routes -------------------
@app.route('/gameweeks', methods=['GET'])
def get_game_weeks():
   cur = db_connect.cursor()
   cur.execute("SELECT * FROM game_week;")
   result = cur.fetchall()
   new_format = []
   for i in result:
      matches = get_game_week_matches(i[0])
      to_add = {'id': i[0], 'week_number': i[1], 'matches': matches}
      new_format.append(to_add)

   response = jsonify(new_format)
   response.status_code = 200
   return response

@app.route('/gameweek/<week_number>', methods=['GET'])
def get_week_matches(week_number):
   cur = db_connect.cursor()
   cur.execute( "SELECT * FROM match WHERE game_week_id = " + str(get_game_week_id(week_number)) )
   result = cur.fetchall()
   new_format = []
   for i in result:
      to_add = { 'id': i[0], 'home_team': get_team_name(i[1]), 'away_team': get_team_name(i[2]), 'home_score': i[3], 'away_score': i[4] }
      new_format.append(to_add)

   response = jsonify(new_format)
   response.status_code = 200
   return response

def get_game_week_matches(id):
   cur = db_connect.cursor()
   cur.execute( "SELECT home_team_id, away_team_id, home_score, away_score FROM match WHERE game_week_id = " + str(id) )
   result = cur.fetchall()
   new_format = []
   for i in result:
      to_add = { 'home_team': get_team_name(i[0]), 'away_team': get_team_name(i[1]), 'home_score': i[2], 'away_score': i[3] }
      new_format.append(to_add)

   return new_format

def get_team_name(id):
   cur = db_connect.cursor()
   cur.execute( "SELECT name FROM team WHERE id = " + str(id) )
   result = cur.fetchone()
   return result[0]

def get_game_week_id(week_number):
   cur = db_connect.cursor()
   cur.execute( "SELECT id FROM game_week WHERE number = " + str(week_number) )
   result = cur.fetchone()
   return result[0]

# ------------------ match routes -------------------
@app.route('/matches', methods=['GET'])
def get_matches():
   cur = db_connect.cursor()
   cur.execute( "SELECT * FROM match;" ) 
   result = cur.fetchall() 
   new_format = []
   for i in result:
      team_kickers = get_team_kickers(i[0])
      to_add = {'id': i[0], 'home_team': get_team_name(i[1]), 'away_team': get_team_name(i[2]), 'home_score': i[3], 'away_score': i[4]}
      new_format.append(to_add)

   response = jsonify(new_format)
   response.status_code = 200
   return response

@app.route('/matches/<id>', methods=['GET'])
def get_match(id):
   cur = db_connect.cursor()
   cur.execute( "SELECT * FROM match WHERE id = " + str(id) ) 
   result = cur.fetchone() 
   match_kicks = get_match_kicks(id)
   new_format = {'id': result[0], 'home_team': get_team_name(result[1]), 'away_team': get_team_name(result[2]), 'home_score': result[3], 'away_score': result[4], 'kicks': match_kicks}

   response = jsonify(new_format)
   response.status_code = 200
   return response

def get_match_kicks(match_id):
   cur = db_connect.cursor()
   cur.execute( "SELECT kicker_id, successful, distance, angle, pressure_score FROM kick WHERE match_id = " + str(match_id) )
   result = cur.fetchall()
   new_format = []
   for i in result:
      to_add = { 'kicker': get_kicker_name(i[0]), 'successful': i[1], 'distance': i[2], 'angle': i[3], 'pressure_score': i[4] }
      new_format.append(to_add)

   return new_format

def get_kicker_name(id):
   cur = db_connect.cursor()
   cur.execute( "SELECT name FROM kicker WHERE id = " + str(id) )
   result = cur.fetchone()
   return result[0]


if __name__ == '__main__':
   app.run(port='3000')
