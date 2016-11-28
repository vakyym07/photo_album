import unittest
import clustering
import math
from clustering import Cluster, Pixel


class Test(unittest.TestCase):
    def setUp(self):
        self.cluster = Cluster(15, 15, (30, 10, 20))

    def test_rgb_dist(self):
        pixel1 = Pixel(10, 10, (12, 14, 15))
        pixel2 = Pixel(15, 18, (14, 20, 10))

        pixel3 = Pixel(10, 10, (13, 15, 17))
        pixel4 = Pixel(15, 18, (16, 9, 14))

        rgb_dist = clustering.rgb_dist(pixel1.rgb, pixel2.rgb)
        rgb_dist1 = clustering.rgb_dist(pixel3.rgb, pixel4.rgb)

        assert True, abs(rgb_dist - math.sqrt(65)) < 0.1
        assert True, abs(rgb_dist1 - math.sqrt(54)) < 0.1

    def test_set_centre(self):
        pixel1 = Pixel(10, 10, (12, 14, 15))
        pixel2 = Pixel(15, 18, (14, 20, 10))
        self.cluster.add_pixel(pixel1)
        self.cluster.add_pixel(pixel2)
        self.cluster.set_centre()
        assert True, self.cluster.cur_x == pixel1.x and \
            self.cluster.cur_y == pixel1.y

    def test_initial_centre(self):
        pixel1 = Pixel(1, 1, (2, 3, 4))
        pixel2 = Pixel(2, 2, (5, 6, 7))
        pixel3 = Pixel(3, 3, (8, 9, 10))
        pixel4 = Pixel(4, 4, (10, 11, 12))
        list_pixels = [pixel1, pixel2, pixel3, pixel4]
        clusarr = clustering.initial_centre(2, list_pixels)
        assert True, len(clusarr) == 2

    def test_bind(self):
        pixel1 = Pixel(1, 1, (2, 3, 4))
        pixel2 = Pixel(2, 2, (5, 6, 7))
        pixel3 = Pixel(3, 3, (8, 9, 10))
        pixel4 = Pixel(4, 4, (10, 11, 12))
        list_pixels = [pixel1, pixel2, pixel3, pixel4]
        clusarr = clustering.initial_centre(2, list_pixels)
        clusarr = clustering.bind(list_pixels, clusarr)
        assert True, len(clusarr[0].list_pixels) == 2 and \
            len(clusarr[1].list_pixels) == 2







