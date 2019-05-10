# index
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