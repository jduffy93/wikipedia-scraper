import requests

class WikipediaScraper:

    def __init__(self):
        self.base_url = 'https://country-leaders.onrender.com'
        self.country_endpoint = '/countries'
        self.leaders_endpoint = '/leaders'
        self.cookies_endpoint = '/cookie'
        self.leaders_data = {}
        self.cookie = None #cookie object

        
    
    def refresh_cookie(self) -> object:
        '''Returns a new cookie if the cookie has expired'''

        return requests.get(self.base_url + self.cookies_endpoint)
  

    def get_countries(self) -> list:
        '''Returns a list of the supported countries from the API'''
        #self.req_countries = requests.get(self.base_url + self.country_endpoint, cookies=self.req_cookie.cookies)

        self.req_countries = requests.get(self.base_url + self.country_endpoint, cookies=self.refresh_cookie().cookies)
        self.countries_list = self.req_countries.json()





    def get_leaders(self, country: str) -> None:
        '''Populates the leader_data object with the leaders of a country retrieved from the API'''
        pass
    

    def get_first_paragraph(self, wikipedia_url: str) -> str:
        '''Returns the first paragraph (defined by the HTML tag <p>) with details about the leader'''
        pass


    def to_json_file(self, filepath: str) -> None:
        '''stores the data structure into a JSON file'''
        pass