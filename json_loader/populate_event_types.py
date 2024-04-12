import psycopg2

import insert_event_types as insert

# connect to PostgreSQL database
conn = psycopg2.connect(
    dbname='project_database',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)

cur = conn.cursor() # a cursor object to execute SQL commands

def _populate_fifty_fifty(event_id : str, fifty_fifty : dict):
    counterpress = None
    if 'counterpress' in fifty_fifty:
        counterpress = fifty_fifty['counterpress']
    fifty_fifty_values = (event_id, fifty_fifty['outcome']['name'],
                          counterpress, event_id)
    cur.execute(insert.fifty_fifty_table, fifty_fifty_values)

def _populate_bad_behaviour(event_id : str, bad_behaviour : dict):
    bad_behaviour_values = (event_id, bad_behaviour['card']['name'], event_id)
    cur.execute(insert.bad_behaviour_table, bad_behaviour_values)

def _populate_ball_receipt(event_id : str, ball_receipt : dict) :
    ball_receipt_values = (event_id, ball_receipt['outcome']['name'],
                           event_id)
    cur.execute(insert.ball_receipt_table , ball_receipt_values)

def _populate_ball_recovery(event_id : str, ball_recovery : dict) :
    ball_recovery_values = (event_id, ball_recovery['offensive'],
                            ball_recovery['recovery_failure'], event_id)
    cur.execute(insert.ball_recovery_table, ball_recovery_values)

def _populate_block(event_id : str, block : dict) :
    deflection, offensive, save_block, counterpress = None, None, None, None
    if 'deflection' in block:
        deflection = block['deflection']
    if 'offensive' in block:
        offensive = block['offensive']
    if 'save_block' in block:
        save_block = block['save_block']
    if 'counterpress' in block:
        counterpress = block['counterpress']
    block_values = (event_id, deflection, offensive, save_block, counterpress,
                    event_id)
    cur.execute(insert.block_table, block_values)

def _populate_carry(event_id : str, carry : dict) :
    carry_values = (event_id, carry['end_location'], event_id)
    cur.execute(insert.carry_table, carry_values)

def _populate_clearance(event_id : str, clearance : dict) :
    aerial_won = None
    if 'aerial_won' in clearance:
        aerial_won = clearance['aerial_won']
    clearance_values = (event_id, aerial_won, clearance['body_part']['name'],
                        event_id)
    cur.execute(insert.clearance_table, clearance_values)

def _populate_dribble(event_id : str, dribble : dict) :
    overrun, nutmeg, no_touch = None, None, None
    if 'overrun' in dribble:
        overrun = dribble['overrun']
    if 'nutmeg' in dribble:
        nutmeg = dribble['nutmeg']
    if 'no_touch' in dribble:
        no_touch = dribble['no_touch']
    dribble_values = (event_id, overrun, nutmeg, dribble['outcome']['name'],
                      no_touch, event_id)
    cur.execute(insert.dribble_table, dribble_values)

def _populate_dribbled_past(event_id : str, dribbled_past : dict) :
    dribbled_past_values = (event_id, dribbled_past['counterpress'], event_id)
    cur.execute(insert.dribbled_past_table, dribbled_past_values)

def _populate_duel(event_id : str, duel : dict) :
    counterpress = None
    if 'counterpress' in duel:
        counterpress = duel['counterpress']
    duel_values = (event_id, counterpress, duel['type']['name'],
                   duel['outcome']['name'], event_id)
    cur.execute(insert.duel_table, duel_values)

def _populate_foul_committed(event_id : str, foul_committed : dict) :
    counterpress, offensive, advantage, penalty, card_name = None, None, \
        None, None, None
    if 'counterpress' in foul_committed:
        counterpress = foul_committed['counterpress']
    if 'offensive' in foul_committed:
        offensive = foul_committed['offensive']
    if 'advantage' in foul_committed:
        advantage = foul_committed['advantage']
    if 'penalty' in foul_committed:
        penalty = foul_committed['penalty']
    if 'card' in foul_committed:
        card_name = foul_committed['card']['name']
    foul_committed_values = (event_id, counterpress, offensive,
                             foul_committed['type']['name'], advantage,
                             penalty, card_name, event_id)
    cur.execute(insert.foul_committed_table, foul_committed_values)

def _populate_foul_won(event_id : str, foul_won : dict) :
    defensive, advantage, penalty, counterpress = None, None, None
    if 'defensive' in foul_won:
        defensive = foul_won['defensive']
    if 'advantage' in foul_won:
        advantage = foul_won['advantage']
    if 'penalty' in foul_won:
        penalty = foul_won['penalty']
    foul_won_values = (event_id, defensive, advantage, penalty, event_id)
    cur.execute(insert.foul_won_table, foul_won_values)

def _populate_goalkeeper(event_id : str, goalkeeper : dict) :
    technique_name, body_part_name, outcome_name = None, None, None
    if 'technique_name' in goalkeeper:
        technique_name = goalkeeper['technique_name']
    if 'body_part_name' in goalkeeper:
        body_part_name = goalkeeper['body_part_name']
    if 'outcome_name' in goalkeeper:
        outcome_name = goalkeeper['outcome_name']
    goalkeeper_values = (event_id, goalkeeper['position']['name'],
                         goalkeeper['technique']['name'],
                         goalkeeper['body_part']['name'],
                         goalkeeper['type']['name'],
                         goalkeeper['outcome']['name'], event_id)
    cur.execute(insert.goalkeeper_table, goalkeeper_values)

def _populate_half_end(event_id : str, half_end : dict) :
    half_end_values = (event_id, half_end['early_video_end'],
                       half_end['match_suspended'], event_id)
    cur.execute(insert.half_end_table, half_end_values)

def _populate_half_start(event_id : str, half_start : dict) :
    half_start_values = (event_id, half_start['late_video_start'], event_id)
    cur.execute(insert.half_start_table, half_start_values)

def _populate_injury_stoppage(event_id : str, injury_stoppage : dict) :
    injury_stoppage_values = (event_id, injury_stoppage['in_chain'], event_id)
    cur.execute(insert.injury_stoppage_table, injury_stoppage_values)

def _populate_interception(event_id : str, interception : dict) :
    interception_values = (event_id, interception['outcome']['name'],
                           event_id)
    cur.execute(insert.interception_table, interception_values)

def _populate_miscontrol(event_id : str, miscontrol : dict) :
    miscontrol_values = (event_id, miscontrol['aerial_won'], event_id)
    cur.execute(insert.miscontrol_table, miscontrol_values)

def _populate_pass(event_id : str, pass_dict : dict) :
    backheel, deflected, miscommunication, cross, cut_back, switch, \
        goal_assist, type_name, outcome_name, technique_name = None, None, \
        None, None, None, None, None, None, None, None
    if 'backheel' in pass_dict:
        backheel = pass_dict['backheel']
    if 'deflected' in pass_dict:
        deflected = pass_dict['deflected']
    if 'miscommunication' in pass_dict:
        miscommunication = pass_dict['miscommunication']
    if 'cross' in pass_dict:
        cross = pass_dict['cross']
    if 'cut_back' in pass_dict:
        cut_back = pass_dict['cut_back']
    if 'switch' in pass_dict:
        switch = pass_dict['switch']
    if 'goal_assist' in pass_dict:
        goal_assist = pass_dict['goal_assist']
    if 'type' in pass_dict:
        type_name = pass_dict['type']['name']
    if 'outcome' in pass_dict:
        outcome_name = pass_dict['outcome']['name']
    if 'technique' in pass_dict:
        technique_name = pass_dict['technique']['name']
    pass_values = (event_id, pass_dict['recipient']['id'],
                   pass_dict['length'], pass_dict['angle'],
                   pass_dict['height']['name'], pass_dict['end_location'],
                   pass_dict['assisted_shot_id'], backheel, deflected,
                   miscommunication, cross, cut_back, switch,
                   pass_dict['shot_assist'], goal_assist,
                   pass_dict['body_part']['name'], type_name, outcome_name,
                   technique_name, event_id)
    cur.execute(insert.pass_table, pass_values)

def _populate_player_off(event_id : str, player_off : dict) :
    player_off_values = (event_id, player_off['permanaent'], event_id)
    cur.execute(insert.player_off_table, player_off_values)

def _populate_pressure(event_id : str, pressure : dict) :
    pressure_values = (event_id, pressure['counterpress'], event_id)
    cur.execute(insert.pressure_table, pressure_values)

def _populate_shot(event_id : str, shot : dict) :
    shot_values = (event_id, shot['key_pass_id'], shot['end_location'],
                   shot['aerial_won'], shot['follows_dribble'],
                   shot['first_time'], shot['freeze_frame'],
                   shot['open_goal'], shot['statsbomb_xg'], shot['deflected'],
                   shot['technique']['name'], shot['body_part']['name'],
                   shot['type']['name'], shot['outcome']['name'], event_id)
    cur.execute(insert.shot_table, shot_values)

def _populate_substitution(event_id : str, substitution : dict) :
    substitution_values = (event_id, substitution['replacement']['name'],
                           substitution['outcome']['name'], event_id)
    cur.execute(insert.substitution_table, substitution_values)

def populate_event_type_tables(event : dict):
    event_id = event['id']
    
    if '50_50' in event:
        _populate_fifty_fifty(event_id, event['50_50'])
    elif 'bad_behaviour' in event:
        _populate_bad_behaviour(event_id, event['bad_behaviour'])
    elif 'ball_receipt' in event:
        _populate_ball_receipt(event_id, event['ball_receipt'])
    elif 'ball_recovery' in event:
        _populate_ball_recovery(event_id, event['ball_recovery'])
    elif 'block' in event:
        _populate_block(event_id, event['block'])
    elif 'carry' in event:
        _populate_carry(event_id, event['carry'])
    elif 'clearance' in event:
        _populate_clearance(event_id, event['clearance'])
    elif 'dribble' in event:
        _populate_dribble(event_id, event['dribble'])
    elif 'dribbled_past' in event:
        _populate_dribbled_past(event_id, event['dribbled_past'])
    elif 'duel' in event:
        _populate_duel(event_id, event['duel'])
    elif 'foul_committed' in event:
        _populate_foul_committed(event_id, event['foul_committed'])
    elif 'foul_won' in event:
        _populate_foul_won(event_id, event['foul_won'])
    elif 'goalkeeper' in event:
        _populate_goalkeeper(event_id, event['goalkeeper'])
    elif 'half_end' in event:
        _populate_half_end(event_id, event['half_end'])
    elif 'half_start' in event:
        _populate_half_start(event_id, event['half_start'])
    elif 'injury_stoppage' in event:
        _populate_injury_stoppage(event_id, event['injury_stoppage'])
    elif 'interception' in event:
        _populate_interception(event_id, event['interception'])
    elif 'miscontrol' in event:
        _populate_miscontrol(event_id, event['miscontrol'])
    elif 'pass' in event:
        _populate_pass(event_id, event['pass'])
    elif 'player_off' in event:
        _populate_pass(event_id, event['player_off'])
    elif 'pressure' in event:
        _populate_pressure(event_id, event['pressure'])
    elif 'shot' in event:
        _populate_shot(event_id, event['shot'])
    elif 'substitution' in event:
        _populate_substitution(event_id, event['substitution'])

    conn.commit() # commit the transaction
    