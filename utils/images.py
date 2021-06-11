import base64
import requests
from PIL import Image
from PIL import ImageDraw

ONLINE_THUMBNAIL = 'https://i.imgur.com/oV79DmH.png'
VOTE_THUMBNAIL = 'https://i.imgur.com/lFQEMTe.png'
MONITORING_THUMBNAIL = 'https://i.imgur.com/BQGIkzE.png'

SPEEDWAGON_AVATAR_IMAGE = 'https://i.imgur.com/4Ml9ZR2.png'

EX_CRAFT_LOGO = 'https://i.imgur.com/vIPnsl6.png'

def upload_image(image: bytes):
	return requests.post('https://api.imgbb.com/1/upload', {'key':'d4a339ea81117c8a109446772b41a198', 'image':base64.b64encode(image)}).json()['data']['url']

def circle_thumbnail(image: Image):
	bigsize = (image.size[0] * 3, image.size[1] * 3)
	mask = Image.new('L', bigsize, 0)
	draw = ImageDraw.Draw(mask)
	draw.ellipse((0, 0) + bigsize, fill=255)
	mask = mask.resize(image.size, Image.ANTIALIAS)
	image.putalpha(mask)
	return image
