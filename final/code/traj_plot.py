import numpy as np
import matplotlib.pyplot as plt

from evaluate_ate_scale import align

col_output = np.matrix([])
col_data = []
with open('col.nvm','r') as f:
    col_data = f.readlines()
col_points = int(col_data[2])
col_x = np.zeros(col_points)
col_y = np.zeros(col_points)
col_z = np.zeros(col_points)
for line in col_data[3:3+col_points]:
    line = line.split(' ')
    try:
        idx = int(line[0].split('.')[0])
        col_x[idx], col_y[idx], col_z[idx] = map(float,line[6:9])
    except:
        continue

orb_id = []
orb_x = np.zeros(col_points)
orb_y = np.zeros(col_points)
orb_z = np.zeros(col_points)
# with open('KeyFrameTrajectory.txt','r') as f:
with open('keyframe.txt','r') as f:
    for line in f:
        line = line.split(' ')
        idx = int(line[0].split('.')[0])
        orb_id.append(idx)
        orb_x[idx], orb_y[idx], orb_z[idx] = map(float,line[1:4])

first_xyz = np.matrix((col_x[orb_id],col_y[orb_id],col_z[orb_id]))
second_xyz = np.matrix((orb_x[orb_id],orb_y[orb_id],orb_z[orb_id]))
rot, transGT, trans_errorGT, trans, trans_error, scale = align(second_xyz,first_xyz)
second_xyz = rot * second_xyz + trans
second_xyz *= scale
trans_xyz = np.asarray(second_xyz)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(col_x,col_y,col_z)
ax.plot(trans_xyz[0],trans_xyz[1],trans_xyz[2])
# ax.plot(orb_x[orb_id],orb_y[orb_id],orb_z[orb_id])
start = orb_id[0]
ax.scatter(col_x[start],col_y[start],col_z[start])
ax.scatter(trans_xyz[0][0],trans_xyz[1][0],trans_xyz[2][0])
ax.set_aspect('auto')
plt.show()

err_val = np.asarray(np.sqrt(np.multiply(second_xyz-first_xyz,second_xyz-first_xyz).sum(0)))[0]
line_len = np.sqrt((col_x[110]-col_x[0])**2+(col_y[110]-col_y[0])**2+(col_z[110]-col_z[0])**2)
print(f'line length: {line_len}')
meter_mul = 20/line_len
print(f'average error: {err_val.mean()} -> {err_val.mean()*meter_mul:.6f} m')
print('start-end error')
col_err = np.sqrt((col_x[-1]-col_x[0])**2+(col_y[-1]-col_y[0])**2+(col_z[-1]-col_z[0])**2)
orb_err = np.sqrt((orb_x[orb_id[-1]]-orb_x[orb_id[0]])**2+(orb_y[orb_id[-1]]-orb_y[orb_id[0]])**2+(orb_z[orb_id[-1]]-orb_z[orb_id[0]])**2)
print(f'- COLMAP  : {col_err} -> {col_err*meter_mul:.6f} m')
print(f'- ORB-SLAM: {orb_err} -> {orb_err*meter_mul:.6f} m')
plt.plot(np.arange(len(err_val)),err_val*meter_mul)
plt.grid(axis='y',ls='--')
plt.show()
