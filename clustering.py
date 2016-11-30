import math
import sys


class Pixel:
    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.rgb = rgb

    def __str__(self):
        return 'x:{}, y:{}, rgb:{}'.\
            format(self.x, self.y, self.rgb)


class Cluster:
    def __init__(self, cur_x, cur_y, rgb):
        self.list_pixels = []
        self.cur_x = cur_x
        self.cur_y = cur_y
        self.rgb = rgb
        self.last_x = None
        self.last_y = None

    def size(self):
        return len(self.list_pixels)

    def add_pixel(self, pixel):
        self.list_pixels.append(pixel)

    def set_centre(self):
        if len(self.list_pixels) != 0:
            weight = sys.float_info.max
            for pixel in self.list_pixels:
                sum = 0
                for c_pixel in self.list_pixels:
                    sum += rgb_dist(pixel.rgb, c_pixel.rgb)
                if sum < weight:
                    weight = sum
                    centre = pixel
            self.last_x = self.cur_x
            self.last_y = self.cur_y
            self.cur_x = centre.x
            self.cur_y = centre.y
            self.rgb = centre.rgb
        else:
            self.last_x = self.cur_x
            self.last_y = self.cur_y

    def clear(self):
        self.list_pixels.clear()

    def __str__(self):
        return 'x:{}, y:{}, rgb:{}'.\
            format(self.cur_x, self.cur_y, self.rgb)


def initial_centre(k, list_pixels):
    clusarr = []
    step = len(list_pixels) // k

    for pixel in list_pixels[::step]:
        cluster = Cluster(pixel.x, pixel.y, pixel.rgb)
        cluster.add_pixel(pixel)
        clusarr.append(cluster)
        if len(clusarr) == k:
            break
    return clusarr


def bind(list_pixels, clusarr):
    for cluster in clusarr:
        cluster.clear()
    for pixel in list_pixels:
        min_dist = rgb_dist(pixel.rgb, clusarr[0].rgb)
        cl = clusarr[0]
        for cluster in clusarr:
            if rgb_dist(pixel.rgb, cluster.rgb) < min_dist:
                min_dist = rgb_dist(pixel.rgb, cluster.rgb)
                cl = cluster
        cl.add_pixel(pixel)
    return clusarr


def start(image, k=32):
    im = image.resize((16, 16))
    pixels = [Pixel(x, y, im.getpixel((x, y)))
              for y in range(im.size[1]) for x in range(im.size[1])]
    clusarr = initial_centre(k, pixels)
    while True:
        chk = 0
        clusarr = bind(pixels, clusarr)
        for cluster in clusarr:
            cluster.set_centre()
            if cluster.cur_x == cluster.last_x and \
                    cluster.cur_y == cluster.last_y:
                chk += 1
        if chk == k:
            break
    weight, height = im.size
    return tuple([(len(cluster.list_pixels) / len(pixels),
                  cluster.cur_x / weight, cluster.cur_y / height)
                  for cluster in clusarr])


def rgb_dist(pixel1, pixel2):
    res = 0
    for e in zip(pixel1, pixel2):
        res += math.pow(e[0] - e[1], 2)
    return math.sqrt(res)
