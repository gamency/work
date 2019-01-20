import pandas as pd
import numpy as np
import simplejson


def parse_data(phase, data_dic, bot_probability):
    init_time = data_dic["initialTimeStamp"]
    if phase == 1:
        rightbutton_info = data_dic['buttonLowerRight']
        leftbutton_info = data_dic['buttonTopLeft']
    else:
        rightbutton_info = data_dic['slideBarLowerRight']
        leftbutton_info = data_dic['slideBarTopLeft']

    first_x = rightbutton_info['x']
    first_y = rightbutton_info['y']
    second_x = leftbutton_info['x']
    second_y = leftbutton_info['y']
    scenario = data_dic['scenario']
    terminal = data_dic['terminal']

    if phase == 2:
        correct_x = data_dic['correctX']
        correct_y = data_dic['correctY']

    df = pd.DataFrame(data_dic['mouseEvents'])
    pox = list(df['point'])
    pox_x = []
    pox_y = []
    for item in pox:
        pox_x.append(item['x'])
        pox_y.append(item['y'])

    df['op_x'] = pox_x
    df['op_y'] = pox_y
    df = df.drop('point', 1)
    df = df.rename(columns={'action': 'Action', 'timestamp': 'Time', 'eventType': 'mouse_event_type'})
    df['Time'] = df['Time'] + init_time

    if phase == 2:
        df['correct_x'] = correct_x
        df['correct_y'] = correct_y

        df['slidebarright_x'] = first_x
        df['slidebarright_y'] = first_y
        df['slidebarleft_x'] = second_x
        df['slidebarleft_y'] = second_y
    else:
        df['first_x'] = first_x
        df['first_y'] = first_y
        df['second_x'] = second_x
        df['second_y'] = second_y
        df['key_event_type'] = ''
        df['dialog_type'] = ''

    df['scenario'] = scenario
    df['terminal'] = terminal
    df['Bot'] = bot_probability
    return df


def Up_Down_Transf(data):
    # df = data[pd.notnull(data['msg'])]

    big_table_phase1 = []
    big_table_phase2 = []

    for i in data.index:
        tmpdata = data.loc[i, 'msg']
        try:
            tmp_msg = simplejson.loads(tmpdata)
        except:
            continue
        if i % 1000 == 0:
            print("i is", i)

        tmp_predict_bot_prob = data.loc[i, 'prob']

        if 'buttonLowerRight' in tmp_msg.keys():
            orbit_df = parse_data(1, tmp_msg, tmp_predict_bot_prob)
            big_table_phase1.append(orbit_df)
        else:
            # aviod the data is null or empty
            if len(tmp_msg.keys()) < 9:
                print("error here")
            else:
                orbit_df = parse_data(2, tmp_msg, tmp_predict_bot_prob)
                big_table_phase2.append(orbit_df)

    return big_table_phase1, big_table_phase2
