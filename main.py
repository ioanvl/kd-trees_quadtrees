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

    print("\nBuilding from given list of points")
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

# =============================================================================

def build_trees(val_range=100, num_elements=1000):
    q = quad_tree()
    k = kd_tree()
    for _ in range(num_elements):
        x = random.randrange(val_range)
        y = random.randrange(val_range)
        q.add_element(x, y)
        k.add_element(x, y)
    return q, k

def test_random_searches(num_searches=50, val_range=100, num_elements=1000, reps=10):
    q_time = 0
    k_time = 0

    print("\nRandom point search")
    print(f"{num_searches} points in popul. of {num_elements}  -  Avg. of {reps} runs")
    q, k = build_trees(val_range=val_range, num_elements=num_elements)
    for _ in tqdm(range(reps)):
        rand_search_points = [(random.randrange(val_range), random.randrange(val_range)) for _ in range(num_searches)]
        
        ts = time()
        for item in tqdm(rand_search_points, position=1, leave=False):
            x, y = item
            _ = q.search(x, y)
        te = time()
        q_time += te - ts

        ts = time()
        for item in tqdm(rand_search_points, position=1, leave=False):
            x, y = item
            _ = k.search(x, y)
        te = time()
        k_time += te - ts
            

    k_time /= reps
    q_time /= reps
    print(f"kD_Tree: {round(k_time, 4)}s   \t\tQuadTree: {round(q_time, 4)}s")

# =============================================================================

def test_storage(val_range=100, num_elements=1000, reps=10):
    q_time = 0
    k_time = 0

    print("\nStorage testing")
    print(f"Trees of {num_elements} popul  -  Avg. of {reps} runs")
    for _ in tqdm(range(reps)):
        q, k = build_trees(val_range=val_range, num_elements=num_elements)
        
        ts = time()
        _ = q.storage()
        te = time()
        q_time += te - ts

        ts = time()
        _ = k.storage()
        te = time()
        k_time += te - ts

    k_time /= reps
    q_time /= reps
    print(f"kD_Tree: {round(k_time, 4)}s   \t\tQuadTree: {round(q_time, 4)}s")

# =============================================================================

def test_knn_search(num_searches=50, max_k=7, val_range=100, num_elements=1000, reps=10):
    print("\nkNN-Search")
    print(f"{num_searches} points in popul. of {num_elements}  -  Avg. of {reps} runs")
    q, k = build_trees(val_range=val_range, num_elements=num_elements)
    for ck in range(1, max_k):
        q_time = 0
        k_time = 0

        txt = f"[k = {ck}]"
        for _ in tqdm(range(reps), desc=txt):
            rand_search_points = [(random.randrange(val_range), random.randrange(val_range)) for _ in range(num_searches)]
            
            ts = time()
            for item in tqdm(rand_search_points, position=1, leave=False):
                x, y = item
                _ = q.knn_search(x, y, ck)
            te = time()
            q_time += te - ts

            ts = time()
            for item in tqdm(rand_search_points, position=1, leave=False):
                x, y = item
                _ = k.knn_search(x, y, ck)
            te = time()
            k_time += te - ts

        k_time /= reps
        q_time /= reps
        print(f"kD_Tree: {round(k_time, 4)}s   \t\tQuadTree: {round(q_time, 4)}s")

# =============================================================================

def test_delete(num_deletions, val_range=100, num_elements=1000, reps=10):
    q_time = 0
    k_time = 0

    print("\nDeletion testing")
    print(f"{num_searches} points in popul. of {num_elements}  -  Avg. of {reps} runs")
    for _ in tqdm(range(reps)):
        k = kd_tree()
        q = quad_tree()
        rand_elements = [(random.randrange(val_range), random.randrange(val_range)) for _ in range(num_elements)]
        for item in rand_elements:
            x, y = item
            q.add_element(x, y)
            k.add_element(x, y)
        deletion_points = []
        for _ in range(num_deletions):
            key = random.randrange(len(rand_elements))
            deletion_points.append(rand_elements[key])
            del rand_elements[key]                

        t_s = time()
        for item in tqdm(deletion_points, position=1, leave=False):
            x, y = item
            _ = k.delete_element(x, y)
        t_e = time()
        k_time += t_e - t_s
        
        t_s = time()
        for item in tqdm(deletion_points, position=1, leave=False):
            x, y = item
            _ = q.delete_element(x, y)
        t_e = time()
        q_time += t_e - t_s
    
    k_time /= reps
    q_time /= reps
    print(f"kD_Tree: {round(k_time, 4)}s   \t\tQuadTree: {round(q_time, 4)}s")

# =============================================================================

if __name__ == "__main__":
    print("Hi!")
    reps = 10
    val_range = 250
    num_elements = 20000
    num_searches = 1000
    max_k = 7
    reduction = 5 
    
    test_random_insertions(val_range=val_range, num_elements=num_elements, reps=reps)
    
    test_build(val_range=int(val_range / reduction), num_elements=int(num_elements / (reduction ** 2)), reps=reps)
    
    test_storage(val_range=val_range, num_elements=num_elements, reps=reps)
    
    test_delete(num_deletions=num_searches, val_range=val_range, num_elements=num_elements, reps=reps)
    
    test_random_searches(num_searches=num_searches,
                         val_range=val_range, num_elements=num_elements, reps=reps)
    
    test_knn_search(num_searches=num_searches, max_k=max_k,
                    val_range=val_range, num_elements=num_elements, reps=reps)