import re


def format_phone(phone: str) -> list:
    """this func converts the phone number to an 11 digit federal format"""
    phone_list = re.sub("[^0-9,]", "", phone).split(",")
    for i in range(len(phone_list)):
        if len(phone_list[i]) == 10:
            phone_list[i] = "8" + phone_list[i]
        elif len(phone_list[i]) == 6:
            if 290000 <= int(phone_list[i]) <= 299999:
                phone_list[i] = "8902663" + phone_list[i][2:]
            elif 370000 <= int(phone_list[i]) <= 379999:
                phone_list[i] = "8927667" + phone_list[i][2:]
            elif 380000 <= int(phone_list[i]) <= 389999:
                phone_list[i] = "8927668" + phone_list[i][2:]
            elif 440000 <= int(phone_list[i]) <= 449999:
                phone_list[i] = "8903358" + phone_list[i][2:]
            elif 460000 <= int(phone_list[i]) <= 464999:
                phone_list[i] = "8902287" + phone_list[i][2:]
            elif 465000 <= int(phone_list[i]) <= 469999:
                phone_list[i] = "8908301" + phone_list[i][2:]
            elif 480000 <= int(phone_list[i]) <= 484999:
                phone_list[i] = "8903322" + phone_list[i][2:]
            elif 485000 <= int(phone_list[i]) <= 489999:
                phone_list[i] = "8903345" + phone_list[i][2:]
            elif 670000 <= int(phone_list[i]) <= 679999:
                phone_list[i] = "8902327" + phone_list[i][2:]
            elif 680000 <= int(phone_list[i]) <= 689999:
                phone_list[i] = "8902328" + phone_list[i][2:]
            else:
                phone_list[i] = "88352" + phone_list[i]
        elif len(phone_list[i]) == 11:
            continue
        else:
            phone_list[i] = None
    return phone_list


def format_date(date: str) -> str:
    """get str like this: "8 мар  15:35" and  return "YYYY-MM-DD HH:MM:SS.SSS"
    I don't need indexes and sorting, if you need it in the future then use unixtime format
    """
    month = {'янв': '01', 'фев': '02', 'мар': '03', 'апр': '04', 'мая': '05', 'июн': '06', 'июл': '07',
             'авг': '08', 'сен': '09', 'окт': '10', 'ноя': '11', 'дек': '12'}
    date_list = date.split()
    return f"2021-{month[date_list[1]]}-{date_list[0]} {date[-5:]}:00:000"


if __name__ == '__main__':
    print(format_date("32 ноя  15:35"))
