from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, DecimalField
from wtforms_components import TimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from wtforms.fields.html5 import DateField

from app.models import User
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators = [DataRequired()])
    email = StringField(_l('Email'), validators = [DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators = [DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators = [DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))

class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators = [DataRequired()])
    about_me = TextAreaField(_l('About me'), validators = [Length(min = 1, max = 140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username = self.username.data).first()
            if user is not None:
                raise ValidationError(_l('That username is taken.'))

class EntryForm(FlaskForm):
    title = StringField(_l('Title'), validators = [DataRequired()])
    content = TextAreaField(_l('Entry'), validators = [DataRequired()])
    is_draft = BooleanField(_l('Save As Draft'))
    submit = SubmitField(_l('Publish'))

class PreliminaryForm(FlaskForm):
    emotions = StringField(_l('How are you feeling?'), validators = [DataRequired()])
    thoughts = StringField(_l('What is going through your mind right now?'), validators = [DataRequired()])
    submit = SubmitField(_l('Done'))

class CrisisStabilizationForm(FlaskForm):
    danger_to_self = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    can_manage_thoughts_and_behaviors = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    healthy_behaviors = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    verbalized_a_plan = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    not_verbalizing_or_glorifying_dangerous_acts = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    can_identify_problems = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    understand_how_behavior_contributes_to_problems = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    motivated_to_address_behavior = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    able_to_identify_potential_issues = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    open_to_feedback = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    understand_behavior_dangerous = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    do_not_accept_blame_for_problems_outside_my_control = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    identified_personal_strengths_to_encourage_coping_decrease_stress = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    identified_weaknesses_that_discourage_coping_and_increase_stress = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    willing_to_increase_support = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    identified_healthy_behaviors = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    can_solve_problems_and_make_decision_healthy = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    willing_to_explore_alternatives = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    have_identified_appropriate_services = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])
    guardians_believe_can_benefit = StringField(_l('PLACEHOLDER_TEXT?'), validators = [DataRequired()])

class DietForm(FlaskForm):
    Date = DateField('Which day is this for? Overrides previous entry, if one exists.')
    num_meals = IntegerField(_l('Number of Meals'))
    drank_water = BooleanField(_l('Drink at least two cups of water?'))
    veggies = BooleanField(_l('Had Veggies?'))
    fruits = BooleanField(_l('Had Fruit?'))
    thirsty = BooleanField(_l('Felt Thirsty Today?'))
    sugar = BooleanField(_l('Had Sugar?'))
    junkfood = BooleanField(_l('Had Junkfood?'))
    alcohol = BooleanField(_l('Had Alcohol?'))
    caffeine = BooleanField(_l('Had Caffeine? (Coffee/Tea/Energy Drink/etc.)'))
    supplement = BooleanField(_l('Consume a multivitamin or nutrition supplement?'))
    diet_quality = IntegerField(_l('On a scale of 1-10 (10 is best), how healthy did you eat?'))

class ExerciseForm(FlaskForm):
    Date = DateField('Which day is this for? Overrides previous entry, if one exists.')
    cardio = BooleanField(_l('Cardio?'))
    strength_training = BooleanField(_l('Strength training?'))
    walked = BooleanField(_l('Walked?'))
    sweat = BooleanField(_l('Sweat during exercise?'))
    feel_sore = BooleanField(_l('Feel sore from exercise?'))
    exercise_quality = IntegerField(_l('On a scale of 1-10 (10 is most), how rigorous was your exercise overall?'))

class SleepForm(FlaskForm):
    Date = DateField('Which day is this for? Overrides previous entry, if one exists.')
    hours = DecimalField(_l('Hours of sleep?'))
    was_interrupted = BooleanField(_l('Sleep interrupted (woke up in middle)?'))
    felt_tired_immediate = BooleanField(_l('Feel tired immediately after getting up?'))
    slept_early = BooleanField(_l('Slept early?'))
    slept_on_time = BooleanField(_l('Slept on time?'))
    slept_late = BooleanField(_l('Slept late?'))
    sleep_quality = IntegerField(_l('On a scale of 1-10 (10 is best), what do you feel was the quality of your sleep?'))

class MoodForm(FlaskForm):
    Date = DateField('Which day is this for? Overrides previous entry, if one exists.')
    content = BooleanField(_l('Did you feel mostly content today?'))
    relaxted = BooleanField(_l('Did you feel mostly relaxed?'))
    excited = BooleanField(_l('Did you feel mostly excited?'))
    confident = BooleanField(_l('Did you feel mostly confident?'))
    productive = BooleanField(_l('Did you feel mostly productive?'))
    laughed = BooleanField(_l('Did you laugh today?'))
    mood_swings = BooleanField(_l('Did you have any mood swings today?'))
    talked_to_people = BooleanField(_l('Talk to more than 2 people in person?'))
    mood_quality = IntegerField(_l('On a scale of 1-10 (10 is best), how was your mood overall?'))


class QuestionaireForm(FlaskForm):
    is_student = BooleanField(_l('Are you a student?'), validators = [])
    has_occupation = BooleanField(_l('Do you have an occupation?'), validators = [])
    does_volunteer = BooleanField(_l('Do you do volunteering?'), validators = [])

    # Int Field
    weekly_work_hours = IntegerField(_l('How many hours a week do you work/study?'), validators = [])

    # Int Field
    hours_slept = IntegerField(_l('About how many hours did you sleep last night?'), validators = [])

    sleep_time = TimeField(_l('Sleep Time'), validators = [])
    wake_time = TimeField(_l('Wake Time'), validators = [])
    sleep_quality = BooleanField(_l('What do you feel the quality of your sleep?'), validators = [])
    num_meals = IntegerField(_l('How many times today did you have a meal?'), validators = [])
    num_snacks = IntegerField(_l('How many times today did you eat a snack?'), validators = [])
    diet_health_rating = BooleanField(_l('How healthy do you think your food choices are?'), validators = [])
    # = BooleanField(_l('Which of these did you have today?'), validators = [])

    has_hobby = BooleanField(_l('Do you play a sport or have a regular hobby?'), validators = [])
    has_exercised = BooleanField(_l('Did you exercise today?'), validators = [])
    type_of_exercise = StringField(_l('If yes, what kind of exercise?'), validators = [])
    exercise_quality = IntegerField(_l('Exercise quality'), validators = [])

    # Int Field
    min_exercised = IntegerField(_l('How many minutes did you spend exercising?'), validators = [])

    has_laughed = BooleanField(_l('Did you laugh today?'), validators = [])
    had_mood_swing = BooleanField(_l('Did you have a mood swing today?'), validators = [])

    # Int Field
    mood_rating = IntegerField(_l('On a scale of 1-10, how was your mood overall?'), validators = [NumberRange(1, 10, "Must choose number between 1-10")])

    # Int Field
    num_friends_seen = IntegerField(_l('About how many of your friends did you see in-person over the past day?'), validators = [])

    is_close_to_family = BooleanField(_l('Are you close to your family?'), validators = [])
    isin_relationship = BooleanField(_l('In a relationship?'), validators = [])
    wasin_relationship = BooleanField(_l('Recently been in a relationship?'), validators = [])
    depressed_today = BooleanField(_l('Did you feel depressed today?'), validators = [])
    anxious_today = BooleanField(_l('Did you feel anxious today?'), validators = [])
    stressed_today = BooleanField(_l('Did you feel stressed today?'), validators = [])

    # = BooleanField(_l('Please check the box if you experienced it today'), validators = [DataRequired()])
    # = BooleanField(_l('Which of these did you feel today, before taking this survey?'), validators = [DataRequired()])
    # = BooleanField(_l('Which of these did you feel today, before taking this survey?'), validators = [DataRequired()])
    # = BooleanField(_l('In the past day, have you...'), validators = [DataRequired()])

    submit = SubmitField(_l('Submit Questionaire'))

# class Occupation(FlaskForm):
#     Date = DateField('Which day is this for? Overrides previous entry, if one exists.')
    # Student_worker
    # Years_of_work

# External Factors
# Relationships
# Hobbies

# class Depression(FlaskForm):
    # Healthy
    # Ex-Depressed
    # Depressed
