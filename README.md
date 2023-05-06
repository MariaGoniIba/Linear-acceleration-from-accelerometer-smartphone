# Linear acceleration from raw smartphone accelerometer data

## Data
I use one gait signal sample downloaded from the [mPower dataset](https://www.synapse.org/#!Synapse:syn4993293/wiki/247859). Each walking recording consists of:
* deviceMotion.json file, which contains the core motion readings and consists of:
  * attitude:  the three dimensional (3D) rotation of the device in space. It has the form of a 4D unit "quaternion" vector q=(qx, qy, qz, qw).
  * userAcceleration: {x, y, z} coordinates in Gs.
  * gravity: {x, y, z} coordinates in Gs
* accel_walking.json file, which contains the accelerometer readings for the 3 axes in gravity units.

The accel_walking data represents the raw acceleration data measured by the accelerometer on the device.
I could calculate the linear acceleration of the device subtracting the gravity vector from this raw acceleration data. 
The main advantage of using this accel_walking data is that it provides a direct measurement of the acceleration of the device. 
However, this raw acceleration data may contain more noise and errors compared to the processed userAcceleration data.
Therefore, I will use the userAcceleration data from the deviceMotion structure for my analysis.

## Steps
The steps that I follow to calculate the linear acceleration for each axis are:

* <ins>Step 1</ins>: Filter the signals with a 4th order Butterworth low-pass filter (LPF) with 20Hz cutoff frequency.

I apply the LPF to remove high-frequency noise from the signal before computing the linear acceleration, so high-frequency noise doesn't contaminate the acceleration estimate.

* <ins>Step 2</ins>: Convert the quaternion vector to a rotation matrix.

* <ins>Step 3</ins>: Multiply the rotation matrix by the gravity vector to obtain the acceleration due to gravity in the device's reference frame.

* <ins>Step 4</ins>: Subtract the acceleration due to gravity from the user acceleration to obtain the linear acceleration.

* <ins>Step 5</ins>: Filter the resulting acceleration with a 3rd order Butterworth high-pass filter (HPF) with 0.3Hz cutoff frequency.

I use the HPF to remove low-frequency noise or drift from the signal.
The reason to apply it after computing the linear acceleration, is because the low-frequency noise or drift can affect the acceleration estimate, 
and removing it beforehand could bias the acceleration estimation.

## Script
* <ins>Step 1</ins>: Prepare and filter the signals

I create the quaternion vector and filter it with the LPF.
```
attitude = data['attitude']
x, y, z, w = np.array([]), np.array([]), np.array([]), np.array([])

for i in attitude:
    x = np.append(x, i['x'])
    y = np.append(y, i['y'])
    z = np.append(z, i['z'])
    w = np.append(w, i['w'])

# Quaternion representing the attitude of the smartphone
q = np.array([x, y, z, w])

q_filt = f_filters.LPfilter(q, data['timestamp'])
```
<p align="center">
    <img width="1000" src="https://github.com/MariaGoniIba/Linear-acceleration-from-accelerometer-smartphone/blob/main/Figure_1.png">
</p>

I do the same with the user_acceleration data.
```
UA = data['userAcceleration']
x_accel, y_accel, z_accel = np.array([]), np.array([]), np.array([])
for i in UA:
    x_accel = np.append(x_accel, i['x'])
    y_accel = np.append(y_accel, i['y'])
    z_accel = np.append(z_accel, i['z'])

user_acceleration = np.array([x_accel, y_accel, z_accel])

user_acceleration_filt = f_filters.LPfilter(user_acceleration, data['timestamp'])
```
<p align="center">
    <img width="1000" src="https://github.com/MariaGoniIba/Linear-acceleration-from-accelerometer-smartphone/blob/main/Figure_2.png">
</p>

And the same with the gravity vector.
```
Grav = data['gravity']
x_gravity, y_gravity, z_gravity = np.array([]), np.array([]), np.array([])
for i in Grav:
    x_gravity = np.append(x_gravity, i['x'])
    y_gravity = np.append(y_gravity, i['y'])
    z_gravity = np.append(z_gravity, i['z'])

gravity = np.array([x_gravity, y_gravity, z_gravity])

gravity_filt = f_filters.LPfilter(gravity, data['timestamp']) 
```
<p align="center">
    <img width="1000" src="https://github.com/MariaGoniIba/Linear-acceleration-from-accelerometer-smartphone/blob/main/Figure_3.png">
</p>

* <ins>Step 2</ins>: Convert the quaternion vector to a rotation matrix using the following formula:
```
R = np.array([
    [1 - 2 * yq * yq - 2 * zq * zq, 2 * xq * yq - 2 * wq * zq, 2 * xq * zq + 2 * wq * yq],
    [2 * xq * yq + 2 * wq * zq, 1 - 2 * xq * xq - 2 * zq * zq, 2 * yq * zq - 2 * wq * xq],
    [2 * xq * zq - 2 * wq * yq, 2 * yq * zq + 2 * wq * xq, 1 - 2 * xq * xq - 2 * yq * yq]
])
```

* <ins>Step 3</ins>: Multiply the rotation matrix by the gravity vector to obtain the acceleration due to gravity in the device's reference frame
```
g_device = np.zeros((3, gravity_filt.shape[1]))
for i in range(gravity_filt.shape[1]):
    g_device[:, i] = np.dot(R[:, :, i], gravity_filt[:, i])
```

* <ins>Step 4</ins>: Subtract the acceleration due to gravity from the user acceleration to obtain the linear acceleration
```
linear_acceleration = user_acceleration_filt - g_device
```

* <ins>Step 5</ins>: Filter the resulting acceleration with HPF.
```
linear_acceleration_filt = f_filters.HPfilter(linear_acceleration, data['timestamp'])
```
<p align="center">
    <img width="1000" src="https://github.com/MariaGoniIba/Linear-acceleration-from-accelerometer-smartphone/blob/main/Figure_4.png">
</p>
