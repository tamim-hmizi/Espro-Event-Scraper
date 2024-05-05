import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.meetup.com/find/?source=EVENTS&eventType=online&sortField=DATETIME&location=tn--Aryanah"

# Send a GET request to the webpage
response = requests.get(url)

# Function to post event data to the Spring Boot endpoint
def post_event_to_springboot(event):
    endpoint_url = "http://localhost:8089/esprobackend/EventScraps/add-event"  # Your Spring Boot endpoint

    # Data to be sent in the POST request
    payload = {
        "name": event.get("title", "No Title"),
        "date": event.get("date", "No Date"),
        "url": event.get("url", "No URL"),
        "image": event.get("image_url", "No Image")
    }

    # Send POST request to add the event to the Spring Boot backend
    response = requests.post(endpoint_url, json=payload)

    if response.status_code == 200:
        print("Event added successfully!")
    else:
        print("Failed to add event. Status code:", response.status_code)

# Check if the request to the meetup page was successful
if response.status_code == 200:
    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all event cards
    event_cards = soup.find_all('div', {'class': 'flex flex-1 flex-row-reverse overflow-hidden md:flex-row'})

    # List to hold event information
    events = []

    # Loop through all event cards to extract title, image URL, event date, and event URL
    for card in event_cards:
        event_info = {}

        # Extract event title
        event_title_tag = card.find('h2', {'class': 'text-gray7 font-medium text-base pb-1 pt-0 line-clamp-3'})
        if event_title_tag:
            event_info['title'] = event_title_tag.text.strip()

        # Extract event image URL
        img_tag = card.find('img')
        if img_tag:
            event_info['image_url'] = img_tag['src']

        # Extract event date
        event_time_tag = card.find('time')
        if event_time_tag:
            event_info['date'] = event_time_tag['datetime']

        # Extract event URL
        event_link_tag = card.find('a', {'href': True})
        if event_link_tag:
            event_info['url'] = event_link_tag['href']

        # Add the event information to the list
        events.append(event_info)

    # Display the extracted information for each event and post it to the Spring Boot endpoint
    for event in events:
        print("Event Title:", event.get("title", "N/A"))
        print("Image URL:", event.get("image_url", "N/A"))
        print("Event Date:", event.get("date", "N/A"))
        print("Event URL:", event.get("url", "N/A"))
        print("-" * 40)

        # Post the event to the Spring Boot endpoint
        post_event_to_springboot(event)

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
