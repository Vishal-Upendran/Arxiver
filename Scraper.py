import urllib2
from bs4 import BeautifulSoup as BS 
import Tkinter as tk
import requests
from functools import partial
from itertools import izip
import datetime as dt
import os


today = str(dt.date.today())
path = today+'/'
if not os.path.isdir(path):
	os.makedirs(path)
basepath ="https://arxiv.org/"
baspath = basepath + "list/"
TopicSubs = {'Astroph':"astro-ph/new",'AI': "cs.AI/recent", 'CompVision':"cs.CV/recent",
				'HCInteraction': "cs.HC/recent",'ImageProcess':"eess.IV/recent"}
#TopicSubs = {'AI': "cs.AI/recent"}
def Download(event,url,name):
	r = requests.get(url)
	with open(path+name+'.pdf','wb') as f:
		f.write(r.content)
def hello(event):
    print 'Double Click to exit'
print "-------------"
j = 0

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, selectbackground = 'white',bd=0, height = 800,highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

var = tk.Tk()
var.configure(background="white")
scframe = VerticalScrolledFrame(var)
scframe.pack()
for k in TopicSubs.keys():
	print "Topic: " + str(k)
	pageurl = baspath+TopicSubs[k]
	page = urllib2.urlopen(pageurl)
	soup = BS(page,'html.parser')
	Title = soup.find_all('div', attrs = {'class':'list-title mathjax'})
	URLS = soup.find_all('a',attrs = {'title':'Download PDF'})
	i = 0
	for u,t in izip(URLS,Title):
		fname = t.text.strip()
		widget = tk.Button(scframe.interior, text=fname[7:],foreground = 'green',activeforeground = 'white')
		widget.pack()
		pdfurl = basepath + str(u['href'])
		widget.bind('<Button-1>', lambda event,url = pdfurl,name = fname[7:]: Download(event,url,name))  
		j = j+1
		i = i+1
	print "--------------"
var.mainloop()

