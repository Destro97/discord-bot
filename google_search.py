from googlesearch import search


def fetch_search_results(query):
    response = {
        "success": False,
        "results": []
    }
    try:
        for link in search(query, tld="co.in", num=5, stop=5):
            response['results'].append(link)
    except Exception as e:
        print(f"Exception occured while searching Google with term {query} as {e}")
    else:
        response['success'] = True
    return response
