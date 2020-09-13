import parser1
import parser2
import parser3
import csv


def del_file_info(filename):
    f = open(filename, 'w')
    f.close()


def write_csv(data, filename):
    with open(filename, 'a+', encoding='utf-8') as f:
        writer = csv.writer(f)

        for data_row in data:
            writer.writerow(data_row)


def run_parser(bot, url, data):
    """

    :param bot: Bot class
    :param url: url of parsed site
    :param data: data = [[column1, column2, column3, ], ]  To write something necessary info to csv after cleaning
    :return: None
    """
    b = bot()
    while True:
        try:
            print("Running parser({})".format(url))
            b.run()
        except Exception:
            print("Happen something bad")
            print("Do you want to reload parser1(parsed data will be removed)?")

            while True:
                text = input('Type y or n: ')

                if text.strip() == 'y':
                    run_parser(bot, url, data)
                elif text.strip() == 'n':
                    del_file_info(b.FILE_NAME)
                    write_csv(data, b.FILE_NAME)
                    print('Parser is shutting down!')
                    return None
                else:
                    print('Please type y or n')
        else:
            print('Data is successfully parsed and extracted to {}'.format(b.FILE_NAME))
            return None


if __name__ == "__main__":
    print('What parser do you want to run?')
    print('1 - gosreestr.kazpatent.kz')
    print('2 - ebulletin.kazpatent.kz')
    print('3 - wipo.int/branddb')
    print('4 - all parsers consistently')

    bots = [parser1.Bot, parser2.Bot2, parser3.Bot3]
    urls = ['gosreestr.kazpatent.kz', 'ebulletin.kazpatent.kz', 'wipo.int/branddb']
    datas = [[['Registration number', 'registration data', 'status', 'owner', 'title', 'МКТУ', 'inspiration date', 'number of bulletin', 'bulletin data', 'image url', 'page url'], ],
             [['Application number', 'data', 'owner', 'codes', 'image'], ],
             [['Brand', 'source', 'status', 'relevance', 'origin', 'holder', 'holder country', 'number', 'app. date', 'image class'], ],
             ]
    arr = zip(bots, urls, datas)

    while True:
        respond = input('Type number: ')

        if respond.strip() == '1':
            run_parser(bots[0], urls[0], datas[0])
            break
        elif respond.strip() == '2':
            run_parser(bots[1], urls[1], datas[1])
            break
        elif respond.strip() == '3':
            run_parser(bots[2], urls[2], datas[2])
            break
        elif respond.strip() == '4':
            for (bot, url, data) in arr:
                run_parser(bot, url, data)
            break
        else:
            print('Please type right number')
