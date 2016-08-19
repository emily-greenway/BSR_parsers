from bsrp import BSRParser
import sys, urllib2, json

# Check a bssid is passed otherwise help
if len(sys.argv) < 2:
    print "Usage python test.py [bssid] [apikey]\nExamples:\npython test.py boston\npython test.py paris MYSECRETAPIKEY123456"
    exit

bssid = sys.argv[1]

apikey = ''
if len(sys.argv) == 3:
    apikey = sys.argv[2]

try:
    res = urllib2.urlopen("http://bikeshare-research.org/api/v1/categories/data/systems/" + bssid)
except urllib2.URLError:
    print "Couldn't retrieve the URL due to either a) Incorrect bssid, or b) Can't establish connection to server."

feeds = json.loads(res.read())

if len(feeds) == 0:
    print "No feed is specified for this BSS."
if len(feeds) > 1:
    print "The feed has " + str(len(feeds)) + " parts."

for feed in feeds:
    if feed['parsername'] is not None:
        print "Using parser: " + feed['parsername']
        parser = BSRParser(feed)

        if apikey is not '':
            print apikey
            parser.set_apikey(apikey)

        parser.retrieve()
        parser.parse()
        print parser.get_string()

        # save
        if isinstance( parser.get_raw(), basestring ):
            parser.save_raw( "" )
            print "Saved raw scraped data to " + bssid + "_test_results_raw.txt"

        parser.save( "" )
        print "Saved cleaned and schematized output to " + bssid + "_test_results.txt"

        break
    else:
        print "Feed " + feed['feedname'] + " does not have a parser assigned."
