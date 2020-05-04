from pexels_api import API
from boto.s3.connection import S3Connection

# Get Config Variables 
s3 = S3Connection(os.environ['PEXELS_API_KEY'])
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