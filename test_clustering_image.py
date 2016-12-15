import unittest
import clustering_image
import os.path


class Test(unittest.TestCase):
    def setUp(self):
        self.size = 16
        self.image_vector = {
            'image1': ((0.4, 4/self.size, 6/self.size),
                       (0.53, 11/self.size, 12/self.size)),
            'image2': ((0.2, 7/self.size, 8/self.size),
                       (0.67, 2/self.size, 5/self.size)),
            'image3': ((0.6, 1/self.size, 9/self.size),
                       (0.3, 4/self.size, 8/self.size)),
            'image4': ((0.3, 10/self.size, 13/self.size),
                       (0.8, 5/self.size, 6/self.size))}

        self.clusarr = clustering_image.initial_clusters(
            self.image_vector.keys())
        self.dist_matrix = clustering_image.get_dist_matrix(
            self.clusarr, self.image_vector)

        self.images = clustering_image.load_images('Test_images')
        self.real_image_vector = clustering_image.get_images('Test_images')

    def test_min_dist_between(self):
        f_cluster, s_cluster, min_dist = clustering_image.min_dist_between_clusters(
            self.dist_matrix)
        assert True, f_cluster.centre == 'image1' and \
            s_cluster.centre == 'image2'

    def test_merge_clusters(self):
        cluster1 = clustering_image.Cluster(images=['image1', 'image2'])
        cluster2 = clustering_image.Cluster(images=['image3', 'image4'])
        new_cluster = clustering_image.merge_cluster(
            cluster1, cluster2, self.image_vector)
        self.assertCountEqual(new_cluster.images, self.image_vector.keys())

    def test_inorder_tree_walk(self):
        cluster1 = clustering_image.Cluster(
            images=['image1', 'image2', 'image3', 'image4'])
        cluster2 = clustering_image.Cluster(
            centre='image1', images=['image1', 'image2'])
        cluster3 = clustering_image.Cluster(
            images=['image3', 'image4'], centre='image4')
        root = clustering_image.Node(cluster1, radius=0.8)
        left_c = clustering_image.Node(cluster2, radius=0.2)
        right_c = clustering_image.Node(cluster3, radius=0.7)
        root.bind(left_c, right_c)
        tree = clustering_image.Tree(root)
        clusarr = tree.get_clusters(0.3)
        assert True, len(clusarr) == 1 and \
            clusarr[0] == cluster2

    def test_similar_func_identical_image(self):
        ans = 0.0
        for path in self.real_image_vector:
           ans += clustering_image.similar_function(
               self.real_image_vector[path], self.real_image_vector[path])
        self.assertEqual(0.0, ans)

    def test_similar_func_not_identical_image(self):
        ans = 0.0
        obj = os.path.join('Test_images', 'choco.jpg')
        for path in self.real_image_vector:
            ans += clustering_image.similar_function(
                self.real_image_vector[obj], self.real_image_vector[path])
        self.assertNotEqual(0.0, ans)

    def test_similar_func_color_image_1(self):
        choko = os.path.join('Test_images', 'choco.jpg')
        choko1 = os.path.join('Test_images', 'choco1.jpg')
        fairy = os.path.join('Test_images', 'fairy.jpg')
        dist1 = clustering_image.similar_function(
            self.real_image_vector[choko], self.real_image_vector[choko1])
        dist2 = clustering_image.similar_function(
            self.real_image_vector[choko], self.real_image_vector[fairy])
        self.assertEqual(True, dist1 < dist2)

    def test_similar_func_color_image_2(self):
        choko = os.path.join('Test_images', 'fairy.jpg')
        choko1 = os.path.join('Test_images', 'fairy1.jpg')
        fairy = os.path.join('Test_images', 'magnet.jpg')
        dist1 = clustering_image.similar_function(
            self.real_image_vector[choko], self.real_image_vector[choko1])
        dist2 = clustering_image.similar_function(
            self.real_image_vector[choko], self.real_image_vector[fairy])
        self.assertEqual(True, dist1 < dist2)

    def test_similar_func_color_color_image_3(self):
        choko = os.path.join('Test_images', 'milk.jpg')
        choko1 = os.path.join('Test_images', 'milk1.jpg')
        fairy = os.path.join('Test_images', 'textbook.jpg')
        dist1 = clustering_image.similar_function(
            self.real_image_vector[choko], self.real_image_vector[choko1])
        dist2 = clustering_image.similar_function(
            self.real_image_vector[choko], self.real_image_vector[fairy])
        self.assertEqual(True, dist1 < dist2)

    def test_similar_func_color_image_4(self):
        choko = os.path.join('Test_images', 'choco.jpg')
        choko1 = os.path.join('Test_images', 'choco2.jpg')
        fairy = os.path.join('Test_images', 'bag.jpg')
        dist1 = clustering_image.similar_function(
            self.real_image_vector[choko], self.real_image_vector[choko1])
        dist2 = clustering_image.similar_function(
            self.real_image_vector[choko], self.real_image_vector[fairy])
        self.assertEqual(True, dist1 < dist2)

    def test_similar_func_black_white_image_1(self):
        peshka = os.path.join('Test_images', 'peshka.jpg')
        peshka1 = os.path.join('Test_images', 'peshka1.jpg')
        hourse = os.path.join('Test_images', 'horse.jpg')
        dist1 = clustering_image.similar_function(
            self.real_image_vector[peshka], self.real_image_vector[peshka1])
        dist2 = clustering_image.similar_function(
            self.real_image_vector[peshka], self.real_image_vector[hourse])
        self.assertEqual(True, dist1 < dist2)

    def test_similar_func_black_white_image_2(self):
        peshka = os.path.join('Test_images', 'peshka.jpg')
        peshka1 = os.path.join('Test_images', 'peshka1.jpg')
        fairy = os.path.join('Test_images', 'fairy.jpg')
        dist1 = clustering_image.similar_function(
            self.real_image_vector[peshka], self.real_image_vector[peshka1])
        dist2 = clustering_image.similar_function(
            self.real_image_vector[peshka], self.real_image_vector[fairy])
        self.assertEqual(True, dist1 < dist2)


if __name__ == '__main__':
    unittest.main()
