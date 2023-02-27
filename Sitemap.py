import os
import datetime

def generate_sitemap(directory, sitemap_set=None, exclude=None, include_ext=None, priority=None, freq=None, max_urls=None):
    # Create the XML sitemap header
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # Scan the directory for files and add them to the sitemap
    urls = 0
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(subdir, file)
            if exclude and any(path in filepath for path in exclude):
                continue
            if include_ext and not filepath.endswith(tuple(include_ext)):
                continue
            if sitemap_set and filepath in sitemap_set:
                continue
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%dT%H:%M:%S%z')
            url = f'<url><loc>file://{filepath}</loc><lastmod>{mod_time}</lastmod>'
            if priority:
                url += f'<priority>{priority}</priority>'
            if freq:
                url += f'<changefreq>{freq}</changefreq>'
            url += '</url>\n'
            sitemap += url
            urls += 1
            if sitemap_set:
                sitemap_set.add(filepath)
            if max_urls and urls >= max_urls:
                sitemap += '</urlset>\n'
                yield sitemap
                sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
                sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                urls = 0

    # Close the sitemap
    sitemap += '</urlset>\n'

    yield sitemap

# Example usage
directory = "path/to/directory"
exclude = [".git", "private"]
include_ext = [".html", ".php"]
priority = "0.8"
freq = "daily"
max_urls = 50000
output_file = "sitemap.xml"

sitemap_set = set()

# Check if the output file already exists and load its contents into the sitemap set
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        for line in f:
            if "file://" in line:
                filepath = line.strip().replace("file://", "")
                sitemap_set.add(filepath)

# Generate the sitemap and write it to the output file
with open(output_file, "a") as f:
    for sitemap in generate_sitemap(directory, sitemap_set, exclude, include_ext, priority, freq, max_urls):
        f.write(sitemap)
