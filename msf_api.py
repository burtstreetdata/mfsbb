import io
import requests
import base64

token_file ='msf_token.txt'
token_directory = '/api/'


def get_msf_token() :
    with open(token_directory + token_file) as tfile :
        token = tfile.read()
    return  token.strip()



# https://api.mysportsfeeds.com/v2.0/pull/mlb/{season}/games/{game}/playbyplay.{format}

def play_by_play_json(season, game) :
    pullurl = "https://api.mysportsfeeds.com/v2.0/pull/mlb/{}/games/{}/playbyplay.json".format(season, game)
    
    token = get_msf_token()

    pullheaders={
        "Authorization": "Basic " + base64.b64encode('{}:{}'.format(token,'MYSPORTSFEEDS').encode('utf-8')).decode('ascii')
        }
    print( pullheaders )
    print("---------")
    
    try:
        r = requests.get(
            url = pullurl,
            params = {},
            headers = pullheaders
            )
        #print('Response HTTP Status Code: {status_code}'.format(status_code=r.status_code))
        return r.content    
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
            


def pbp_to_json_file(game_id, file_name) :
    pbp = play_by_play_json('2018-reqular', game_id)
    with open (file_name, "wb") as f :
        f.write(pbp)
            
# pbp = play_by_play_json('2018-regular', '44792')

json_file = "/tmp/pbpx.json"

pbp_to_json_file('44793', json_file)
 
