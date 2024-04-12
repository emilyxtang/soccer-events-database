def add_where_not_exists(table_name : str) -> str:
    return '''
        WHERE NOT EXISTS (
            SELECT 1
            FROM {table}
            WHERE event_id = %s
        );
    '''.format(table=table_name)

create_50_50_table = '''
    CREATE TABLE IF NOT EXISTS 50_50_events (
        event_id UUID PRIMARY KEY,
        outcome_name VARCHAR(255),
        counterpress BOOLEAN
    );
'''

insert_50_50_table = '''
    INSERT INTO 50_50_events (event_id, outcome_name, counterpress)
    SELECT
        %s AS event_id,
        %s AS outcome_name,
        %s AS counterpress
''' + add_where_not_exists('50_50_events')

create_bad_behaviour_table = '''
    CREATE TABLE IF NOT EXISTS bad_behaviour_events (
        event_id UUID PRIMARY KEY,
        card_name VARCHAR(255)
    );
'''

insert_bad_behaviour_table = '''
    INSERT INTO bad_behaviour_events (event_id, card_name)
    SELECT
        %s AS event_id,
        %s AS card_name
''' + add_where_not_exists('bad_behaviour_events')

create_ball_receipt_table = '''
    CREATE TABLE IF NOT EXISTS ball_receipt_events (
        event_id UUID PRIMARY KEY,
        outcome_name VARCHAR(255)
    );
'''

insert_ball_receipt_table = '''
    INSERT INTO (event_id, outcome_name)
    SELECT
        %s AS event_id,
        %s AS outcome_name
''' + add_where_not_exists('ball_receipt_events')

create_ball_recovery_table = '''
    CREATE TABLE IF NOT EXISTS ball_recovery_events (
        event_id UUID PRIMARY KEY,
        offensive BOOLEAN,
        recovery_failure BOOLEAN
    );
'''

insert_ball_recovery_table = '''
    INSERT INTO (event_id, offensive, recovery_failure)
    SELECT
        %s AS event_id,
        %s AS offensive,
        %s AS recovery_failure
''' + add_where_not_exists('ball_recovery_events')

create_block_table = '''
    CREATE TABLE IF NOT EXISTS block_events (
        event_id UUID PRIMARY KEY,
        deflection BOOLEAN,
        offensive BOOLEAN,
        save_block BOOLEAN,
        counterpress BOOLEAN
    );
'''

insert_block_table = '''
    INSERT INTO (event_id, deflection, offensive, save_block, counterpress)
    SELECT
        %s AS event_id,
        %s AS deflection,
        %s AS offensive,
        %s AS save_block,
        %s AS counterpress
''' + add_where_not_exists('block_events')

create_carry_table = '''
    CREATE TABLE IF NOT EXISTS carry_events (
        event_id UUID PRIMARY KEY,
        end_location INT[]
    );
'''

insert_carry_table = '''
    INSERT INTO (event_id, end_location)
    SELECT
        %s AS event_id,
        %s AS end_location
''' + add_where_not_exists('carry_events')

create_clearance_table = '''
    CREATE TABLE IF NOT EXISTS clearance_events (
        event_id UUID PRIMARY KEY,
        aerial_won BOOLEAN,
        body_part_name VARCHAR(255)   
    );
'''

insert_clearance_table = '''
    INSERT INTO (event_id, aerial_won, body_part_name)
    SELECT
        %s AS event_id,
        %s AS aerial_won,
        %s AS body_part_name
''' + add_where_not_exists('clearance_events')

create_dribble_table = '''
    CREATE TABLE IF NOT EXISTS dribble_events (
        event_id UUID PRIMARY KEY,
        overrun BOOLEAN,
        nutmeg BOOLEAN,
        outcome_name VARCHAR(255),
        no_touch BOOLEAN
    );
'''

insert_dribble_table = '''
    INSERT INTO (event_id, overrun, nutmeg, outcome_name, no_touch)
    SELECT
        %s AS event_id,
        %s AS overrun,
        %s AS nutmeg,
        %s AS outcome_name,
        %s AS no_touch
''' + add_where_not_exists('dribble_events')

create_dribbled_past_table = '''
    CREATE TABLE IF NOT EXISTS dribbled_past_events (
        event_id UUID PRIMARY KEY,
        counterpress BOOLEAN
    );
'''

insert_dribbled_past_table = '''
    INSERT INTO (event_id, counterpress)
    SELECT
        %s AS event_id,
        %s AS counterpress
''' + add_where_not_exists('dribbled_past_events')

create_duel_table = '''
    CREATE TABLE IF NOT EXISTS duel_events (
        event_id UUID PRIMARY KEY,
        counterpress BOOLEAN,
        type_name VARCHAR(255),
        outcome_name VARCHAR(255)
    );
'''

insert_duel_table = '''
    INSERT INTO (event_id, counterpress, type_name, outcome_name)
    SELECT
        %s AS event_id,
        %s AS counterpress,
        %s AS type_name,
        %s AS outcome_name
''' + add_where_not_exists('duel_events')

create_foul_committed_table = '''
    CREATE TABLE IF NOT EXISTS foul_committed_events (
        event_id UUID PRIMARY KEY,
        counterpress BOOLEAN,
        offensive BOOLEAN,
        type_name VARCHAR(255),
        advantage BOOLEAN,
        penalty BOOLEAN,
        card_name VARCHAR(255)
    );
'''

insert_foul_committed_table = '''
    INSERT INTO (event_id, counterpress, offensive, type_name, advantage,
    penalty, card_name)
    SELECT
        %s AS event_id,
        %s AS counterpress,
        %s AS offensive,
        %s AS type_name,
        %s AS advantage,
        %s AS penalty,
        %s AS card_name
''' + add_where_not_exists('foul_committed_events')

create_foul_won_table = '''
    CREATE TABLE IF NOT EXISTS foul_won_events (
        event_id UUID PRIMARY KEY,
        defensive BOOLEAN,
        offensive BOOLEAN,
        penalty BOOLEAN
    );
'''

insert_foul_won_table = '''
    INSERT INTO (event_id, defensive, offensive, penalty)
    SELECT
        %s AS event_id,
        %s AS defensive,
        %s AS offensive,
        %s AS penalty
''' + add_where_not_exists('foul_won_events')

create_goalkeeper_table = '''
    CREATE TABLE IF NOT EXISTS goalkeeper_events (
        event_id UUID PRIMARY KEY,
        position_name VARCHAR(255),
        technique_name VARCHAR(255),
        body_part_name VARCHAR(255),
        type_name VARCHAR(255),
        outcome_name VARCHAR(255)
    );
'''

insert_goalkeeper_table = '''
    INSERT INTO (event_id, position_name, technique_name, body_part_name,
    type_name, outcome_name)
    SELECT
        %s AS event_id,
        %s AS position_name,
        %s AS technique_name,
        %s AS body_part_name,
        %s AS type_name,
        %s AS outcome_name
''' + add_where_not_exists('goalkeeper_events')

create_half_end_table = '''
    CREATE TABLE IF NOT EXISTS half_end_events (
        event_id UUID PRIMARY KEY,
        early_video_end BOOLEAN,
        match_suspended BOOLEAN
    );
'''

insert_half_end_table = '''
    INSERT INTO (event_id, early_video_end, match_suspended)
    SELECT
        %s AS event_id,
        %s AS early_video_end,
        %s AS match_suspended
''' + add_where_not_exists('half_end_events')

create_half_start_table = '''
    CREATE TABLE IF NOT EXISTS half_start_events (
        event_id UUID PRIMARY KEY,
        late_video_start BOOLEAN
    );
'''

insert_half_start_table = '''
    INSERT INTO (event_id, late_video_start)
    SELECT
        %s AS event_id,
        %s AS late_video_start
''' + add_where_not_exists('half_start_events')

create_injury_stoppage_table = '''
    CREATE TABLE IF NOT EXISTS injury_stoppage_events (
        event_id UUID PRIMARY KEY,
        in_chain BOOLEAN
    );
'''

insert_injury_stoppage_table = '''
    INSERT INTO (event_id, in_chain)
    SELECT
        %s AS event_id,
        %s AS in_chain
''' + add_where_not_exists('injury_stoppage_events')

create_interception_table = '''
    CREATE TABLE IF NOT EXISTS interception_events (
        event_id UUID PRIMARY KEY,
        outcome_name VARCHAR(255)
    );
'''

insert_interception_table = '''
    INSERT INTO (event_id, outcome_name)
    SELECT
        %s AS event_id,
        %s AS outcome_name
''' + add_where_not_exists('interception_events')

create_miscontrol_table = '''
    CREATE TABLE IF NOT EXISTS miscontrol_events (
        event_id UUID PRIMARY KEY,
        aerial_won BOOLEAN
    );
'''

insert_miscontrol_table = '''
    INSERT INTO (event_id, aerial_won)
    SELECT
        %s AS event_id,
        %s AS aerial_won
''' + add_where_not_exists('miscontrol_events')

create_pass_table = '''
    CREATE TABLE IF NOT EXISTS pass_events (
        event_id UUID PRIMARY KEY,
        recipient_id INT,
        length DECIMAL(10, 10),
        angle DECIMAL(10, 10),
        height_name VARCHAR(255),
        end_location INT[],
        assisted_shot_id UUID,
        backheel BOOLEAN,
        deflected BOOLEAN,
        miscommunication BOOLEAN,
        cross BOOLEAN,
        cut_back BOOLEAN,
        switch BOOLEAN,
        shot_assist BOOLEAN,
        goal_assist BOOLEAN,
        body_part_name VARCHAR(255),
        type_name VARCHAR(255),
        outcome_name VARCHAR(255),
        technique_name VARCHAR(255)
    );
'''

insert_pass_table = '''
    INSERT INTO (event_id, recipient_id, length, angle, height_name,
    end_location, assisted_shot_id, backheel, deflected, miscommunication,
    cross, cut_back, switch, shot_assist, goal_assist, body_part_name,
    type_name, outcome_name, technique_name)
    SELECT
        %s AS event_id,
        %s AS recipient_id,
        %s AS length,
        %s AS angle,
        %s AS height_name,
        %s AS end_location,
        %s AS assisted_shot_id,
        %s AS backheel,
        %s AS deflected,
        %s AS miscommunication,
        %s AS cross,
        %s AS cut_back,
        %s AS switch,
        %s AS shot_assist,
        %s AS goal_assist,
        %s AS body_part_name,
        %s AS type_name,
        %s AS outcome_name,
        %s AS technique_name
''' + add_where_not_exists('pass_events')

create_player_off_table = '''
    CREATE TABLE IF NOT EXISTS player_off_events (
        event_id UUID PRIMARY KEY,
        permanent BOOLEAN
    );
'''

insert_player_off_table = '''
    INSERT INTO (event_id, permanent)
    SELECT
        %s AS event_id,
        %s AS permanent
''' + add_where_not_exists('player_off_events')

create_pressure_table = '''
    CREATE TABLE IF NOT EXISTS pressure_events (
        event_id UUID PRIMARY KEY,
        counterpress BOOLEAN
    );
'''

insert_pressure_table = '''
    INSERT INTO (event_id, counterpress)
    SELECT
        %s AS event_id,
        %s AS counterpress
''' + add_where_not_exists('pressure_events')

create_shot_table = '''
    CREATE TABLE IF NOT EXISTS shot_events (
        event_id UUID PRIMARY KEY,
        key_pass_id UUID,
        end_location INT[],
        aerial_won BOOLEAN,
        follows_dribble BOOLEAN,
        first_time BOOLEAN,
        freeze_frame JSONB,
        open_goal BOOLEAN,
        statsbomb_xg DECIMAL(10, 10),
        deflected BOOLEAN,
        technique_name VARCHAR(255),
        body_part_name VARCHAR(255),
        type_name VARCHAR(255),
        outcome_name VARCHAR(255)
    );
'''

insert_shot_table = '''
    INSERT INTO (event_id, key_pass_id, end_location, aerial_won,
    follows_dribble, first_time, freeze_frame, open_goal, statsbomb_xg,
    deflected, technique_name, body_part_name, type_name, outcome_name)
    SELECT
        %s AS event_id,
        %s AS key_pass_id,
        %s AS end_location,
        %s AS aerial_won,
        %s AS follows_dribble,
        %s AS first_time,
        %s AS freeze_frame,
        %s AS open_goal,
        %s AS statsbomb_xg,
        %s AS deflected,
        %s AS technique_name,
        %s AS body_part_name,
        %s AS type_name,
        %s AS outcome_name
''' + add_where_not_exists('shot_events')

create_substitution_table = '''
    CREATE TABLE IF NOT EXISTS substitution_events (
        event_id UUID PRIMARY KEY,
        replacement_name VARCHAR(255),
        outcome_name VARCHAR(255)
    );
'''

insert_substitution_table = '''
    INSERT INTO (event_id, replacement_name, outcome_name)
    SELECT
        %s AS event_id,
        %s AS replacement_name,
        %s AS outcome_name
''' + add_where_not_exists('substitution_events')

create_event_type_tables = create_50_50_table + create_bad_behaviour_table \
    + create_ball_receipt_table + create_ball_recovery_table \
    + create_block_table + create_carry_table + create_clearance_table \
    + create_dribble_table + create_dribbled_past_table + create_duel_table \
    + create_foul_committed_table + create_foul_won_table \
    + create_goalkeeper_table + create_half_end_table \
    + create_half_start_table + create_injury_stoppage_table \
    + create_interception_table + create_miscontrol_table \
    + create_pass_table + create_player_off_table + create_pressure_table \
    + create_shot_table + create_substitution_table
