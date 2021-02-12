import math
import parse_rinex


GM = 3.986005 * 10**14
OMEGA_e = 7.292115 * 10**(-5)

def _calculate_tk(t, toe) -> float:
    tk = t - toe
    if tk > 302400.0:
        tk = tk - 604800.0
    elif tk < -302400.0:
        tk = tk + 604800.0

    return tk

def _calculate_Ek(Mk, e):
    Ek = Mk
    temp = Ek
    while math.fabs(Ek-temp) >= 1e-10:
        temp = Ek
        Ek = Mk + e*math.sin(Ek)

    return Ek

def calculate_satpos(sat_rinex: dict) -> tuple:
    A = sat_rinex['sqrt_A']**2
    n_0 = math.sqrt(GM/ (A**3))
    n = n_0 + sat_rinex['Delta_n']
    e = sat_rinex['e_Eccentricity']
    tk = _calculate_tk(sat_rinex['TTM'],sat_rinex['Toe'])
    Mk = sat_rinex['M0'] + n * tk
    Ek = _calculate_Ek(Mk, e)
    
    vk = math.atan2(math.sqrt(1-e*e) * math.sin(Ek), math.cos(Ek) - e)
    phi_k = vk + sat_rinex['omega']

    d_uk = sat_rinex['Cuc'] * math.cos(2*phi_k) + sat_rinex['Cus'] * math.sin(2*phi_k)
    d_rk = sat_rinex['Crc'] * math.cos(2*phi_k) + sat_rinex['Crs'] * math.sin(2*phi_k)
    d_ik = sat_rinex['Cic'] * math.cos(2*phi_k) + sat_rinex['Cis'] * math.sin(2*phi_k)

    uk = phi_k + d_uk
    rk = A * (1 - e * math.cos(Ek)) + d_rk
    ik = sat_rinex['i0'] + d_ik + sat_rinex['IDOT'] * tk

    xk_prim = rk * math.cos(uk)
    yk_prim = rk * math.sin(uk)

    omega_k = sat_rinex['OMEGA'] + (sat_rinex['OMEGA_DOT'] - OMEGA_e) * tk - OMEGA_e * sat_rinex['Toe'] 

    xk = xk_prim * math.cos(omega_k) - yk_prim * math.cos(ik) * math.sin(omega_k)
    yk = xk_prim * math.sin(omega_k) - yk_prim * math.cos(ik) * math.cos(omega_k)
    zk = yk_prim * math.sin(ik)

    return (xk, yk, zk)


def calculate_positions(sat_data: dict) -> dict:
    sat_pos = {}

    for _, sat_rinex in sat_data.items():
        xk, yk, zk = calculate_satpos(sat_rinex)

        sat_pos[str(sat_rinex['PRN'])] = {
            'x': xk,
            'y': yk,
            'z': zk
        }
    
    return sat_pos


if __name__ == '__main__':
    sat_data = parse_rinex.read_rinex('./test/940779338I_1.17N')
    sat_pos = calculate_positions(sat_data)
    print(sat_pos)