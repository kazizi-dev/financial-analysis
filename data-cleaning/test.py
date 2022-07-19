import math

p = ['p1','p2','p3']
pc_map = {
    'p1': (0,1),
    'p2': (2,3),
    'p3': (3,4)
}
pr_map = {
    'p1': 5,
    'p2': 20,
    'p3': 9
}

h = ['h1','h2','h3']
hc_map = {
    'h3': (11,12),
    'h2': (9,10),
    'h1': (7,8)
}
hl_map = {
    'h1': 2,
    'h2': 4,
    'h3': 1
}

def calculate_distance(pc, hc):
    a = abs(pc[0]-hc[0])
    b = abs(pc[1]-hc[1])
    return math.sqrt(a*a + b*b)


