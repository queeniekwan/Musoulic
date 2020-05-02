from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
import spotify as sp
import pexels as px

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracks.db'
# db = SQLAlchemy(app)

# class Track(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     track_name = db.Column(db.String(50), nullable = False)
#     track_id = db.Column(db.String(50), nullable = False)
#     artist_name = db.Column(db.String(50), nullable = False)
#     artist_id = db.Column(db.String(50), nullable = False)
#     album = db.Column(db.String(50), nullable = False)
#     released_date = db.Column(db.String(50), nullable = False)
#     acousticness = db.Column(db.Float, nullable = False)
#     danceability = db.Column(db.Float, nullable = False)
#     energy = db.Column(db.Float, nullable = False)
#     instrumentalness = db.Column(db.Float, nullable = False)
#     liveness = db.Column(db.Float, nullable = False)
#     loudness = db.Column(db.Float, nullable = False)
#     speechiness = db.Column(db.Float, nullable = False)
#     tempo = db.Column(db.Float, nullable = False)
    
#     date_searched = db.Column(db.DateTime, default = datetime.utcnow)


#     def __repr__(self):
#         return '<Profile %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    ''' home page '''
    return render_template('index.html')

@app.route('/search-song/', methods=['GET', 'POST'])
def search():
    '''get result for a search'''
    if request.method == 'POST':
        try:
            query = str(request.form['query'])
        except:
            return render_template('search.html', empty=True)
        
        # get basic track info
        song_info = sp.search_song(query)
        if not song_info:
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
        plot=figdata_png.decode('utf8'), pic=pic_link)
    
    return render_template('search.html')

if __name__ == "__main__":
    app.run(debug=True)