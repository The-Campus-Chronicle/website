# Load config file
import yaml



config = ''
with open('.\_config.yml', 'r') as f:
    config = f.read()

# Only use the text after authors: and before defaults:
config = config.split('authors:')[1].split('# Defaults')[0]

authors_data = yaml.safe_load(config)

authors = list(authors_data.values())


# Print information about each author
for author_name, author in authors_data.items():
    print("Author:", author_name)
    print("Name:", author["name"])
    print("Avatar:", author["avatar"])
    print("Role:", author["role"])
    print("Bio:", author["bio"])
    print("Email:", author["email"])
    print("School:", author["school"])
    print("Grade:", author["grade"])

    # Generate the author pages
    home = f'---\ntitle: "{author["name"]}"\nlayout: default\npermalink: "/author-{author["name"].lower().replace(" ", "-")}.html"\n---'
    body = '{% assign site_author = site.authors.$name$ %}\n{% assign name = "$name$" %}\n{% include author-content.html %}'
    body = body.replace('$name$', author_name)
    with open(f'_pages/author-{author_name}.html', 'w') as f:
        f.write(home + '\n' + body)