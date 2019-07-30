import requests
import datetime
from random import randint
try:
  import simplejson as json
except:
  import json
import cfscrape
import lxml.html
from io import BytesIO
from PIL import Image
import base64


# Get comment rank
def comment_rank():
    comment_id = 1
    comment = db.comment(comment_id)
    epochtime = (comment.created_on - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    # Let 1 vote equal bumping up comment by 1 hour
    rank = epochtime + max(-345600, min(345600, (comment.like-comment.dislike)*3600))
    test = (request.now - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    return locals()


# Like comment
@auth.requires(not auth.has_membership('banned'))
def comment_like():
    vars = request.post_vars
    comment = db.comment(vars.id)
    comment_vote = db((db.comment_vote.comment==vars.id)&(db.comment_vote.created_by==auth.user.id)).select().first()
    if not(comment_vote) or comment_vote.vote==0:
        db.comment_vote.update_or_insert((db.comment_vote.comment==vars.id) & (db.comment_vote.created_by==auth.user.id), comment=vars.id, created_by=auth.user.id, vote=1)
        like_count = comment.like + 1
        db(db.comment.id==vars.id).update(like=like_count)
        return str(like_count)
    elif comment_vote.vote==-1:
        db.comment_vote.update_or_insert((db.comment_vote.comment==vars.id) & (db.comment_vote.created_by==auth.user.id), comment=vars.id, created_by=auth.user.id, vote=1)
        like_count = comment.like + 1
        dislike_count = comment.dislike - 1
        db(db.comment.id==vars.id).update(like=like_count, dislike=dislike_count)
        return str(like_count)
    else:
        db.comment_vote.update_or_insert((db.comment_vote.comment==vars.id) & (db.comment_vote.created_by==auth.user.id), comment=vars.id, created_by=auth.user.id, vote=0)
        like_count = comment.like - 1
        db(db.comment.id==vars.id).update(like=like_count)
        html_output = str(like_count) if like_count > 0 else ''
        return html_output


# Upload avatar
@auth.requires(not auth.has_membership('banned'))
def update_profile():
    vars = request.post_vars
    if vars.image != '':
        image_base64 = vars.image
        image_processed = image_base64[image_base64.find(",")+1:]
        image_processed = image_processed.replace(' ','+')
        image1 = Image.open(BytesIO(base64.b64decode(image_processed)))
        output = BytesIO()
        image1.save(output, format='PNG')  # or another format
        output.seek(0)
        db(db.auth_user.id==auth.user.id).update(username=vars.username, description=vars.bio, website=vars.website, ethaddress=vars.ethaddress, avatar = db.auth_user.avatar.store(output, 'avatar.png'))
    else:
        db(db.auth_user.id==auth.user.id).update(username=vars.username, description=vars.bio, website=vars.website, ethaddress=vars.ethaddress)
    session.flash = 'Your profile has been updated successfully'
    return 'success'


# Load search suggestions
def search():
    vars = request.post_vars
    searchTerm = vars.search_term.strip()
    list = db((db.master.symbol.startswith(searchTerm))|(db.master.name.startswith(searchTerm))).select(orderby=~db.master.usd_market_cap,limitby=(0, 12))
    html_string = ''
    counter = 0
    for coin in list:
        if counter==0:
            html_string = (html_string+'<a class="dropdown-item active first-result" href="/coin/'+coin.custom_slug+'"><img src="/static/_0.0.0/image_thumb/'+str(coin['image_thumb'])+'">  '+coin.name+' ('+coin.symbol+')</a>')
            counter = 1
        else:
            html_string = (html_string+'<a class="dropdown-item" href="/coin/'+coin.custom_slug+'"><img src="/static/_0.0.0/image_thumb/'+str(coin['image_thumb'])+'">  '+coin.name+' ('+coin.symbol+')</a>')
    return html_string

# Check if username exists in registration form
def check_username():
    vars = request.post_vars
    username_slug = IS_SLUG.urlify(vars.username)
    if len(username_slug)>3:
        user = db.auth_user(username_slug=username_slug)
        if user:
            if auth.user:
                if user.id == auth.user.id:
                    return ''
                else:
                    return 'taken'
            else:
                return 'taken'
        else:
            return 'available'

# Check if email exists in registration form
def check_email():
    vars = request.post_vars
    if db.auth_user(email=vars.email):
        return '<span style="color:red;">Email has been registered</span>'
    else:
        return ''

# Upload comment body and image
@auth.requires(not auth.has_membership('banned'))
def upload():
    vars = request.post_vars
    if vars and auth.user:
        db.comment.insert(body=vars.body)
    return 'success'

# Vote comment
@auth.requires(not auth.has_membership('banned'))
def comment_vote():
    vars = request.post_vars
    comment = db.comment(vars.id)
    if comment:
        if vars.action == "like":
            db.comment_vote.update_or_insert((db.comment_vote.comment == vars.id) & (db.comment_vote.created_by == auth.user.id),
                                        comment=vars.id,
                                        created_by=auth.user.id,
                                        vote=1)
            like_count = db((db.comment_vote.comment == vars.id)&(db.comment_vote.vote == 1)).count()
            db(db.comment.id==vars.id).update(like=like_count)
            return str(like_count)
        elif vars.action == "unlike":
            db.comment_vote.update_or_insert((db.comment_vote.comment == vars.id) & (db.comment_vote.created_by == auth.user.id),
                                        comment=vars.id,
                                        created_by=auth.user.id,
                                        vote=0)
            like_count = db((db.comment_vote.comment == vars.id)&(db.comment_vote.vote == 1)).count()
            db(db.comment.id==vars.id).update(like=like_count)
            html_output = str(like_count) if like_count > 0 else ''
            return html_output
        elif vars.action == "dislike":
            db.comment_vote.update_or_insert((db.comment_vote.comment == vars.id) & (db.comment_vote.created_by == auth.user.id),
                                        comment=vars.id,
                                        created_by=auth.user.id,
                                        vote=-1)
            dislike_count = db((db.comment_vote.comment == vars.id)&(db.comment_vote.vote == -1)).count()
            db(db.comment.id==vars.id).update(dislike=dislike_count)
            return str(dislike_count)
        elif vars.action == "undislike":
            db.comment_vote.update_or_insert((db.comment_vote.comment == vars.id) & (db.comment_vote.created_by == auth.user.id),
                                        comment=vars.id,
                                        created_by=auth.user.id,
                                        vote=0)
            like_count = db((db.comment_vote.comment == vars.id)&(db.comment_vote.vote == 1)).count()
            db(db.comment.id==vars.id).update(like=like_count)
            html_output = str(like_count) if like_count > 0 else ''
            return html_output
