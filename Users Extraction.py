## Get's the user details
r = []
jsonfil = []
notfound = []

count = 0
for i in my_lis:
  try:
    url = "https://api.stocktwits.com/api/2/streams/user/" + str(i) + ".json?since="
    jsonfil = requests.get(url).json()
    r.append(jsonfil['user'])
    count = count + 1
    print(count)
    print("found",i)
  except:
    notfound.append(i)
    print("Not_found",i)

no_followers = []
no_following = []
date_joined = []
watchlist_count = []
likes_count = []
username = []
userid = []

for iter in r:
  no_followers.append(iter['followers'])
  no_following.append(iter['following'])
  date_joined.append(iter['join_date'])
  watchlist_count.append(iter['watchlist_stocks_count'])
  likes_count.append(iter['like_count'])
  username.append(iter['username'])
  userid.append(iter['id'])

df = pd.DataFrame([userid,username,no_followers,no_following,date_joined,watchlist_count,likes_count])
df = df.T

df2 = pd.DataFrame([notfound])
df.columns = ["userid","username","no_of_followers","no_of_following","date_joined","watchlist_count","likes_count"]
df.to_csv('*****.csv', index=False)
df2.to_csv('*****.csv', index=False)
