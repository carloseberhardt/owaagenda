"""
Screen scrape a single day view of OWA calendar
	example call
	python agenda.py "https://mail.example.com/owa/?ae=Folder&t=IPF.Appointment" username
"""
import sys, urllib2, urlparse, json, getpass
from urllib2 import URLError
from bs4 import BeautifulSoup


def getBaseUrl(url):
	baseurl = urlparse.urlparse(url)
	return "%s://%s/" % (baseurl.scheme, baseurl.netloc) 

def getHtml(url, user, pwd):
	pwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	pwdmgr.add_password(None, getBaseUrl(url), user, pwd)
	handler = urllib2.HTTPBasicAuthHandler(pwdmgr)
	html = None
	try:
		opener = urllib2.build_opener(handler)
		request = urllib2.Request(url)
		calendar = opener.open(request)
		html = calendar.read()
	except URLError, e:
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
		elif hasattr(e, 'code'):
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code
	return html

def txt_class_with_link(tag):
	return ("class","txt") in tag.attrs.items() and tag.find("a")

def scrapeAgenda(html):
	bs = BeautifulSoup(html)
	agenda = []
	for td in bs.find_all("td", {"class": "txt"}):
		for a in td.find_all("a"):
			#TODO - fix this with better parsing (time, description, location)
			tm, desc = a["title"].split(",")
			s = desc.find(";")
			if s > 0:
				desc, loc = desc[:s], desc[s+1:]
			else:
				loc = ""
			d = dict(time=tm.strip(), description=desc.strip(),location=loc.strip())
			agenda.append(d)
	return agenda

def textFormatter(thelist):
	thelist = ["%s: %s - %s" % (x['time'],x['description'],x['location']) for x in thelist]
	return "\n".join(thelist)

def jsonFormatter(thelist):
	return json.dumps(thelist)

if __name__ == '__main__':
	# better argument handling please
	url = sys.argv[1] 
	user = sys.argv[2] 
	pwd = getpass.getpass("Password: ")
	html = getHtml(url,user,pwd)
	if html == None:
		sys.exit(1)
	agenda = scrapeAgenda(html)
	print textFormatter(agenda)
