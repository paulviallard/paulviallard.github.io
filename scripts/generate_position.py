import re
import os
import copy
import functools
from datetime import datetime
from pybtex.database import parse_file


###############################################################################

BIBTEX_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "position.bib")
POSITION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "position.md")
POSITION_TYPE_LIST = {
    "internship": "Internships"
}

###############################################################################


def get_title(entry):
    title = entry.fields.get("title", "")
    title = remove_latex(title)
    return title


def get_semester(entry):
    semester = entry.fields.get("semester", "")
    semester = remove_latex(semester)
    return semester


def get_year(entry):
    return entry.fields.get("year", "")


def get_href(entry):
    return entry.fields.get("href", "")


def get_keywords(entry):
    keywords = entry.fields["keywords"].split(", ")
    return keywords

###############################################################################


def get_entry_dict(bibtex_file):

    bib = parse_file(bibtex_file)
    entry_dict = {}

    for entry in bib.entries.values():

        title = get_title(entry)
        semester = get_semester(entry)
        year = get_year(entry)
        href = get_href(entry)

        new_entry = {
            "title": title,
            "semester": semester,
            "year": year,
            "href": href,
        }
        if("keywords" in entry.fields):
            keywords = get_keywords(entry)
            for keyword in keywords:
                keyword = keyword.strip()
                if(keyword not in entry_dict):
                    entry_dict[keyword] = []
                entry_dict[keyword].append(new_entry)

    return entry_dict


def compare_entry(a, b):
    if(a["year"] > b["year"]):
        return +1
    elif(a["year"] < b["year"]):
        return -1
    if(a["semester"] > b["semester"]):
        return -1
    elif(a["semester"] < b["semester"]):
        return +1
    elif(a["title"] > b["title"]):
        return +1
    elif(a["title"] < b["title"]):
        return -1
    else:
        return 0

###############################################################################

def remove_latex(string):
    string = re.sub(r"\{*(.*?)\}*", r"\1", string)
    string = string.replace(r"\\", "")
    string = string.replace(r"\&", "&")
    string = string.replace(r"\!{\bf *}", "")
    return string


def generate_string_entry(entry):
    string = f"* **{entry['semester']} {entry['year']}** --- {entry['title']}"
    string += f" [[details]({entry['href']})]\n"
    return string


def generate_string():

    string = ""
    entry_dict = get_entry_dict(BIBTEX_FILE)

    for position_type in POSITION_TYPE_LIST.keys():
        if(position_type not in entry_dict):
            continue

        string += f"### {POSITION_TYPE_LIST[position_type]}\n\n"

        entry_list = entry_dict[position_type]
        entry_list = sorted(
            entry_list, key=functools.cmp_to_key(compare_entry), reverse=True)

        for entry in entry_list:
            string += generate_string_entry(entry)+"\n"

    return string

###############################################################################

def main():
    string = generate_string()
    with open(POSITION_FILE, "w") as file:
        file.write(string)

# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    main()
