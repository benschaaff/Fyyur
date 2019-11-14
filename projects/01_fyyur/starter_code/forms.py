from datetime import datetime
from enum import Enum

import us
from flask_wtf import FlaskForm
from wtforms import (DateTimeField, SelectField, SelectMultipleField,
                     StringField)
from wtforms.validators import URL, AnyOf, DataRequired


class Genre(Enum):
    ALTERNATIVE = 'Alternative'
    BLUES = 'Blues'
    CLASSICAL = 'Classical'
    COUNTRY = 'Country'
    ELECTRONIC = 'Electronic'
    FOLK = 'Folk'
    FUNK = 'Funk'
    HIP_HOP = 'Hip-Hop'
    HEAVY_METAL = 'Heavy Metal'
    INSTRUMENTAL = 'Instrumental'
    JAZZ = 'Jazz'
    MUSICAL_THEATRE = 'Musical Theatre'
    POP = 'Pop'
    PUNK = 'Punk'
    R_AND_B = 'R&B'
    REGGAE = 'Reggae'
    ROCK_N_ROLL = 'Rock n Roll'
    SOUL = 'Soul'
    OTHER = 'Other'


class ShowForm(FlaskForm):
    artist_id = StringField('artist_id')
    venue_id = StringField('venue_id')
    start_time = DateTimeField('start_time', validators=[DataRequired()],
                               default=datetime.today())


class VenueForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()],
                        choices=[state.abbr for state in us.states.STATES])
    address = StringField('address', validators=[DataRequired()])
    phone = StringField('phone')
    image_link = StringField('image_link')
    genres = SelectMultipleField('genres', validators=[DataRequired()],
                                 choices=[(g.value, g.value) for g in Genre])
    facebook_link = StringField('facebook_link', validators=[URL()])
    website = StringField('website', validators=[URL()])


class ArtistForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField('state', validators=[DataRequired()],
                        choices=[state.abbr for state in us.states.STATES])
    phone = StringField('phone')
    image_link = StringField('image_link')
    genres = SelectMultipleField('genres', validators=[DataRequired()],
                                 choices=[(g.value, g.value) for g in Genre])
    facebook_link = StringField('facebook_link', validators=[URL()])
    website = StringField('website', validators=[URL()])

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
