import clustering
import os
import os.path
import math
import sys
from PIL import Image
from shutil import copyfile, rmtree


def load_images(path):
    images = []
    if os.path.exists(path):
        for e in os.listdir(path=path):
            if os.path.isfile(os.path.join(path, e)):
                try:
                    image = Image.open(os.path.join(path, e))
                    images.append(image)
                except OSError:
                    pass
        return images
    else:
        raise FileNotFoundError('The system can not find '
                                'the path specified: "{}"'.format(path))


def get_images(path):
    images = load_images(path)
    image_vector = {}
    for image in images:
        image_vector[image.filename] = clustering.start(image)
    return image_vector


class Node:
    def __init__(self, cluster):
        self.cluster = cluster
        self.left_child = None
        self.right_child = None
        self.radius = None

    def bind(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child

    def set_radius(self, image_vector):
        radius = 0
        for image in self.cluster.images:
            c_dist = similar_function(image_vector[image],
                                      image_vector[self.cluster.centre])
            if c_dist > radius:
                radius = c_dist
        self.radius = radius


class Tree:
    def __init__(self, root):
        self.root = root

    def get_clusters(self, radius):
        clusarr = []
        self.inorder_tree_walk(self.root, radius, clusarr)
        return clusarr

    def inorder_tree_walk(self, node, radius, clusarr):
        if node.radius <= radius:
            clusarr.append(node.cluster)
            return
        if node is not None:
            self.inorder_tree_walk(node.left_child, radius, clusarr)
            self.inorder_tree_walk(node.right_child, radius, clusarr)


class Cluster:
    def __init__(self, centre=None, images=None):
        self.images = []
        self.centre = centre
        if images is not None:
            self.images = images
        else:
            self.images.append(centre)

    def add_image(self, image):
        self.images.append(image)

    def set_centre(self, image_vector):
        weight = sys.float_info.max
        centre = None
        for image in self.images:
            c_sum = 0
            for c_image in self.images:
                c_sum += similar_function(image_vector[image],
                                          image_vector[c_image])
            if c_sum < weight:
                weight = c_sum
                centre = image
        self.centre = centre

    def __eq__(self, other):
        if self.centre == other.centre and \
                        len(self.images) == len(other.images):
            return True
        return False

    def __hash__(self):
        return hash(self.centre) + hash(len(self.images))


def initial_clusters(images):
    clusarr = set()
    for image in images:
        cluster = Cluster(centre=image)
        clusarr.add(cluster)
    return clusarr


def dist(comp1, comp2):
    if comp1[0] > 0 and comp2[0] > 0:
        return math.sqrt(math.pow(comp1[1] - comp2[1], 2) +
                         math.pow(comp1[2] - comp2[2], 2)) / \
               (32 * math.sqrt(2))
    else:
        return 1


def similar_function(vector1, vector2, alpha=0.1, betta=0.5):
    res = 0
    for i in range(len(vector1)):
        res += (abs(vector1[i][0] - vector2[i][0]) + alpha) * \
                   (dist(vector1[i], vector2[i]) + betta) - alpha * betta
    return res


def dist_clusters(cluster1, cluster2, image_vector):
    return similar_function(image_vector[cluster1.centre],
                            image_vector[cluster2.centre])


def get_dist_matrix(clusarr, image_vector):
    dist_matrix = {}
    for cluster in clusarr:
        for c_cluster in clusarr:
            if cluster != c_cluster:
                if dist_matrix.get(cluster) is None:
                    dist_matrix[cluster] = []
                dist_matrix[cluster].append(
                    (c_cluster, dist_clusters(cluster, c_cluster, image_vector)))
    return dist_matrix


def min_dist_between_clusters(dist_matrix):
    min_dist = sys.float_info.max
    f_cluster = None
    s_cluster = None
    for cluster in dist_matrix:
        for c_cluster in dist_matrix[cluster]:
            if c_cluster[1] < min_dist:
                min_dist = c_cluster[1]
                f_cluster = cluster
                s_cluster = c_cluster[0]
    return f_cluster, s_cluster


def merge_cluster(cluster1, cluster2, image_vector):
    new_cluster = Cluster(images=cluster1.images + cluster2.images)
    new_cluster.set_centre(image_vector)
    return new_cluster


def create_node(cluster, cluster_node):
    if cluster_node.get(cluster) is not None:
        return cluster_node[cluster]
    cluster_node[cluster] = Node(cluster)
    return cluster_node[cluster]


def start(path):
    cluster_node = {}
    image_vector = get_images(path)
    clusarr = initial_clusters(image_vector.keys())

    while len(clusarr) > 1:
        dist_matrix = get_dist_matrix(clusarr, image_vector)
        f_cluster, s_cluster = min_dist_between_clusters(dist_matrix)
        new_cluster = merge_cluster(f_cluster, s_cluster, image_vector)

        c_node1 = create_node(f_cluster, cluster_node)
        c_node1.set_radius(image_vector)
        c_node2 = create_node(s_cluster, cluster_node)
        c_node2.set_radius(image_vector)
        new_node = create_node(new_cluster, cluster_node)
        new_node.set_radius(image_vector)
        new_node.bind(c_node1, c_node2)

        clusarr.remove(f_cluster)
        clusarr.remove(s_cluster)
        clusarr.add(new_cluster)
    return Tree(cluster_node[new_cluster])


def start_clustering(path, r=0.33):
    path = os.path.normpath(path)
    tree = start(path)
    clusarr = tree.get_clusters(r)
    for cluster in clusarr:
        print(cluster.images)

    if os.access(path, os.W_OK):
        c_path = os.path.join(path, "Clusters")
        try:
            os.mkdir(c_path)
        except FileExistsError:
            pass
        for cluster in clusarr:
            head, tail = os.path.split(cluster.centre)
            dst_path = os.path.join(c_path, tail.split('.')[0])
            try:
                os.mkdir(dst_path)
            except FileExistsError:
                rmtree(dst_path)
                os.mkdir(dst_path)

            for image in cluster.images:
                head_image, tail_image = os.path.split(image)
                dst = os.path.join(dst_path, tail_image)
                try:
                    copyfile(image, dst)
                except PermissionError:
                    raise PermissionError("Permission denied")
                except FileNotFoundError:
                    raise FileNotFoundError("No such file or directory: {}".format('dst'))
    else:
        raise PermissionError("Permission denied")

start_clustering("C:\\Users\\Артём\\PycharmProjects\\PhotoAlbum\\Test")
