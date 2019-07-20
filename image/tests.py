from django.test import TestCase
from image.models import Image
from django.test import Client

# Create your tests here.


class ImageTest(TestCase):
    def setUp(self):
        self.c = Client()
        im = Image(colors=[
            [0, 0, 0] for i in range(3)], path="image/test_image.jpeg")
        im.save()

    def test_get_closest_valid(self):
        """Should return valid response for a valid color"""
        response = self.c.get('/get_closest/ff00ff')
        self.assertEqual(response.status_code, 200)

    def test_get_closest_too_long(self):
        """Should return error 404 for a too long color"""
        response = self.c.get('/get_closest/ff00ffff')
        self.assertEqual(response.status_code, 404)

    def test_get_closest_too_short(self):
        """Should return error 404 for a too short color"""
        response = self.c.get('/get_closest/ff00')
        self.assertEqual(response.status_code, 404)

    def test_get_closest_invalid(self):
        """Should return 404 error for a not hex symbol in color"""
        response = self.c.get('/get_closest/ffr000')
        self.assertEqual(response.status_code, 404)

    def upload_file(self, path):
        """Just a helper function"""
        with open(path, "rb") as f:
            response = self.c.post("/upload_image", {"image": f})
            return response.status_code

    def test_upload_image_valid(self):
        """Should return 200 for a valid image save"""
        self.assertEqual(self.upload_file("image/test_image.jpeg"), 200)

    def test_upload_image_invalid_file_type(self):
        """Should return error 415 for invalid file"""
        self.assertEqual(self.upload_file("image/tests.py"), 415)

    def test_get_image_valid(self):
        """Should return 200 for a valid id"""
        id = Image.objects.all().first().id
        response = self.c.get(f"/get_image/{id}")
        self.assertEqual(response.status_code, 200)

    def test_get_image_invalid(self):
        """Should return an error 404 for id not in range"""
        id = Image.objects.all().last().id
        response = self.c.get(f"/get_image/{id + 1}")
        self.assertEqual(response.status_code, 404)
