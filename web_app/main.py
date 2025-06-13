from pyscript import when
from js import document, Blob, URL

import re

# Parse the raw tab-separated text
def parse_data(raw_text):
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    affil_map = {}
    affil_list = []
    affil_counter = 1
    author_affils = []

    for line in lines:
        parts = re.split(r'\t+', line)
        if not parts or not parts[0]:
            continue
        author = parts[0].strip()
        affils = [a.strip() for a in parts[1:] if a.strip()]
        affil_nums = []
        for affil in affils:
            if affil not in affil_map:
                affil_map[affil] = affil_counter
                affil_list.append(affil)
                affil_counter += 1
            affil_nums.append(affil_map[affil])
        author_affils.append((author, affil_nums))

    return author_affils, affil_list, affil_map

def format_plain_text(author_affils, affil_list, affil_map):
    # One line of authors, like: John Doe (1,2), Jane Smith (3)
    author_line = []
    for author, nums in author_affils:
        affil_str = f" ({','.join(str(n) for n in sorted(nums))})" if nums else ""
        author_line.append(f"{author}{affil_str}")
    author_line_str = ', '.join(author_line)
    
    # Affiliation lines
    affil_lines = [f"{affil_map[affil]}. {affil}" for affil in affil_list]
    return f"{author_line_str}\n\n" + '\n'.join(affil_lines)


# Format as HTML
def format_html(author_affils, affil_list, affil_map):
    lines = []
    for author, nums in author_affils:
        affil_str = f"<sup>{','.join(str(n) for n in sorted(nums))}</sup>" if nums else ""
        lines.append(f"{author}{affil_str}")
    author_line = ", ".join(lines)
    affil_lines = "<br>\n".join([f"{affil_map[affil]}. {affil}" for affil in affil_list])
    return f"<p>{author_line}</p><br><p>{affil_lines}</p>"

# Display HTML in output div
@when("click", "#process-btn")
def show_html(event):
    raw_text = document.querySelector("#author-info").value
    author_affils, affil_list, affil_map = parse_data(raw_text)
    html = format_html(author_affils, affil_list, affil_map)
    document.querySelector("#author-output").innerHTML = html

# Show plain text in output
@when("click", "#show-plain-btn")
def show_plain_text(event):
    raw_text = document.querySelector("#author-info").value
    author_affils, affil_list, affil_map = parse_data(raw_text)
    plain = format_plain_text(author_affils, affil_list, affil_map)
    document.querySelector("#author-output").innerText = plain

# Export HTML
@when("click", "#export-html-btn")
def export_html(event):
    raw_text = document.querySelector("#author-info").value
    author_affils, affil_list, affil_map = parse_data(raw_text)
    html = "<html><body>" + format_html(author_affils, affil_list, affil_map) + "</body></html>"

    blob = Blob.new([html], { "type": "text/html" })
    url = URL.createObjectURL(blob)

    link = document.createElement("a")
    link.href = url
    link.download = "author_affiliations.html"
    link.click()

# Export plain text
@when("click", "#export-plain-btn")
def export_plain(event):
    raw_text = document.querySelector("#author-info").value
    author_affils, affil_list, affil_map = parse_data(raw_text)
    text = format_plain_text(author_affils, affil_list, affil_map)

    blob = Blob.new([text], { "type": "text/plain" })
    url = URL.createObjectURL(blob)

    link = document.createElement("a")
    link.href = url
    link.download = "author_affiliations.txt"
    link.click()
