from flask import Flask, render_template, request, url_for, redirect
import spotify as sp
import pexels as px

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    ''' home page '''
    return render_template('index.html')

@app.route('/search-song/', methods=['POST'])
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
        
        # get track features and visualization
        features = sp.song_features(song_info['song_id'])
        chart_uri = sp.features_visualization(features)
        key = sp.key(features['key'])
        mode = sp.mode(features['mode'])

        # get recommendations
        recommendations = sp.recommendations(song_id=song_info['song_id'], artist_id=song_info['artist_id'])
        
        # get emotion tag and search for pics
        emotion = sp.emotion(features)
        emotion_pics = px.search_photo(emotion)

        return render_template('result.html', 
        name=song_info['song'], artist=song_info['artist'], albumn=song_info['album'], release_date=song_info['release_date'],
        recommendations=recommendations, 
        key=key, mode=mode, tempo=features['tempo'], meter=features['time_signature'],
        chart=chart_uri, 
        emotion=emotion, pics=emotion_pics)
    
    return render_template('search.html')

if __name__ == "__main__":
    app.run()