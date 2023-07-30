from os import makedirs, sep
from glob import glob
from datetime import datetime

from flask import Flask, render_template, request

from .constants import POSTS_DIR
from .utility import is_dir_empty, PostContainer, r_mru_post

# logging configuration
application = Flask(__name__)
posts = PostContainer()

makedirs(POSTS_DIR, exist_ok=True)


@application.route("/")
def index():
	'''
		@brief Route for the default index page
		@author oldgod
		@date Fri, 21 Jul 2023 00:59:16 +0530
	'''
	global posts
	rcontent = ""
	if not is_dir_empty(POSTS_DIR):
		rcontent = r_mru_post(lfiles=glob(f"{POSTS_DIR}{sep}*.txt"), post_container=posts)

	return render_template("index.html", posts=list(posts.dfiles.values()), recent_content=rcontent,
						post_name=list(posts.dfiles.keys())[0] if len(posts.dfiles) > 0 else None)

@application.route("/post")
def post():
	global posts

	rcontent = ""
	if len(posts.dfiles) > 0:
		with open(posts.dfiles[request.args.get('name')]) as rfile:
			rcontent = rfile.readlines()
			rcontent = [line.strip() for line in rcontent]
	return render_template("post.html", page_content=rcontent, posts=list(posts.dfiles.values()),
						post_name=request.args.get('name'))

@application.route("/new")
def create_post():
	'''
	'''
	global posts

	# fixme: add the code for getting the data from the text area and the performing the creation of the file
	return render_template("new_post.html", posts=list(posts.dfiles.values()))

@application.route("/newpost", methods=["POST"])
def new_post():
	post_filepath = f"{POSTS_DIR}{sep}{datetime.now().year}-{datetime.now().month}-{datetime.now().day}-" + \
			f"{datetime.now().hour}-{datetime.now().minute}-{datetime.now().second}.txt"
	with open(post_filepath, "w") as postfile:
		postfile.write(request.form['postcontent'])

	global posts
	rcontent = ""
	if not is_dir_empty(POSTS_DIR):
		rcontent = r_mru_post(lfiles=glob(f"{POSTS_DIR}{sep}*.txt"), post_container=posts)

	return render_template("index.html", posts=list(posts.dfiles.values()), recent_content=rcontent,
						post_name=list(posts.dfiles.keys())[0] if len(posts.dfiles) > 0 else None)

@application.route("/editpost", methods=["POST"])
def edit_post():
	global posts
	post_filepath = posts.dfiles[request.form.get('postname')]
	with open(post_filepath, "w") as postfile:
		postfile.write(request.form['postcontent'])

	rcontent = ""
	if len(posts.dfiles) > 0:
		with open(posts.dfiles[request.form.get('postname')]) as rfile:
			rcontent = rfile.readlines()
			rcontent = [line.strip() for line in rcontent]
	return render_template("post.html", page_content=rcontent, posts=list(posts.dfiles.values()),
						post_name=request.form.get('postname'))

@application.route("/edit")
def edit():
	global posts
	rcontent = ""
	with open(posts.dfiles[request.args.get('name')], "r") as efile:
		rcontent = efile.readlines()
		rcontent = [line for line in rcontent if len(line) > 0]
	return render_template("edit_post.html", page_content=''.join(rcontent), posts=list(posts.dfiles.values()),
			post_name=request.args.get('name'))
