import requests, json


def queryDBpedia(state):
    state = state.replace(" ", "_")

    query = '''
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    SELECT * where {
    dbr:''' + state + ''' dbo:abstract ?abstract
    FILTER (langMatches(lang(?abstract),"en"))
    }
    '''


    response = requests.get(
        'http://dbpedia.org/sparql',
        params={'query': query, 'format': 'json'},
    )
    json_response = response.json()
    print(json_response)
    return json_response


def get_universities():

    # use `keyword` to query and get a list of states
    states = []
    university = []
    extraQuery = "SERVICE <http://dbpedia.org/sparql> {?s foaf:knows ?o }"
    uniQuery = '''

        PREFIX uni: <http://www.semanticweb.org/project/group101#>
        SELECT * where { 
            ?university a uni:University.
            '''+extraQuery+'''
        } 

        '''

    uniQuery2 = """
    
    PREFIX uni: <http://www.semanticweb.org/university#>
    PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT *  FROM <http://dbpedia.org/sparql> 
    where { 

    
    SERVICE <http://localhost:7200/repositories/project> {
        ?university a uni:University.
    ?university geo:isLocatedIn geo:Massachusetts.
    BIND (URI(CONCAT("http://dbpedia.org/resource/",STRAFTER(str(?university), str(uni:)))) AS ?Db_university)
    }
   
} 
    """
    response = requests.get(
        'http://localhost:7200/repositories/project',
        params={'query': uniQuery2},
        headers={'Accept': 'application/sparql-results+json'},
    )
    json_response = json.loads(response.text)
    print(json_response)

    for universities in json_response['results']['bindings']:
         university.append(universities['university']['value'].split('#')[-1])

    print(university)
    return

get_universities()