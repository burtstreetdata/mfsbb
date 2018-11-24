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

json_file = "/tmp/game43469.json"

pbp_to_json_file('43469', json_file)
 


def enrich_bat_plays(ab_orig) :
    ab = copy.deepcopy(ab_orig)
    ab['lineups']=[]
    ab['lineup_hashes'] = []
    positions = ['pitcher', 'batter', 'catcher',
            'firstBaseman', 'secondBaseman', 'thirdBaseman',
            'shortStop', 
             'leftFielder', 'centerFielder', 'rightFielder' ]
    pitches = 0 ;
    lineups_enountered  = [];
# 1. gather aggregate info about atbat
# what defensive lineups are used
# count pitches
# count pitcher changes
# list involved fielders
# 2. enrich each at bat with the aggregate
    lineup_dicts = []
    for abp  in ab['atBatPlay']  :
        if 'pitch' in abp.keys() :
            pitches +=1 
        if 'playStatus' in abp.keys() :
            abp_lineuphash = ''
            lineup = abp['playStatus']
            for x in positions :
                abp_lineuphash += x
                if x in lineup.keys() and lineup[x] is not None  :
                    if 'id' in lineup[x].keys():
                        abp_lineuphash += str(lineup[x]['id'])
                    else:
                        pass
            if abp_lineuphash not in lineups_enountered :
                lineups_enountered.append(abp_lineuphash)
                lineup_dict = dict()
                for x in positions :
                    if x in lineup.keys() :
                        if lineup[x] is None :
                            lineup_dict[x] = None
                        else:
                            lineup_dict[x] = {}
                            lineup_dict[x]['id'] = lineup[x]['id']
                ab['lineups'].append( lineup_dict) 
                        
   
            abp['lineup'] = lineups_enountered.index(abp_lineuphash)
            for x in positions :
                if x in abp['playStatus'] :
                    del abp['playStatus'][x]
                    
        
        ab['lineup_hashes'] = lineups_enountered
            

    return ab
