
## Considerations: ##
# 1) Play nice! Obey robots.txt, etc
# 2) Determine a good seed page (or pages)


###############################################################################
## HELPER FUNCTIONS ###########################################################

def union(p,q):
	for e in q:
		if e not in p:
			p.append(e)

###############################################################################
## INDEXING FUNCTIONS #########################################################

def add_to_index(index, keyword, url):
	if keyword in index:
		index[keyword].append(url)
	else:
    	index[keyword] = [url]


def add_page_to_index(index, url, content):
    keywords = content.split()
    for key in keywords:
        add_to_index(index, key, url)


def lookup(index, keyword):
	if keyword in index:
		return index[keyword]
	return None

###############################################################################
## CRAWLING FUNCTIONS #########################################################

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote


def get_all_links(page):
	links = []
	while True:
		url, endpos = get_next_target(page)
		if url:
			links.append(url)
			page = page[endpos:]
		else:
			break
	return links


def get_page(url):
    proxy = {'http':'http://proxyw1.mitre.org:80', 'https':'https://proxyw1.mitre.org:80'}
    try:
        import urllib
        return urllib.urlopen(url, proxies=proxy).read()
    except:
        return ''


def crawl_web(seed):
	to_crawl = [seed]
	crawled = []
	index = {}
	while to_crawl:
		page = to_crawl.pop()
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			union(to_crawl, get_all_links(content))
			crawled.append(page)
	return index

###############################################################################
## Test Code ##################################################################
seed = 'http://www.google.com'
print(crawl_web(seed))
