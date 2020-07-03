from googlesearch import search


### Method to search Google with provided search query
def fetch_search_results(query):

    ### Define response structure
    response = {
        "success": False,
        "results": []
    }

    try:
        ### Find results using 'search' method from google library
        ### Traverse the returned search results to put them in a list
        for link in search(query, tld="co.in", num=5, stop=5):
            response['results'].append(link)
    except Exception as e:
        ### Log the error in case search google operation raised an Exception
        print(f"Exception occured while searching Google with term {query} as {e}")
    else:
        ### Change response success status in case of postive search
        response['success'] = True

    return response
