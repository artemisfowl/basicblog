'''
	@brief file containing common routines
'''

from typing import Union
from collections import OrderedDict
from datetime import datetime
from os import scandir, sep

class PostContainer:
	def __init__(self) -> None:
		self.dfiles = OrderedDict()
		self.current = ""

	@property
	def dfiles(self) -> OrderedDict:
		return self._dfiles

	@dfiles.setter
	def dfiles(self, value: OrderedDict):
		self._dfiles = value

	@property
	def current(self):
		return self._current

	@current.setter
	def current(self, value: str):
		self._current = value

def is_dir_empty(path: str) -> bool:
	'''
		@brief function to check if the path provided is empty or has contents in it
	'''
	if not path:
		return False

	if not next(scandir(path), None):
		return True

	return False

def convert_to_odict(lfiles: list, post_container: PostContainer):
	'''
	'''
	dtmp = {file[file.rindex(f"{sep}")+1:file.rindex('.')]: file for file in lfiles if len(file) != 0}
	post_container.dfiles = OrderedDict(reversed(sorted(
		dtmp.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d-%H-%M-%S"))))

def r_mru_post(lfiles: list, post_container: PostContainer) -> Union[None, list]:
	'''
		@brief function to read the most recently updated file
	'''
	if not lfiles or len(lfiles) == 0:
		return None

	if not post_container:
		return None

	content = ""
	# convert from the list of files into a simple dictionary
	convert_to_odict(lfiles=lfiles, post_container=post_container)
	with open(post_container.dfiles[list(post_container.dfiles.keys())[0]], "r") as ifile:
		content = ifile.readlines()
		content = [line.strip() for line in content]

	return content
