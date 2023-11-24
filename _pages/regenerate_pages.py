import glob
# read the author-akash.html file to get the template
template_body = '{% assign author_data = site.authors.$first_name$ %}\n{% include author-content.html site_author=author_data name="$first_name$" %}'

# Open all files named "author-*.html"
for filename in glob.glob("_pages/author-*.html"):
    # keep the header of the template
    lines = open(filename, "r").readlines()
    header = lines[:5]

    name = header[3].split("author-")[1].replace('.html"', "")
    # print(name)

    first_name = name.split("-")[0]
    # print(first_name)

    generate_template = template_body.replace("$first_name$", first_name)
    # print(generate_template)

    new_file = "".join(header) + generate_template
    print(new_file)

    # write the new file
    open(filename, "w").write(new_file)