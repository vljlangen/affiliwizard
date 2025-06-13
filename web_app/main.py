from pyscript import when
from js import document, Blob, URL

# Mapping digits to superscript unicode
SUPERSCRIPTS = {
    '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3',
    '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077',
    '8': '\u2078', '9': '\u2079', ',': ','
}

def to_superscript_seq(seq):
    return ''.join(SUPERSCRIPTS.get(ch, ch) for ch in seq)

def parse_data(raw_text):
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    author_affils = []
    affil_map = {}
    affil_list = []
    affil_counter = 1

    for line in lines:
        parts = line.split('\t')
        if not parts:
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

def generate_html(author_affils, affil_list, affil_map):
    # Author line with superscripts
    authors = []
    for name, nums in author_affils:
        num_seq = ','.join(str(n) for n in sorted(nums))
        supers = f"<sup>{num_seq}</sup>" if num_seq else ""
        authors.append(f"{name}{supers}")
    author_line = ', '.join(authors)

    # Affiliation list
    affil_lines = [f"{affil_map[a]}. {a}" for a in affil_list]
    affil_html = '<br>'.join(affil_lines)

    return f"<p>{author_line}</p><br><p>{affil_html}</p>"

@when("click", "#process-btn")
def handle_show_text(event):
    raw_text = document.querySelector("#author-info").value
    author_affils, affil_list, affil_map = parse_data(raw_text)
    output_html = generate_html(author_affils, affil_list, affil_map)
    document.querySelector("#author-output").innerHTML = output_html

@when("click", "#export-html")
def handle_export_html(event):
    raw_text = document.querySelector("#author-info").value
    author_affils, affil_list, affil_map = parse_data(raw_text)
    body = generate_html(author_affils, affil_list, affil_map)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Exported Author Info</title></head>
<body>{body}</body></html>
"""
    blob = Blob.new([html], { "type": "text/html" })
    url = URL.createObjectURL(blob)
    link = document.createElement("a")
    link.href = url
    link.download = "author_affiliations.html"
    link.click()
    URL.revokeObjectURL(url)
