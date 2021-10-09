from io import TextIOWrapper


class EndOfFile(Exception):
    pass

class ErrorOBSRecord(Exception):
    pass


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


def _fix_negative_num(nums: list) -> list:
    fixed_nums = []
    for num in nums:
        fixed_num = _split_neg_num(num)
        if fixed_num is not None:
            for fn in fixed_num:
                fixed_nums.append(fn)
        else:
            fixed_nums.append(num)

    return fixed_nums


def skip_header(rinex_file: TextIOWrapper) -> int:
    noLine = 0
    while True:
        noLine += 1
        if 'END' in rinex_file.readline():
            break

    return noLine


def read_PRN_EPOCH_SV_CLK(nums: list) -> dict:
    if len(nums) != 10:
        raise ErrorOBSRecord(f'PRN_EPOCH_SV_CLK read error str: {str(nums)}')
    
    return {
        'PRN': nums[0],
        'EPOCH': {
            'YEAR': nums[1],
            'MONTH': nums[2],
            'DAY': nums[3],
            'HOUR': nums[4],
            'MINUTE': nums[5],
            'SECOND': nums[6],
        },
        'SV_clock_bias':float(nums[7]),
        'SV_clock_drift':float(nums[8]),
        'SV_clock_drift_rate':float(nums[9])
    }
    

def read_BROADCAST_ORBIT_1(nums: list) -> dict:
    if len(nums) != 4:
        raise ErrorOBSRecord(f'BROADCAST_ORBIT_1 read error str: {str(nums)}')

    return {
        'IODE': float(nums[0]),
        'Crs': float(nums[1]),
        'Delta_n': float(nums[2]),
        'M0': float(nums[3])
    }

def read_BROADCAST_ORBIT_2(nums: list) -> dict:
    if len(nums) != 4:
        raise ErrorOBSRecord(f'BROADCAST_ORBIT_2 read error str: {str(nums)}')

    return {
        'Cuc': float(nums[0]),
        'e_Eccentricity': float(nums[1]),
        'Cus': float(nums[2]),
        'sqrt_A': float(nums[3])
    }

def read_BROADCAST_ORBIT_3(nums: list) -> dict:
    if len(nums) != 4:
        raise ErrorOBSRecord(f'BROADCAST_ORBIT_3 read error str: {str(nums)}')

    return {
        'Toe': float(nums[0]),
        'Cic': float(nums[1]),
        'OMEGA': float(nums[2]),
        'Cis': float(nums[3])
    }

def read_BROADCAST_ORBIT_4(nums: list) -> dict:
    if len(nums) != 4:
        raise ErrorOBSRecord(f'BROADCAST_ORBIT_4 read error str: {str(nums)}')

    return {
        'i0': float(nums[0]),
        'Crc': float(nums[1]),
        'omega': float(nums[2]),
        'OMEGA_DOT': float(nums[3])
    }

def read_BROADCAST_ORBIT_5(nums: list) -> dict:
    if len(nums) != 4:
        raise ErrorOBSRecord(f'BROADCAST_ORBIT_5 read error str: {str(nums)}')

    return {
        'IDOT': float(nums[0]),
        'Codes_L2_channel': float(nums[1]),
        'GPS_week': float(nums[2]),
        'L2_P': float(nums[3])
    }

def read_BROADCAST_ORBIT_6(nums: list) -> dict:
    if len(nums) != 4:
        raise ErrorOBSRecord(f'BROADCAST_ORBIT_6 read error str: {str(nums)}')

    return {
        'SV_accuracy': float(nums[0]),
        'SV_health': float(nums[1]),
        'TGD': float(nums[2]),
        'IODC': float(nums[3])
    }

def read_BROADCAST_ORBIT_7(nums: list) -> dict:
    if len(nums) != 2:
        raise ErrorOBSRecord(f'BROADCAST_ORBIT_7 read error str: {str(nums)}')

    return {
        'TTM': float(nums[0]),
        'Fit_interval': float(nums[1])
    }


def _next_line(rinex_file: TextIOWrapper) -> list:
    line = rinex_file.readline()
    if not line or line.isspace():
        raise EndOfFile

    nums = [num for num in line.strip().replace('D', 'e').split(' ') if num != '']
    fixed_nums = _fix_negative_num(nums)

    return fixed_nums


def _extract_data(rinex_file: TextIOWrapper) -> dict:    
    ext_data = {}
    nr_sat = 0
    nr_line = 0
    while True:
        try:
            str_data = []

            for _ in range(8):
                nr_line += 1
                data_from_string = _next_line(rinex_file)
                str_data.append(data_from_string)
                
            ex_data_l1 = read_PRN_EPOCH_SV_CLK(str_data[0])
            key = f"{nr_sat}_{str(ex_data_l1['PRN'])}"
            nr_sat += 1

            ext_data[key] = ex_data_l1
            ext_data[key].update(read_BROADCAST_ORBIT_1(str_data[1]))
            ext_data[key].update(read_BROADCAST_ORBIT_2(str_data[2]))
            ext_data[key].update(read_BROADCAST_ORBIT_3(str_data[3]))
            ext_data[key].update(read_BROADCAST_ORBIT_4(str_data[4]))
            ext_data[key].update(read_BROADCAST_ORBIT_5(str_data[5]))
            ext_data[key].update(read_BROADCAST_ORBIT_6(str_data[6]))
            ext_data[key].update(read_BROADCAST_ORBIT_7(str_data[7]))

        except EndOfFile:
            break
        
        except ErrorOBSRecord as eobsr:
            print(f'Error: OBS Record {nr_sat}, Data: {str_data}, NoLine: {nr_line}', eobsr)
            break
        
    return ext_data


def read_rinex(filename: str) -> dict:
    ext_data = None
    with open(filename, 'r') as rinex_file:
        skipped_lines = skip_header(rinex_file)
        ext_data = _extract_data(rinex_file)
    return ext_data

