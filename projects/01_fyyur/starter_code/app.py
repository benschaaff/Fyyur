#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import logging
import re
from logging import FileHandler, Formatter
from typing import Dict, List

from flask import (Flask, Response, flash, redirect, render_template, request,
                   url_for, make_response, abort, jsonify)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, or_

import babel
import dateutil.parser
from flask_migrate import Migrate
from flask_moment import Moment
from forms import *


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


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
    website = website = db.Column(db.String(120))
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
            f'<Show {self.id} \nVenue: {self.venue.name} \nArtist: {self.artist.name} \nTime: {self.start_time}>\n'
        )
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/', methods=['GET'])
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    shows_by_city = {}

    upcoming_shows = Show.query.filter(
        Show.start_time > datetime.utcnow()
    ).subquery()

    venues_query = (
        Venue.query
        .outerjoin(upcoming_shows, Venue.id == upcoming_shows.c.venue_id)
        .with_entities(
            Venue.city, Venue.state, Venue.id, Venue.name,
            func.count(upcoming_shows.c.venue_id)
        )
        .group_by(Venue.id)
    )

    for v in venues_query:
        city_state = f'{v[0]}_{v[1]}'
        location = shows_by_city.setdefault(city_state, {})
        venues = location.setdefault('venues', [])
        venues.append({'id': v[2], 'name': v[3], 'num_upcoming_shows': v[4]})

    data = [
        {'city': c.split('_')[0],
         'state': c.split('_')[1],
         'venues': shows_by_city[c]['venues']}
        for c in shows_by_city
    ]

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
    data = [
        {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(venue.upcoming_shows),
        }
        for venue in venues
    ]

    response = {
        "count": len(data),
        "data": data
    }

    return render_template('pages/search_venues.html', results=response, search_term=search_term)


@app.route('/venues/<int:venue_id>', methods=['GET'])
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if venue:
        past_shows = venue.past_shows
        upcoming_shows = venue.upcoming_shows

        data = {
            "id": venue_id,
            "name": venue.name,
            "genres": json.loads(venue.genres),
            "address": venue.address,
            "city": venue.city,
            "state": venue.state,
            "phone": venue.phone,
            "website": venue.website,
            "facebook_link": venue.facebook_link,
            "seeking_talent": venue.seeking_talent,
            "seeking_description": venue.seeking_description,
            "image_link": venue.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
        }

        return render_template('pages/show_venue.html', venue=data)

    abort(404)


@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    try:
        db.session.delete(venue)
        db.session.commit()
        message = f'Venue {venue.name} was successfully deleted!', 'info'
    except:
        db.session.rollback()
        message = f'An error occurred. Venue {venue.name} could not be deleted.', 'danger'
    flash(*message)
    return jsonify({'redirect': '/'})


@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue():
    form = VenueForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            venue = Venue(name=form.name.data,
                          genres=json.dumps(form.genres.data),
                          city=form.city.data,
                          state=form.state.data,
                          address=form.address.data,
                          phone=form.phone.data,
                          facebook_link=form.facebook_link.data,
                          website=form.website.data,
                          seeking_talent=form.seeking_talent.data,
                          seeking_description=form.seeking_description.data,
                          email=form.email.data)
            try:
                db.session.add(venue)
                db.session.commit()
                message = f'Venue {venue.name} was successfully listed!', 'info'
            except Exception as e:
                app.logger.error(e)
                db.session.rollback()
                message = f'An error occurred. Venue {venue.name} could not be listed.', 'danger'
            flash(*message)
            return redirect(url_for('index'))
        else:
            errors = form.errors
            for e in errors:
                flash(f'{e}: {errors[e][0]}', 'danger')
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm()

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": json.loads(venue.genres),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "email": venue.email
    }

    return render_template('forms/edit_venue.html', form=form, venue=data)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(request.form)
    try:
        venue.name = form.name.data
        venue.genres = json.dumps(form.genres.data)
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.website = form.website.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        venue.image_link = form.image_link.data
        venue.email = form.email.data

        db.session.commit()
        message = f'Venue ID {venue.id} was updated!', 'info'
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        message = f'An error occurred. Changes not saved :(', 'danger'

    flash(*message)

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():

    data = [
        {
            "id": artist.id,
            "name": artist.name
        }
        for artist in Artist.query
    ]

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))

    data = [
        {
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(artist.upcoming_shows),
        }
        for artist in artists
    ]

    response = {
        "count": len(data),
        "data": data
    }

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if artist:
        past_shows = artist.past_shows
        upcoming_shows = artist.upcoming_shows
        data = {
            "id": artist_id,
            "name": artist.name,
            "genres": json.loads(artist.genres),
            "city": artist.city,
            "state": artist.state,
            "phone": artist.phone,
            "website": artist.website,
            "facebook_link": artist.facebook_link,
            "seeking_venue": artist.seeking_venue,
            "seeking_description": artist.seeking_description,
            "image_link": artist.image_link,
            "past_shows": past_shows,
            "upcoming_shows": upcoming_shows,
            "past_shows_count": len(past_shows),
            "upcoming_shows_count": len(upcoming_shows),
            "email": artist.email
        }
        return render_template('pages/show_artist.html', artist=data)
    else:
        abort(404)


@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    if artist:
        if request.method == 'GET':
            form = ArtistForm()
            data = {
                "id": artist.id,
                "name": artist.name,
                "genres": json.loads(artist.genres),
                "city": artist.city,
                "state": artist.state,
                "phone": artist.phone,
                "website": artist.website,
                "facebook_link": artist.facebook_link,
                "seeking_venue": artist.seeking_venue,
                "seeking_description": artist.seeking_description,
                "image_link": artist.image_link,
                "email": artist.email
            }
            return render_template('forms/edit_artist.html', form=form, artist=data)
        elif request.method == 'POST':
            form = ArtistForm(request.form)
            try:
                artist.name = form.name.data
                artist.genres = json.dumps(form.genres.data)
                artist.city = form.city.data
                artist.state = form.state.data
                artist.phone = form.phone.data
                artist.website = form.website.data
                artist.facebook_link = form.facebook_link.data
                artist.seeking_venue = form.seeking_venue.data
                artist.seeking_description = form.seeking_description.data
                artist.image_link = form.image_link.data
                artist.email = form.email.data

                db.session.commit()
                message = f'Artist ID {artist.id} was updated!', 'info'
            except Exception as e:
                app.logger.error(e)
                db.session.rollback()
                message = f'An error occurred. Changes not saved :(', 'danger'

            flash(*message)

            return redirect(url_for('show_artist', artist_id=artist_id))
    else:
        abort(404)


@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist():
    form = ArtistForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            artist = Artist(name=form.name.data,
                            genres=json.dumps(form.genres.data),
                            city=form.city.data,
                            state=form.state.data,
                            phone=form.phone.data,
                            facebook_link=form.facebook_link.data,
                            website=form.website.data,
                            seeking_venue=form.seeking_venue.data,
                            seeking_description=form.seeking_description.data,
                            email=form.email.data,
                            image_link=form.image_link.data)
            try:
                db.session.add(artist)
                db.session.commit()
                message = f'Artist {artist.name} was successfully listed!', 'info'
            except:
                db.session.rollback()
                message = f'An error occurred. Artist {artist.name} could not be listed.', 'danger'

            flash(*message)
            return redirect(url_for('index'))
        else:
            errors = form.errors
            for e in errors:
                flash(f'{e}: {errors[e][0]}', 'danger')
    return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    show_query = db.session.query(Show, Venue, Artist).filter(Show.venue_id == Venue.id,
                                                              Show.artist_id == Artist.id)

    data = [
        {
            "venue_id": s.Venue.id,
            "venue_name": s.Venue.name,
            "artist_id": s.Artist.id,
            "artist_name": s.Artist.name,
            "artist_image_link": s.Artist.image_link,
            "start_time": str(s.Show.start_time)
        }
        for s in show_query
    ]

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = request.form

    show = Show(artist_id=form['artist_id'],
                venue_id=form['venue_id'],
                start_time=form['start_time'])

    try:
        db.session.add(show)
        db.session.commit()
        message = f'Show: artist {show.artist_id} at venue {show.venue_id} was successfully listed!', 'info'
    except Exception as e:
        app.logger.error(e)
        db.session.rollback()
        message = f'An error occurred. Show: artist {show.artist_id} at venue {show.venue_id} could not be listed.', 'danger'

    flash(*message)

    return redirect(url_for('index'))


#  Error Handlers
#  ----------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''


# TODO: add the db constraints for email, etc.
# TODO: add docs, including readme
