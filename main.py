import pandas as pd
import requests
import re
from bs4 import BeautifulSoup


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

def get_event_detail_info(artist, event):
    event_detail = {}
    name = event['name']
    date = event['dates']['start']['localDate']

    if ('localTime' in event['dates']['start']):
        time = event['dates']['start']['localTime']
    else:
        time = 'TBD'

    currency = event['priceRanges'][0]['currency']

    if (len(event['priceRanges']) and 'min' in event['priceRanges'][0]):
        min_price = event['priceRanges'][0]['min']
    else:
        min_price = 'NA'

    if (len(event['priceRanges']) and 'max' in event['priceRanges'][0]):
        max_price = event['priceRanges'][0]['max']
    else:
        max_price = 'NA'

    venue_name = event['_embedded']['venues'][0]['name']
    venue_city = event['_embedded']['venues'][0]['city']['name']
    venue_state = event['_embedded']['venues'][0]['state']['name']

    event_detail.update({'artist': artist})
    event_detail.update({'name': name})
    event_detail.update({'date': date})
    event_detail.update({'time': time})
    event_detail.update({'currency': currency})
    event_detail.update({'min_price': min_price})
    event_detail.update({'max_price': max_price})
    event_detail.update({'venue_name': venue_name})
    event_detail.update({'venue_city': venue_city})
    event_detail.update({'venue_state': venue_state})

    return event_detail


def get_ticket_master_concerts(artists):
    all_events = []
    for artist in artists:
        url = f'https://app.ticketmaster.com/discovery/v2/events.json?keyword={artist}&classificationName=music&countryCode=US&apikey=tGH1pww1hL8vibSfiVt2nEMjuLDLmm0E'       
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
    artists = get_billboard_top100_artists()
    allConcerts = get_ticket_master_concerts(artists)
    df = pd.DataFrame(allConcerts)
    df.to_csv("top_artists'_concerts")

    choice = ""
    while choice == "":
        artist_name = input("Enter an artist's name: ")
        df2 = df[df['artist'].str.lower() == artist_name.lower()]
        if df2.empty == True:
            print('Sorry, this artist is not in the top 100 artists this week, or they do not have any concerts. Try another artist')
        else:
            df2.to_csv(f"{artist_name.lower()}'s_concerts.csv", index=False)
            choice = "done"
            print(f"Data on {artist_name.lower()}'s concerts has been gathered.")
if __name__ == "__main__":
    main()