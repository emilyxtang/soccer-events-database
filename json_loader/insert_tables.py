seasons_query = '''
    INSERT INTO seasons (season_id, season_name)
    SELECT
        %s AS season_id,
        %s AS season_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM seasons
        WHERE season_id = %s
    );
'''

competitions_query = '''
    INSERT INTO competitions (competition_id, season_id, country_name,
    competition_name, competition_gender, competition_youth,
    competition_international, season_name)
    SELECT
        %s AS competition_id,
        %s AS season_id,
        %s AS country_name,
        %s AS competition_name,
        %s AS competition_gender,
        %s AS competition_youth,
        %s AS competition_international,
        %s AS season_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM competitions
        WHERE season_name = %s
    );
'''

managers_query = '''
    INSERT INTO managers (id, name, nickname, dob, country_name)
    SELECT
        %s AS id,
        %s AS name,
        %s AS nickname,
        %s AS dob,
        %s AS country_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM managers
        WHERE id = %s
    )
'''

teams_query = '''
    INSERT INTO teams (team_id, team_name, team_gender, team_group,
    country_name, manager_id)
    SELECT
        %s AS team_id,
        %s AS team_name,
        %s AS team_gender,
        %s AS team_group,
        %s AS country_name,
        %s AS manager_id
    WHERE NOT EXISTS (
        SELECT 1
        FROM teams
        WHERE team_id = %s
    )
'''

stadiums_query = '''
    INSERT INTO stadiums (id, name, country_name)
    SELECT
        %s AS id,
        %s AS name,
        %s AS country_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM stadiums
        WHERE id = %s
    )
'''

referees_query = '''
    INSERT INTO referees (id, name, country_name)
    SELECT
        %s AS id,
        %s AS name,
        %s AS country_name
    WHERE NOT EXISTS (
        SELECT 1
        FROM referees
        WHERE id = %s
    )
'''

matches_query = '''
    INSERT INTO matches (match_id, match_date, kick_off, competition_id,
    season_id, home_team_id, away_team_id, home_score, away_score, match_week,
    competition_stage_name, stadium_id, referee_id)
    SELECT
        %s AS match_id,
        %s AS match_date,
        %s AS kick_off,
        %s AS competition_id,
        %s AS season_id,
        %s AS home_team_id,
        %s AS away_team_id,
        %s AS home_score,
        %s AS away_score,
        %s AS match_week,
        %s AS competition_stage_name,
        %s AS stadium_id,
        %s AS referee_id
    WHERE NOT EXISTS (
        SELECT 1
        FROM matches
        WHERE match_id = %s
    );
'''

lineups_query = '''
    INSERT INTO lineups (match_id, team_id, team_name, lineup)
    SELECT
        %s AS match_id,
        %s AS team_id,
        %s AS team_name,
        %s AS lineup
    WHERE NOT EXISTS (
        SELECT 1
        FROM lineups
        WHERE match_id = %s AND team_id = %s
    );
'''

players_query = '''
    INSERT INTO players (match_id, player_id, player_name, player_nickname,
    jersey_number, country_name, cards, positions)
    SELECT
        %s AS match_id,
        %s AS player_id,
        %s AS player_name,
        %s AS player_nickname,
        %s AS jersey_number,
        %s AS country_name,
        %s AS cards,
        %s AS positions
    WHERE NOT EXISTS (
        SELECT 1
        FROM players
        WHERE match_id = %s AND player_id = %s
    );
'''

cards_query = '''
    INSERT INTO cards (match_id, player_id, card_id, time, card_type, reason,
    period)
    SELECT
        %s AS match_id,
        %s AS player_id,
        %s AS card_id,
        %s AS time,
        %s AS card_type,
        %s AS reason,
        %s AS period
    WHERE NOT EXISTS (
        SELECT 1
        FROM cards
        WHERE match_id = %s AND player_id = %s AND card_id = %s
    )
'''

positions_query = '''
    INSERT INTO positions (match_id, player_id, position_id, position,
    from_time, to_time, from_period, to_period, start_reason, end_reason)
    SELECT
        %s AS match_id,
        %s AS player_id,
        %s AS position_id,
        %s AS position,
        %s AS from_time,
        %s AS to_time,
        %s AS from_period,
        %s AS to_period,
        %s AS start_reason,
        %s AS end_reason
    WHERE NOT EXISTS (
        SELECT 1
        FROM positions
        WHERE match_id = %s AND player_id = %s AND position_id = %s
    )
'''

events_query = '''
    INSERT INTO events (id, match_id, index, period, timestamp, minute,
    type_name, possession, possession_team_id, play_pattern_name, team_id,
    player_id, position_id, location, duration, under_pressure, off_camera,
    out, related_events)
    SELECT
        %s AS id,
        %s AS match_id,
        %s AS index,
        %s AS period,
        %s AS timestamp,
        %s AS minute,
        %s AS type_name,
        %s AS possession,
        %s AS possession_team_id,
        %s AS play_pattern_name,
        %s AS team_id,
        %s AS player_id,
        %s AS position_id,
        %s AS location,
        %s AS duration,
        %s AS under_pressure,
        %s AS off_camera,
        %s AS out,
        %s AS related_events
    WHERE NOT EXISTS (
        SELECT 1
        FROM events
        WHERE id = %s
    )
'''

tactics_query = '''
    INSERT INTO tactics (tactic_id, formation, lineup)
    SELECT (
        %s AS tactic_id,
        %s AS formation,
        %s AS lineup
    )
    WHERE NOT EXISTS (
        SELECT 1
        FROM tactics
        WHERE tactic_id = %s
    )
'''
