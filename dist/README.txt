AffiliWizard v1.0.0
-------------------

A GUI tool to format author-affiliation lists and export them to .docx, .html, or .txt files.

Usage:
1. Copy your author-affiliation data from Excel.
2. Paste it into the text box in AffiliWizard.
3. Click one of the export buttons (.docx, HTML, or Plain Text) to save your formatted file.

Input format example:
Author Name [TAB] Affiliation 1 [TAB] Affiliation 2 ...

Example:
John Doe, MD    Bogus Institute, CA, USA    Example Institute, TS, USA
Jane Doe, MD    Sample University, TX, USA

Files included:
- AffiliWizard-macOS-arm64.dmg   (macOS Apple Silicon installer)
- AffiliWizard.exe              (Windows executable)

If your platform is not supported, you can always use the online version at:
https://affiliwizard.netlify.app/

Build on Linux
--------------

If you’re using Linux and want to run AffiliWizard natively, you can build it from source:

1. Make sure you have Python 3 installed (recommended 3.8+).
2. Install required Python packages (you can use a virtual environment):

`python3 -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

3. Run the application directly with:

`python author_affiliations_gui.py`

4. (Optional) To create a standalone executable, you can use PyInstaller:

`pip install pyinstaller`
`pyinstaller --onefile --windowed --icon=favicon.ico author_affiliations_gui.py`

This will generate an executable in the `dist/` folder.

Note: Because Linux distributions vary, pre-built binaries are not provided, but building from source is straightforward.

License:
MIT License - Free to use and modify. Please credit the author.

Source code & support:
https://github.com/vljlangen/affiliwizard

Contact:
Ville Langén

Thank you for using AffiliWizard!
