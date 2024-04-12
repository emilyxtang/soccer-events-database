# Created by Gabriel Martell

'''
Version 1.11 (04/02/2024)
=========================================================
queries.py (Carleton University COMP3005 - Database Management Student Template Code)

This is the template code for the COMP3005 Database Project 1, and must be accomplished on an Ubuntu Linux environment.
Your task is to ONLY write your SQL queries within the prompted space within each Q_# method (where # is the question number).

You may modify code in terms of testing purposes (commenting out a Qn method), however, any alterations to the code, such as modifying the time, 
will be flagged for suspicion of cheating - and thus will be reviewed by the staff and, if need be, the Dean. 

To review the Integrity Violation Attributes of Carleton University, please view https://carleton.ca/registrar/academic-integrity/ 

=========================================================
'''

# Imports
import psycopg
import csv
import subprocess
import os
import re

# Connection Information
''' 
The following is the connection information for this project. These settings are used to connect this file to the autograder.
You must NOT change these settings - by default, db_host, db_port and db_username are as follows when first installing and utilizing psql.
For the user "postgres", you must MANUALLY set the password to 1234.
'''
root_database_name = "project_database"
query_database_name = "query_database"
db_username = 'postgres'
# FIXME: CHANGE THIS BACK TO 1234
# db_password = '1234'
db_password = 'postgres'
db_host = 'localhost'
db_port = '5432'

# Directory Path - Do NOT Modify
dir_path = os.path.dirname(os.path.realpath(__file__))

# Loading the Database after Drop - Do NOT Modify
#================================================
def load_database(cursor, conn):
    drop_database(cursor, conn)

    # Create the Database if it DNE
    try:
        conn.autocommit = True
        cursor.execute(f"CREATE DATABASE {query_database_name};")
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        conn.autocommit = False
    conn.close()
    
    # Connect to this query database.
    dbname = query_database_name
    user = db_username
    password = db_password
    host = db_host
    port = db_port
    conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cursor = conn.cursor()
    
    # Import the dbexport.sql database data into this database
    try:
        command = f'psql -h {host} -U {user} -d {query_database_name} -a -f {os.path.join(dir_path, "dbexport.sql")}'
        env = {'PGPASSWORD': password}
        subprocess.run(command, shell=True, check=True, env=env)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while loading the database: {e}")
    
    # Return this connection.
    return conn    

# Dropping the Database after Query n Execution - Do NOT Modify
#================================================
def drop_database(cursor, conn):
    # Drop database if it exists.
    try:
        conn.autocommit = True
        cursor.execute(f"DROP DATABASE IF EXISTS {query_database_name};")
        conn.commit()
    except Exception as error:
        print(error)
        pass
    finally:
        conn.autocommit = False

# Reconnect to Root Database - Do NOT Modify
#================================================
def reconnect(cursor, conn):
    cursor.close()
    conn.close()

    dbname = root_database_name
    user = db_username
    password = db_password
    host = db_host
    port = db_port
    return psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Getting the execution time of the query through EXPLAIN ANALYZE - Do NOT Modify
#================================================
def get_time(cursor, conn, sql_query):
    # Prefix your query with EXPLAIN ANALYZE
    explain_query = f"EXPLAIN ANALYZE {sql_query}"

    try:
        # Execute the EXPLAIN ANALYZE query
        cursor.execute(explain_query)
        
        # Fetch all rows from the cursor
        explain_output = cursor.fetchall()
        
        # Convert the output tuples to a single string
        explain_text = "\n".join([row[0] for row in explain_output])
        
        # Use regular expression to find the execution time
        # Look for the pattern "Execution Time: <time> ms"
        match = re.search(r"Execution Time: ([\d.]+) ms", explain_text)
        if match:
            execution_time = float(match.group(1))
            return f"Execution Time: {execution_time} ms"
        else:
            print("Execution Time not found in EXPLAIN ANALYZE output.")
            return f"NA"
    except:
        print("[ERROR] Error getting time.")


# Write the results into some Q_n CSV. If the is an error with the query, it is a INC result - Do NOT Modify
#================================================
def write_csv(execution_time, cursor, conn, i):
    # Collect all data into this csv, if there is an error from the query execution, the resulting time is INC.
    try:
        colnames = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        filename = f"{dir_path}/Q_{i}.csv"

        with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Write column names to the CSV file
            csvwriter.writerow(colnames)
            
            # Write data rows to the CSV file
            csvwriter.writerows(rows)

    except Exception as error:
        execution_time[i-1] = "INC"
        print(error)
    
#================================================
        
'''
The following 10 methods, (Q_n(), where 1 < n < 10) will be where you are tasked to input your queries.
To reiterate, any modification outside of the query line will be flagged, and then marked as potential cheating.
Once you run this script, these 10 methods will run and print the times in order from top to bottom, Q1 to Q10 in the terminal window.
'''
def Q_1(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================
    # Enter QUERY within the quotes:

    # query = """ """

    query = '''
        SELECT p.name, AVG(s.statsbomb_xg) AS avg_xgScore
        FROM players p
        JOIN events e ON p.player_id = e.player_id
        JOIN matches m ON m.match_id = e.match_id
        JOIN competitions c ON c.competition_id = m.competition_id AND c.season_id = m.season_id
        JOIN shot_events s ON s.event_id = e.id
        WHERE c.competition_name = 'La Liga' AND c.season_name = '2020/2021' AND s.statsbomb_xg > 0
        GROUP BY p.player_name
        ORDER BY avg_xgScore DESC;
    '''

    # SELECT p.name, AVG(s.statsbomb_xg) AS avg_xgScore
    # FROM players p
    # JOIN events e ON p.player_id = e.player_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.competition_id = m.competition_id AND c.season_id = m.season_id
    # JOIN shot_events s ON s.event_id = e.id
    # WHERE c.competition_name = 'La Liga' AND c.season_name = '2020/2021' AND s.statsbomb_xg > 0
    # GROUP BY p.player_name
    # ORDER BY avg_xgScore DESC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[0] = (time_val)

    write_csv(execution_time, cursor, connection, 1)
    return reconnect(cursor, connection)

def Q_2(cursor, conn, execution_time):

    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:

    query = """ """

    # SELECT p.name, COUNT(*) AS num_shots
    # FROM players p
    # JOIN events e ON p.player_id = e.player_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.compeition_id = m.competition_id AND m.season_id = c.season_id
    # WHERE c.competition_name = 'La Liga' AND c.season_name = '2020/2021' 
    # AND e.event_type = 'Shot'
    # HAVING num_shots > 0
    # ORDER BY num_shots DESC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[1] = (time_val)

    write_csv(execution_time, cursor, connection, 2)
    return reconnect(cursor, connection)
    
def Q_3(cursor, conn, execution_time):

    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """ """

    # SELECT p.player_name, COUNT(*) AS num_first_shot
    # FROM players p
    # JOIN events e ON p.player_id = e.player_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.competition_id = m.competition_id AND m.season_id = c.season_id
    # JOIN shot_events s ON s.event_id = e.id
    # WHERE c.competition_name = 'La Liga'
    # AND c.season_name IN ('2020/2021','2019/2020','2019/2019')
    # AND s.first_time = TRUE
    # HAVING num_first_shot > 0
    # GROUP BY p.player_name
    # ORDER BY num_first_shot DESC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[2] = (time_val)

    write_csv(execution_time, cursor, connection, 3)
    return reconnect(cursor, connection)

def Q_4(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """ """

    # SELECT t.team_name. COUNT(*) AS num_passes
    # FROM teams t
    # JOIN events e ON e.team_id = t.team_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.competition_id = m.competition_id AND m.season_id = c.season_id
    # WHERE c.competition_name = 'La Liga' AND c.season_name = '2020/2021' 
    # AND e.event_type = 'Pass'
    # HAVING num_passes > 0
    # GROUP BY t.team_name
    # ORDER BY num_passes DESC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[3] = (time_val)

    write_csv(execution_time, cursor, connection, 4)
    return reconnect(cursor, connection)

def Q_5(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """ """

    # SELECT p.player_name, COUNT(*) AS num_receive_passes
    # FROM players p
    # JOIN events e ON e.team_id = t.team_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.competition_id = m.competition_id AND m.season_id = c.season_id
    # JOIN pass_events pe ON pe.event_id = e.id
    # WHERE c.competition_name = 'Premier League' AND c.season_name = '2003/2004'
    # AND pe.recipient_id = p.player_id
    # HAVING num_receive_passes > 0
    # GROUP BY p.player_name
    # ORDER BY num_receive_passes DESC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[4] = (time_val)

    write_csv(execution_time, cursor, connection, 5)
    return reconnect(cursor, connection)

def Q_6(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """ """

    # SELECT t.team_name, COUNT(*) as num_shots
    # FROM teams t
    # JOIN events e ON e.team_id = t.team_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.competition_id = m.competition_id AND m.season_id = c.season_id
    # WHERE c.competition_name = 'Premier League' AND c.season_name = '2003/2004'
    # AND e.event_type = 'Shot'
    # HAVING num_shots > 0
    # GROUP BY t.team_name
    # ORDER BY num_shots DESC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[5] = (time_val)

    write_csv(execution_time, cursor, connection, 6)
    return reconnect(cursor, connection)

def Q_7(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """ """

    # SELECT p.player_name, COUNT(*) num_through_balls
    # FROM players p
    # JOIN events e ON e.team_id = t.team_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.competition_id = m.competition_id AND m.season_id = c.season_id
    # JOIN pass_events pe ON pe.event_id = e.id
    # WHERE c.competition_name = 'La Liga' AND c.season_name = '2020/2021'
    # AND pe.technique_name = "Through Ball"
    # HAVING num_through_balls > 0
    # GROUP BY p.player_name
    # ORDER BY num_through_balls DESC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[6] = (time_val)

    write_csv(execution_time, cursor, connection, 7)
    return reconnect(cursor, connection)

def Q_8(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """ """

    # SELECT t.team_name, COUNT(*) AS num_through_balls
    # FROM teams t
    # JOIN events e ON e.team_id = t.team_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.competition_id = m.competition_id AND m.season_id = c.season_id
    # JOIN pass_events pe ON pe.event_id = e.id
    # WHERE c.competition_name = 'La Liga' AND c.season_name = '2020/2021'
    # AND pe.technique_name = "Through Ball"
    # HAVING num_through_balls > 0
    # GROUP BY t.team_name
    # ORDER BY num_through_balls DESC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[7] = (time_val)

    write_csv(execution_time, cursor, connection, 8)
    return reconnect(cursor, connection)

def Q_9(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """ """

    # SELECT p.player_name, COUNT(*) AS num_dribble
    # FROM players p
    # JOIN events e ON e.team_id = t.team_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.competition_id = m.competition_id AND m.season_id = c.season_id
    # JOIN dribble_events d ON d.event_id = e.id
    # WHERE c.competition_name = 'La Liga'
    # AND c.season_name IN ('2020/2021','2019/2020','2019/2019')
    # AND d.outcome_name = 'Completed'
    # HAVING num_dribble > 0
    # GROUP BY p.player_name
    # ORDER BY num_dribble DESC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[8] = (time_val)

    write_csv(execution_time, cursor, connection, 9)
    return reconnect(cursor, connection)

def Q_10(cursor, conn, execution_time):
    connection = load_database(cursor, conn)
    cursor = connection.cursor()

    #==========================================================================    
    # Enter QUERY within the quotes:
    
    query = """ """

    # SELECT p.player_name, COUNT(*) AS num_dribbled_past
    # FROM players p
    # JOIN events e ON e.team_id = t.team_id
    # JOIN matches m ON m.match_id = e.match_id
    # JOIN competitions c ON c.competition_id = m.competition_id AND m.season_id = c.season_id
    # WHERE c.competition_name = 'La Liga'
    # AND c.season_name = '2020/2021'
    # AND e.event_type = 'Dribbled Past'
    # HAVING num_dribbled_past > 0
    # GROUP BY p.player_name
    # ORDER BY num_dribbled_past ASC;

    #==========================================================================

    time_val = get_time(cursor, connection, query)
    cursor.execute(query)
    execution_time[9] = (time_val)

    write_csv(execution_time, cursor, connection, 10)
    return reconnect(cursor, connection)

# Running the queries from the Q_n methods - Do NOT Modify
#=====================================================
def run_queries(cursor, conn, dbname):

    execution_time = [0,0,0,0,0,0,0,0,0,0]

    conn = Q_1(cursor, conn, execution_time)
    conn = Q_2(cursor, conn, execution_time)
    conn = Q_3(cursor, conn, execution_time)
    conn = Q_4(cursor, conn, execution_time)
    conn = Q_5(cursor, conn, execution_time)
    conn = Q_6(cursor, conn, execution_time)
    conn = Q_7(cursor, conn, execution_time)
    conn = Q_8(cursor, conn, execution_time)
    conn = Q_9(cursor, conn, execution_time)
    conn = Q_10(cursor, conn, execution_time)

    for i in range(10):
        print(execution_time[i])

''' MAIN '''
try:
    if __name__ == "__main__":

        dbname = root_database_name
        user = db_username
        password = db_password
        host = db_host
        port = db_port

        conn = psycopg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cursor = conn.cursor()
        
        run_queries(cursor, conn, dbname)
except Exception as error:
    print(error)
    #print("[ERROR]: Failure to connect to database.")
#_______________________________________________________