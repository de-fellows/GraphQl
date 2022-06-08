from flask import Flask

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
db = SQLAlchemy(app)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


@app.route('/')
def index():
    return "<h1>Music Genres!</h>"


@app.route("/music")
def get_music():
    music = Music.query.all()

    output = []
    for genre in music :
        music_info = {'name': genre.name, 'description': genre.description}

        output.append(music_info)

    return {"music": output}


@app.route('/music/<id>')
def get_music_id(id):         
    music = Music.query.get_or_404(id)         # this will either fetch the drink with a specific id or return a 404 error
    return {"name": music.name, "description":music.description}



if __name__ == "__main__":
    app.run()