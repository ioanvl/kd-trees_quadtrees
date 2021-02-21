import random
from time import time
import warnings
warnings.filterwarnings('ignore')

from tqdm import tqdm

from tree_modules import kd_tree, quad_tree
    
def test_random_insertions(val_range=100, num_elements=1000, reps=10):
    q_time = 0
    k_time = 0

    print("\nRandom element insertion")
    print(f"{num_elements} points, x,y:[0,{val_range}]  -  Avg. of {reps} runs")
    for _ in tqdm(range(reps)):
        k = kd_tree()
        q = quad_tree()
        rand_elements = [(random.randrange(val_range), random.randrange(val_range)) for _ in range(num_elements)]

        t_s = time()
        for item in tqdm(rand_elements, position=1, leave=False):
            x, y = item
            q.add_element(x, y)
        t_e = time()
        q_time += t_e - t_s
        
        t_s = time()
        for item in tqdm(rand_elements, position=1, leave=False):
            x, y = item
            k.add_element(x, y)
        t_e = time()
        k_time += t_e - t_s
    
    k_time /= reps
    q_time /= reps
    print(f"kD_Tree: {round(k_time, 4)}s   \t\tQuadTree: {round(q_time, 4)}s")

# =============================================================================

def test_build(val_range=100, num_elements=1000, reps=10):
    q_time = 0
    k_time = 0

    print("Building from given list of points")
    print(f"{num_elements} points, x,y:[0,{val_range}]  -  Avg. of {reps} runs")
    for _ in tqdm(range(reps)):
        k = kd_tree()
        q = quad_tree()
        rand_elements = [(random.randrange(val_range), random.randrange(val_range)) for _ in range(num_elements)]

        t_s = time()
        q.build(point_list=rand_elements)
        t_e = time()
        q_time += t_e - t_s
        
        t_s = time()
        k.build(point_list=rand_elements)
        t_e = time()
        k_time += t_e - t_s
    
    k_time /= reps
    q_time /= reps
    print(f"kD_Tree: {round(k_time, 4)}s   \t\tQuadTree: {round(q_time, 4)}s")
    
    
    
    
if __name__ == "__main__":
    #k = kd_tree()
    #rand_elements = [(random.randrange(2000), random.randrange(2000)) for _ in range(20000)]
    print('go')
    #k.build(rand_elements)
    test_build()
    print('done')
