import re
from pyscript import when
from js import document

def parse_data(raw_text):
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    affil_map = {}
    affil_list = []
    affil_counter = 1
    author_affils = []
    for line in lines:
        cols = re.split(r'\t+', line)
        if not cols or not cols[0]:
            continue
        author = cols[0].strip()
        affils = [a.strip() for a in cols[1:] if a.strip()]
        affil_nums = []
        for affil in affils:
            if affil not in affil_map:
                affil_map[affil] = affil_counter
                affil_list.append(affil)
                affil_counter += 1
            affil_nums.append(affil_map[affil])
        author_affils.append((author, affil_nums))
    return author_affils, affil_list, affil_map

def to_superscript_seq(seq):
    SUPERSCRIPTS = {
        '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3',
        '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079', ',': ','
    }
    return ''.join(SUPERSCRIPTS.get(ch, ch) for ch in seq)

def format_block(author_affils, affil_list, affil_map):
    author_line = []
    for author, nums in author_affils:
        sorted_nums = sorted(nums)
        num_seq = ','.join(str(n) for n in sorted_nums)
        supers = to_superscript_seq(num_seq)
        author_line.append(f"{author}{supers}")
    author_line_str = ', '.join(author_line)
    affil_lines = [f"{affil_map[affil]}. {affil}" for affil in affil_list]
    return f"{author_line_str}\n\n" + '\n'.join(affil_lines)

@when("click", "#process-btn")
def process_author_info(event):
    raw_text = document.querySelector("#author-info").value
    if not raw_text.strip():
        document.querySelector("#author-output").innerHTML = "<p style='color: red;'>Please paste author-affiliation data first.</p>"
        return
    try:
        author_affils, affil_list, affil_map = parse_data(raw_text)
        output = format_block(author_affils, affil_list, affil_map)
        document.querySelector("#author-output").innerHTML = f"<pre>{output}</pre>"
    except Exception as e:
        document.querySelector("#author-output").innerHTML = f"<p style='color: red;'>Error: {e}</p>"
