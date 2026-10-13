#!/usr/bin/env python3
"""Reproducible static-site icons and social cards from tracked SVG sources."""
from pathlib import Path
from io import BytesIO
import json
import cairosvg
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'brand-source'; DST=ROOT/'assets'; DST.mkdir(exist_ok=True)

def raster_svg(name,size=None):
    kw={'url':str(SRC/name)}
    if size: kw.update(output_width=size[0],output_height=size[1])
    return Image.open(BytesIO(cairosvg.svg2png(**kw))).convert('RGBA')

icon=raster_svg('brand-icon.svg',(1024,1024))
for size in (16,32,48,96,152,167,180,192,256,512,1024):
    im=icon.resize((size,size),Image.Resampling.LANCZOS)
    filename=('apple-touch-icon.png' if size==180 else f'icon-{size}.png')
    im.convert('RGB').save(DST/filename,optimize=True)
for n in (152,167):
    (DST/f'apple-touch-icon-{n}.png').write_bytes((DST/f'icon-{n}.png').read_bytes())
icon.save(DST/'favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48)],append_images=[])
background=Image.new('RGB',(512,512),'#065ca7');draw=ImageDraw.Draw(background)
for yy in range(512):
    t=yy/511
    draw.line((0,yy,512,yy),fill=(int(3+8*t),int(62+67*t),int(145+35*t)))
thumb=icon.resize((344,344),Image.Resampling.LANCZOS)
background.paste(thumb,(84,84),thumb)
background.save(DST/'icon-maskable-512.png',optimize=True)
social=raster_svg('social-preview.svg',(1200,630)).convert('RGB')
social.save(DST/'social-preview.png',optimize=True)
social.save(DST/'social-preview.jpg',quality=90,optimize=True,subsampling=0)
print(json.dumps({p.name:p.stat().st_size for p in DST.iterdir()},indent=2))
