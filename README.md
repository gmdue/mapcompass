# mapscompass


# scraping_all_info.py file
This code snippet is a script that uses Selenium and BeautifulSoup to scrape information from Google Maps. It performs a search for a specific place, clicks on the search result, and extracts various details such as name, type of food, rating, address, and reviews of the place. The extracted details are then saved to a JSON file.

The script starts by setting up the web driver and opening the Google Maps search link for the specified place. It defines a function to find and click on elements using CSS selectors. It then performs a series of clicks to navigate to the desired search result.

After scrolling down the sidebar until all elements are loaded, the script counts the number of search results. It defines a function to get the text of an element. It then iterates over the search results and extracts details such as name, type of food, rating, etc. It also extracts the reviews for each search result.

Finally, the extracted details are appended to a list and saved to a JSON file. The web driver is closed at the end of the script.
