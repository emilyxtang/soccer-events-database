def add_where_not_exists(table_name : str) -> str:
    return '''
        WHERE NOT EXISTS (
            SELECT 1
            FROM {table}
            WHERE event_id = %s
        );
    '''.format(table=table_name)

fifty_fifty_table = '''
    INSERT INTO 50_50_events (event_id, outcome_name, counterpress)
    SELECT
        %s AS event_id,
        %s AS outcome_name,
        %s AS counterpress
''' + add_where_not_exists('50_50_events')

bad_behaviour_table = '''
    INSERT INTO bad_behaviour_events (event_id, card_name)
    SELECT
        %s AS event_id,
        %s AS card_name
''' + add_where_not_exists('bad_behaviour_events')

ball_receipt_table = '''
    INSERT INTO (event_id, outcome_name)
    SELECT
        %s AS event_id,
        %s AS outcome_name
''' + add_where_not_exists('ball_receipt_events')

ball_recovery_table = '''
    INSERT INTO (event_id, offensive, recovery_failure)
    SELECT
        %s AS event_id,
        %s AS offensive,
        %s AS recovery_failure
''' + add_where_not_exists('ball_recovery_events')

block_table = '''
    INSERT INTO (event_id, deflection, offensive, save_block, counterpress)
    SELECT
        %s AS event_id,
        %s AS deflection,
        %s AS offensive,
        %s AS save_block,
        %s AS counterpress
''' + add_where_not_exists('block_events')

carry_table = '''
    INSERT INTO (event_id, end_location)
    SELECT
        %s AS event_id,
        %s AS end_location
''' + add_where_not_exists('carry_events')

clearance_table = '''
    INSERT INTO (event_id, aerial_won, body_part_name)
    SELECT
        %s AS event_id,
        %s AS aerial_won,
        %s AS body_part_name
''' + add_where_not_exists('clearance_events')

dribble_table = '''
    INSERT INTO (event_id, overrun, nutmeg, outcome_name, no_touch)
    SELECT
        %s AS event_id,
        %s AS overrun,
        %s AS nutmeg,
        %s AS outcome_name,
        %s AS no_touch
''' + add_where_not_exists('dribble_events')

dribbled_past_table = '''
    INSERT INTO (event_id, counterpress)
    SELECT
        %s AS event_id,
        %s AS counterpress
''' + add_where_not_exists('dribbled_past_events')

duel_table = '''
    INSERT INTO (event_id, counterpress, type_name, outcome_name)
    SELECT
        %s AS event_id,
        %s AS counterpress,
        %s AS type_name,
        %s AS outcome_name
''' + add_where_not_exists('duel_events')

foul_committed_table = '''
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

foul_won_table = '''
    INSERT INTO (event_id, defensive, offensive, penalty)
    SELECT
        %s AS event_id,
        %s AS defensive,
        %s AS offensive,
        %s AS penalty
''' + add_where_not_exists('foul_won_events')

goalkeeper_table = '''
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

half_end_table = '''
    INSERT INTO (event_id, early_video_end, match_suspended)
    SELECT
        %s AS event_id,
        %s AS early_video_end,
        %s AS match_suspended
''' + add_where_not_exists('half_end_events')

half_start_table = '''
    INSERT INTO (event_id, late_video_start)
    SELECT
        %s AS event_id,
        %s AS late_video_start
''' + add_where_not_exists('half_start_events')

injury_stoppage_table = '''
    INSERT INTO (event_id, in_chain)
    SELECT
        %s AS event_id,
        %s AS in_chain
''' + add_where_not_exists('injury_stoppage_events')

interception_table = '''
    INSERT INTO (event_id, outcome_name)
    SELECT
        %s AS event_id,
        %s AS outcome_name
''' + add_where_not_exists('interception_events')

miscontrol_table = '''
    INSERT INTO (event_id, aerial_won)
    SELECT
        %s AS event_id,
        %s AS aerial_won
''' + add_where_not_exists('miscontrol_events')

pass_table = '''
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

player_off_table = '''
    INSERT INTO (event_id, permanent)
    SELECT
        %s AS event_id,
        %s AS permanent
''' + add_where_not_exists('player_off_events')

pressure_table = '''
    INSERT INTO (event_id, counterpress)
    SELECT
        %s AS event_id,
        %s AS counterpress
''' + add_where_not_exists('pressure_events')

shot_table = '''
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

substitution_table = '''
    INSERT INTO (event_id, replacement_name, outcome_name)
    SELECT
        %s AS event_id,
        %s AS replacement_name,
        %s AS outcome_name
''' + add_where_not_exists('substitution_events')
