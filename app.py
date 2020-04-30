from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import spotify as ap
import pexels as px

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracks.db'
db = SQLAlchemy(app)

class Track(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    track_name = db.Column(db.String(50), nullable = False)
    track_id = db.Column(db.String(50), nullable = False)
    artist_name = db.Column(db.String(50), nullable = False)
    artist_id = db.Column(db.String(50), nullable = False)
    album = db.Column(db.String(50), nullable = False)
    released_date = db.Column(db.String(50), nullable = False)
    acousticness = db.Column(db.Float, nullable = False)
    danceability = db.Column(db.Float, nullable = False)
    energy = db.Column(db.Float, nullable = False)
    instrumentalness = db.Column(db.Float, nullable = False)
    liveness = db.Column(db.Float, nullable = False)
    loudness = db.Column(db.Float, nullable = False)
    speechiness = db.Column(db.Float, nullable = False)
    tempo = db.Column(db.Float, nullable = False)
    
    date_searched = db.Column(db.DateTime, default = datetime.utcnow)


    def __repr__(self):
        return '<Profile %r>' % self.id

@app.route('/')
def index():
    ''' home page '''
    return render_template('index.html')

# @app.route('/search-result')


if __name__ == "__main__":
    app.run(debug=True)