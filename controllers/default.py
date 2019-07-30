from gluon.custom_import import track_changes; track_changes(True)
from datetime import datetime, date, timedelta
import time
import gluon.contrib.simplejson as json
import oauth2

# time.sleep(5) # Set time lag


def dashboard():
    ethereum_id = 243 # ethereum
    litecoin_id = 2 # litecoin
    monero_id = 110 # monero
    moneroHistory = db(db.coin_history.coin_id==monero_id).select()
    ethereumHistory = db(db.coin_history.coin_id==ethereum_id).select()
    litecoinHistory = db(db.coin_history.coin_id==litecoin_id).select()
    
    moneroDescending = db(db.coin_history.coin_id==monero_id).select(orderby=~db.coin_history.price_date)
    ethereumDescending = db(db.coin_history.coin_id==ethereum_id).select(orderby=~db.coin_history.price_date)
    litecoinDescending = db(db.coin_history.coin_id==litecoin_id).select(orderby=~db.coin_history.price_date)
    return locals()

def insights():
    CONSUMER_KEY = '2972187968-JmUT3zeu2UyVIw315arct0tFjFO0J92r5ozwE1W'
    CONSUMER_SECRET = 'FLqXC5f1UGUX4AwaKURWNDSUrB2FkRDajZemus9TKWhwY'
    ACCESS_KEY = 'Z0ITlc1Fp5fAjZmX1ks8OzM2j'
    ACCESS_SECRET = 'aLqR5uoV2vLLHCkIFmej3R43WGrqrfluZAguHuRRq0Xk8ScDBa'

    consumer = oauth2.Consumer(key=ACCESS_KEY, secret=ACCESS_SECRET)
    token = oauth2.Token(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    client = oauth2.Client(consumer, token)

    todaysDate = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
#     coin = db(db.master.id < 1000).select(orderby='<random>').first() # Uncomment this for random coin
    coin = db(db.master.id == 1).select().first() # Uncomment this for Bitcoin
    searchTerm = "$"+coin.symbol
    url = 'https://api.twitter.com/1.1/search/tweets.json?q='+searchTerm+'&result_type=recent&count=100&lang=en&until='+todaysDate

    resp, content = cache.disk('tweets:'+coin.name, lambda:client.request(url, method="GET", headers=None), time_expire=60)

    tweets_list = json.loads(content)['statuses']

    tweets = list(map(get_tweet_analysis, tweets_list))

    humanReadableDate = date.today().strftime("%d %B, %Y")

    #time.sleep(1)

    allPositiveTweets = filter(positiveTweets, tweets)
    allNegativeTweets = filter(negativeTweets, tweets)
    allNeutralTweets = filter(neutralTweets, tweets)
    positiveCount = len(allPositiveTweets)
    negativeCount = len(allNegativeTweets)
    neutralCount = len(allNeutralTweets)
    isBullish = (len(allPositiveTweets) >= len(allNegativeTweets))

    placeholder = "" if auth.user else "Please login or register"
    if auth.user and not auth.has_membership('banned'):
        registerModal = ""
        form = SQLFORM(db.comment)
        if form.process().accepted:
            parent_author = db(db.auth_user.id == form.vars.parent_author).select().first()
            if parent_author:
                parent_author.update_record(count_new_reply = parent_author.count_new_reply + 1)
            redirect(URL('comment',args=[num_encode(int(form.vars.root_parent)+10000)],anchor='comment'+str(form.vars.id)))
        elif form.errors:
            form.errors.body = ''
            response.flash = 'Submission error. Please key in a minimum of 5 characters.'
    else:
        registerModal = "#registerModal"
        form=A('Please login to comment',_rel="nofollow",_href=URL('user/login',vars=dict(_next=URL(args=request.args, vars=request.vars))))

    return locals()


# Get first post to show on page based on page number
POST_PER_PAGE = 15
def start(page):
    page=int(page)
    start_id = page*POST_PER_PAGE
    return start_id

# Get last post to show on page based on page number
def stop(page):
    page=int(page)
    stop_id = start(page)+POST_PER_PAGE
    return stop_id

def coin():
    custom_slug = request.args(0)
    coin = db(db.master.custom_slug==custom_slug).select().first() or redirect(URL('index'))

    CONSUMER_KEY = '2972187968-JmUT3zeu2UyVIw315arct0tFjFO0J92r5ozwE1W'
    CONSUMER_SECRET = 'FLqXC5f1UGUX4AwaKURWNDSUrB2FkRDajZemus9TKWhwY'
    ACCESS_KEY = 'Z0ITlc1Fp5fAjZmX1ks8OzM2j'
    ACCESS_SECRET = 'aLqR5uoV2vLLHCkIFmej3R43WGrqrfluZAguHuRRq0Xk8ScDBa'

    consumer = oauth2.Consumer(key=ACCESS_KEY, secret=ACCESS_SECRET)
    token = oauth2.Token(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    client = oauth2.Client(consumer, token)

    todaysDate = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    searchTerm = "$"+coin.symbol
    url = 'https://api.twitter.com/1.1/search/tweets.json?q='+searchTerm+'&result_type=recent&count=100&lang=en&until='+todaysDate

    resp, content = client.request(url, method="GET", headers=None)

    tweets_list = json.loads(content)['statuses']

    tweets = list(map(get_tweet_analysis, tweets_list))

    humanReadableDate = date.today().strftime("%d %B, %Y")

    #time.sleep(1)

    allPositiveTweets = filter(positiveTweets, tweets)
    allNegativeTweets = filter(negativeTweets, tweets)
    allNeutralTweets = filter(neutralTweets, tweets)
    positiveCount = len(allPositiveTweets)
    negativeCount = len(allNegativeTweets)
    neutralCount = len(allNeutralTweets)

    isBullish = (len(allPositiveTweets) >= len(allNegativeTweets))          

    placeholder = "" if auth.user else "Please login or register"
    if auth.user and not auth.has_membership('banned'):
        registerModal = ""
        form = SQLFORM(db.comment)
        if form.process().accepted:
            parent_author = db(db.auth_user.id == form.vars.parent_author).select().first()
            if parent_author:
                parent_author.update_record(count_new_reply = parent_author.count_new_reply + 1)
            redirect(URL('comment',args=[num_encode(int(form.vars.root_parent)+10000)],anchor='comment'+str(form.vars.id)))
        elif form.errors:
            form.errors.body = ''
            response.flash = 'Submission error. Please key in a minimum of 5 characters.'
    else:
        registerModal = "#registerModal"
        form=A('Please login to comment',_rel="nofollow",_href=URL('user/login',vars=dict(_next=URL(args=request.args, vars=request.vars))))
    return locals()


@auth.requires(not auth.has_membership('banned'))
def edit_profile():
    user = db(db.auth_user.id==auth.user.id).select().first()
    return locals()


def profile():
    username_slug = request.args(0)
    member = db(db.auth_user.username_slug==username_slug).select().first() or redirect(URL('index'))
    vars = request.get_vars
    page = 0 if not vars.page else int(vars.page)
    comment_count = db(db.comment.parent==None).count()
    last_comment_on_page = stop(page)
    sqlQuery = "SELECT c.*, d.reply_count, e.name, e.custom_slug FROM (SELECT a.*,b.username,b.username_slug,b.description,b.avatar FROM comment a LEFT JOIN auth_user b ON a.created_by=b.id WHERE a.created_by="+str(member.id)+" AND a.parent IS NULL ORDER BY a.created_on DESC LIMIT "+str(POST_PER_PAGE)+" OFFSET "+str(start(page))+") c LEFT JOIN (SELECT root_parent AS root,COUNT(*) AS reply_count FROM comment GROUP BY root) d ON c.id = d.root LEFT JOIN master e ON c.coin=e.id;"
    comments = db.executesql(sqlQuery, as_dict=True)
    placeholder = "" if auth.user else "Please login or register"
    if auth.user and not auth.has_membership('banned'):
        registerModal = ""
        form = SQLFORM(db.comment)
        if form.process().accepted:
            parent_author = db(db.auth_user.id == form.vars.parent_author).select().first()
            if parent_author:
                parent_author.update_record(count_new_reply = parent_author.count_new_reply + 1)
            redirect(URL('comment',args=[num_encode(int(form.vars.root_parent)+10000)],anchor='comment'+str(form.vars.id)))
        elif form.errors:
            form.errors.body = ''
            response.flash = 'Submission error. Please key in a minimum of 5 characters.'
    else:
        registerModal = "#registerModal"
        form=A('Please login to comment',_rel="nofollow",_href=URL('user/login',vars=dict(_next=URL(args=request.args, vars=request.vars))))
    return locals()

def comment():
    slug = request.args(0) or redirect(URL('index'))
    comment_id = num_decode(slug)-10000
    sqlQuery = "SELECT c.*, d.reply_count, e.name, e.custom_slug FROM (SELECT a.*,b.username,b.username_slug,b.description,b.avatar FROM comment a LEFT JOIN auth_user b ON a.created_by=b.id WHERE a.id="+str(comment_id)+") c LEFT JOIN (SELECT root_parent AS root,COUNT(*) AS reply_count FROM comment GROUP BY root) d ON c.id = d.root LEFT JOIN master e ON c.coin=e.id;"
    comment = db.executesql(sqlQuery, as_dict = True)
    comment = comment[0]
    placeholder = "" if auth.user else "Please login or register"
    if auth.user and not auth.has_membership('banned'):
        registerModal = ""
        form = SQLFORM(db.comment)
        if form.process().accepted:
            parent_author = db(db.auth_user.id == form.vars.parent_author).select().first()
            if parent_author:
                parent_author.update_record(count_new_reply = parent_author.count_new_reply + 1)
            redirect(URL('comment',args=[num_encode(int(form.vars.root_parent)+10000)],anchor='comment'+str(form.vars.id)))
        elif form.errors:
            form.errors.body = ''
            response.flash = 'Submission error. Please key in a minimum of 5 characters.'
    else:
        registerModal = "#registerModal"
        form=A('Please login to comment',_rel="nofollow",_href=URL('user/login',vars=dict(_next=URL(args=request.args, vars=request.vars))))
    return locals()


def index():
    import keywords
    vars = request.get_vars
    page = 0 if not vars.page else int(vars.page)
    comment_count = db(db.comment.parent==None).count()
    last_comment_on_page = stop(page)

    sqlQuery = "SELECT c.*, d.reply_count, e.name, e.custom_slug FROM (SELECT a.*,b.username,b.username_slug,b.description,b.avatar FROM comment a LEFT JOIN auth_user b ON a.created_by=b.id WHERE a.parent IS NULL ORDER BY a.created_on DESC LIMIT "+str(POST_PER_PAGE)+" OFFSET "+str(start(page))+") c LEFT JOIN (SELECT root_parent AS root,COUNT(*) AS reply_count FROM comment GROUP BY root) d ON c.id = d.root LEFT JOIN master e ON c.coin=e.id;"
    comments = db.executesql(sqlQuery, as_dict = True)

    nowDate = datetime.now().date()
    ethereumStats = db((db.coin_history.coin_id==243)&(db.coin_history.price_date==nowDate)).select().first()
    litecoinStats = db((db.coin_history.coin_id==2)&(db.coin_history.price_date==nowDate)).select().first()
    moneroStats = db((db.coin_history.coin_id==110)&(db.coin_history.price_date==nowDate)).select().first()

    placeholder = "" if auth.user else "Please login or register"
    if auth.user and not auth.has_membership('banned'):
        registerModal = ""
        form = SQLFORM(db.comment)
        if form.process().accepted:
            parent_author = db(db.auth_user.id == form.vars.parent_author).select().first()
            if parent_author:
                parent_author.update_record(count_new_reply = parent_author.count_new_reply + 1)
            redirect(URL('comment',args=[num_encode(int(form.vars.root_parent)+10000)],anchor=form.vars.id))
        elif form.errors:
            form.errors.body = ''
            response.flash = 'Submission error. Please key in a minimum of 5 characters.'
    else:
        registerModal = "#registerModal"
        form=A('Please login to comment',_rel="nofollow",_href=URL('user/login',vars=dict(_next=URL(args=request.args, vars=request.vars))))
    return locals()

# ---- Action for login/register/etc (required for auth) -----
def user():
    page = request.args(0)
    redirect_URL = request.get_vars._next
    if page == 'profile':
        db.auth_user.email.writable = False
        db.auth_user.email.readable = False
        db.auth_user.newsletter.writable = True
        db.auth_user.description.writable = True
        db.auth_user.website.writable = True
        db.auth_user.avatar.writable = True
        form = auth()

        if form.process().accepted:
            db.auth_user(form.vars.id).update_record(username_slug=IS_SLUG.urlify(form.vars.username))
            auth.user.update(username=form.vars.username)
            redirect(URL("profile")) if redirect_URL == "/" else redirect(redirect_URL)
    elif page == 'login':
        db.auth_user.username.label = T("Username or Email")
        auth.settings.login_userfield = 'username'
        if request.vars.username and not IS_EMAIL()(request.vars.username)[1]:
            auth.settings.login_userfield = 'email'
            request.vars.email = request.vars.username
            request.post_vars.email = request.vars.email
            request.vars.username = None
            request.post_vars.username = None
        form=auth()
    elif page == 'request_reset_password':
        db.auth_user.username.label = T("Email")
        auth.settings.login_userfield = 'email'
        form = auth()
    else:
        form = auth()
    return locals()


# ---- action to server uploaded static content (required) ---
@cache.action(time_expire=315360000)
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
