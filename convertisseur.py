from openpyxl import load_workbook
import os
import re

columns_to_keep = [0, 2, 4, 26, 32, 33, 34, 35]


def write_first_line(sheet):
    with open("data.csv", "a") as f:
        for j, row in enumerate(sheet):
            if j == 0:
                line = []
                for i, cell in enumerate(row):
                    if i in columns_to_keep:
                        line.append(cell.value)
                f.write(",".join(line)+"\n")


def process_sheet(sheet):
    global columns_to_keep

    with open("data.csv", "a") as f:
        for j, row in enumerate(sheet):
            if j != 0:
                line = []
                for i, cell in enumerate(row):
                    if i in columns_to_keep:
                        if cell.value is not None or i == 32:
                            if i == 0 or i == 2 or i == 4 or i == 26:
                                line.append("{}".format(int(cell.value)))
                            elif i == 32:
                                if cell.value is None:
                                    line.append("0")
                                else:
                                    value = str(cell.value).replace("UTC", "").replace("GMT", "").replace("na", "").replace("hour", "").replace("UCT", "").replace(" ", "")
                                    if value != "":
                                        if ":30" in value:
                                            line.append("{}.5".format(int(float(value.replace(":30", "")))))
                                        elif "3.5" in value:
                                            line.append("3.5")
                                        elif "9.9" in value:
                                            line.append("9.9")
                                        else:
                                            line.append("{}".format(int(float(value))))
                                    else:
                                        line.append("0")
                            elif 33 <= i <= 35:
                                val = str(cell.value)
                                if val.replace(" ", "") == "":
                                    line.append("|")
                                else:
                                    val = val.replace("[", "").replace("]", "").split(",")
                                    l = []
                                    for p in range(len(val)-1):
                                        if p % 2 == 0:
                                            un = val[p].replace(".5", ":30")
                                            de = val[p+1].replace(".5", ":30")
                                            if len(un.split(":")) == 1:
                                                un = "{}:00".format(un)
                                            if len(de.split(":")) == 1:
                                                de = "{}:00".format(de)
                                            l.append("[{}-{}]".format(un, de))
                                    line.append("-".join(l))
                            elif "na" in str(cell.value):
                                line.append("|")
                            else:
                                line.append("{}".format(cell.value))
                        else:
                            line.append("|")

                str_line = ",".join(line)
                if not str_line.startswith("-"):
                    if re.match(r"\|+", str_line) is None:
                        f.write("{}\n".format(str_line))


def main():
    try:
        os.remove("data.csv")
    except OSError:
        pass

    wb = load_workbook('data/data.xlsx', data_only=True)
    sheets_to_read = filter(lambda x: x.isdigit(), wb.get_sheet_names())
    write_first_line(wb["15"])
    for _, v in enumerate(sheets_to_read):
        process_sheet(wb[v])


if __name__ == '__main__':
    main()
