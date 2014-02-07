from Handler import *
import jinja2
import urllib2
import xml.dom.minidom
import logging
import string

def login(username, password):
	user = username
	passwd = password
	auth_handler = urllib2.HTTPBasicAuthHandler()
	auth_handler.add_password(
		realm='New mail feed',
		uri='https://mail.google.com/mail/feed/atom/t-square',
		user='%s@gmail.com' % user,
		passwd=passwd
		)
	opener = urllib2.build_opener(auth_handler)
	urllib2.install_opener(opener)
	logging.error("Login")

def get_xkcd_data():
	xkcd_url = "http://xkcd.com/rss.xml"
	xkcd_content = urllib2.urlopen(xkcd_url).read()
	dom = xml.dom.minidom.parseString(xkcd_content)
	dom_items = dom.getElementsByTagName("item")[0]
	dom_img = dom_items.getElementsByTagName("description")[0]
	dom_title = dom_items.getElementsByTagName("title")[0]
	xkcd_img = dom_img.childNodes[0].data
	xkcd_title = dom_title.childNodes[0].data
	xkcd_img = jinja2.Markup(xkcd_img)
	return xkcd_title, xkcd_img

def get_gmail_tsquare_data():
	gmail_tsquare_url = "https://mail.google.com/mail/feed/atom/t-square"
	gmail_tsquare_content = urllib2.urlopen(gmail_tsquare_url).read()
	gmail_tsquare_content = gmail_tsquare_content.replace("""<link rel="alternate" href=\"""", "<link>")
	gmail_tsquare_content = gmail_tsquare_content.replace("""\" type="text/html" />""", "</link>")
	dom = xml.dom.minidom.parseString(gmail_tsquare_content)
	dom_entries = dom.getElementsByTagName("entry")
	titles = []
	summaries = []
	links = []
	for i in range(len(dom_entries)):
		titles.append(dom_entries[i].getElementsByTagName("title")[0].childNodes[0].data)
		summaries.append(dom_entries[i].getElementsByTagName("summary")[0].childNodes[0].data)
		link = dom_entries[i].getElementsByTagName("link")[0].childNodes[0].data
		links.append(link)
	return titles, summaries, links

def get_show_data():
	show_url = "http://showrss.info/rss.php?user_id=164896&hd=null&proper=null"
	show_content = urllib2.urlopen(show_url).read()
	dom = xml.dom.minidom.parseString(show_content)
	dom_items = dom.getElementsByTagName("item")
	titles = []
	links = []
	times = []
	for i in range(len(dom_items)):
		titles.append(dom_items[i].getElementsByTagName("title")[0].childNodes[0].data)
		links.append(dom_items[i].getElementsByTagName("link")[0].childNodes[0].data)
		times.append(dom_items[i].getElementsByTagName("pubDate")[0].childNodes[0].data)
	for link in links:
		link = jinja2.Markup(link);
	for i in range(len(times)):
		times[i] = times[i][:17]
	return titles, links, times

class PersonalHandler(Handler):
	def get(self):
		logged_in = False
		xkcd = get_xkcd_data()
		show_data = get_show_data()
		multi_tab = """window.open("https://mail.google.com/mail/u/0/?shva=1#inbox", name="_blank").focus(); window.open("http://www.youtube.com/feed/subscriptions", name="_blank").focus(); window.open("http://www.reddit.com/", name="_blank").focus();"""
		self.render("personal.html", multi_tab = multi_tab, xkcd_title = xkcd[0], xkcd_img = xkcd[1],
			show_titles = show_data[0], show_links = show_data[1], show_times = show_data[2], logged_in = logged_in)

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		login(username, password)
		logged_in = True
		xkcd = get_xkcd_data()
		gmail_tsquare = get_gmail_tsquare_data()
		show_data = get_show_data()
		multi_tab = """window.open("https://mail.google.com/mail/u/0/?shva=1#inbox", name="_blank").focus(); window.open("http://www.youtube.com/feed/subscriptions", name="_blank").focus(); window.open("http://www.reddit.com/", name="_blank").focus();"""
		self.render("personal.html", multi_tab = multi_tab, xkcd_title = xkcd[0], xkcd_img = xkcd[1],
			tsquare_titles = gmail_tsquare[0], tsquare_summaries = gmail_tsquare[1], tsquare_links = gmail_tsquare[2],
			show_titles = show_data[0], show_links = show_data[1], show_times = show_data[2], logged_in = logged_in)

	
