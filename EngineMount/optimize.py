from bayes_opt import BayesianOptimization
from driver import driver
from math import pow

def optimize(x_1, y_1, z_1, x_2, y_2, z_2, x_3, y_3, z_3, k_x_1, k_y_1, k_z_1, k_x_2, k_y_2, k_z_2, k_x_3, k_y_3, k_z_3):
    # Write bounds 
    bounds = {
        'x_1':(x_1-0.05,x_1+0.05),
        'y_1':(y_1-0.05,y_1+0.05), 
        'z_1':(z_1-0.05,z_1+0.05), 
        'x_2':(x_2-0.05,x_2+0.05), 
        'y_2':(y_2-0.05,y_2+0.05), 
        'z_2':(z_2-0.05,z_2+0.05), 
        'x_3':(x_3-0.05,x_3+0.05), 
        'y_3':(y_3-0.05,y_3+0.05), 
        'z_3':(z_3-0.05,z_3+0.05), 
        'k_x_1':(5*pow(10,4), pow(10,8)), 
        'k_y_1':(5*pow(10,4), pow(10,8)), 
        'k_z_1':(5*pow(10,4), pow(10,8)), 
        'k_x_2':(5*pow(10,4), pow(10,8)), 
        'k_y_2':(5*pow(10,4), pow(10,8)), 
        'k_z_2':(5*pow(10,4), pow(10,8)), 
        'k_x_3':(5*pow(10,4), pow(10,8)), 
        'k_y_3':(5*pow(10,4), pow(10,8)), 
        'k_z_3':(5*pow(10,4), pow(10,8))
    }
    # Create optimization object
    optimizer = BayesianOptimization(
    f=driver,
    pbounds=bounds,
    random_state=1,
    )
    optimizer.maximize(
    init_points=2,
    n_iter=10000,
    )
    print(optimizer.max)

# optimize(-0.25,0.25,-0.25,0.30,-0.10,0.05,-0.35,-0.35,-0.35,0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5),0.6*pow(10,5))