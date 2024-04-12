create_tables_query = '''
    CREATE TABLE IF NOT EXISTS seasons (
        season_id INT PRIMARY KEY,
        season_name VARCHAR(9)
    );
    CREATE TABLE IF NOT EXISTS competitions (
        id SERIAL PRIMARY KEY,
        competition_id INT,
        season_id INT,
        country_name VARCHAR(255),
        competition_name VARCHAR(255),
        competition_gender VARCHAR(255),
        competition_youth BOOLEAN,
        competition_international BOOLEAN,
        season_name VARCHAR(9),
        FOREIGN KEY (season_id) REFERENCES seasons (season_id)
    );
    CREATE TABLE IF NOT EXISTS managers (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        nickname VARCHAR(255),
        dob DATE,
        country_name VARCHAR(255)     
    );
    CREATE TABLE IF NOT EXISTS teams (
        team_id INT PRIMARY KEY,
        team_name VARCHAR(255),
        team_gender VARCHAR(255),
        team_group VARCHAR(255),
        country_name VARCHAR(255),
        manager_id INT,
        FOREIGN KEY (manager_id) REFERENCES managers (id)
    );
    CREATE TABLE IF NOT EXISTS stadiums (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        country_name VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS referees (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        country_name VARCHAR(255)
    );
    CREATE TABLE IF NOT EXISTS matches (
        match_id INT PRIMARY KEY,
        match_date DATE,
        kick_off TIME,
        competition_id INT,
        season_id INT,
        home_team_id INT,
        away_team_id INT,
        home_score INT,
        away_score INT,
        match_week INT,
        competition_stage_name VARCHAR(255),
        stadium_id INT,
        referee_id INT,
        FOREIGN KEY (season_id) REFERENCES seasons (season_id),
        FOREIGN KEY (home_team_id) REFERENCES teams (team_id),
        FOREIGN KEY (away_team_id) REFERENCES teams (team_id),
        FOREIGN KEY (stadium_id) REFERENCES stadiums (id),
        FOREIGN KEY (referee_id) REFERENCES referees (id)
    );
    CREATE TABLE IF NOT EXISTS lineups (
        match_id INT,
        team_id INT,
        team_name VARCHAR(255),
        lineup INT[],
        FOREIGN KEY (match_id) REFERENCES matches (match_id)
    );
    CREATE TABLE IF NOT EXISTS players (
        match_id INT,
        player_id INT,
        player_name VARCHAR(255),
        player_nickname VARCHAR(255),
        jersey_number INT,
        country_name VARCHAR(255),
        cards INT[],
        positions INT[],
        PRIMARY KEY (match_id, player_id)
    );
    CREATE TABLE IF NOT EXISTS cards (
        match_id INT,
        player_id INT,
        card_id INT,
        time INTERVAL,
        card_type VARCHAR(255),
        reason VARCHAR(255),
        period INT,
        PRIMARY KEY (card_id),
        FOREIGN KEY (match_id) REFERENCES matches (match_id),
        FOREIGN KEY (match_id, player_id) REFERENCES players (match_id, player_id)
    );
    CREATE TABLE IF NOT EXISTS positions (
        match_id INT,
        player_id INT,
        position_id INT,
        position VARCHAR(255),
        from_time INTERVAL,
        to_time INTERVAL,
        from_period INT,
        to_period INT,
        start_reason VARCHAR(255),
        end_reason VARCHAR(255),
        FOREIGN KEY (match_id) REFERENCES matches (match_id),
        FOREIGN KEY (match_id, player_id) REFERENCES players (match_id, player_id)
    );
    CREATE TABLE IF NOT EXISTS events (
        id VARCHAR(255) PRIMARY KEY,
        match_id INT,
        index INT,
        period INT,
        timestamp TIME,
        minute INT,
        type_name VARCHAR(255),
        possession INT,
        possession_team_id INT,
        play_pattern_name VARCHAR(255),
        team_id INT,
        player_id INT,
        position_id INT,
        location DECIMAL[],
        duration DECIMAL(10, 5),
        under_pressure BOOLEAN,
        off_camera BOOLEAN,
        out BOOLEAN,
        related_events VARCHAR[],
        FOREIGN KEY (match_id) REFERENCES matches (match_id)
    );
    CREATE TABLE IF NOT EXISTS tactics (
        tactic_id VARCHAR(255) PRIMARY KEY,
        formation INT,
        lineup INT[]
    );
'''