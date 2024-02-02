from src.scraper import WikipediaScraper


if __name__ == "__main__":
    wikipediascraper = WikipediaScraper()
    wikipediascraper.get_countries()

    # Loop over the list of countries, to get the leaders for each country
    for country in wikipediascraper.countries_list:
        wikipediascraper.get_leaders(country=country)
        
    # Loop over the country elements in leaders data, and then the leader key to scrape the first paragraph from wikipedia and add it to the leaders_data dictionary
    for country in wikipediascraper.leaders_data:
        for leader_key in wikipediascraper.leaders_data[country]:
            leader = wikipediascraper.leaders_data[country][leader_key]

            wikipediascraper.get_first_paragraph(wikipedia_url=leader.get('wikipedia_url'),
                                                 country=country,
                                                 leader_key=leader_key)

    # Write dictionary to a JSON file
    wikipediascraper.to_json_file(filepath = 'leaders_data.json')

