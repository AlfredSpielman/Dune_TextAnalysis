from os import listdir, getcwd
from os.path import isfile, join
import epub

epub_dir = getcwd() + r"\epub"
epub_files = [f for f in listdir(epub_dir) if isfile(join(epub_dir, f))]