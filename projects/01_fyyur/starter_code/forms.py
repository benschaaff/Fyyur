from datetime import datetime
from enum import Enum

import us
from flask_wtf import FlaskForm
from wtforms import (DateTimeField, SelectField, SelectMultipleField,
                     StringField, BooleanField)
from wtforms.validators import URL, AnyOf, DataRequired, ValidationError
import re


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


def validate_phone(form, field):
    phone_number = field.data
    if not phone_number:
        return
    valid = re.search('^[0-9]{10}$', phone_number)
    if not valid:
        raise ValidationError('Please enter a valid U.S. phone number.')


class VenueForm(FlaskForm):
    # Required Fields
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[(state.abbr, state.abbr) for state in us.states.STATES])
    address = StringField('address', validators=[DataRequired()])
    genres = SelectMultipleField('genres', validators=[DataRequired()],
                                 choices=[(g.value, g.value) for g in Genre])
    seeking_talent = BooleanField(
        'seeking_talent', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])

    # Optional Fields
    phone = StringField('phone')
    image_link = StringField('image_link')
    facebook_link = StringField('facebook_link')
    website = StringField('website')
    seeking_description = StringField('seeking_description')


class ArtistForm(FlaskForm):
    # Required Fields
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[(state.abbr, state.abbr) for state in us.states.STATES])
    genres = SelectMultipleField('genres', validators=[DataRequired()],
                                 choices=[(g.value, g.value) for g in Genre])
    email = StringField('email', validators=[DataRequired()])

    # Optional Fields
    seeking_venue = BooleanField('seeking_venue')
    phone = StringField('phone')
    image_link = StringField('image_link')
    facebook_link = StringField('facebook_link')
    website = StringField('website')
    seeking_description = StringField('seeking_description')

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
