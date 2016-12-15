from PIL import Image
import PIL.ExifTags

KEYS = {"Comment": "XPComment",
        "Title": "XPTitle",
        "Topic": "XPSubject",
        "Author": "XPAuthor",
        "Key word": "XPKeywords"}

PATH = 'C:\\Users\\Артём\\PycharmProjects\\PhotoAlbum\\Test_images\\forest.bmp'


def get_image_property(path):
    try:
        img = Image.open(path)
        if img.format == 'JPEG':
            if img._getexif() is not None:
                exif = {
                    PIL.ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in PIL.ExifTags.TAGS
                    }
                return exif
    except OSError:
        pass


def response(dic_req, list_path):
    resp = []
    for path in list_path:
        exif = get_image_property(path)
        if exif:
            for key in dic_req:
                if exif.get(KEYS[key]):
                    try:
                        example = exif[KEYS[key]].\
                            decode('utf-8').replace('\0', '')
                    except AttributeError:
                        example = exif[KEYS[key]]
                    if example.replace(' ', '').lower() == \
                            dic_req[key].replace(' ', '').lower():
                        resp.append(path)
                        break
    return resp
