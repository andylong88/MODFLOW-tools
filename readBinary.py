import flopy.utils.binaryfile as bf
import csv

# ---- USER INPUTS -----
headfile = 'model-output/SES_tr.hds'

# List of points as (layer, row, col) indices.
# Python indices are zero based (MODFLOW indicies are one bases).
# Subtract 1 from MODFLOW layer, row, & col in the list of points below:
points = [
    (6, 199, 199),  
    (7, 199, 199),    
]

# ---- EXTRACT & SAVE TIME SERIES FOR EACH CELL -----
head_obj = bf.HeadFile(headfile)

with open('head_timeseries.csv', mode='w', newline='') as tsfile:
    tswriter = csv.writer(tsfile)
    tswriter.writerow(['Layer', 'Row', 'Column', 'Time', 'Head'])  # Header
    for (lay, row, col) in points:
        try:
            ts = head_obj.get_ts(idx=(lay, row, col))  # timeseries: [[time, head]]
            for time, h in ts:
                tswriter.writerow([lay + 1, row + 1, col + 1, time, h])  # 1-based indexing for output
        except Exception as e:
            print(f"Could not extract data for cell (layer={lay+1}, row={row+1}, col={col+1}): {e}")

print('Head time series saved to head_timeseries.csv')
