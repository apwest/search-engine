
## Considerations: ##
# 1) Play nice! Obey robots.txt, etc
# 2) Determine a good seed page (or pages)


###############################################################################
## HELPER FUNCTIONS ###########################################################

def union(p,q):
	for e in q:
		if e not in p:
			p.append(e)


def quick_sort(elems, valfunc):
    if len(elems) <= 1:
        return elems
    pivot = elems[0]
    lte = []
    gt = []
    for e in elems[1:]:
        if valfunc(e) <= valfunc(pivot):
            lte.append(e)
        else:
            gt.append(e)
    return quick_sort(gt, valfunc) + [pivot] + quick_sort(lte, valfunc)


def collusion_with(g, k, a):
    c = []
    collusion_with_r(g, k, a, [a], c)
    return c


def collusion_with_r(g,k,a,l,c):
    b = l[-1]
    if k == 0:
        if a in g[b]:
            for i in range(len(l)-1):
                c.append((l[i],l[i+1]))
            c.append((b,a))
        return
    for node in g[b]:
        if node == a:
            for i in range(len(l)-1):
                c.append((l[i],l[i+1]))
            c.append((b,a))
        else:
            collusion_with_r(g,k-1,a,l+[node],c)

###############################################################################
## RANKING FUNCTIONS ##########################################################

def compute_ranks(graph, k=0):
	d = 0.8		# damping factor
	n = 10		# number of times to go through

	ranks = {}
	npages = len(graph)
	for page in graph:
		ranks[page] = 1.0 / npages

	for i in range(n):
		newranks = {}
		for page in graph:
			c = collusion_with(graph, k, page)
			newrank = (1-d) / npages
			for p in graph:
				if page in graph[p] and (node, page) not in c:
					newrank += d * ranks[p] / len(graph[p])
			newranks[page] = newrank
		ranks = newranks
	return ranks


def lucky_search(index, ranks, keyword):
	"""
	Limitations: this only works on a single keyword
	Todo: modify to accecpt a list of keywords and return the best
		page for all the keywords
	"""
    if keyword not in index:
        return None
    best_page = index[keyword][0]
    for page in index[keyword][1:]:
        if ranks[page] > ranks[best_page]:
            best_page = page
    return best_page


def ordered_search(index, ranks, keyword):
    if keyword not in index:
        return None
    return quick_sort(index[keyword], lambda e: ranks[e])

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
	graph = {}
	while to_crawl:
		page = to_crawl.pop()
		if page not in crawled:
			content = get_page(page)
			add_page_to_index(index, page, content)
			outlinks = get_all_links(content)
			union(to_crawl, outlinks)
			graph[page] = outlinks
			crawled.append(page)
	return index, graph

###############################################################################
## Test Code ##################################################################
seed = 'http://www.udacity.com/cs101x/urank/index.html'
print(crawl_web(seed))
