import os
import re
from datetime import datetime

from flask import render_template, flash, redirect, request, url_for, g
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EntryForm, ResetPasswordRequestForm, ResetPasswordForm, PreliminaryForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Entry
from werkzeug.urls import url_parse
# from app.algos import get_polarity_and_subjectivity, get_text_metrics, get_depression_factor, all_or_nothing_thinking, jumping_to_conclusions, should_or_must_thinking, labeling
from app.algos import *
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from flask_babel import get_locale
from guess_language import guess_language
from sqlalchemy import and_
import stripe

SCALING_CONSTANT = 10

STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our',
             'ours', 'ourselves', 'you', 'your', 'yours',
             'yourself', 'yourselves', 'he', 'him', 'his',
             'himself', 'she', 'her', 'hers', 'herself',
             'it', 'its', 'itself', 'they', 'them', 'their',
             'theirs', 'themselves', 'what', 'which', 'who',
             'whom', 'this', 'that', 'these', 'those', 'am',
             'is', 'are', 'was', 'were', 'be', 'been', 'being',
             'have', 'has', 'had', 'having', 'do', 'does', 'did',
             'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
             'because', 'as', 'until', 'while', 'of', 'at', 'by',
             'for', 'with', 'about', 'against', 'between', 'into',
             'through', 'during', 'before', 'after', 'above', 'below',
             'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
             'under', 'again', 'further', 'then', 'once', 'here', 'there',
             'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
             'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
             'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's',
             't', 'can', 'will', 'just', 'don', 'should', 'now']

stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

CURRENT_EMOTIONS = ""
CURRENT_THOUGHTS = ""

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    return render_template('index.html',
                            title = 'Home',
                            user = current_user)
    # page = request.args.get('page', 1, type = int)
    # posts = current_user.get_own_entries().paginate(page, app.config['POSTS_PER_PAGE'], False)
    # next_url = url_for('user', username = username, page = posts.next_num) if posts.has_next else None
    # prev_url = url_for('user', username = username, page = posts.prev_num) if posts.has_prev else None
    # return render_template('user.html',
    #                         user = user,
    #                         posts = posts.items,
    #                         next_url = next_url,
    #                         prev_url = prev_url)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():

        # Verify User
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # Login
        login_user(user, remember = form.remember_me.data)

        # Redirect
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title = 'Sign In', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():

        # Set Password
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Redirect
        flash('Congratulations, {} you are now a registered user!'.format(form.username.data))
        return redirect(url_for('login'))

    return render_template('register.html', title = 'Register', form = form)


@app.route('/reset_password_request', methods = ['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title = 'Reset Password', form = form)


@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form = form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()

    form = PreliminaryForm(current_user.username)
    if form.validate_on_submit():
        global CURRENT_EMOTIONS, CURRENT_THOUGHTS
        CURRENT_EMOTIONS = form.emotions.data
        CURRENT_THOUGHTS = form.thoughts.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username = current_user))

    return render_template('user.html',
                            user = current_user,
                            form = form)


@app.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    form = EntryForm()
    if form.validate_on_submit():
        
        # Sentic Package
        phrase_sentics = get_text_metrics(form.content.data)

        
        
        sentiment = phrase_sentics["sentiment"]
        polarity = phrase_sentics["polarity"]

        if not phrase_sentics["moodtags"] and not phrase_sentics["semantics"]:
            mood_tags = ""
            semantics = ""
        else:
            mood_tags = ' '.join(phrase_sentics["moodtags"])
            semantics = ' '.join(phrase_sentics["semantics"])

        if phrase_sentics["sentics"]:
            attention = phrase_sentics["sentics"]["attention"]
            sensitivity = phrase_sentics["sentics"]["sensitivity"]
            pleasantness = phrase_sentics["sentics"]["pleasantness"]
            aptitude = phrase_sentics["sentics"]["aptitude"]
        else:
            attention = 0.0
            sensitivity = 0.0
            pleasantness = 0.0
            aptitude = 0.0


        depression_factor = get_depression_factor(form.content.data)

        language = guess_language(form.content.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''

        # Build the Entry
        entry = Entry(title = form.title.data,
                      content = form.content.data,
                      slug = re.sub('[^\w]+', '-', form.title.data.lower()),
                      is_published = (not form.is_draft.data),
                      timestamp = datetime.utcnow(),
                      author = current_user,
                      language = language,

                      # Metric Info below
                      word_semantics = semantics,
                      mood_tags = mood_tags,
                      sentiment = sentiment,
                      polarity = polarity,
                      attention = attention,
                      sensitivity = sensitivity,
                      pleasantness = pleasantness,
                      aptitude = aptitude,

                      depression_factor = depression_factor)

        db.session.add(entry)
        db.session.commit()

        # Redirect
        flash('New Entry Composed!')
        return redirect(url_for('entries', username = current_user.username))

    return render_template('create.html', title = 'Create New Entry', form = form)


@app.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username = current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',
                            title='Edit Profile',
                            form=form)


@app.route('/entries/<username>')
@login_required
def entries(username):
    page = request.args.get('page', 1, type = int)
    posts = current_user.get_own_entries().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('entries', username = username, page = posts.next_num) if posts.has_next else None
    prev_url = url_for('entries', username = username, page = posts.prev_num) if posts.has_prev else None
    return render_template('entries.html',
                            user = current_user,
                            posts = posts.items,
                            next_url = next_url,
                            prev_url = prev_url)


@app.route('/<username>/<slug>/')
@login_required
def detail(username, slug):
    post = Entry.query.filter_by(slug = slug, author = current_user).first_or_404()
    all_or_none = all_or_nothing_thinking(post.content)
    jump_conclusions = jumping_to_conclusions(post.content)
    should_or_must = should_or_must_thinking(post.content)
    label = labeling(post.content)
    return render_template('detail.html', username = current_user.username,
                            post = post, slug = slug,
                            all_or_none = all_or_none,
                            jump_conclusions = jump_conclusions,
                            should_or_must = should_or_must,
                            label = labeling)

@app.route('/<username>/dashboard/')
@login_required
def dashboard(username):
    posts = [post for post in current_user.get_own_entries().all()]
    posts.reverse()
    labels = [' '.join(post.content.split()[:5]) + "..." for post in posts[-7:]]
    text_lengths = [len(post.content.split()) for post in posts[-7:]]
    polarity = [post.polarity if post.polarity else 0 for post in posts[-7:]]
    attention = [post.attention / (len([1 for word in post.content if word.lower() not in STOPWORDS]) + 1) if post.attention else 0 for post in posts[-7:]]
    sensitivity = [post.sensitivity / (len([1 for word in post.content if word.lower() not in STOPWORDS]) + 1) if post.sensitivity else 0 for post in posts[-7:]]
    pleasantness = [post.pleasantness / (len([1 for word in post.content if word.lower() not in STOPWORDS]) + 1) if post.pleasantness else 0 for post in posts[-7:]]
    depression_factor = [post.depression_factor for post in posts[-7:]]
    return render_template('dashboard.html',
                            labels = labels,
                            text_lengths = text_lengths,
                            polarity = polarity,
                            attention = attention,
                            sensitivity = sensitivity,
                            pleasantness = pleasantness,
                            depression_factor = depression_factor)


@app.route('/charge', methods = ['GET', 'POST'])
@login_required
def charge():
    if request.method == 'POST':
        # Amount in cents
        amount = 500

        customer = stripe.Customer.create(
            email = 'customer@example.com',
            source = request.form['stripeToken']
        )

        charge = stripe.Charge.create(
            customer = customer.id,
            amount = amount,
            currency = 'usd',
            description = 'Flask Charge'
        )

        dollars = amount / 100
        cents = amount % 100
        flash('Thanks! Your payment of {} has been processed.'.format("$" + str(dollars) + "." + str(cents)))
        return render_template('charge.html', amount = amount, key = stripe_keys['publishable_key'])

    else:
        return render_template('charge.html', key = stripe_keys['publishable_key'])

@app.route('/daily_logs', methods = ['GET', 'POST'])
@login_required
def daily_logs():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    form = EntryForm()
    if form.validate_on_submit():
        
        # Sentic Package
        phrase_sentics = get_text_metrics(form.content.data)

        sentiment = phrase_sentics["sentiment"]
        polarity = phrase_sentics["polarity"]

        if not phrase_sentics["moodtags"] and not phrase_sentics["semantics"]:
            mood_tags = ""
            semantics = ""
        else:
            mood_tags = ' '.join(phrase_sentics["moodtags"])
            semantics = ' '.join(phrase_sentics["semantics"])

        if phrase_sentics["sentics"]:
            attention = phrase_sentics["sentics"]["attention"]
            sensitivity = phrase_sentics["sentics"]["sensitivity"]
            pleasantness = phrase_sentics["sentics"]["pleasantness"]
            aptitude = phrase_sentics["sentics"]["aptitude"]
        else:
            attention = 0.0
            sensitivity = 0.0
            pleasantness = 0.0
            aptitude = 0.0


        depression_factor = get_depression_factor(form.content.data)

        language = guess_language(form.content.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''

        # Build the Entry
        entry = Entry(title = form.title.data,
                      content = form.content.data,
                      slug = re.sub('[^\w]+', '-', form.title.data.lower()),
                      is_published = (not form.is_draft.data),
                      timestamp = datetime.utcnow(),
                      author = current_user,
                      language = language,

                      # Metric Info below
                      word_semantics = semantics,
                      mood_tags = mood_tags,
                      sentiment = sentiment,
                      polarity = polarity,
                      attention = attention,
                      sensitivity = sensitivity,
                      pleasantness = pleasantness,
                      aptitude = aptitude,

                      depression_factor = depression_factor)

        db.session.add(entry)
        db.session.commit()

        # Redirect
        flash('New Entry Composed!')
        return redirect(url_for('entries', username = current_user.username))

    return render_template('daily_logs.html', title = 'Daily Logs', form = form)
