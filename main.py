import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


def get_billboard_top100_artists():
    billboard_url = 'https://www.billboard.com/charts/artist-100/'
    try:
        response = requests.get(billboard_url)

        if response.status_code != 200:
            print(f'failed to get the webpage: {response.status_code}')
            return []
        
        soup = BeautifulSoup(response.text,'html.parser')
       
        title_tags = soup.find_all("h3", class_=re.compile("^c-title a-no-trucate"), id="title-of-a-story")
        artists = [title.text.strip() for title in title_tags]
        return artists
    
    except Exception as e:
        print(f'An error has occured: {e}')
        return []

def get_value_or_default(key, data):
    if (key in data):
        return data[key]
    else:
        return ''
    
def get_event_detail_info(artist, event):
    name = get_value_or_default('name', event)
    date = get_value_or_default('localDate', event['dates']['start'])
    time = get_value_or_default('localTime', event['dates']['start'])

    if (len(event['priceRanges'])):
        currency = get_value_or_default('currency', event['priceRanges'][0])
        min_price = get_value_or_default('min', event['priceRanges'][0])
        max_price = get_value_or_default('max', event['priceRanges'][0])
    else:
        currency = min_price = max_price = ''

    if (len(event['_embedded']['venues'])):
        venue_name = get_value_or_default('name', event['_embedded']['venues'][0])
        venue_city = get_value_or_default('name', event['_embedded']['venues'][0]['city'])
        venue_state = get_value_or_default('name', event['_embedded']['venues'][0]['state'])
    else:
        venue_name = venue_city = venue_state = ''

    event_detail = {
        'artist': artist,
        'name': name,
        'date': date,
        'time': time,
        'currency': currency,
        'min_price': min_price,
        'max_price': max_price,
        'venue_name': venue_name,
        'venue_city': venue_city,
        'venue_state': venue_state
    }

    return event_detail


def get_ticket_master_concerts(artists):
    load_dotenv()
    ticketmaster_api_key = os.getenv("ticketmaster_api_key")

    all_events = []
    for artist in artists:
        url = f'https://app.ticketmaster.com/discovery/v2/events.json?keyword={artist}&classificationName=music&countryCode=US&apikey={ticketmaster_api_key}'       
        json_data = requests.get(url).json()
        if ('_embedded' in json_data):
            embedded_data = json_data['_embedded']
            if ('events' in embedded_data):
                events = embedded_data['events']
                if (len(events) > 0):
                    for i in range(0, len(events)):
                        if ('priceRanges' in events[i]):
                            all_events.append(get_event_detail_info(artist, events[i]))
    return all_events
            
    
def main():
    print ("Please wait. Gathering data...\n")
    artists = get_billboard_top100_artists()
    allConcerts = get_ticket_master_concerts(artists)
    df = pd.DataFrame(allConcerts)
    df.to_csv("top_artists'_concerts", index=False)


    print (f"This week's Billboard top 100 artists are: \n{artists}\n")
    choice = ""
    while choice == "":
        artist_name = input("Enter an artist's name: ")
        df_artist_concert = df[df['artist'].str.lower() == artist_name.lower()]
        if df_artist_concert.empty == True:
            print('Sorry, this artist is not in the top 100 artists this week, or they do not have any concerts. Try another artist')
        else:
            df_artist_concert.to_csv(f"{artist_name.lower()}'s_concerts.csv", index=False)
            choice = "done"
            print(f"Data on {artist_name.lower()}'s concerts has been gathered.")
if __name__ == "__main__":
    main()