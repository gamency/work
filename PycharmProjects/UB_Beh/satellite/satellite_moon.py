import pandas as pd
import matplotlib.pyplot as plt


def parse_data(data_dic):
    #     data = data_dic['mouseEvents']
    init_time = data_dic["initialTimeStamp"]
    rightbutton_info = data_dic['buttonLowerRight']
    leftbutton_info = data_dic['buttonTopLeft']
    first_x = rightbutton_info['x']
    first_y = rightbutton_info['y']
    second_x = leftbutton_info['x']
    second_y = leftbutton_info['y']
    scenario = data_dic['scenario']
    terminal = data_dic['terminal']

    df = pd.DataFrame(data_dic['mouseEvents'])
    pox = list(df['point'])
    #     print(df.head())
    pox_x = []
    pox_y = []
    for item in pox:
        #         print(item['x'])
        pox_x.append(item['x'])
        pox_y.append(item['y'])
    df['op_x'] = pox_x
    df['op_y'] = pox_y
    df = df.drop('point', 1)
    df = df.rename(columns={'action': 'Action', 'timestamp': 'Time', 'eventType': 'mouse_event_type'})
    df['Time'] = df['Time'] + init_time
    df['first_x'] = first_x
    df['first_y'] = first_y
    df['second_x'] = second_x
    df['second_y'] = second_y
    df['scenario'] = scenario
    df['terminal'] = terminal
    df['Bot'] = 1
    return df


def visualization(data_dic):
    df = pd.DataFrame(data_dic['mouseEvents'])
    pox = list(df['point'])
    pox_x = []
    pox_y = []
    for item in pox:
#         print(item['x'])
        pox_x.append(item['x'])
        pox_y.append(item['y'])
    plt.plot(pox_x, pox_y)
    plt.show()


def save_file_to_csv(dataframe, save_file):
    dataframe.to_csv(save_file, index=None)


def main():
    # base_dir = "/Users/kite/Desktop/Mobile_verify/Data/trainData/PC/FirstBig"
    dfte = {"buttonLowerRight": {"x": 841, "y": 411}, "buttonTopLeft": {"x": 576, "y": 389},
            "initialTimeStamp": 1518079784211,
            "mouseEvents": [{"action": 0, "eventType": 1, "point": {"x": 788, "y": 336}, "timestamp": 558},
                            {"action": 0, "eventType": 1, "point": {"x": 794, "y": 330}, "timestamp": 575},
                            {"action": 0, "eventType": 1, "point": {"x": 801, "y": 325}, "timestamp": 591},
                            {"action": 0, "eventType": 1, "point": {"x": 808, "y": 318}, "timestamp": 607},
                            {"action": 0, "eventType": 1, "point": {"x": 819, "y": 306}, "timestamp": 625},
                            {"action": 0, "eventType": 1, "point": {"x": 826, "y": 297}, "timestamp": 641},
                            {"action": 0, "eventType": 1, "point": {"x": 832, "y": 290}, "timestamp": 658},
                            {"action": 0, "eventType": 1, "point": {"x": 837, "y": 282}, "timestamp": 674},
                            {"action": 0, "eventType": 1, "point": {"x": 841, "y": 277}, "timestamp": 691},
                            {"action": 0, "eventType": 1, "point": {"x": 847, "y": 270}, "timestamp": 708},
                            {"action": 0, "eventType": 1, "point": {"x": 847, "y": 268}, "timestamp": 959},
                            {"action": 0, "eventType": 1, "point": {"x": 841, "y": 228}, "timestamp": 976},
                            {"action": 0, "eventType": 1, "point": {"x": 825, "y": 161}, "timestamp": 993},
                            {"action": 38, "eventType": 1, "point": {"x": 797, "y": 53}, "timestamp": 1008},
                            {"action": 0, "eventType": 0, "point": {"x": 797, "y": 53}, "timestamp": 1405},
                            {"action": 0, "eventType": 1, "point": {"x": 684, "y": 414}, "timestamp": 26232},
                            {"action": 0, "eventType": 1, "point": {"x": 688, "y": 414}, "timestamp": 26327},
                            {"action": 0, "eventType": 1, "point": {"x": 696, "y": 414}, "timestamp": 26344},
                            {"action": 0, "eventType": 1, "point": {"x": 708, "y": 416}, "timestamp": 26360},
                            {"action": 0, "eventType": 1, "point": {"x": 724, "y": 417}, "timestamp": 26377},
                            {"action": 0, "eventType": 1, "point": {"x": 736, "y": 418}, "timestamp": 26394},
                            {"action": 0, "eventType": 1, "point": {"x": 742, "y": 418}, "timestamp": 26411},
                            {"action": 0, "eventType": 1, "point": {"x": 748, "y": 418}, "timestamp": 26427},
                            {"action": 0, "eventType": 1, "point": {"x": 752, "y": 418}, "timestamp": 26444},
                            {"action": 0, "eventType": 1, "point": {"x": 753, "y": 418}, "timestamp": 26462},
                            {"action": 0, "eventType": 1, "point": {"x": 754, "y": 418}, "timestamp": 26477},
                            {"action": 0, "eventType": 1, "point": {"x": 754, "y": 418}, "timestamp": 26494},
                            {"action": 0, "eventType": 1, "point": {"x": 754, "y": 417}, "timestamp": 26511},
                            {"action": 0, "eventType": 1, "point": {"x": 754, "y": 417}, "timestamp": 26528},
                            {"action": 38, "eventType": 1, "point": {"x": 755, "y": 417}, "timestamp": 26544},
                            {"action": 0, "eventType": 2, "point": {"x": 755, "y": 417}, "timestamp": 26671},
                            {"action": 36, "eventType": 3, "point": {"x": 755, "y": 417}, "timestamp": 26675}],
            "scenario": 0, "terminal": 0}
    dfparse = parse_data(dfte)
    print(dfparse)

    visualization(dfte)


if __name__ == '__main__':
    main()
