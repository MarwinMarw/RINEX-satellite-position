from RSP.parse_rinex import read_rinex
from RSP.satpos import calculate_positions


sat_data = read_rinex('./test/940779338I_1.17N')
sat_pos = calculate_positions(sat_data)
print(sat_pos)