import re
import os
import copy
import functools
from pybtex.database import parse_file
from collections import defaultdict


###############################################################################

BIBTEX_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "publication.bib")
PUBLICATION_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "publication.md")
PUB_TYPE_LIST = {
    "conference": "International Conference",
    "journal": "International Journal",
    "workshop": "International Workshop",
    "report": "Unpublished Research Reports",
    "nat-conference": "French Conferences",
    "misc": "Miscellaneous",
}

###############################################################################


def get_title(entry):
    title = entry.fields.get("title", "")
    title = remove_latex(title)
    return title


def get_authors(entry):
    authors_list = entry.persons.get("author", [])
    first_name_list = []
    last_name_list = []

    authors = ""
    for person in authors_list:
        first_name = " ".join(person.first_names)
        last_name = " ".join(person.last_names)
        last_name = remove_latex(last_name)
        first_name_list.append(first_name)
        last_name_list.append(last_name)
    return first_name_list, last_name_list


def get_journal_conf(entry):
    booktitle = entry.fields.get("booktitle", "")
    journal = entry.fields.get("journal", "")
    if(booktitle != ""):
        return booktitle
    return journal


def get_pdf(entry):
    return entry.fields.get("pdf", "")


def get_slides(entry):
    return entry.fields.get("slides", "")


def get_code(entry):
    return entry.fields.get("code", "")


def get_bibtex(entry):
    return entry.fields.get("bibtex", "")


def get_year(entry):
    return entry.fields.get("year", "")


def get_note(entry):
    return entry.fields.get("note", "")


def get_keywords(entry):
    return entry.fields["keywords"].split(", ")

###############################################################################


def get_entry_dict(bibtex_file):

    bib = parse_file(bibtex_file)
    entry_dict = {}

    for entry in bib.entries.values():

        title = get_title(entry)
        first_name, last_name = get_authors(entry)
        year = get_year(entry)
        journal_conf = get_journal_conf(entry)
        pdf = get_pdf(entry)
        slides = get_slides(entry)
        code = get_code(entry)
        bibtex = get_bibtex(entry)
        note = get_note(entry)
        keywords = get_keywords(entry)

        new_entry = {
            "title": title,
            "first_name": first_name,
            "last_name": last_name,
            "journal_conf": journal_conf,
            "year": year,
            "pdf": pdf,
            "slides": slides,
            "code": code,
            "bibtex": bibtex,
            "note": note,
            "keywords": keywords,
        }

        for keyword in keywords:
            keyword = keyword.strip()
            if(keyword not in entry_dict):
                entry_dict[keyword] = []
            entry_dict[keyword].append(new_entry)

    return entry_dict


def compare_entry(a, b):

    if((a["year"] == "" and b["year"] == "") or (a["year"] == b["year"])):
        year_comp = 0
    elif(int(a["year"]) > int(b["year"])):
        year_comp = +1
    else:
        year_comp = -1

    if("".join(a["last_name"]) == "".join(b["last_name"])):
        last_name_comp = 0
    elif("".join(a["last_name"]) < "".join(b["last_name"])):
        last_name_comp = +1
    else:
        last_name_comp = -1

    if("".join(a["first_name"]) == "".join(b["first_name"])):
        first_name_comp = 0
    elif("".join(a["first_name"]) < "".join(b["first_name"])):
        first_name_comp = +1
    else:
        first_name_comp = -1

    if(a["title"] == b["title"]):
        title_comp = 0
    elif(a["title"] > b["title"]):
        title_comp = +1
    else:
        title_comp = -1

    if(year_comp != 0):
        return year_comp
    if(last_name_comp != 0):
        return last_name_comp
    if(first_name_comp != 0):
        return first_name_comp
    return title_comp


###############################################################################

def remove_latex(string):
    string = string.replace(r"\!{\bf *}", "")
    string = re.sub(r"\{*(.*?)\}*", r"\1", string)
    string = string.replace(r"\\", "")
    string = string.replace(r"\&", "&")
    return string


def generate_string_entry(entry):

    entry = copy.deepcopy(entry)
    string = f"**{entry['title']}**  \n"

    for first_name, last_name in zip(entry['first_name'], entry['last_name']):

        if(f"{first_name} {last_name}" == "Paul Viallard"):
            string += f"_{first_name} {last_name}_, "
        else:
            string += f"{first_name} {last_name}, "
    string = string[:-2]+"  \n"

    if(entry["journal_conf"] != ""):
        string += f"{entry['journal_conf']}, "
        if(entry["year"] != ""):
            string += f"{entry['year']}  \n"
        else:
            string = string[:-2]+"  \n"

    if(entry["keywords"][0] == "misc"):
        if(entry["note"] != ""):
            string += f"{entry['note']}, "
            if(entry["year"] != ""):
                string += f"{entry['year']}  \n"
            else:
                string = string[:-2]+"  \n"

    if(entry["pdf"] == "" and entry["code"] == ""
       and entry["slides"] == "" and entry["bibtex"] == ""
       ):
        string = string[:-3]
    if(entry["pdf"] != ""):
        string += f"[[pdf]({entry['pdf']})] "
    if(entry["slides"] != ""):
        string += f"[[slides]({entry['slides']})] "
    if(entry["code"] != ""):
        string += f"[[code]({entry['code']})] "
    if(entry["bibtex"] != ""):
        string += f"[[bibtex]({entry['bibtex']})] "

    return string


def generate_string():

    string = ""
    entry_dict = get_entry_dict(BIBTEX_FILE)

    for pub_type in PUB_TYPE_LIST.keys():
        if(pub_type not in entry_dict):
            continue

        string += f"### {PUB_TYPE_LIST[pub_type]}\n\n"

        entry_list = entry_dict[pub_type]
        sorted_entry_list = sorted(
            entry_list, key=functools.cmp_to_key(compare_entry), reverse=True)

        for entry in sorted_entry_list:
            string += generate_string_entry(entry)+"\n\n"

    return string

###############################################################################

def main():
    string = generate_string()
    with open(PUBLICATION_FILE, "w") as file:
        file.write(string)

# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    main()
