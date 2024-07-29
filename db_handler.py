import psycopg2

# connect to the database
conn = psycopg2.connect(
    host="localhost", 
    port=5432,
    dbname="postgres",
    user="postgres",
    password="K0lade001."
)
cur = conn.cursor() # create a sursor for your database

# Write your queries here.
cur.execute(

    """
        CREATE TABLE IF NOT EXISTS person(
        id INT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        gender CHAR
        );
    """)

cur.execute(
    """
    INSERT INTO person (id, name, age, gender) VALUES 
    (1, 'Kolade Atanseiye', 24, 'M'),
    (2, 'Odun Atanseiye', 22, 'M'),
    (3, 'Mercy Atanseiye', 21, 'F'),
    (4, 'Lekan Atanseiye', 25, 'M'),
    (5, 'Tope Atanseiye', 24, 'M'),
    (6, 'Esther Atanseiye', 29, 'F');
    """
)

# cur.fetchone()

conn.commit() # commit all your changes

cur.close() #close the cursor
conn.close() #close the connection