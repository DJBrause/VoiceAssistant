import wikipedia

# https://wikipedia.readthedocs.io/en/latest/code.html#api


def search_in_wikipedia(searched_term):
    search_result = wikipedia.search(str(searched_term))
    page = wikipedia.WikipediaPage(title=search_result[0], pageid=None)
    # page_summary = page.summary
    try:
        page_summary_2 = wikipedia.summary(page, sentences=3)
        return page_summary_2
    except Exception as e:
        print(e)
