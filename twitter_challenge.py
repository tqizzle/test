
import json as js

tweet_file = open('C:/Users/tq/Documents/Python Scripts/tweets.txt','r').readlines()

tweets = []
for i in tweet_file:
    values = js.loads(i)
    tweets.append(values)

target = open('C:/Users/tq/Documents/Python Scripts/ft1.txt','w')
#def char_trimmer(tweet): 
unicode_count = 0

for i in range(0,len(tweets)):  
    try:
        target.write(tweets[i]['text'].encode('ascii','ignore') + ' (timestamp: %s) \n'  %(str(tweets[i]['created_at'])))
        try:
            str(tweets[i]['text'])
        except UnicodeEncodeError:
            unicode_count = unicode_count + 1
    except KeyError:
        pass
    
    
    
target.write('\n%i tweet(s) contained unicode.' % (unicode_count))
target.close()

counts = {}
for i in range(0,len(tweets[1650]['entities']['hashtags'])):
    if tweets[1650]['entities']['hashtags'][i]['text'].encode('ascii','ignore') not in counts.keys():
        counts[tweets[1650]['entities']['hashtags'][i]['text'].encode('ascii','ignore')] = 1
    elif tweets[1650]['entities']['hashtags'][i]['text'].encode('ascii','ignore') in counts.keys():
        counts[tweets[1650]['entities']['hashtags'][i]['text'].encode('ascii','ignore')] += 1
