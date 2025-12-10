import re
import os
import copy
import functools
from datetime import datetime
from pybtex.database import parse_file


###############################################################################

BIBTEX_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "talk.bib")
TALK_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "talk.md")
TALK_TYPE_LIST = {
    "tutorial": "Tutorials",
    "seminar": "Seminars",
    "popularization": "Science popularization",
}

###############################################################################


def get_note(entry):
    note = entry.fields.get("note", "")
    note = remove_latex(note)
    return note


def get_title(entry):
    title = entry.fields.get("title", "")
    title = remove_latex(title)
    return title


def get_event(entry):
    event_default = entry.fields.get("event", "")
    event_en = entry.fields.get("event-en", "")
    if(event_default != ""):
        return event_default
    return event_en


def get_place(entry):
    place_default = entry.fields.get("place", "")
    place_en = entry.fields.get("place-en", "")
    if(place_default != ""):
        return place_default
    return place_en


def get_date(entry):
    return entry.fields.get("date", "").split("-")


def get_website(entry):
    return entry.fields.get("website", "")


###############################################################################


def get_entry_dict(bibtex_file):

    bib = parse_file(bibtex_file)
    entry_dict = {}

    for entry in bib.entries.values():

        title = get_title(entry)
        event = get_event(entry)
        place = get_place(entry)
        year, month, day = get_date(entry)
        note = get_note(entry)
        website = get_website(entry)

        new_entry = {
            "title": title,
            "event": event,
            "place": place,
            "year": year,
            "month": month,
            "day": day,
            "note": note,
            "website": website
        }
        if("keywords" in entry.fields):
            keywords = entry.fields["keywords"].split(", ")
            for keyword in keywords:
                keyword = keyword.strip()
                if(keyword not in entry_dict):
                    entry_dict[keyword] = []
                entry_dict[keyword].append(new_entry)

    return entry_dict


def compare_entry(a, b):

    if(a["year"] > b["year"]):
        return +1
    elif(a["year"] == b["year"]):
        return 0
    else:
        if(a["month"] > b["month"]):
            return +1
        elif(a["month"] == b["month"]):
            return 0
        else:
            if(a["day"] > b["day"]):
                return +1
            elif(a["day"] == b["day"]):
                return 0
            else:
                return -1


###############################################################################

def remove_latex(string):
    string = re.sub(
        r"\\href\{([^}]+)\}\{([^}]+)\}",
        r"[\2](\1)",
        string
    )
    string = re.sub(r"\{*(.*?)\}*", r"\1", string)
    string = string.replace(r"\\", "")
    string = string.replace(r"\&", "&")
    string = string.replace(r"\!{\bf *}", "")
    return string


def generate_string_entry(entry):

    day = int(entry["day"])
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    date = datetime.strptime(
        entry["year"]+"-"+entry["month"]+"-"+entry["day"], "%Y-%m-%d")
    date = date.strftime("%b %d, %Y")
    date = date.replace(" 0", " ")
    date = date.replace(str(day), f"{day}{suffix}")

    string = f"{date}: "
    string += f"**{entry['title']}**  \n"
    string += f"{entry['event']}, {entry['place']}  \n"
    if(entry["website"] != ""):
        string += f"{entry['note']}  \n"

    if(entry["website"] == ""):
        string = string[:-3]
    else:
        string += f"[[website]({entry['website']})]"

    return string


def generate_string():

    string = ""
    entry_dict = get_entry_dict(BIBTEX_FILE)

    for talk_type in TALK_TYPE_LIST.keys():
        if(talk_type not in entry_dict):
            continue

        string += f"### {TALK_TYPE_LIST[talk_type]}\n\n"

        entry_list = entry_dict[talk_type]
        entry_list = sorted(
            entry_list, key=functools.cmp_to_key(compare_entry), reverse=True)

        for entry in entry_list:
            string += generate_string_entry(entry)+"\n\n"

    return string

###############################################################################

def main():
    string = generate_string()
    with open(TALK_FILE, "w") as file:
        file.write(string)

# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    main()
