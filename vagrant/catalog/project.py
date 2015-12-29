from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, App, User
from flask import session as login_session
import random
import string

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Discover Virtual Reality Apps"


# Connect to Database and create database session

engine = create_engine('sqlite:///vrappswithusers.db')
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def createUsers(login_session):
    newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def getUserID(email):
    try: 
        user = session.query(User).filter_by(email = email).one()
        userID  = user.id
        return userID
    except: 
        print "No User can be found"
        return None


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    if "username" not in login_session:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
        login_session['state'] = state
        # return "The current session state is %s" % login_session['state']
        return render_template('login.html', STATE=state)
    else:
        output =""
        output += '<h1>Hi, '
        output += login_session['username']
        output += '!</h1>'
        output += '<img src="'
        output += login_session['picture']
        output += ' " style = "width: 200px; height: 200px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
        output += '<script>setTimeout(function(){ window.location.href="/category";}, 2000)</script>'
        flash("You are now logged in as %s" % login_session['username'])
        print "done!"
        return output
   
@app.route('/clearsession') 
def clearSession():
    del login_session['credentials'] 
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    output = "Session Cleared"
    output += '<script>setTimeout(function(){ window.location.href="/category";}, 3000)</script>'
    return output

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['credentials'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    print login_session['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUsers(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<p style = "color: #000000;">Welcome, '
    output += login_session['username']
    output += '!</p>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: 50px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output

#DISCONNECT - Revoke a current user's token and reset their login session.

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials']
    print 'In gdisconnect access token is %s' % access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['credentials']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # print 'result is '
    # print result
    if result['status'] == '200':
        del login_session['credentials'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("Successfully disconnected!")
        return redirect("/category")
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Category Information
@app.route('/category/<category_name>/apps/JSON')
def categoryAppJSON(category_name):
    category = session.query(Category).filter_by(name = category_name).one()
    category_id = category.id
    apps = session.query(App).filter_by(
        category_id=category_id).all()
    return jsonify(apps=[i.serialize for i in apps])


@app.route('/category/<category_name>/apps/<app_name>/JSON')
def appJSON(category_name, app_name):
    app = session.query(App).filter_by(name = app_name).one()
    return jsonify(app=app.serialize)


@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# Show all Categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    apps = session.query(App).order_by(App.id.desc()).limit(10)
    if 'username' in login_session:
        return render_template('categories.html', categories = categories, apps = apps)
    else:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
        login_session['state'] = state
        return render_template('publiccategories.html', STATE = state, categories=categories, apps= apps)

# Show apps in a specific category
@app.route('/category/<category_name>/')
@app.route('/category/<category_name>/apps/')
def showApp(category_name):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name = category_name).one()
    # creator = getUserInfo(category.user_id)
    apps = session.query(App).filter_by(category_id=category.id).all()
    count = session.query(App).filter_by(category_id=category.id).count()
    if count <= 1:
        count_record = str(count) + " App"
    else:
        count_record = str(count) + " Apps"
    if 'username' not in login_session:
        return render_template('publicapps.html', apps = apps, count = count_record, categories = categories, category=category)
    else:
        return render_template('apps.html', apps=apps, category=category,count = count_record, categories = categories) 

@app.route('/category/<category_name>/apps/<app_name>/')
def showAppDetails(category_name, app_name):
    app = session.query(App).filter_by(name = app_name).one()
    category = session.query(Category).filter_by(name = category_name).one()
    creator = getUserInfo(app.user_id)
    if 'username' not in login_session or creator.id !=login_session['user_id']:
        return render_template('publicappdetails.html', app = app)
    else:
        return render_template('appdetails.html', app = app, category = category)

# Create a new App item global
@app.route('/category/apps/new/', methods=['GET', 'POST'])
def newApp():
    if "username" not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        if session.query(App).filter_by(name =name).one():
            flash("An App with the same name existed.")
            return redirect(url_for('newApp'))
        newApp = App(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], website=request.form['website'], developer = request.form['developer'], category_id = request.form["category_id"], user_id = login_session['user_id'])
        session.add(newApp)
        session.commit()
        flash('New App %s Successfully Created' % (newApp.name))
        return redirect("/")
    else:
        return render_template('newApp.html')

# Create a new App item within a category
@app.route('/category/<category_name>/apps/new/', methods=['GET', 'POST'])
def newAppInCategory(category_name):
    if "username" not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(name=category_name).one()
    category_id = category.id
    if request.method == 'POST':
        # Check if the app existed.
        name = request.form['name']
        if session.query(App).filter_by(name =name).one():
            flash("An App with the same name existed.")
            return redirect(url_for('newAppInCategory', category_name = category.name))
        else:
            newApp = App(name=request.form['name'], description=request.form[
                               'description'], price=request.form['price'], website=request.form['website'], developer = request.form['developer'], category_id = category_id,user_id = login_session['user_id'])
            session.add(newApp)
            session.commit()
            flash('New App %s Successfully Created' % (newApp.name))
            return redirect(url_for('showApp', category_name=category_name))
    else:
        return render_template('newappincategory.html', category_name=category.name)

# Edit a App item


@app.route('/category/<category_name>/apps/<app_name>/edit', methods=['GET', 'POST'])
def editApp(category_name, app_name):
    editedapp = session.query(App).filter_by(name = app_name).one()
    category = session.query(Category).filter_by(name = category_name).one()
    if request.method == 'POST':
        if request.form['name']:
            editedapp.name = request.form['name']
        if request.form['description']:
            editedapp.description = request.form['description']
        if request.form['website']:
            editedapp.website = request.form['website']
        if request.form['developer']:
            editedapp.developer = request.form['developer']
        if request.form['price']:
            editedapp.price = request.form['price']
        if request.form['category_id'] != category.id:
            editedapp.category_id = request.form['category_id']
            category = session.query(Category).filter_by(id = editedapp.category_id).one()
        session.add(editedapp)
        session.commit()
        flash('App Successfully Edited')
        return redirect(url_for('showAppDetails', category_name = category.name, app_name = editedapp.name))
    else:
        return render_template('editApp.html', category = category, app = editedapp)


# Delete a App item
@app.route('/Category/<int:Category_id>/App/<int:App_id>/delete', methods=['GET', 'POST'])
def deleteApp(Category_id, App_id):
    Category = session.query(Category).filter_by(id=Category_id).one()
    itemToDelete = session.query(App).filter_by(id=App_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('App Item Successfully Deleted')
        return redirect(url_for('showApp', Category_id=Category_id))
    else:
        return render_template('deleteApp.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)