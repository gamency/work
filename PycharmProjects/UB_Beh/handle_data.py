# -*- coding: utf-8 -*-
from X_Engine.master_lightsaber import lightsaber
import pickle
import pandas as pd
import os
import json

file_path = os.path.split(os.path.realpath(__file__))[0]

JEDI = pickle.load((open(file_path + os.sep + "./Model/")))


def handle(params):
    event_behavior_data_str = params.get("event_info")
    event_behavior_data = json.loads(event_behavior_data_str)
    data = pd.DataFrame(event_behavior_data)

    result = lightsaber(data, JEDI)

    return {"source": str(result)}


if __name__ == "__main__":
    params = {}
