'''
Computes seed loss probability with a Monte Carlo approach. The habitat
shape is defined by a polygon, and the dispersal kernel is definined by
a random sampling function. monte_carlo(h, d) accepts a habitat h and a
dispersal kernel d and returns the seed loss probability. The results
can be rendered visually and overlayed with a satleite image. As an
example habitat, we define a polygon with the shape of McKnight Prairie,
and as an example dispersal kernel, we define a Wald distrubtion
parameterized for common milkweek.
'''

import numpy as np
import cv2 as cv
rng = np.random.default_rng() # random number generator


class Polygon:
    def __init__(self, verts):
        '''
        verts = [[x1, y1], [x2, x2], ... [xn, yn]]

        You can list the verticies clockwise or counter-clockwise.
        Concave polygons are fine, but no self-crossings (no figure-8s).
        '''
        self.verts = np.array(verts, dtype=np.float64)
        self.n = len(self.verts)

    def perimeter(self):
        perim = 0
        for i in range(self.n):
            edge = self.verts[i] - self.verts[i-1]
            perim += np.linalg.norm(edge)
        return perim

    def area(self):
        # "shoelace" formula
        area = 0
        for i in range(self.n):
            area += (self.verts[i, 0]*self.verts[i-1, 1] -
                     self.verts[i, 1]*self.verts[i-1, 0])/2
        return abs(area)

    def contains(self, p):
        '''
        p = [x, y]

        Checks if point p is inside the polygon.
        '''
        # Counts how many times polygon crosses through the ray that
        # points rightward from p.
        # Upward crossing = +1, downward crossing = -1
        crossings = 0
        rel_verts = self.verts - p
        for i in range(self.n):
            ax = rel_verts[i-1, 0]
            ay = rel_verts[i-1, 1]
            bx = rel_verts[i, 0]
            by = rel_verts[i, 1]
            if ay < 0 and by >= 0 and ax*by - bx*ay > 0:
                crossings += 1 # upward crossing
            if ay >= 0 and by < 0 and bx*ay - ax*by > 0:
                crossings -= 1 # downward crossing

        if crossings == 0:
            return False
        elif crossings in [1, -1]:
            return True
        else:
            print("something went wrong... maybe the polygon has \
                   self-crossings?")
            raise ValueError(rel_verts)


#############################  DISPERSAL KERNEL  ##############################

def wald_2D(u, l, bias=0, direction=0):
    '''
    u = mean distance (meters)
    l = shape parameter (meters)
    bias = amount of asymmetry
    direction = direction of bias (radians)

    Returns a random seed dispersal vector [x, y]. The vector's magnitude
    is picked from an inverse Gaussian ("Wald") distribution. The
    direction is uniformly random if bias == 0. If bias > 0, the
    vector is more likely to point in the direction specified.
    '''
    r = rng.wald(u, l)
    if bias == 0:
        t = rng.uniform(0, 2*np.pi) # t for theta
    else:
        k = np.arctan(np.pi*bias)
        t = np.tan(rng.uniform(-k, k))/bias # pdf(t) = bias/(2k(1+(bias*t)^2))
        t += direction
    x = r*np.cos(t)
    y = r*np.sin(t)
    return np.array([x, y])


##############################    COMPUTING P    ##############################

def monte_carlo(h, d, n=1000, return_lost_seeds=False):
    '''
    h = a Polygon representing the habitat
    d = a function to generate random dispersal vectors
    n = number seeds
    return_lost_seeds returns list of [x, y] seed landings insead of p
    
    Computes the probability of seed loss (p) by random sampling.
    '''
    x_max = max(h.verts[:,0])
    x_min = min(h.verts[:,0])
    y_max = max(h.verts[:,1])
    y_min = min(h.verts[:,1])
    i = 0
    lost_count = 0
    lost_seeds = []
    while i < n:
        x = rng.uniform(x_min, x_max)
        y = rng.uniform(y_min, y_max)
        plant = np.array([x, y])
        if h.contains(plant):
            i += 1
            seed = plant + d()
            if not h.contains(seed):
                lost_count += 1
                if return_lost_seeds:
                    lost_seeds.append(seed)

    p = lost_count/n
    return lost_seeds if return_lost_seeds else p
    

##############################  RENDERING STUFF  ##############################

def render_polygon(img, poly, scale, color=[255,255,255], thickness=6):
    '''
    img = numpy array, shape: (height, width, 3), dtype: np.uint8
    poly = Polygon([[x1, y1], [x2, y2], ... [xn, yn]] in meters
    scale = meters/pixel
    color = [B,G,R] (0-255)
    thickness = pixels (int)
    '''
    pts = poly.verts/scale
    pts = pts*[1, -1] + [0, img.shape[0]] # flip y-axis to make it mathy
    bit_shift = 8 # for fractional pixels
    pts = np.array([pts*2**bit_shift], dtype=np.int32)
    return cv.polylines(img, pts, True, color, thickness, cv.LINE_AA,
                        bit_shift)


def render_points(img, pts, scale, color=[255,255,255], radius=4):
    '''
    img = numpy array, shape: (height, width, 3), dtype: np.uint8
    pts = [[x0, y0], [x1, y1], ... ] in meters
    scale = meters/pixel
    color = [B,G,R] (0-255)
    radius = pixels (float)
    thickness = pixels (int)
    '''
    pts = np.array(pts)/scale
    pts = pts*[1, -1] + [0, img.shape[0]] # flip y-axis to make it mathy
    bit_shift = 8 # for fractional pixels
    pts = np.array(pts*2**bit_shift, dtype=np.int32)
    radius = int(radius*2**bit_shift)
    for pt in pts:
        img = cv.circle(img, pt, radius, color, -1, cv.LINE_AA,
                        bit_shift)
    return img


#############################  MCKNIGHT PRAIRIE  ##############################

# Habitat polygon is defined by manually entering the coordinates of
# each vertex (in meters) to line up with a satelite image.
h = Polygon([[75, 142], [77, 160], [77, 305], [869, 291], [872, 122],
             [840, 108], [810, 100], [780, 101], [737, 118],
             [690, 128], [507, 125],
             [308, 132], [110, 131]])

# Mean dispersal distance (u) for Asclepias syriaca L. is computed
# by ballistic equation. Windspeed from Cedar Creek E080.
# Release height and terminal velocity from Sullivan.
windspeed = 4.23    # average max windspeed near seeding date (m/s)
                    # (from wind_reader.py)
hr = 0.866          # seed release height (m)
vt = 0.219          # seed terminal velocity (m/s)
u = hr*windspeed/vt # mean dispersal distance (m)

# Shape parameter (l) is straight from Sullivan, who computed it from
# "canopy height" (1 m) and "scaling coefficient for dense uniform
# canopies" (0.3). 
l = 2.50            # lambda, shape parameter for Wald distribution (m)

if __name__ == "__main__":
    print(f"Habitat area: {h.area():.1f} m^2")
    print(f"Habitat perimeter: {h.perimeter():.1f} m")
    print(f"Mean dispersal distance: {u:.2f} m")
    print(f"Shape parameter (lambda): {l:.2f} m")

    n = 10**7 # takes some time to run
    
    for case in ["SYMMETRIC", "ASYMMETRIC"]:
        if case == "SYMMETRIC":
            def d():
                return wald_2D(u, l)
            bound = u*h.perimeter()/np.pi/h.area()
        else:
            def d():
                return wald_2D(u, l, bias=np.sqrt(10), direction=np.pi/2)
            bound = u*h.perimeter()/2/h.area()
        
        p = monte_carlo(h, d, n)
        error = np.sqrt(p*(1-p)/n) # standard deviation of average of n
                                   # coin flips, each with probability p

        print(f"\n{case} CASE")
        print(f"p = {100*p:.3f}% within about {100*error:.3f}%")
        print(f"Upper bound: {100*bound:.3f}%")

        img = cv.imread("McKnight.png")
        scale = 50/128 # 50 m scale bar on satalite image was 128 pixels long
        img = render_polygon(img, h, scale)
        lost_seeds = monte_carlo(h, d, n=2*10**4, return_lost_seeds=True)
        img = render_points(img, lost_seeds, scale)
        scale_bar = Polygon([[15,15], [115,15], [115,17], [15,17]]) # new 100 m
                                                                    # scale bar
        img = render_polygon(img, scale_bar, scale)
        cv.imwrite(f"{case}.png", img)

