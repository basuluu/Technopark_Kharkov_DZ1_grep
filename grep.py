import argparse
import sys
import re

def output(line):
    print(line)


def grep(lines, params):
    num_vh = []
    if '?' in params.pattern or '*' in params.pattern:
        params.pattern = params.pattern.replace('?','.')
        params.pattern = params.pattern.replace('*','\w*')

    if params.invert:
        for f in range(len(lines)):
            lines[f] = lines[f].rstrip()
            if not params.ignore_case:
                if re.search(params.pattern, lines[f]) == None:
                    lines[f] = lines[f] + '\n'
                    num_vh.append(f)
            else:
                if re.search(params.pattern.lower(), lines[f].lower()) == None:
                    lines[f] = lines[f] + '\n'
                    num_vh.append(f)
                     
    else:
        for f in range(len(lines)):
            lines[f] = lines[f].rstrip()    
            if not params.ignore_case:
                if re.search(params.pattern, lines[f]):
                    lines[f] = lines[f] + '\n'
                    num_vh.append(f)
            else:
                if re.search(params.pattern.lower(), lines[f].lower()) :
                    lines[f] = lines[f] + '\n'
                    num_vh.append(f)

    if params.count:
        k = 0
        for line in lines:
            if re.search('\n', line):
                k += 1
        output(str(k))
        return 0
  

    if params.context:
        for f in num_vh:
            if (f - params.context >= 0) & (len(lines) - params.context > f):
                for g in range(f - params.context, f + params.context + 1):
                    lines[g] = lines[g] + '\t'
  
            elif (f - params.context < 0) & (len(lines) - params.context > f):
                for g in range(0, f + params.context + 1):
                    lines[g] = lines[g] + '\t'

            elif (f - params.context >= 0) & (len(lines) - params.context <= f):
                for g in range(f - params.context, len(lines)):
                    lines[g] = lines[g] + '\t'
            else:
                for g in range(0, len(lines)):
                    lines[g] = lines[g] + '\t'
      
    if params.before_context:
        for f in num_vh:
            if (f - params.before_context >= 0):
                for g in range(f - params.before_context, f + 1):
                    lines[g] = lines[g] + '\t'
            else:
                for g in range(0, f + 1):
                    lines[g] = lines[g] + '\t'
    
    if params.after_context:
        for f in num_vh:
            if (len(lines) - params.after_context > f):
                for g in range(f, f + params.after_context + 1):
                    lines[g] = lines[g] + '\t'
            else:
                for g in range(f, len(lines)):
                    lines[g] = lines[g] + '\t'

    for f in range(len(lines)):
        if params.context or params.before_context or params.after_context:
            if '\t' in lines[f]:
                lines[f] = lines[f].strip()
                if params.line_number:
                    if f in num_vh:
                        output(str(f + 1) + ':' + lines[f])
                    else:
                        output(str(f + 1) + '-' + lines[f])
                else: 
                    output(lines[f])
        else:
            if '\n' in lines[f]:
                lines[f] = lines[f].strip()
                if params.line_number:
                    output(str(f + 1) + ':' + lines[f])
                else:
                    output(lines[f])
            
            
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
