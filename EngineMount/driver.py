from math import pow
import numpy as np
from models import ForcePhasor, Engine, Mount
import utils
import pprint


def driver(x_1, y_1, z_1, x_2, y_2, z_2, x_3, y_3, z_3, k_x_1, k_y_1, k_z_1, k_x_2, k_y_2, k_z_2, k_x_3, k_y_3, k_z_3):
    principal_moments = [4,10,8]
    theta = [5,12.3,-20.7]
    engine = Engine(mass=170, principal_moments=principal_moments, theta=theta)

    # mount_1 = Mount(x=-0.25, y=0.25, z=-0.25, k_x=0.6*pow(10,5),k_y=0.6*pow(10,5), k_z=0.6*pow(10,5), n_x=0.1, n_y=0.1, n_z=0.1)
    # k_matrix_1 = mount_1.k_matrix()
    # mount_2 = Mount(x=-0.30, y=-0.10, z=0.05, k_x=0.6*pow(10,5),k_y=0.6*pow(10,5), k_z=0.6*pow(10,5), n_x=0.1, n_y=0.1, n_z=0.1)
    # k_matrix_2 = mount_2.k_matrix()
    # mount_3 = Mount(x=-0.35, y=-0.35, z=-0.35, k_x=0.6*pow(10,5),k_y=0.6*pow(10,5), k_z=0.6*pow(10,5), n_x=0.1, n_y=0.1, n_z=0.1)
    # k_matrix_3 = mount_3.k_matrix()

    mount_1 = Mount(x=x_1, y=y_1, z=z_1, k_x=k_x_1,k_y=k_y_1, k_z=k_z_1, n_x=0.1, n_y=0.1, n_z=0.1)
    k_matrix_1 = mount_1.k_matrix()
    mount_2 = Mount(x=x_2, y=y_2, z=z_2, k_x=k_x_2,k_y=k_y_2, k_z=k_z_2, n_x=0.1, n_y=0.1, n_z=0.1)
    k_matrix_2 = mount_2.k_matrix()
    mount_3 = Mount(x=x_3, y=y_3, z=z_3, k_x=k_x_3,k_y=k_y_3, k_z=k_z_3, n_x=0.1, n_y=0.1, n_z=0.1)
    k_matrix_3 = mount_3.k_matrix()

    objective_function_values = []
    time = 0
    for i in range(0,2000):
        time = time + i*0.1
        phasor_angle_1 = np.zeros([6,1])
        phasor_angle_1[2]=-3
        phasor_angle_1[3]=1.8
        phasor_angle_1[4]=3.0
        force_phasor_1 = ForcePhasor(angular_frequency=194, phasor_angle=phasor_angle_1, f_z=220, m_x=85, m_y=3.0)
        force_matrix_1 = force_phasor_1.force_phasor_matrix(time=time)

        phasor_angle_2 = np.zeros([6,1])
        phasor_angle_2[2]=0.35
        phasor_angle_2[3]=1.6
        phasor_angle_2[4]=3.0
        force_phasor_2 = ForcePhasor(angular_frequency=388, phasor_angle=phasor_angle_1, f_z=33, m_x=44, m_y=2.9)
        force_matrix_2 = force_phasor_2.force_phasor_matrix(time=time)

        phasor_angle_3 = np.zeros([6,1])
        phasor_angle_3[3]=1.5
        force_phasor_3 = ForcePhasor(angular_frequency=582, phasor_angle=phasor_angle_1, m_x=15)
        force_matrix_3 = force_phasor_3.force_phasor_matrix(time=time)

        combined_k_matrix = np.concatenate((k_matrix_1,k_matrix_2,k_matrix_3), axis=1)
        combined_force_matrix = np.concatenate((force_matrix_1,force_matrix_2,force_matrix_3), axis=1)
        angular_frequencies=np.array([force_phasor_1.angular_frequency, force_phasor_2.angular_frequency, force_phasor_3.angular_frequency])

        com_displacement = utils.calculate_center_of_masss_displacement(
                                                                combined_k_matrix=combined_k_matrix, 
                                                                mass_matrix=engine.mass_matrix(),
                                                                angular_frequencies=angular_frequencies,
                                                                combined_force_phasors= combined_force_matrix,
                                                                num_phasors=3
                                                                )

        mount_array = [mount_1, mount_2, mount_3]
        objective_function_values.append(utils.calculate_objective_function(com_displacement=com_displacement, num_mounts=3, mounts=mount_array))

    # print(max(objective_function_values))

    return pow(max(objective_function_values),2)

# o = driver(-0.25,0.25,-0.25,0.30,-0.10,0.05,-0.35,-0.35,-0.35,0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5))
# print(o)
