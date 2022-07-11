
def format_date_string(date_string, string_delimiter="-"):
    year, month, day = date_string.split(string_delimiter)
    reformatted_date = f"{day.zfill(2)}/{month.zfill(2)}/{year[-2:]}"

    return reformatted_date


def change_date_format_to_dmy(date_string, string_delimiter="/"):
    month, day, year = date_string.split(string_delimiter)
    reformatted_date = f"{day.zfill(2)}/{month.zfill(2)}/{year[-2:]}"

    return reformatted_date




