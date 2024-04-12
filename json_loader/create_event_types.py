create_fifty_fifty_table = '''
    CREATE TABLE IF NOT EXISTS "50_50_events" (
        event_id UUID PRIMARY KEY,
        outcome_name VARCHAR(255),
        counterpress BOOLEAN
    );
'''

create_bad_behaviour_table = '''
    CREATE TABLE IF NOT EXISTS bad_behaviour_events (
        event_id UUID PRIMARY KEY,
        card_name VARCHAR(255)
    );
'''

create_ball_receipt_table = '''
    CREATE TABLE IF NOT EXISTS ball_receipt_events (
        event_id UUID PRIMARY KEY,
        outcome_name VARCHAR(255)
    );
'''

create_ball_recovery_table = '''
    CREATE TABLE IF NOT EXISTS ball_recovery_events (
        event_id UUID PRIMARY KEY,
        offensive BOOLEAN,
        recovery_failure BOOLEAN
    );
'''

create_block_table = '''
    CREATE TABLE IF NOT EXISTS block_events (
        event_id UUID PRIMARY KEY,
        deflection BOOLEAN,
        offensive BOOLEAN,
        save_block BOOLEAN,
        counterpress BOOLEAN
    );
'''

create_carry_table = '''
    CREATE TABLE IF NOT EXISTS carry_events (
        event_id UUID PRIMARY KEY,
        end_location INT[]
    );
'''

create_clearance_table = '''
    CREATE TABLE IF NOT EXISTS clearance_events (
        event_id UUID PRIMARY KEY,
        aerial_won BOOLEAN,
        body_part_name VARCHAR(255)   
    );
'''

create_dribble_table = '''
    CREATE TABLE IF NOT EXISTS dribble_events (
        event_id UUID PRIMARY KEY,
        overrun BOOLEAN,
        nutmeg BOOLEAN,
        outcome_name VARCHAR(255),
        no_touch BOOLEAN
    );
'''

create_dribbled_past_table = '''
    CREATE TABLE IF NOT EXISTS dribbled_past_events (
        event_id UUID PRIMARY KEY,
        counterpress BOOLEAN
    );
'''

create_duel_table = '''
    CREATE TABLE IF NOT EXISTS duel_events (
        event_id UUID PRIMARY KEY,
        counterpress BOOLEAN,
        type_name VARCHAR(255),
        outcome_name VARCHAR(255)
    );
'''

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

create_foul_won_table = '''
    CREATE TABLE IF NOT EXISTS foul_won_events (
        event_id UUID PRIMARY KEY,
        defensive BOOLEAN,
        offensive BOOLEAN,
        penalty BOOLEAN
    );
'''

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

create_half_end_table = '''
    CREATE TABLE IF NOT EXISTS half_end_events (
        event_id UUID PRIMARY KEY,
        early_video_end BOOLEAN,
        match_suspended BOOLEAN
    );
'''

create_half_start_table = '''
    CREATE TABLE IF NOT EXISTS half_start_events (
        event_id UUID PRIMARY KEY,
        late_video_start BOOLEAN
    );
'''

create_injury_stoppage_table = '''
    CREATE TABLE IF NOT EXISTS injury_stoppage_events (
        event_id UUID PRIMARY KEY,
        in_chain BOOLEAN
    );
'''

create_interception_table = '''
    CREATE TABLE IF NOT EXISTS interception_events (
        event_id UUID PRIMARY KEY,
        outcome_name VARCHAR(255)
    );
'''

create_miscontrol_table = '''
    CREATE TABLE IF NOT EXISTS miscontrol_events (
        event_id UUID PRIMARY KEY,
        aerial_won BOOLEAN
    );
'''

create_pass_table = '''
    CREATE TABLE IF NOT EXISTS pass_events (
        event_id UUID PRIMARY KEY,
        recipient_id INT,
        length DECIMAL(10, 5),
        angle DECIMAL(10, 5),
        height_name VARCHAR(255),
        end_location DECIMAL[],
        assisted_shot_id UUID,
        backheel BOOLEAN,
        deflected BOOLEAN,
        miscommunication BOOLEAN,
        "cross" BOOLEAN,
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

create_player_off_table = '''
    CREATE TABLE IF NOT EXISTS player_off_events (
        event_id UUID PRIMARY KEY,
        permanent BOOLEAN
    );
'''

create_pressure_table = '''
    CREATE TABLE IF NOT EXISTS pressure_events (
        event_id UUID PRIMARY KEY,
        counterpress BOOLEAN
    );
'''

create_shot_table = '''
    CREATE TABLE IF NOT EXISTS shot_events (
        event_id UUID PRIMARY KEY,
        key_pass_id UUID,
        end_location DECIMAL[],
        aerial_won BOOLEAN,
        follows_dribble BOOLEAN,
        first_time BOOLEAN,
        freeze_frame JSONB,
        open_goal BOOLEAN,
        statsbomb_xg DECIMAL(10, 5),
        deflected BOOLEAN,
        technique_name VARCHAR(255),
        body_part_name VARCHAR(255),
        type_name VARCHAR(255),
        outcome_name VARCHAR(255)
    );
'''

create_substitution_table = '''
    CREATE TABLE IF NOT EXISTS substitution_events (
        event_id UUID PRIMARY KEY,
        replacement_name VARCHAR(255),
        outcome_name VARCHAR(255)
    );
'''

event_type_tables_query = create_fifty_fifty_table \
    + create_bad_behaviour_table + create_ball_receipt_table \
    + create_ball_recovery_table + create_block_table \
    + create_carry_table + create_clearance_table + create_dribble_table \
    + create_dribbled_past_table + create_duel_table \
    + create_foul_committed_table + create_foul_won_table \
    + create_goalkeeper_table + create_half_end_table \
    + create_half_start_table + create_injury_stoppage_table \
    + create_interception_table + create_miscontrol_table \
    + create_pass_table + create_player_off_table + create_pressure_table \
    + create_shot_table + create_substitution_table
