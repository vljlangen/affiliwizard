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

Building for Linux:
Linux users can build their own executable by cloning the repository and running:

  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  pyinstaller --onefile --windowed --icon=favicon.ico AffiliWizard.py

License:
MIT License - Free to use and modify. Please credit the author if the code is reused. No need to credit if only used for writing a paper.

Source code & support:
https://github.com/vljlangen/affiliwizard

Contact:
Ville Langén

Thank you for using AffiliWizard!
