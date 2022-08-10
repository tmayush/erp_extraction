import datetime


def get_formatted_date():
    cur_datetime_obj = datetime.datetime.now()
    return cur_datetime_obj.strftime("%A, %d-%m-%Y")


def main():
    print(get_formatted_date())


if __name__ == "__main__":
    main()
