import bibtexparser

def format_authors(author_str, emphasize='Kaustubh Joshi'):
    """Wrap the emphasized name in <em> tags."""
    authors = [a.strip() for a in author_str.split(" and ")]
    formatted = []
    for a in authors:
        if emphasize.lower() in a.lower():
            formatted.append(f"<em>{a}</em>")
        else:
            formatted.append(a)
    return ", ".join(formatted)

def format_entry(entry, emphasize='Kaustubh Joshi'):
    """Format a BibTeX entry into an HTML paragraph."""
    title = entry.get('title', '')
    authors = format_authors(entry.get('author', ''), emphasize)
    year = entry.get('year', '')
    
    # Build publication details based on entry type
    pub_details = ""
    etype = entry['ENTRYTYPE'].lower()
    if etype == 'article':
        pub_details = entry.get('journal', '')
        if 'pages' in entry:
            pub_details += ", " + entry['pages']
        if year:
            pub_details += ", " + year
    elif etype == 'inproceedings':
        pub_details = entry.get('booktitle', '')
        if 'pages' in entry:
            pub_details += ", " + entry['pages']
        if year:
            pub_details += ", " + year
    elif etype in ['phdthesis', 'mastersthesis']:
        pub_details = f"{entry.get('school', '')}, {year}"
    else:
        pub_details = year

    html = f"<p> <strong>{title}</strong> \n"
    html += f"<br> {authors} \n"
    if pub_details:
        html += f"<br> {pub_details} \n"
    html += "\n</p>\n"
    return html

def group_entries(entries):
    """Group entries into categories."""
    groups = {
        "Journal Articles": [],
        "Peer-Reviewed Conference Articles": [],
        "Theses": [],
        "Other": []
    }
    for entry in entries:
        etype = entry['ENTRYTYPE'].lower()
        if etype == 'article':
            groups["Journal Articles"].append(entry)
        elif etype == 'inproceedings':
            groups["Peer-Reviewed Conference Articles"].append(entry)
        elif etype in ['phdthesis', 'mastersthesis']:
            groups["Theses"].append(entry)
        else:
            groups["Other"].append(entry)

        for group_name in groups:
            groups[group_name].sort(key=lambda e: int(e.get('year', 0)), reverse=True)

    return groups

def main():
    # Read your BibTeX file (update the file name if necessary)
    with open('publications.bib', encoding='utf8') as bibtex_file:
        bib_db = bibtexparser.load(bibtex_file)
    
    groups = group_entries(bib_db.entries)
    
    # Start building the HTML output
    html_output = """<!-- Content -->
<section>
  <header class="main">
    <h1>Publications</h1>
  </header>
"""
    # For each category, if there are entries, add a sub-header and the formatted entries.
    for group_name, entries in groups.items():
        if entries:
            html_output += f'\n<h2 id="content"> <u>{group_name}</u> </h2>\n'
            for entry in entries:
                html_output += format_entry(entry, emphasize="Kaustubh Joshi")
    
    html_output += "\n</section>\n"
    
    # Write the HTML file
    with open("sec-pub.html", "w", encoding="utf8") as f:
        f.write(html_output)
    print("Generated publications.html successfully.")

if __name__ == '__main__':
    main()
