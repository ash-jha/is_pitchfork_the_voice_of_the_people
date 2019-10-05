import sys
import pandas as pd
import random
import billboard
import requests
import backoff
import time
from collections import defaultdict
from datetime import datetime,timedelta
import pickle

################################################
# Usage: python fetch_billboard_album_sales.py #
################################################

def main():

    if len(sys.argv) != 2:
        print('Please provide output path for csv file.')
        print('Usage: python fetch_billboard_album_sales.py [output csv path]')
        sys.exit(1)

    start_date = '2019-10-05'  # Week before final's week of module 1
    end_date = '1999-01-05'
    chart_week_dates = generate_date_list(start_date, end_date)
    list_of_charts = scrape_album_sales_charts(chart_week_dates)

    # Optional
    # with open('chart.pkl', 'wb') as fp:
    #     pickle.dump(list_of_charts, fp)

    album_ranks = generate_album_peak_positions(list_of_charts)

    output_csv_path = sys.argv[1]
    export_to_csv(album_ranks,output_csv_path)


def generate_date_list(start_date,end_date):

    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')

    chart_week_dates = []
    current_dt = start_dt # would be best if start date is a valid date for week of xxx billboard, should be saturday
    while(current_dt > end_dt):
        chart_week_dates.append(str(current_dt.date()))    
        current_dt = current_dt - timedelta(days=7)
        # exit loop as soon as current date less than end date

    return chart_week_dates


def backoff_error_msg(details):
    print ("Backing off {wait:0.1f} seconds afters {tries} tries "
           "calling function {func} with args {args} and kwargs "
           "{kwargs}".format(**details))


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, on_backoff=backoff_error_msg)
def get_chart(url): # Use exponential backoff when there's a 429 request error
    print('Requesting... '+url)
    chart = billboard.ChartData(url)
    print('FINISH')
    return chart

def scrape_album_sales_charts(chart_week_dates):
    api_urls = ['top-album-sales/'+date for date in chart_week_dates]
    charts=[]
    while len(api_urls) != 0:
        url = api_urls.pop(0)
        chart = get_chart(url)
        charts.append(chart)
        sleep_sec = round(random.random(),2)*10 % 5
        time.sleep(sleep_sec)

    return charts


def generate_album_peak_positions(charts):
    album_ranks = defaultdict(lambda: 666)  # default ranking is 666 which is lower than 100 (lowest possible rank)

    for chart in charts:

        for entry in chart:
            artist_name = entry.artist
            album_name = entry.title
            peak_chart_ranking = entry.peakPos
            key = (artist_name, album_name)

            if peak_chart_ranking == None:
                continue  # weird that sometimes it's none

            if album_ranks[
                key] > peak_chart_ranking:  # If stored rank is lower than this week's peak, we replace the stored rank with the new higher ranking
                album_ranks[key] = peak_chart_ranking

    return  album_ranks


def export_to_csv(album_ranks,output_csv_path):
    billboard_chart_ranks = pd.DataFrame(columns=['artist', 'title', 'peak_chart_ranking'])
    counter = 0
    for key, peak_chart_ranking in album_ranks.items():
        artist_name, album_name = key
        new_row = [artist_name.lower().strip(), album_name.lower().strip(), peak_chart_ranking]
        billboard_chart_ranks.loc[counter] = new_row
        counter += 1

    billboard_chart_ranks.to_csv(output_csv_path)


if __name__ == '__main__':
    main()