import psycopg2

conn = psycopg2.connect(
   database = 'pp_db',
   user = 'harryturner',
   password = 'Honeyjerry16',
   host = 'localhost',
   port = '5432'
)

print('Connected!!')

