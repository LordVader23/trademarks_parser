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


def run_parser(bot, url):
    """

    :param bot: object of class Bot
    :return:
    """
    while True:
        try:
            print("Running parser({})".format(url))
            bot.run()
        except Exception:
            print("Happen something bad")
            print("Do you want to reload parser1(parsed data will be removed)?")
            text = input('Type y or n')

            while True:
                if text.strip() == 'y':
                    pass
                elif text.strip() == 'n':
                    del_file_info(bot.FILE_NAME)
                    print('Parser is shutting down!')
                    break
                else:
                    print('Please type y or n')
        else:
            pass


if __name__ == "__main__":
    while True:
        try:
            b1 = parser1.Bot1()
            print("Run first parser(gosreestr.kazpatent.kz)")
            b1.run()
        except Exception:
            print("Happen something bad")
            print("Do you want to reload parser1(parsed data will be removed)?")
            text = input('Type y or n')

            while True:
                if text.strip() == 'y':
                    pass
                elif text.strip() == 'n':
                    print('Parser is shutting down!')
                    break
                else:
                    print('Please type y or n')