import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from docx import Document
import re
from docx.oxml.ns import qn

# Superscript mapping for 1-9
SUPERSCRIPTS = {
    '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3',
    '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079'
}

def to_superscript(number):
    return ''.join(SUPERSCRIPTS[d] for d in str(number))

def to_superscript_seq(seq):
    # Converts a string like '1,2' to '¹,²'
    SUPERSCRIPTS = {
        '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3',
        '4': '\u2074', '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079', ',': ','
    }
    return ''.join(SUPERSCRIPTS.get(ch, ch) for ch in seq)

def parse_data(raw_text):
    lines = [line.strip() for line in raw_text.strip().split('\n') if line.strip()]
    authors = []
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

def format_block(author_affils, affil_list, affil_map):
    # Author line with all superscript numbers and commas
    author_line = []
    for author, nums in author_affils:
        num_seq = ','.join(str(n) for n in nums)
        supers = to_superscript_seq(num_seq)
        author_line.append(f"{author}{supers}")
    author_line_str = ', '.join(author_line)
    # Affiliation list with plain numbers
    affil_lines = [f"{affil_map[affil]} {affil}" for affil in affil_list]
    return f"{author_line_str}\n\n" + '\n'.join(affil_lines)

def create_new_docx(docx_path, author_affils, affil_list, affil_map):
    doc = Document()
    # Set default font to Arial
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
    # Author line with true superscript for numbers/commas
    p = doc.add_paragraph()
    for idx, (author, nums) in enumerate(author_affils):
        run = p.add_run(author)
        run.font.name = 'Arial'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
        if nums:
            num_seq = ','.join(str(n) for n in nums)
            sup_run = p.add_run(num_seq)
            sup_run.font.superscript = True
            sup_run.font.name = 'Arial'
            sup_run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
        if idx < len(author_affils) - 1:
            comma_run = p.add_run(", ")
            comma_run.font.name = 'Arial'
            comma_run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
    doc.add_paragraph("")  # Blank line
    # Affiliation list with plain numbers and period after digit
    for affil in affil_list:
        para = doc.add_paragraph(f"{affil_map[affil]}. {affil}")
        for run in para.runs:
            run.font.name = 'Arial'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
    doc.save(docx_path)

class AuthorAffiliationsApp:
    def __init__(self, root):
        self.root = root
        root.title("Author Affiliations Docx Creator")
        self.text = scrolledtext.ScrolledText(root, width=80, height=20)
        self.text.pack(padx=10, pady=10)
        self.create_btn = tk.Button(root, text="Create .docx File", command=self.process)
        self.create_btn.pack(pady=10)

    def process(self):
        raw_text = self.text.get("1.0", tk.END)
        if not raw_text.strip():
            messagebox.showerror("Error", "Please paste author-affiliation data.")
            return
        try:
            author_affils, affil_list, affil_map = parse_data(raw_text)
            save_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")], title="Save new .docx file")
            if not save_path:
                return
            create_new_docx(save_path, author_affils, affil_list, affil_map)
            messagebox.showinfo("Success", f"New .docx file created at:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = AuthorAffiliationsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 