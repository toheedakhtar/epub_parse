# epub parser + reader in python

### Features
- does not use external libraries
- written in pure python
- parses metadata, manifest and spine of epub
- extracts text from epub 
- gives chapters path

### Usage 
- `git clone` the repo

- You can use the following functions to:

	- `get_opf_path()` 	- returns opf path from conatiner.xml file
	- `get_opf_data()` 	- returns package.opf data
	- `get_metadata()` 	- return metadata (title, author name, identifier)
	- `get_manifest()` 	- return manifest of epub
	- `get_spine()`	   	- return spine content
	- `get_chapter_path()` 	- returns path to all chapters
	- `get_text()`		- returns full text of epub

- if your run `epub.py` as script you can read epub or see its metadata.

The 2 epubs were freely available on the web.
