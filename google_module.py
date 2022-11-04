# https://www.geeksforgeeks.org/performing-google-search-using-python-code/

from googlesearch import search

result = search("what is raviolli", stop=3)

for i in result:
    print(i)

