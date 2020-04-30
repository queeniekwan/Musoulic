''' Installation
pip3 install pexels-api
'''

from pexels_api import API

PEXELS_API_KEY = '563492ad6f91700001000001f15d07838df1429bb172cf9081a1f0cc'

# Create API object
px = API(PEXELS_API_KEY)

def search_photo(query='', results_per_page=1):
    '''
    Search a photo on Pexels using the string query, 
    return a dictionary with the photographer and photo address (original size)
    '''
    px.search(query=query, results_per_page=results_per_page, page=1)  
    photos = px.get_entries()
    photo_d = {}
    for photo in photos:
        photo_d['photographer'] = photo.photographer
        photo_d['link'] = photo.original
    return photo_d

def main():
    p = search_photo('sadness')
    print(p)
    

if __name__ == "__main__":
    main()