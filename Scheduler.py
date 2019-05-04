import sys
import re
import math
import time
import numpy as np
import pandas as pd

from datetime import timedelta,date


class Scheduler:

    latestOrderTime = 0

    @staticmethod
    def calculatedistance(locString):
        """Parse coordinates and return time in seconds to deliver the order"""
        pattern = '[0-9]+'
        coords = re.findall(pattern, locString)
        distance = math.sqrt(int(coords[0])**2 + int(coords[1])**2)
        return distance*60


def main(filepath):

    df = pd.read_csv(filepath, sep=" ", header=None)
    df.columns = ['id', 'coordinates', 'order_time']
    df['distance_sec'] = df['coordinates'].apply(lambda x: Scheduler.calculatedistance(x))
    todayDt = date.today().strftime("%Y-%m-%d")
    df['order_time_sec'] = df['order_time'].apply(lambda x: time.mktime(time.strptime(todayDt+ " " + x, "%Y-%m-%d %H:%M:%S")))
    df['elapsed'] = df['order_time_sec'].max()-df['order_time_sec']
    df['best_delivery'] = df['elapsed']+df['distance_sec']
    df['scheduled'] = False

    top_third = df['distance_sec'].quantile(0.33)
    top_half = df['distance_sec'].quantile(0.5)



    print(df)
    nxt_picks_df = df[(df['scheduled'] == False) & (df['best_delivery'] <= 3600) & (df['distance_sec'] < top_third)]

    while(not nxt_picks_df.empty):
        nxt_picks_df = df[(df['scheduled'] == False) & (df['best_delivery'] <= 3600) & (df['distance_sec'] < top_third )]
        if nxt_picks_df.empty:
            nxt_picks_df = df[(df['scheduled'] == False) & (df['best_delivery'] <= 3*3600) & (df['distance_sec'] < top_third)]
            if nxt_picks_df.empty:
                nxt_picks_df = df[
                    (df['scheduled'] == False) & (df['best_delivery'] <= 3 * 3600) & (df['distance_sec'] < top_half)]
                if nxt_picks_df.empty:
                    nxt_picks_df = df[(df['scheduled'] == False)]
        if not nxt_picks_df.empty:
            nxt_pck_idx = nxt_picks_df['best_delivery'].idxmax()
            deliveryTime = df.iloc[nxt_pck_idx]['distance_sec']
            df.loc[nxt_pck_idx, 'scheduled'] = True

            df.loc[df['scheduled']==False, 'elapsed'] = df.loc[df['scheduled']==False, 'elapsed']  + 2*deliveryTime
            df.loc[df['scheduled']==False, 'best_delivery'] = df.loc[df['scheduled']==False, 'elapsed']  + df.loc[df['scheduled']==False, 'distance_sec']

    df['delivery_time_sec'] = df['order_time_sec'] + df['elapsed']

    df['actual_delivery_time'] = pd.to_datetime(df['delivery_time_sec'], unit='s')

    df.sort_values(by=['actual_delivery_time'], inplace=True)


    promScore = np.sum(df.elapsed <= 3600)
    detractorScore = np.sum(df.elapsed > 10800)

    print(df)

    print(promScore-detractorScore)

    print("Writing to output.txt")

    df[['id', 'actual_delivery_time']].to_csv("output.txt", sep=" ")

    with open("output.txt", 'a') as f:
        f.write("NPS " + str(promScore-detractorScore))



if __name__ == '__main__': main("/home/chandana/abc/python/walmart/input.txt")
# if __name__ == '__main__': main(sys.argv[1])
