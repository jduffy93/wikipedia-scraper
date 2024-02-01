from src.scraper import WikipediaScraper


if __name__ == "__main__":
    #print('main 1')
    wikipediascraper = WikipediaScraper()
    #print('main 2')

    wikipediascraper.get_countries()

    for country in wikipediascraper.countries_list:
        wikipediascraper.get_leaders(country=country)
    
    '''
    counter_index_date = 0
    for url in wikipediascraper.wikipedia_url_list:

        wikipediascraper.get_first_paragraph(url, wikipediascraper.birth_date_list[counter_index_date])
        counter_index_date += 1
    '''
    for i in range(len(wikipediascraper.wikipedia_url_list)):

        wikipediascraper.get_first_paragraph(wikipediascraper.wikipedia_url_list[i], wikipediascraper.birth_date_list[i])
    print(len(wikipediascraper.wikipedia_url_list))


    #print('main 3')
