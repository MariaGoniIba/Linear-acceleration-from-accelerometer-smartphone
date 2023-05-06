import json
import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import f_filters

with open('gait.tmp', 'r') as f:
    data = json.load(f)

data = pd.DataFrame(data)
data.head()

# Attitude of the smartphone
attitude = data['attitude']
x, y, z, w = np.array([]), np.array([]), np.array([]), np.array([])

for i in attitude:
    x = np.append(x, i['x'])
    y = np.append(y, i['y'])
    z = np.append(z, i['z'])
    w = np.append(w, i['w'])

# Quaternion representing the attitude of the smartphone
q = np.array([x, y, z, w])

q_filt = f_filters.LPfilter(q, data['timestamp'])  # LPF

# Plot attitude
plt.figure()
plt.plot(q_filt[0], label='x'); plt.plot(q_filt[1], label='y'); plt.plot(q_filt[2], label='z'); plt.plot(q_filt[3], label='w')
plt.xlim(0, len(q_filt[0]) - 1)
plt.title('Attitude data (x, y, z, w)')
plt.xlabel('Samples')
plt.legend()

# User acceleration in Gs units
UA = data['userAcceleration']
x_accel, y_accel, z_accel = np.array([]), np.array([]), np.array([])
for i in UA:
    x_accel = np.append(x_accel, i['x'])
    y_accel = np.append(y_accel, i['y'])
    z_accel = np.append(z_accel, i['z'])

user_acceleration = np.array([x_accel, y_accel, z_accel])

user_acceleration_filt = f_filters.LPfilter(user_acceleration, data['timestamp'])  # LPF

# Plot user acceleration
plt.figure()
plt.plot(user_acceleration_filt[0], label='x'); plt.plot(user_acceleration_filt[1], label='y'); plt.plot(user_acceleration_filt[2], label='z')
plt.xlim(0, len(user_acceleration_filt[0]) - 1)
plt.title('User acceleration')
plt.xlabel('Samples')
plt.legend()

# Gravity in Gs units
Grav = data['gravity']
x_gravity, y_gravity, z_gravity = np.array([]), np.array([]), np.array([])
for i in Grav:
    x_gravity = np.append(x_gravity, i['x'])
    y_gravity = np.append(y_gravity, i['y'])
    z_gravity = np.append(z_gravity, i['z'])

gravity = np.array([x_gravity, y_gravity, z_gravity])

gravity_filt = f_filters.LPfilter(gravity, data['timestamp'])  # LPF

# Plot gravity
plt.figure()
plt.plot(gravity_filt[0], label='x'); plt.plot(gravity_filt[1], label='y'); plt.plot(gravity_filt[2], label='z')
plt.xlim(0, len(gravity_filt[0]) - 1)
plt.title('Gravity')
plt.xlabel('Samples')
plt.legend()

# Convert the quaternion vector to a rotation matrix using the following formula
xq = q[0];
yq = q[1];
zq = q[2];
wq = q[3]
R = np.array([
    [1 - 2 * yq * yq - 2 * zq * zq, 2 * xq * yq - 2 * wq * zq, 2 * xq * zq + 2 * wq * yq],
    [2 * xq * yq + 2 * wq * zq, 1 - 2 * xq * xq - 2 * zq * zq, 2 * yq * zq - 2 * wq * xq],
    [2 * xq * zq - 2 * wq * yq, 2 * yq * zq + 2 * wq * xq, 1 - 2 * xq * xq - 2 * yq * yq]
])

# Multiply the rotation matrix by the gravity vector to obtain the acceleration due to gravity in the device's reference frame
g_device = np.zeros((3, gravity_filt.shape[1]))
for i in range(gravity_filt.shape[1]):
    g_device[:, i] = np.dot(R[:, :, i], gravity_filt[:, i])

# Compute linear acceleration
linear_acceleration = user_acceleration_filt - g_device

# HF
linear_acceleration_filt = f_filters.HPfilter(linear_acceleration, data['timestamp'])

# Plot linear acceleration
plt.figure()
plt.plot(linear_acceleration_filt[0], label='x'); plt.plot(linear_acceleration_filt[1], label='y'); plt.plot(linear_acceleration_filt[2], label='z')
plt.xlim(0, len(linear_acceleration_filt[0]) - 1)
plt.title('Linear acceleration')
plt.xlabel('Samples')
plt.legend()

# Plot all figures
plt.show()
