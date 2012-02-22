"""
Screen scrape a single day view of OWA calendar
	example call
	python agenda.py "https://mail.example.com/owa/?ae=Folder&t=IPF.Appointment" username password
"""
import sys, urllib2, urlparse, json, getpass
from bs4 import BeautifulSoup


def getBaseUrl(url):
	baseurl = urlparse.urlparse(url)
	return "%s://%s/" % (baseurl.scheme, baseurl.netloc) 

def getHtml(url, user, pwd):
	pwdmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	pwdmgr.add_password(None, getBaseUrl(url), user, pwd)
	handler = urllib2.HTTPBasicAuthHandler(pwdmgr)
	opener = urllib2.build_opener(handler)
	request = urllib2.Request(url)
	calendar = opener.open(request)
	html = calendar.read()
	return html

def txt_class_with_link(tag):
	return ("class","txt") in tag.attrs.items() and tag.find("a")

def scrapeAgenda(html):
	bs = BeautifulSoup(html)
	agenda = []
	for td in bs.find_all("td", {"class": "txt"}):
		for a in td.find_all("a"):
			#TODO - fix this with better parsing (time, description, location)
			agenda.append(a["title"].split(","))
	return agenda

def textFormatter(thelist):
	thelist = [",".join(x) for x in thelist]
	return "\n".join(thelist)

def jsonFormatter(thelist):
	return json.dumps(thelist)

if __name__ == '__main__':
	# better argument handling please
	url = sys.argv[1] 
	user = sys.argv[2] 
	pwd = getpass.getpass("Password: ")
	html = getHtml(url,user,pwd) 
	agenda = scrapeAgenda(html)
	print textFormatter(agenda)