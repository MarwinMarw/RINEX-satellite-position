
from io import TextIOWrapper


GM = 3.986005 * pow(10, 14)
OMEGA_e = 7.292115 * pow(10, -5)

def _split_neg_num(number, start_index=0):
    index_minus = number.find('-', start_index)
    fixed = []

    if index_minus > 0 and not number[index_minus-1].isalpha():
        num1 = number[:index_minus]
        num2 = number[index_minus:]
        fixn1 = _split_neg_num(num1)
        fixn2 = _split_neg_num(num2)
        
        if fixn1 is None:
            fixed.append(num1)
        else:
            for i in fixn1:
                fixed.append(i)

        if fixn2 is None:
            fixed.append(num2)
        else:
            for i in fixn2:
                fixed.append(i)

        return fixed

    else:    
        if index_minus != -1:
            return _split_neg_num(number, index_minus+1)
        else:
            return None


def _skip_header(rinex_file: TextIOWrapper) -> None:
    header_end_founded = False

    while True:
        line = rinex_file.readline()
        if 'END' not in line and not header_end_founded:
            continue
        elif 'END' in line:
            header_end_founded = True
            break

def _extract_data(rinex_file: TextIOWrapper) -> dict:    
    ext_data = {}
    line = rinex_file.readline()
    while line:
        nums = [num for num in line.strip().replace('D', 'e').split(' ') if num != '']
        


        line = rinex_file.readline()


def read_rinex(filename):
    with open(filename, 'r') as rinex_file:
        _skip_header(rinex_file)
        ext_data = _extract_data(rinex_file)
        

        





if __name__ == '__main__':
    read_rinex('./test/gmez0380.21n')