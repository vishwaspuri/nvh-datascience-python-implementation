from math import pow
import numpy as np
from models import ForcePhasor, Engine, Mount
import math

def calculate_center_of_masss_displacement(combined_k_matrix, mass_matrix, angular_frequencies, combined_force_phasors, num_phasors):
    if num_phasors==None:
        raise Exception('num_phasors parameter is not given.')
    if len(angular_frequencies)!=num_phasors:
        raise Exception('Angular momentums incorrect.')
    rows, columns = np.shape(combined_k_matrix)
    if rows!=(6*num_phasors) and columns!=(6*num_phasors):
        raise TypeError('combined_k_matrix has incorrect dimensions.')
    rows, columns = np.shape(combined_force_phasors)
    if rows!=6 and columns!=num_phasors:     
        raise TypeError('combined_force_matrix has incorrect dimensions.')
    displacement = np.zeros([6,1], dtype=int)
    # print(displacement)
    for i in range(0,int(num_phasors)):
        force_phasor    = combined_force_phasors[:,i]
        k_matrix        = combined_k_matrix[:,(i*6):((i+1)*6)]
        inverse_matrix  = np.linalg.inv(k_matrix - pow(angular_frequencies[i],2)*mass_matrix)
        # print('inverse and dot')
        # print(np.dot(inverse_matrix,np.transpose(force_phasor)).reshape([6,1]))
        displacement = displacement+np.dot(inverse_matrix,np.transpose(force_phasor)).reshape([6,1])
    return displacement

def calculate_mount_displacement(com_displacement, mount):
    g_matrix = mount.g_matrix()
    mount_displacement = np.dot(g_matrix,com_displacement)
    # print(np.shape(np.dot(g_matrix,com_displacement)))
    # print('Mount displacement:\n',mount_displacement)
    return mount_displacement

def mount_force(com_displacement, mount):
    mount_displacement = calculate_mount_displacement(com_displacement=com_displacement, mount=mount)
    local_mount_stiffness = mount.local_stiffness_matrix()
    # print("Stiffness Matrix Shape: ", np.shape(local_mount_stiffness))
    # print("Mount Displacement Shape: ", np.shape(mount_displacement))
    return np.dot(local_mount_stiffness,mount_displacement) 

def calculate_objective_function(com_displacement, num_mounts, mounts):
    if len(mounts)!=num_mounts:
        raise TypeError('num_mounts not correct.')
    objective_function_value_square = 0
    for mount in mounts:
        force = mount_force(com_displacement, mount=mount)
        # print("Force Matrix Shape: ",np.shape(force))
        force = force.reshape([3,1])
        for i in range(0,3):
            force_complex = force[i,:]
            force_real_part = np.complex(force_complex).real
            objective_function_value_square = objective_function_value_square + pow(force_real_part, 2)
    # print(objective_function_value_square)
    return pow(objective_function_value_square, 0.5)
