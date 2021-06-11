import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from utils import fonts
from utils.images import upload_image, circle_thumbnail

def player_skin(nickname):
	dst = Image.new('RGBA', (444, 264))
	dst.paste(Image.open(BytesIO(requests.get(f'https://excalibur-craft.ru/engine/ajax/lk/skin3d.php?login={nickname}&mode=profile').content)), (0, 0))
	dst.paste(Image.open(BytesIO(requests.get(f'https://excalibur-craft.ru/engine/ajax/lk/skin3d.php?login={nickname}&mode=profile&hr=-190').content)), (152, 0))
	cape = requests.get(f'https://bestlife.romanov.by/crop_img.php?nick={nickname}', headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
	if len(cape.content) > 5:
		dst.paste(Image.open(BytesIO(cape.content)).resize((120, 186), Image.ANTIALIAS), (312, 0))
	buffered = BytesIO()
	dst.save(buffered, format='PNG')

	return upload_image((buffered.getvalue())), len(cape.content) > 5

def welcome_card(nickname: str, avatar: str, member_number: int):
	thumbnail = circle_thumbnail(Image.open(BytesIO(requests.get(avatar).content)).convert('RGBA')).resize((149, 149), Image.ANTIALIAS)
	card = Image.new('RGBA', (523, 157))
	card.paste(Image.open('images/templates/welcome_card.png'), (0, 0))
	card.paste(thumbnail, (4, 4), mask=thumbnail)
	draw = ImageDraw.Draw(card)
	draw.text(xy=(170, 55), text=nickname, font=ImageFont.truetype(fonts.calibri, 26), fill=(112, 112, 112))
	draw.text(xy=(170, 85), text=f'{member_number}-й пользователь сервера', font=ImageFont.truetype(fonts.calibri, 16), fill=(122, 122, 122))
	buffered = BytesIO()
	card.save(buffered, format='PNG')

	return upload_image((buffered.getvalue()))

