# Concert Lookup Program
## Website Used:
    The website used for this project is: https://www.billboard.com/charts/artist-100/
    I chose this website because this list will update on a weekly basis and will change depending on which artists are currently popular. 
    The data scraped from this website is a list of the top 100 artists of the week. 
## API Used:
    I chose to use the Ticketmaster API in order to find concert information for artists. In order to gain access to the Ticketmaster API, you need to register a free developer account with ticketmaster. I used the Ticketmaster API in order to gather information on the artists' upcoming concerts. Data gathered includes:
        - artist name
        - concert name
        - date of concert
        - time of concert
        - currency of ticket price
        - minimum price of ticket
        - maximum price of ticket
        - venue name
        - venue city
        - venue state
## Purpose of Program:
    The purpose of this program is to gather the latest list of top 100 artists and what concerts they have coming up. Additionally, users can input an artist and check if they are within the top 100 artists of the week and whether they have a concert coming up. If the artist fits both of those requirements, an additional dataset with just that artist's concerts will be generated.
## Value of this Dataset:
    I believe this dataset can provide value to those who like to keep up with music trends and want an easy way to track which artists are popular right now and whether they can go see them live at a concert. There are so many artists across many music genres and it can be hard to individually keep track of their popularity and tour dates. This dataset might not exist yet because both the top 100 artists and their tour dates are constantly updating and changing. Someone would need to maintain and update this dataset constantly for others to find value. By creating this program to collect this information for an individual, they can easily update this list by running the program and have the latest information on artists and their concerts.
## How to Use:
    Before running the program, you need to pip install the requirements.txt file. Additionally, you will need to register a developer account with ticketmaster in order to gain the API key. This process is free and just requires you to enter your email. Afterwards, you will need to create a .env file and label the key: ticketmaster_api_key.