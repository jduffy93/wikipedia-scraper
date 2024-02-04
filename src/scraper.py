import requests
from bs4 import BeautifulSoup
import json

class WikipediaScraper:
    '''
    The WikipediaScraper object gets infortmation related to various world leaders from the country-leaders.onrender API, and scrape their Wikipedia page for the first paragraph.
    It has methods to:
        1 - get and refresh the API cookie
        2 - get the list of countries from the API
        3 - get the leaders and their information for a respective country from the API
        4 - scrape the first paragraph of a leader from wikipedia
        5 - output the information from methods 2-4 in a json file

    Attributes
    ----------
    base_url : str
        This is where we store the root url.
    country_endpoint : str
        This is where we store the url endpoint for country.
    leaders_endpoint : str
        This is where we store the url endpoint for leaders.
    cookies_endpoint : str
        This is where we store the url endpoint for cookies.
    leaders_data : dict[str, dict[str, [dict[str, str]]]]
        A dictionary where we will save all of the outputs of countries -> leader_key -> leader details
    progress_counter : int
        A counter which incremements for every leader added to dictionary. Used to show progress in terminal.
    cookie : None
        Not used. Instead run refresh_cookie() every ime a cookie is required.
    '''

    def __init__(self):
        self.base_url = 'https://country-leaders.onrender.com'
        self.country_endpoint = '/countries'
        self.leaders_endpoint = '/leaders'
        self.cookies_endpoint = '/cookie'
        self.leaders_data = {}
        self.progress_counter = 0
        self.cookie = None # Cookie object. Not used

        
    
    def refresh_cookie(self) -> object:
        '''Returns a Response object with a cookie for the API.'''

        return requests.get(self.base_url + self.cookies_endpoint)
  

    def get_countries(self) -> list:
        '''Returns a list of the supported countries from the API.'''

        self.req_countries = requests.get(self.base_url + self.country_endpoint, cookies=self.refresh_cookie().cookies)
        self.countries_list = self.req_countries.json()


    def get_leaders(self, country: str) -> dict[str, dict[str, dict[str, str]]]:
        '''Populates the leader_data object with the leaders of a country and their details retrieved from the API, and then adds them to the leaders_data dictionary.'''

        self.country = country
        self.req_leaders = requests.get(self.base_url + self.leaders_endpoint, params={'country' : country}, cookies=self.refresh_cookie().cookies).json()
        self.leader_data = {}
        self.leader_key = 0 # Create a key for leader to be used in the leader_data dictionary

        for leader in self.req_leaders:

            self.leader_key += 1 # Increment leader_key. (Start at one for user legibility)

            # Create a dictionary with a unique leader_key, with it's value being another dictionary with information specific to a leader
            self.leader_data[f'{self.leader_key}'] = {
                                                    'first_name': f'{leader.get('first_name')}',
                                                    'last_name': f'{leader.get('last_name')}',
                                                    'wikipedia_url': f'{leader.get('wikipedia_url')}',
                                                    'birth_date': f'{leader.get('birth_date')}',
                                                    'death_date': f'{leader.get('death_date')}',
                                                    'place_of_birth': f'{leader.get('place_of_birth')}',
                                                    'start_mandate': f'{leader.get('start_mandate')}',
                                                    'end_mandate': f'{leader.get('end_mandate')}'
                                                      }

        # Add the leader_data dictionaries to the leaders_data dictionary with the country as key.
        self.leaders_data[f'{self.country}'] = self.leader_data
    

    def get_first_paragraph(self, wikipedia_url: str, country: str, leader_key: str) -> dict[str, dict[str, dict[str, str]]]:
        '''Returns the first paragraph (defined by the HTML tag <p>) with details about the leader'''
        self.wikipedia_url = wikipedia_url
        self.country = country
        self.leader_key = leader_key

        r = requests.get(f'{self.wikipedia_url}').text  # Returns the content of the response object for url, in unicode 
        soup = BeautifulSoup(r, 'html.parser') # Creates a BeautifulSoup object, which is the parsed wikipedia page
        paragraphs = soup.find_all('p') # Searches all tags for the p tag and assigns them all to paragraphs as a list
        self.progress_counter +=1 # Increment counter

        for paragraph in paragraphs:
            if paragraph is None:   # Checks if paragraph is empty, if True go to next paragraph
                continue
            
            elif paragraph.find('b') and len([tag.name for tag in paragraph.find_all()])>1:
                # Searches tags for first instance of b tag (bold) and checks if there are more than one tag
                # (reason being that sometimes the side table of wikipedia appears first and that has a bold tag but no other tags)

                self.leaders_data[self.country][self.leader_key]['first_paragraph'] = f'{paragraph.text}'

                break
            else:
                pass
                
        
        print(f'Processing {self.progress_counter}/{sum(len(v) for v in self.leaders_data.values())} leaders') # Prints out a processing message, to notify user of progress


    def to_json_file(self, filepath: str) -> None:
        '''Stores leaders_data in a JSON file'''

        with open(filepath, 'w', encoding='utf-8') as fp:
            json.dump(self.leaders_data, fp, ensure_ascii=False)
