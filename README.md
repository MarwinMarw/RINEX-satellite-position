# RINEX-SATELLITE-POSITION
The modules are created to parsing the [***RINEX format V2***](https://www.ngs.noaa.gov/CORS/RINEX211.txt) files  and calculating positions of satellites which data are described in the RINEX files.

Positions presented in [ECEF](https://en.wikipedia.org/wiki/ECEF) coordinate system.

## How to use (example)
```python 
from RSP.parse_rinex import read_rinex
from RSP.satpos import calculate_satpos


sat_data = read_rinex(filename)
for key, rinex_info in sat_data.items():
    pos = calculate_satpos(rinex_info)
```

As result of the ***read_rinex*** function you can see a dictionary with processed data of the file specified as argument of the function.

Below you can see one of the records:
```python
{'14': {'PRN': '14', 'EPOCH': {'YEAR': '17', 'MONTH': '12', 'DAY': '4', 'HOUR': '12', 'MINUTE': '0', 'SECOND': '0.0'}, 'SV_clock_bias': -8.9911278337e-05, 'SV_clock_drift': -7.9580786405e-13, 'SV_clock_drift_rate': 0.0, 'IODE': 90.0, 'Crs': -18.0, 'Delta_n': 4.5944770927e-09, 'M0': -1.5157133401, 'Cuc': -9.5367431641e-07, 'e_Eccentricity': 0.0092511395924, 'Cus': 9.760260582e-06, 'sqrt_A': 5153.7131844, 'Toe': 129600.0, 'Cic': 2.2724270821e-07, 'OMEGA': 2.5507638894, 'Cis': 1.1548399925e-07, 'i0': 0.96156005357, 'Crc': 193.0625, 'omega': -1.9530666137, 'OMEGA_DOT': -7.8846141401e-09, 'IDOT': -8.7146487144e-10, 'Codes_L2_channel': 0.0, 'GPS_week': 1978.0, 'L2_P': 0.0, 'SV_accuracy': 2.4, 'SV_health': 0.0, 'TGD': -9.7788870335e-09, 'IODC': 90.0, 'TTM': 122418.0, 'Fit_interval': 0.0}}

```

After this, need to process the received data to get satellites positions described in the ***RINEX file***. For this task we can use ***calculate_satpos*** function.

The function return tuple with a position of the satellite (x, y, z)

Return example:
```python
 (-3666055.9598023687, -14502006.7903851, 21551445.60757155)
 ```

 Or we can use the ***calculate_positions*** function to process all records which we can get from the ***read_rinex*** function.

```python
from RSP.parse_rinex import read_rinex
from RSP.satpos import calculate_positions


sat_data = read_rinex(filename)
sat_pos = calculate_positions(sat_data)
 ```
 Examplethe output of the code is:

 ```python

 {'14': {'x': -3666055.9598023687, 'y': -14502006.7903851, 'z': 21551445.60757155}, '17': {'x': 17072083.067698468, 'y': 4702360.387043671, 'z': 14688820.05491982}}
 ```

 Where key of the dictionary is a PRN of a satellite.