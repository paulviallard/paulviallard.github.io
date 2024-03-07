import re
import os
import copy
import functools
from datetime import datetime
from pybtex.database import parse_file


###############################################################################

BIBTEX_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "student.bib")
STUDENT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "student.md")
STUDENT_TYPE_LIST = {
    "master": "Master student"
}

###############################################################################


def get_title(entry):
    title = entry.fields.get("title", "")
    title = remove_latex(title)
    return title


def get_subject(entry):
    subject = entry.fields.get("subject", "")
    subject = remove_latex(subject)
    return subject


def get_supervision(entry):
    supervision = entry.fields.get("supervision", "")
    supervision = supervision.split(", ")
    return supervision


def get_date_begin(entry):
    return entry.fields.get("date-begin", "").split("-")


def get_date_end(entry):
    return entry.fields.get("date-end", "").split("-")


def get_keywords(entry):
    keywords = entry.fields["keywords"].split(", ")
    for i, keyword in enumerate(keywords):
        keyword = keyword.replace("master-1", "master")
        keyword = keyword.replace("master-2", "master")
        keywords[i] = keyword
    return keywords



###############################################################################


def get_entry_dict(bibtex_file):

    bib = parse_file(bibtex_file)
    entry_dict = {}

    for entry in bib.entries.values():

        title = get_title(entry)
        subject = get_subject(entry)
        supervision = get_supervision(entry)
        year_begin, month_begin, day_begin = get_date_begin(entry)
        year_end, month_end, day_end = get_date_end(entry)

        new_entry = {
            "title": title,
            "subject": subject,
            "supervision": supervision,
            "year_begin": year_begin,
            "month_begin": month_begin,
            "day_begin": day_begin,
            "year_end": year_end,
            "month_end": month_end,
            "day_end": day_end,
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

    if(a["year_begin"] > b["year_begin"]):
        return +1
    elif(a["year_begin"] < b["year_begin"]):
        return -1
    elif(a["month_begin"] > b["month_begin"]):
        return +1
    elif(a["month_begin"] < b["month_begin"]):
        return -1
    elif(a["day_begin"] > b["day_begin"]):
        return +1
    elif(a["day_begin"] < b["day_begin"]):
        return -1
    elif(a["year_end"] > b["year_end"]):
        return +1
    elif(a["year_end"] < b["year_end"]):
        return -1
    elif(a["month_end"] > b["month_end"]):
        return +1
    elif(a["month_end"] < b["month_end"]):
        return -1
    elif(a["day_end"] > b["day_end"]):
        return +1
    elif(a["day_end"] < b["day_end"]):
        return -1
    elif(a["title"] > b["title"]):
        return +1
    elif(a["title"] < b["title"]):
        return -1
    elif(a["subject"] > b["subject"]):
        return +1
    elif(a["subject"] < b["subject"]):
        return -1
    elif(a["supervision"] > b["supervision"]):
        return +1
    elif(a["supervision"] < b["supervision"]):
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

    date_begin = datetime.strptime(
        entry["year_begin"]+"-"+entry["month_begin"]+"-"+entry["day_begin"],
        "%Y-%m-%d")
    date_begin = date_begin.strftime("%B %Y")
    date_end = datetime.strptime(
        entry["year_end"]+"-"+entry["month_end"]+"-"+entry["day_end"],
        "%Y-%m-%d")
    date_end = date_end.strftime("%B %Y")

    supervision = ""
    supervision_list = entry["supervision"]
    if(len(supervision_list) >= 1):
        supervision += "co-supervised with "

    for i, person in enumerate(supervision_list):
        if(len(supervision_list) >=2 and i+1 == len(supervision_list)-1):
            supervision += f"{person}, and "
        elif(len(supervision_list) >=2 and i+1 < len(supervision_list)-1):
            supervision += f"{person}, "
        else:
            supervision += f"{person}"

    string = f"**{entry['title']}** --- {entry['subject']}  \n"
    string += f"{date_begin} - {date_end}, {supervision}  "
    return string


def generate_string():

    string = ""
    entry_dict = get_entry_dict(BIBTEX_FILE)

    for student_type in STUDENT_TYPE_LIST.keys():
        if(student_type not in entry_dict):
            continue

        entry_list = entry_dict[student_type]
        entry_list = sorted(
            entry_list, key=functools.cmp_to_key(compare_entry), reverse=True)

        for entry in entry_list:
            string += generate_string_entry(entry)+"\n\n"

    return string

###############################################################################

def main():
    string = generate_string()
    with open(STUDENT_FILE, "w") as file:
        file.write(string)

# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    main()
