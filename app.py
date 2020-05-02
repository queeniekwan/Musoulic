from flask import Flask, render_template, request, url_for, redirect
import spotify as sp
import pexels as px

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    ''' home page '''
    return render_template('index.html')

@app.route('/search-song/', methods=['GET', 'POST'])
def search():
    '''get result for a search'''
    if request.method == 'POST':
        query = str(request.form['query'])
        if not query:
            return render_template('search.html', empty=True)
        
        # get basic track info
        try:
            song_info = sp.search_song(query)
        except:
            return render_template('search.html', error=True)
        
        # get track features and visualize
        features = sp.song_features(song_info['song_id'])
        figdata_png = sp.features_visualization(features)

        # get recommendations
        recommendations = sp.recommendations(song_id=song_info['song_id'], artist_id=song_info['artist_id'])
        
        # get emotion tag and search for pic
        emotion = sp.emotion(features)
        emotion_pic = px.search_photo(emotion)
        pic_link = emotion_pic['link']

        return render_template('result.html', name=song_info['song'], artist=song_info['artist'], 
        albumn=song_info['album'], release_date=song_info['release_date'],
        recommendations=recommendations, emotion=emotion,
        plot=figdata_png.decode('utf8'), pic=pic_link)
    
    return render_template('search.html')

if __name__ == "__main__":
    app.run(debug=True)