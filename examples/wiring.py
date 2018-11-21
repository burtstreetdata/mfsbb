#Querying elasticsearch

q=json.dumps({
  "query": { "match_all": {} },
    "_source": "game",
      "size": 3
})
url="http://localhost:9200/games/_search"
jh = {'Content-Type' : 'application/json'}
r = requests.get(url, headers=jh, data = q)
r.json()



# Loading elasticsearch


with open( "/tmp/game43469.json","r") as f :
    pbp = json.load(f)

res = requests.put("http://localhost:9200/games/game/3", headers={'Content-Type' : 'application/json'}, data = json.dumps(pbp))

# Note -- data can't be a dictionary, it has to be a string 
