import argparse
import sys
import re

def output(line):
    print(line)


def grep(lines, params):
    if '?' in params.pattern or '*' in params.pattern:
        params.pattern = params.pattern.replace('?','.')
        params.pattern = params.pattern.replace('*','\w*')

    if params.invert:
        for line in lines:
            line = line.rstrip()
            if re.search(params.pattern, line) == None:
                output(line)
    
    elif params.ignore_case:
        for line in lines:
            line = line.rstrip()
            if re.search(params.pattern.lower(), line.lower()):
                output(line)

    elif params.count:
        k = 0
        for line in lines:
            line = line.rstrip()
            if re.search(params.pattern, line):
                k += 1
        output(str(k))
            
    elif params.context:
        
        num_vh = []
        for f in range(len(lines)):
            lines[f] = lines[f].strip()
            if re.search(params.pattern, lines[f]):
                num_vh.append(f)
                lines[f] = lines[f] + '\n'
       
        for f in num_vh:
            if (f - params.context >= 0) & (len(lines) - params.context > f):
                for g in range(f - params.context, f + params.context + 1):
                    lines[g] = lines[g] + '\n'

            elif (f - params.context < 0) & (len(lines) - params.context > f):
                for g in range(0, f + params.context + 1):
                    lines[g] = lines[g] + '\n'

            elif (f - params.context >= 0) & (len(lines) - params.context <= f):
                for g in range(f - params.context, len(lines)):
                    lines[g] = lines[g] + '\n'
            else:
                for g in range(0, len(lines)):
                    lines[g] = lines[g] + '\n'
        
        if params.line_number:
            for f in range(len(lines)):
                if re.search(params.pattern, lines[f]):
                    lines[f] = str(f+1) + ':' + lines[f]
                else:
                    lines[f] = str(f+1) + '-' + lines[f] 

        for line in lines:
            if '\n' in line:
                output(line.strip())           
            
        for f in range(len(lines)):
            lines[f] = lines[f].strip()

    elif params.line_number:
        k = 1
        for line in lines:
            line = line.rstrip()
            line = str(k) + ':' + line
            if re.search(params.pattern, line):
                output(line)
            k += 1

    elif params.before_context:
        num_vh = []
        for f in range(len(lines)):
            lines[f] = lines[f].strip()
            if re.search(params.pattern, lines[f]):
                num_vh.append(f)
                lines[f] = lines[f] + '\n'
        for f in num_vh:
            if (f - params.before_context >= 0):
                for g in range(f - params.before_context, f):
                    lines[g] = lines[g] + '\n'
            else:
                for g in range(0, f):
                    lines[g] = lines[g] + '\n'
        for line in lines:
            if '\n' in line:
                 output(line.strip())
      
    elif params.after_context:
        num_vh = []
        for f in range(len(lines)):
            lines[f] = lines[f].strip()
            if re.search(params.pattern, lines[f]):
                num_vh.append(f)
                lines[f] = lines[f] + '\n'
        for f in num_vh:
            if (len(lines) - params.after_context > f):
                for g in range(f, f + params.after_context + 1):
                    lines[g] = lines[g] + '\n'
            else:
                for g in range(f, len(lines)):
                    lines[g] = lines[g] + '\n'
        for line in lines:
            if '\n' in line:
                 output(line.strip())

    else:
       for line in lines:
           line = line.rstrip()
           if re.search(params.pattern, line):
               output(line)

            
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
