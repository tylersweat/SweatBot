from PIL import Image, ImageFont, ImageDraw
from OSRSBytes import Hiscores

FONT_SIZE = 18
OFFSET = (21, 16)
ROW1 = 6
ROW2 = 52
ROW3 = 98
ROW4 = 144
ROW5 = 190
ROW6 = 236
ROW7 = 282
ROW8 = 328

COL1 = 56
COL2 = 162
COL3 = 268

TOTAL_3 = (248,343)
TOTAL_4 = (248,343)


coordinates = {
    'attack': (COL1, ROW1),
    'strength': (COL1, ROW2),
    'defense': (COL1, ROW3),
    'ranged': (COL1, ROW4),
    'prayer': (COL1, ROW5),
    'magic': (COL1, ROW6),
    'runecrafting': (COL1, ROW7),
    'construction': (COL1, ROW8),
    'hitpoints': (COL2, ROW1),
    'agility': (COL2, ROW2),
    'herblore': (COL2, ROW3),
    'thieving': (COL2, ROW4),
    'crafting': (COL2, ROW5),
    'fletching': (COL2, ROW6),
    'slayer': (COL2, ROW7),
    'hunter': (COL2, ROW8),
    'mining': (COL3, ROW1),
    'smithing': (COL3, ROW2),
    'fishing': (COL3, ROW3),
    'cooking': (COL3, ROW4),
    'firemaking': (COL3, ROW5),
    'woodcutting': (COL3, ROW6),
    'farming': (COL3, ROW7)
}

def sum_tuple(a,b):
    return tuple(map(sum, zip(a, b)))


def create_stats(rsn, out):
    user = Hiscores(rsn)
    total = int(user.skill('total'))
    img = Image.open('static/blank.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('static/osrs.ttf', FONT_SIZE)
    for skill in coordinates:
        draw.text(coordinates[skill], str(user.skill(skill, 'level')), (255,255,0), font=font)
        draw.text(sum_tuple(coordinates[skill], OFFSET), str(user.skill(skill, 'level')), (255,255,0), font=font)
    if total < 1000:
        draw.text(TOTAL_3, str(total), (255,255,0), font=font)
    else:
        draw.text(TOTAL_4, str(total), (255,255,0), font=font)
    img.save(out, format='PNG')
    out.seek(0)
