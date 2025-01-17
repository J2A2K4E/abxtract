from gluon.contrib.markmin.markmin2html import markmin2html # library for markmin
from urllib import quote_plus # For encoding URLs
import re # For removing html tags
import string
from decimal import Decimal
import sentiment_analyzer
# reload(sentiment_analyzer)

stop_words = ["a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can","couldn","couldn't","d","did","didn","didn't","do","does","doesn","doesn't","doing","don","don't","down","during","each","few","for","from","further","had","hadn","hadn't","has","hasn","hasn't","have","haven","haven't","having","he","her","here","hers","herself","him","himself","his","how","i","if","in","into","is","isn","isn't","it","it's","its","itself","just","ll","m","ma","me","mightn","mightn't","more","most","mustn","mustn't","my","myself","needn","needn't","no","nor","not","now","o","of","off","on","once","only","or","other","our","ours","ourselves","out","over","own","re","s","same","shan","shan't","she","she's","should","should've","shouldn","shouldn't","so","some","such","t","than","that","that'll","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","ve","very","was","wasn","wasn't","we","were","weren","weren't","what","when","where","which","while","who","whom","why","will","with","won","won't","wouldn","wouldn't","y","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","could","he'd","he'll","he's","here's","how's","i'd","i'll","i'm","i've","let's","ought","she'd","she'll","that's","there's","they'd","they'll","they're","they've","we'd","we'll","we're","we've","what's","when's","where's","who's","why's","would","able","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","afterwards","ah","almost","alone","along","already","also","although","always","among","amongst","announce","another","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","arent","arise","around","aside","ask","asking","auth","available","away","awfully","b","back","became","become","becomes","becoming","beforehand","begin","beginning","beginnings","begins","behind","believe","beside","besides","beyond","biol","brief","briefly","c","ca","came","cannot","can't","cause","causes","certain","certainly","co","com","come","comes","contain","containing","contains","couldnt","date","different","done","downwards","due","e","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","ff","fifth","first","five","fix","followed","following","follows","former","formerly","forth","found","four","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","h","happens","hardly","hed","hence","hereafter","hereby","herein","heres","hereupon","hes","hi","hid","hither","home","howbeit","however","hundred","id","ie","im","immediate","immediately","importance","important","inc","indeed","index","information","instead","invention","inward","itd","it'll","j","k","keep","keeps","kept","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","line","little","'ll","look","looking","looks","ltd","made","mainly","make","makes","many","may","maybe","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","moreover","mostly","mr","mrs","much","mug","must","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","nobody","non","none","nonetheless","noone","normally","nos","noted","nothing","nowhere","obtain","obtained","obviously","often","oh","ok","okay","old","omitted","one","ones","onto","ord","others","otherwise","outside","overall","owing","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","said","saw","say","saying","says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","shed","shes","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","sufficiently","suggest","sup","sure","take","taken","taking","tell","tends","th","thank","thanks","thanx","thats","that've","thence","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","theyd","theyre","think","thou","though","thoughh","thousand","throug","throughout","thru","thus","til","tip","together","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","unfortunately","unless","unlike","unlikely","unto","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","via","viz","vol","vols","vs","w","want","wants","wasnt","way","wed","welcome","went","werent","whatever","what'll","whats","whence","whenever","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","whim","whither","whod","whoever","whole","who'll","whomever","whos","whose","widely","willing","wish","within","without","wont","words","world","wouldnt","www","x","yes","yet","youd","youre","z","zero","a's","ain't","allow","allows","apart","appear","appreciate","appropriate","associated","best","better","c'mon","c's","cant","changes","clearly","concerning","consequently","consider","considering","corresponding","course","currently","definitely","described","despite","entirely","exactly","example","going","greetings","hello","help","hopefully","ignored","inasmuch","indicate","indicated","indicates","inner","insofar","it'd","keep","keeps","novel","presumably","reasonably","second","secondly","sensible","serious","seriously","sure","t's","third","thorough","thoroughly","three","well","wonder","a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount", "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as", "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the","a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "co","op","research-articl", "pagecount","cit","ibid","les","le","au","que","est","pas","vol","el","los","pp","u201d","well-b", "http", "volumtype", "par", "0o", "0s", "3a", "3b", "3d", "6b", "6o", "a1", "a2", "a3", "a4", "ab", "ac", "ad", "ae", "af", "ag", "aj", "al", "an", "ao", "ap", "ar", "av", "aw", "ax", "ay", "az", "b1", "b2", "b3", "ba", "bc", "bd", "be", "bi", "bj", "bk", "bl", "bn", "bp", "br", "bs", "bt", "bu", "bx", "c1", "c2", "c3", "cc", "cd", "ce", "cf", "cg", "ch", "ci", "cj", "cl", "cm", "cn", "cp", "cq", "cr", "cs", "ct", "cu", "cv", "cx", "cy", "cz", "d2", "da", "dc", "dd", "de", "df", "di", "dj", "dk", "dl", "do", "dp", "dr", "ds", "dt", "du", "dx", "dy", "e2", "e3", "ea", "ec", "ed", "ee", "ef", "ei", "ej", "el", "em", "en", "eo", "ep", "eq", "er", "es", "et", "eu", "ev", "ex", "ey", "f2", "fa", "fc", "ff", "fi", "fj", "fl", "fn", "fo", "fr", "fs", "ft", "fu", "fy", "ga", "ge", "gi", "gj", "gl", "go", "gr", "gs", "gy", "h2", "h3", "hh", "hi", "hj", "ho", "hr", "hs", "hu", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ic", "ie", "ig", "ih", "ii", "ij", "il", "in", "io", "ip", "iq", "ir", "iv", "ix", "iy", "iz", "jj", "jr", "js", "jt", "ju", "ke", "kg", "kj", "km", "ko", "l2", "la", "lb", "lc", "lf", "lj", "ln", "lo", "lr", "ls", "lt", "m2", "ml", "mn", "mo", "ms", "mt", "mu", "n2", "nc", "nd", "ne", "ng", "ni", "nj", "nl", "nn", "nr", "ns", "nt", "ny", "oa", "ob", "oc", "od", "of", "og", "oi", "oj", "ol", "om", "on", "oo", "oq", "or", "os", "ot", "ou", "ow", "ox", "oz", "p1", "p2", "p3", "pc", "pd", "pe", "pf", "ph", "pi", "pj", "pk", "pl", "pm", "pn", "po", "pq", "pr", "ps", "pt", "pu", "py", "qj", "qu", "r2", "ra", "rc", "rd", "rf", "rh", "ri", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "rv", "ry", "s2", "sa", "sc", "sd", "se", "sf", "si", "sj", "sl", "sm", "sn", "sp", "sq", "sr", "ss", "st", "sy", "sz", "t1", "t2", "t3", "tb", "tc", "td", "te", "tf", "th", "ti", "tj", "tl", "tm", "tn", "tp", "tq", "tr", "ts", "tt", "tv", "tx", "ue", "ui", "uj", "uk", "um", "un", "uo", "ur", "ut", "va", "wa", "vd", "wi", "vj", "vo", "wo", "vq", "vt", "vu", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y2", "yj", "yl", "yr", "ys", "yt", "zi", "zz"]

def rm_html_tags(str):
    html_prog = re.compile(r'<[^>]+>',re.S)
    return html_prog.sub('', str)

def rm_html_escape_characters(str):
    pattern_str = r'&quot;|&amp;|&lt;|&gt;|&nbsp;|&#34;|&#38;|&#60;|&#62;|&#160;|&#20284;|&#30524;|&#26684|&#43;|&#20540|&#23612;'
    escape_characters_prog = re.compile(pattern_str, re.S)
    return escape_characters_prog.sub('', str)

def rm_at_user(str):
    return re.sub(r'@[a-zA-Z_0-9]*', '', str)

def rm_url(str):
    return re.sub(r'http[s]?:[/+]?[a-zA-Z0-9_\.\/]*', '', str)

def rm_repeat_chars(str):
    return re.sub(r'(.)(\1){2,}', r'\1\1', str)

def rm_hashtag_symbol(str):
    return re.sub(r'#', '', str)

def replace_emoticon(emoticon_dict, str):
    for k, v in emoticon_dict.items():
        str = str.replace(k, v)
    return str

def rm_time(str):
    return re.sub(r'[0-9][0-9]:[0-9][0-9]', '', str)

def rm_punctuation(current_tweet):
    return re.sub(r'[^\w\s]','',current_tweet)

def preprocess(str):
    if str[:2] == 'RT':
        str = str[2:]

    str = re.sub(r'[0-9]', '', str)

    str = str.lower()
    str = rm_url(str)
    str = rm_at_user(str)
    str = rm_repeat_chars(str)
    str = rm_hashtag_symbol(str)
    str = rm_time(str)
    str = rm_punctuation(str)
## Keep stopwords because some idioms contain stopwords
#     def remove_stopwords(str):
#         result = []
#         for word in str.split():
#             if word not in stop_words:
#                 result.append(word)
#         return ' '.join(result)
#     str = remove_stopwords(str)
    return str

def get_sentiment_results(str):
    preprocessed_data = preprocess(str)
    analyzed_sentiment = sentiment_analyzer.predict(preprocessed_data)
    if analyzed_sentiment[0] > analyzed_sentiment[2]:
          prediction = 'Negative'
    elif analyzed_sentiment[0] < analyzed_sentiment[2]:
          prediction = 'Positive'
    else:
          prediction = 'Neutral'

    return {'prediction': prediction, 'values': analyzed_sentiment}

def get_tweet_analysis(tweet_obj):
        #return tweet_obj['user']['screen_name'] + unicode('\n|\n','utf-8') + tweet_obj['text'] + unicode('\n|\n','utf-8') + unicode(get_sentiment_results(tweet_obj['text']), 'utf-8')
        timestamp_in_utc = datetime.strptime(tweet_obj['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        offset_hours = 8
        timestamp_in_sgt = timestamp_in_utc + timedelta(hours=offset_hours)

        return {
            'id': tweet_obj['id'],
            'user': tweet_obj['user'],
            'text': tweet_obj['text'],
            'sentiment_analysis': get_sentiment_results(tweet_obj['text']),
            'created_at': datetime.strftime(timestamp_in_sgt, '%I:%M:%S %p - %d %b %Y')
        }

def positiveTweets(tweet):
        if tweet['sentiment_analysis']['prediction'] == 'Positive':
            return True
        else:
            return False

def negativeTweets(tweet):
    if tweet['sentiment_analysis']['prediction'] == 'Negative':
        return True
    else:
        return False

def neutralTweets(tweet):
    if tweet['sentiment_analysis']['prediction'] == 'Neutral':
        return True
    else:
        return False


ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)
PERMITTED_TAGS = ['b', 'blockquote', 'br/', 'i', 'li', 'ol', 'ul', 'p', 'cite', 'code', 'pre', 'img/']
ALLOWED_ATTRIBUTES = {'img':['src','alt'], 'blockquote':['type']}

def getReturns(a, b):
    if b==0:
        return "-"
    else:
        if a > b:
            return "<span class='text-green'>{:,.1f}".format((a/b-1)*100)+"%</span>"
        else:
            return "<span class='text-red'>{:,.1f}".format((a/b-1)*100)+"%</span>"

def num_encode(n):
    s = []
    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0: break
    return ''.join(reversed(s))

def num_decode(s):
    n = 0
    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]
    return n

# Convert empty values to none
def empty_to_none(value):
    return (None if value == '' else value, None)

# Remove html tags from string
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Check if comment has been liked
def comment_voted(comment_id, user_id, score):
    vote = db.comment_vote(comment=comment_id, created_by=user_id)
    if vote and vote.vote == score:
        return "voted"
    else:
        return ""

# Get avatar URL
def get_avatar_url(avatar_url):
    if avatar_url:
        return URL('default','download',args=avatar_url,scheme=True,host=True)
    else:
        return '/static/_0.0.0/images/default_avatar.jpg'

# author function automatically converts user.id to user.first_name with hyperlink
def author(id):
    if id is None:
        return "Unknown"
    else:
        user = db.auth_user(id)
        html_string = "<a href='"+URL('profile',args=[user.username_slug],host=True)+"'>"+str(user.username)+"</a>"
        return html_string

db.define_table('coin_history',
    Field('coin_id','reference master'),
    Field('price_date','date'),
    Field('price_usd','decimal(30,10)',requires=empty_to_none),
    Field('bullish_count','integer',requires=empty_to_none),
    Field('bearish_count','integer',requires=empty_to_none),
    Field('neutral_count','integer',requires=empty_to_none),
    Field('influential_tweet_id','string',requires=empty_to_none),
    Field('influential_tweet_sentiment','integer',requires=empty_to_none))

# Table for Tweets
db.define_table('tweet',
                Field('tweet_id','string',unique=True,requires=IS_NOT_EMPTY()),
                Field('coin_symbol','string',length=10,requires=IS_NOT_EMPTY()),
                Field('body','text',requires=IS_NOT_EMPTY()),
                Field('created_at', 'datetime'),
                Field('retweet_count','integer'),
                Field('favorite_count','integer'),
                Field('user_id','integer'),
                Field('user_followers_count','integer'),
                Field('sentiment','integer'))

# Table for comments
db.define_table('comment',
                Field('coin','integer',requires=empty_to_none),
                Field('parent','integer',requires=empty_to_none),
                Field('parent_author','integer',requires=empty_to_none),
                Field('root_parent','integer',requires=empty_to_none),
                Field('secondary_parent','integer',requires=empty_to_none),
                Field('body','text',requires=IS_NOT_EMPTY()),
                Field('image_url','string',writable=False,requires=empty_to_none),
                Field('like','integer',default=0,writable=False),
                Field('dislike','integer',default=0,writable=False),
                Field('seen','boolean',default=False,writable=False),
                Field('link_url','string',writable=False,requires=empty_to_none),
                Field('link_title','string',writable=False,requires=empty_to_none),
                Field('link_desc','string',writable=False,requires=empty_to_none),
                Field('link_image','string',writable=False,requires=empty_to_none),
                Field('is_hidden','boolean',default=False),
                auth.signature)

# Table for comment votes
db.define_table('comment_vote',
                Field('comment','reference comment'),
                Field('vote','integer',default=0),
                Field('created_by','reference auth_user'))


db.define_table('master',
                Field('wallet_address','string',length=60,requires=empty_to_none),
                Field('is_exchange','string',length=1,requires=empty_to_none),
                Field('is_active_erc20','string',length=1,requires=empty_to_none),
                Field('cmc_id','integer',unique=True,requires=empty_to_none),
                Field('name','string',length=100,requires=IS_NOT_EMPTY()),
                Field('symbol','string',length=100,requires=IS_NOT_EMPTY()),
                Field('cmc_slug',requires=[IS_SLUG()]),
                Field('custom_slug',requires=[IS_SLUG(),IS_NOT_EMPTY()]),
                Field('coingecko_id',requires=[IS_SLUG()]),
                Field('image_url','string',requires=empty_to_none),
                Field('type','string',requires=empty_to_none),
                Field('sector','string',requires=empty_to_none),
                Field('market_cap_rank','integer',requires=empty_to_none),
                Field('circulating_supply','decimal(20,1)',requires=empty_to_none),
                Field('total_supply','decimal(20,1)',requires=empty_to_none),
                Field('usd_price','decimal(20,7)',requires=empty_to_none),
                Field('usd_volume_24h','decimal(20,2)',requires=empty_to_none),
                Field('usd_market_cap','decimal(20,1)',requires=empty_to_none),
                Field('usd_percent_change_24h','decimal(20,2)',requires=empty_to_none),
                Field('usd_percent_change_7d','decimal(20,2)',requires=empty_to_none),
                Field('website','string',requires=empty_to_none),
                Field('explorer','string',requires=empty_to_none),
                Field('github','string',requires=empty_to_none),
                Field('telegram','string',requires=empty_to_none),
                Field('discord','string',requires=empty_to_none),
                Field('bitcointalk','string',requires=empty_to_none),
                Field('twitter','string',requires=empty_to_none),
                Field('medium','string',requires=empty_to_none),
                Field('reddit','string',requires=empty_to_none),
                Field('status','string',length=50),
                Field('image_thumb', 'upload', uploadfolder=os.path.join(request.folder,'static','image_thumb'), requires=IS_EMPTY_OR(IS_IMAGE()),autodelete=True),
                Field('image_small', 'upload', uploadfolder=os.path.join(request.folder,'static','image_small'), requires=IS_EMPTY_OR(IS_IMAGE()),autodelete=True))
