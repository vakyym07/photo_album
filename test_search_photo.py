import unittest
import search_photo as sp
import clustering_image as ci
import os.path


class Test(unittest.TestCase):
    def setUp(self):
        self.list_path = ci.load_images('Test_images')

    def test_1(self):
        dic_req = {"Topic": "room"}
        right_resp = [os.path.join('Test_images', 'fairy.jpg'),
                      os.path.join('Test_images', 'bag.jpg'),
                      os.path.join('Test_images', 'fairy1.jpg'),
                      os.path.join('Test_images', 'fairy2.jpg'),
                      os.path.join('Test_images', 'fairy3.jpg'),
                      os.path.join('Test_images', 'magnet.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(
            True, len(resp) == 6 and flag)

    def test_2(self):
        dic_req = {"Comment": "This is fairy"}
        right_resp = [os.path.join('Test_images', 'fairy.jpg'),
                      os.path.join('Test_images', 'fairy1.jpg'),
                      os.path.join('Test_images', 'fairy2.jpg'),
                      os.path.join('Test_images', 'fairy3.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(
            True, len(resp) == 4 and flag)

    def test_3(self):
        dic_req = {"Comment": "This is chess"}
        right_resp = [os.path.join('Test_images', 'horse.jpg'),
                      os.path.join('Test_images', 'horse1.jpg'),
                      os.path.join('Test_images', 'horse2.jpg'),
                      os.path.join('Test_images', 'peshka3.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(
            True, len(resp) == 4 and flag)

    def test_3(self):
        dic_req = {"Comment": "This is chess"}
        right_resp = [os.path.join('Test_images', 'horse.jpg'),
                      os.path.join('Test_images', 'horse1.jpg'),
                      os.path.join('Test_images', 'horse2.jpg'),
                      os.path.join('Test_images', 'peshka3.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(
            True, len(resp) == 4 and flag)

    def test_4(self):
        dic_req = {"Comment": "This is magnet"}
        right_resp = [os.path.join('Test_images', 'magnet.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(
            True, len(resp) == 1 and flag)

    def test_5(self):
        dic_req = {"Comment": "This is textbook"}
        right_resp = [os.path.join('Test_images', 'textbook.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(
            True, len(resp) == 1 and flag)

    def test_6(self):
        dic_req = {"Comment": "This is peshka"}
        right_resp = [os.path.join('Test_images', 'peshka.jpg'),
                      os.path.join('Test_images', 'peshka1.jpg'),
                      os.path.join('Test_images', 'peshka2.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(
            True, len(resp) == 3 and flag)

    def test_7(self):
        dic_req = {"Comment": "This is animal"}
        right_resp = [os.path.join('Test_images', 'rabbit.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(
            True, len(resp) == 1 and flag)

    def test_7(self):
        dic_req = {"Key word": "wash",
                   "Topic": "python"}
        right_resp = [os.path.join('Test_images', 'fairy.jpg'),
                      os.path.join('Test_images', 'fairy1.jpg'),
                      os.path.join('Test_images', 'fairy2.jpg'),
                      os.path.join('Test_images', 'fairy3.jpg'),
                      os.path.join('Test_images', 'choco.jpg'),
                      os.path.join('Test_images', 'choco1.jpg'),
                      os.path.join('Test_images', 'choco2.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(
            True, len(resp) == 7 and flag)

    def test_8(self):
        dic_req = {"Key word": "something",
                   "Topic": "something"}
        resp = sp.response(dic_req, self.list_path)
        self.assertEqual(0, len(resp))

    def test_9(self):
        dic_req = {"Title": "bag",
                   "Topic": "something"}
        right_resp = [os.path.join('Test_images', 'bag.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(True, len(resp) == 1 and flag)

    def test_10(self):
        dic_req = {"Title": "что-то",
                   "Topic": "хохох",
                   "Author": 'автор'}
        resp = sp.response(dic_req, self.list_path)
        self.assertEqual(0, len(resp))

    def test_11(self):
        dic_req = {}
        resp = sp.response(dic_req, self.list_path)
        self.assertEqual(0, len(resp))

    def test_12(self):
        dic_req = {"Title": "Bag"}
        right_resp = [os.path.join('Test_images', 'bag.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(True, len(resp) == 1 and flag)

    def test_13(self):
        dic_req = {"Title": "    Bag   "}
        right_resp = [os.path.join('Test_images', 'bag.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(True, len(resp) == 1 and flag)

    def test_14(self):
        dic_req = {"Title": "B A G "}
        right_resp = [os.path.join('Test_images', 'bag.jpg')]
        resp = sp.response(dic_req, self.list_path)
        flag = True
        for r_rsp in right_resp:
            if r_rsp not in resp:
                flag = False
                break
        self.assertEqual(True, len(resp) == 1 and flag)

if __name__ == '__main__':
    unittest.main()
