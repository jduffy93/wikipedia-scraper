import requests
from bs4 import BeautifulSoup

class WikipediaScraper:

    def __init__(self):
        self.base_url = 'https://country-leaders.onrender.com'
        self.country_endpoint = '/countries'
        self.leaders_endpoint = '/leaders'
        self.cookies_endpoint = '/cookie'
        self.wikipedia_url_list = []
        self.birth_date_list = []
        self.leader_name_list = []
        self.leaders_data = {}
        self.counter = 0
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
        self.country = country
        #print(self.country)
        self.req_leaders = requests.get(self.base_url + self.leaders_endpoint, params={'country' : country}, cookies=self.refresh_cookie().cookies).json()
        
        for leader in self.req_leaders:
            self.wikipedia_url_list.append(leader.get('wikipedia_url'))

            if leader.get('birth_date'):
                birthdate = leader.get('birth_date').split('-')
                self.birth_date_list.append(birthdate[0])
            else:
                self.birth_date_list.append('99999')

            # Check this
            if leader.get('last_name'):
                self.leader_name = f'{leader.get('first_name')} {leader.get('last_name')}'
            else:
                self.leader_name = f'{leader.get('first_name')}'

    

    def get_first_paragraph(self, wikipedia_url: str, birth_year) -> str:
        '''Returns the first paragraph (defined by the HTML tag <p>) with details about the leader'''
        self.wikipedia_url = wikipedia_url
        self.birth_year = birth_year
        print(birth_year,wikipedia_url)

        r = requests.get(f'{self.wikipedia_url}').text
        soup = BeautifulSoup(r, 'html')
        paragraphs = soup.find_all('p')
        self.counter +=1
        for paragraph in paragraphs:
            if birth_year in paragraph:
                print('birth_year')
                print(paragraph)
                break
            elif paragraph is None:
                continue

            elif paragraph.find('b'):
                print('bold', self.counter)
                print(paragraph)
                break
            else:
                pass
        


    def to_json_file(self, filepath: str) -> None:
        '''stores the data structure into a JSON file'''
        pass