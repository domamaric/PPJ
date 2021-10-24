class DataTypes:
    KEYWORDS = {
        'KR_ZA': 'za',
        'KR_OD': 'od',
        'KR_DO': 'do',
        'KR_AZ': 'az'
    }
    OPERATORS = {
        'OP_PRIDRUZI': '=',
        'OP_PLUS': '+',
        'OP_MINUS': '-',
        'OP_PUTA': '*',
        'OP_DIJELI': '/'
    }


class Analyzer:
    @staticmethod
    def remove_comments(lines: list):
        ret_list = []
        for line in lines:
            if line.startswith('//'):
                # Remove comments from the begging of line
                ret_list.append('')
            elif '//' in line:
                # Remove comment in the middle of line
                index = line.index('//')
                line = line[:index]
                ret_list.append(line)
            else:
                # No comments in line, append line
                ret_list.append(line)

        return list(enumerate(ret_list, 1))

    @staticmethod
    def analyze(lines: list):
        # tpl -> tuple(int, str)
        for tpl in lines:
            if not tpl[1]: # Line is empty, do nothing
                continue
            print(tpl)


def main():
    # data = [x.strip() for x in stdin.readlines()]
    filename = 'primjer.in'
    with open(filename) as f:
        data = [line.strip() for line in f]
    data = Analyzer.remove_comments(data)  # data[0] vraca tuple
    Analyzer.analyze(data)


if __name__ == '__main__':
    main()
