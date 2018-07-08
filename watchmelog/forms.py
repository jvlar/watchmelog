from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import Required, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput

from watchmelog.models.games import MAP_CHOICES, HERO_CHOICES
from watchmelog.template_helpers import get_curr_season


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class GameForm(FlaskForm):
    sr = IntegerField("SR", validators=[Required(), NumberRange(0, 5000)])
    season = IntegerField(
        "Season",
        default=get_curr_season(),
        validators=[Required(), NumberRange(1, get_curr_season())],
    )
    map = SelectField("Played Map", choices=[(m, m) for m in MAP_CHOICES])
    heroes = MultiCheckboxField("Played Heroes", choices=[(h, h) for h in HERO_CHOICES])
