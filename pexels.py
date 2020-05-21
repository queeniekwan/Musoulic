from pexels_api import API
from configparser import ConfigParser

# Get Config
config = ConfigParser()
config.read('config.ini')
PEXELS_API_KEY = config.get('Pexels', 'PEXELS_API_KEY')

# Create API object
px = API(PEXELS_API_KEY)

def search_photo(query='', results_per_page=9):
    '''
    Search 6 photo on Pexels using the string query, 
    return a list of image urls (original size)
    '''
    px.search(query=query, results_per_page=results_per_page, page=1)  
    photos = px.get_entries()
    photos_link = []
    for photo in photos:
        photos_link.append(photo.landscape)
    return photos_link

def main():
    p = search_photo('sadness')
    print(p)

if __name__ == "__main__":
    main()