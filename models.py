from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from typing import Dict, List

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    email = db.Column(db.String(120), nullable=False)

    shows = db.relationship('Show', backref='venue',
                            lazy='dynamic', passive_deletes=True)

    @staticmethod
    def _format_shows(shows: List['Show']) -> List[Dict]:
        return [
            {
                "artist_id": show.artist.id,
                "artist_name": show.artist.name,
                "artist_image_link": show.artist.image_link,
                "start_time": str(show.start_time)
            }
            for show in shows
        ]

    @property
    def past_shows(self) -> List[Dict]:
        shows = self.shows.filter(Show.start_time < datetime.utcnow()).all()
        return self._format_shows(shows)

    @property
    def upcoming_shows(self) -> List[Dict]:
        shows = self.shows.filter(Show.start_time >= datetime.utcnow()).all()
        return self._format_shows(shows)

    def __repr__(self):
        return (
            f'''
            <Venue {self.id}
            Name: {self.name}
            City: {self.city}
            State: {self.state}
            Email: {self.email}
            Genres: {self.genres}>
            '''
        )


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String(120))
    email = db.Column(db.String(120), nullable=False)

    shows = db.relationship('Show', backref='artist', lazy='dynamic',
                            cascade='all, delete-orphan', passive_deletes=True)

    @staticmethod
    def _format_shows(shows: List['Show']) -> List[Dict]:
        return [
            {
                "venue_id": show.venue.id,
                "venue_name": show.venue.name,
                "venue_image_link": show.venue.image_link,
                "start_time": str(show.start_time)
            }
            for show in shows
        ]

    @property
    def past_shows(self) -> List[Dict]:
        shows = self.shows.filter(Show.start_time < datetime.utcnow())
        return self._format_shows(shows)

    @property
    def upcoming_shows(self) -> List[Dict]:
        shows = self.shows.filter(Show.start_time >= datetime.utcnow())
        return self._format_shows(shows)

    def __repr__(self):
        return (
            f'''
            <Artist {self.id}
            Name: {self.name}
            City: {self.city}
            State: {self.state}
            Email: {self.email}
            Genres: {self.genres}>
            '''
        )


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id', ondelete='CASCADE'))
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id', ondelete='CASCADE'))
    start_time = db.Column(db.DateTime)

    def __repr__(self):
        return (
            f'''
            <Show {self.id}
            Venue: {self.venue.name}
            Artist: {self.artist.name}
            Time: {self.start_time}>
            '''
        )


db.create_all()
