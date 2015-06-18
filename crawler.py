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


def union(p,q):
	for e in q:
		if e not in p:
			p.append(e)


def crawl_web(seed):
	to_crawl = [seed]
	crawled = []
	while to_crawl:
		page = to_crawl.pop()
		if page not in crawled:
			crawled.append(page)
			union(to_crawl, get_all_links(get_page(page)))
	return crawled


seed = 'http://www.google.com'
print(crawl_web(seed))
