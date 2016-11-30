import unittest
import clustering_image


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

    def test_min_dist_between(self):
        f_cluster, s_cluster = clustering_image.min_dist_between_clusters(
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
        cluster2 = clustering_image.Cluster(centre='image1', images=['image1', 'image2'])
        cluster3 = clustering_image.Cluster(images=['image3', 'image4'], centre='image4')
        root = clustering_image.Node(cluster1, radius=0.8)
        left_c = clustering_image.Node(cluster2, radius=0.2)
        right_c = clustering_image.Node(cluster3, radius=0.7)
        root.bind(left_c, right_c)
        tree = clustering_image.Tree(root)
        clusarr = tree.get_clusters(0.3)
        assert True, len(clusarr) == 1 and \
            clusarr[0] == cluster2
