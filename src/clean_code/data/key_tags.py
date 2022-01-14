from datetime import datetime, time
import logging

import numpy as np
import pandas as pd

_logger = logging.getLogger(__name__)


def load_key_tags(key_tags_path):
    _logger.info("Loading key tags")
    df = pd.read_csv(key_tags_path)
    df['timestamp2'] = df.timestamp.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    df['date'] = df.timestamp.apply(lambda x: datetime.strptime(x[:10], '%Y-%m-%d'))
    df['time'] = df.timestamp2.apply(lambda x: x.time())
    df['timestamp'] = df['timestamp2']
    df = df.drop('timestamp2', axis=1)
    result = pd.DataFrame(np.array(df.date), columns=['date']).drop_duplicates()

    # print(df.name.unique())
    for name in df.name.unique():
        lunchdates = []
        for datum in df.date.unique():
            df2 = df[df.name == name]
            df2 = df2[df2.date == datum]

            dataframe_check_in = df2[df2.event == "check in"]
            dataframe_check_in = dataframe_check_in[dataframe_check_in.time < time(12, 0, 0)]

            df_check_out = df2[df2.event == "check out"]
            df_check_out = df_check_out[df_check_out.time > time(12, 0, 0)]
            if df_check_out.shape[0] > 0 and dataframe_check_in.shape[0] > 0:
                lunchdates.append(datum)

        result[f"{name}"] = result.date.apply(lambda x: 1 if x in list(lunchdates) else 0)

    result['date'] = result['date']  # .apply(str)

    _logger.debug("Key tags loaded")
    return result
