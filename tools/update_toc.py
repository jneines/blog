from pathlib import Path
from collections import defaultdict

from loguru import logger

# example:
# blog/2023/20231231-party_on/20231231-party_on.md

# entry dir for all blog items
blog_base_dir = Path("blog")

# A model to hold all blog items in a structured manner.
# There will be a list of tuples for every year
# Each tuple contains the date string and the path to the blog.
# This way, the model can easily be sorted

blog_model = defaultdict(list)

# The toc model is used to create the _toc.yml file later.
# It will be populated based on the contents of the blog_model
toc_model = [
    "format: jb-book",
    "root: intro",
    "chapters:",
]

# find all blog items and add them to the blog_model
blog_paths = blog_base_dir.glob("20??/20??????-*/20??????-*.*")
for blog_path in blog_paths:
    logger.debug(f"Found {blog_path}")
    base_dir, year_dir, blog_dir, blog_file = blog_path.parts
    date_str, blog_title = blog_path.stem.split("-")
    year_str = year_dir
    blog_model[year_str].append((date_str, blog_path))


# Iterate over years in reverse order: Newest items come 1st
for year_str in sorted(blog_model.keys())[::-1]:
    # Add entry for overview to the toc_model 1st
    toc_entry = f"- file: {year_str}.md\n  sections:"
    logger.debug(f"Adding new {toc_entry=}")
    toc_model.append(toc_entry)

    # Iterate over blog items of this year in reverse order.
    # Again: Newest items come 1st
    for date_str, blog_path in sorted(blog_model[year_str])[::-1]:
        rel_path = blog_path.relative_to(blog_base_dir)
        toc_entry = f"  - file: {rel_path.as_posix()}"
        logger.debug(f"Adding new {toc_entry=}")
        toc_model.append(toc_entry)

    # generate overview page for the year
    logger.debug(f"Generating overview page for {year_str}")
    with (blog_base_dir / f"{year_str}.md").open("w") as fd:
        fd.write(f"# {year_str}\n\n")


logger.debug(f"Final toc: {"\n".join(toc_model)}")
# now update the toc
logger.debug("Writing _toc.yml")
with (blog_base_dir / "_toc.yml").open("w") as fd:
    fd.write("\n".join(toc_model))
