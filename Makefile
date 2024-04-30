target:=blog

all: toc book

new: clean toc book

toc:
	python3 tools/update_toc.py

book:
	jupyter-book build $(target)

open:
	open $(target)/_build/html/index.html

clean:
	rm -rf $(target)/_build
