import argparse
import sys
import re

def output(line):
    print(line)

def check(line, params):
    if params.invert:
        if not params.ignore_case:
            return not re.search(params.pattern, line)
        else:
            return not re.search(params.pattern.lower(), line.lower())     
    else:
        if not params.ignore_case:
            return re.search(params.pattern, line)
        else:
            return re.search(params.pattern.lower(), line.lower())     

def grep(lines, params):
    buff = []
    buff_after = []
    nomer = 1
    k = 0
    if params.count:    
        count = 0
        for line in lines:
            if check(line, params):
                count += 1
        output(str(count))
        return 0

    if params.context:
        if params.context >= params.before_context:
            params.before_context = params.context
        if params.context >= params.after_context:
            params.after_context = params.context
 
    if '?' in params.pattern or '*' in params.pattern:
        params.pattern = params.pattern.replace('?','.')
        params.pattern = params.pattern.replace('*','\w*')

    for line in lines:
        line = line.rstrip()

        flag = check(line, params)

        if params.before_context:
            if len(buff) > params.before_context:
                del buff[0]
            if flag:
                nomer = nomer - len(buff) - 1
                for line_buff in buff:
                    nomer += 1
                    if not params.line_number:
                        output(line_buff)
                    else:
                        output("{}-{}".format(nomer, line_buff))
                nomer += 1
                buff.clear()
                    
        if params.before_context:
            if not flag:            
                buff.append(line)

        if params.after_context:
            if flag:
                k = params.after_context
            else:
                if k > 0:
                    if not params.line_number:
                        output(line)
                    else:
                        output("{}-{}".format(nomer, line))
                    k -= 1
                    buff.clear()

        if flag:
            if params.line_number:
                output("{}:{}".format(nomer, line))
            else:
                output(line)       
        nomer += 1
def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
