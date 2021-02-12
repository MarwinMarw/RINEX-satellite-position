from RSP.parse_rinex import read_rinex
from RSP.satpos import calculate_satpos, calculate_positions


sat_data = read_rinex('./test/gmez0380.21n')
sat_pos = calculate_positions(sat_data)
print(sat_pos)
