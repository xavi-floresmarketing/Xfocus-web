from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='fonts/fontsource-montserrat/files/montserrat-latin-%d-normal.woff'
def mf(w,s): return ImageFont.truetype(F%w,s)
WHITE=(255,255,255);TINTA=(32,33,36);ROJO=(234,67,53);AZUL=(26,115,232);AMA=(251,188,4);VERDE=(24,128,56)
W,H=1080,1920; SHIFT=230
src=Image.open('/root/.claude/uploads/9d338d03-6138-591e-b5c2-abe75ccfc6ed/5a3fbb32-image.png').convert('RGBA')
src=src.resize((W,int(src.height*W/src.width)),Image.LANCZOS)
im=Image.new('RGBA',(W,H))
# extend sky: stretch top 40px strip over SHIFT area
strip=src.crop((0,0,W,40)).resize((W,SHIFT+2),Image.BICUBIC)
im.paste(strip,(0,0)); im.paste(src,(0,SHIFT))
d=ImageDraw.Draw(im)
def shadowed(fn):
    sh=Image.new('RGBA',im.size,(0,0,0,0)); fn(ImageDraw.Draw(sh),True)
    sh=sh.filter(ImageFilter.GaussianBlur(10)); im.alpha_composite(sh,(0,6)); fn(ImageDraw.Draw(im),False)
X=72
# logo
logo=Image.open('logo_xfocus_color.png').convert('RGBA'); a=logo.split()[3].point(lambda v:255 if v>40 else 0); logo=logo.crop(a.getbbox())
lh=46; logo=logo.resize((int(logo.width*lh/logo.height),lh),Image.LANCZOS)
fl=mf(900,30); tw=d.textlength('XFOCUS',font=fl); ly=272
box=(X,ly,X+16+logo.width+14+tw+20,ly+lh+24)
shadowed(lambda dd,s: dd.rounded_rectangle(box,16,fill=(0,0,0,150) if s else WHITE))
im.alpha_composite(logo,(X+16,ly+12)); d=ImageDraw.Draw(im)
d.text((X+16+logo.width+14,ly+18),'XFOCUS',font=fl,fill=TINTA)
# headline
fh=mf(900,112); asc,_=fh.getmetrics()
def txt(x,y,t,fill):
    shadowed(lambda dd,s: dd.text((x,y),t,font=fh,fill=(0,0,0,120) if s else fill))
y=372
txt(X,y,'Tu feria',WHITE); y+=128
txt(X,y,'empieza',WHITE); y+=128
w=d.textlength('antes',font=fh)
shadowed(lambda dd,s: dd.rounded_rectangle((X-14,y+8,X+w+18,y+asc+16),16,fill=(0,0,0,150) if s else ROJO))
d=ImageDraw.Draw(im); d.text((X,y),'antes',font=fh,fill=WHITE)
# chips stacked on the left, beside the head
fc=mf(800,34)
cy=y+asc+46; cx=X
for t,c,tc in [('1 · Antes',AZUL,WHITE),('2 · Durante',AMA,TINTA),('3 · Después',VERDE,WHITE)]:
    tw=d.textlength(t,font=fc); a_,_=fc.getmetrics(); b=(cx,cy,cx+tw+44,cy+a_+26)
    shadowed(lambda dd,s,b=b: dd.rounded_rectangle(b,14,fill=(0,0,0,150) if s else c))
    d=ImageDraw.Draw(im); d.text((cx+22,cy+13),t,font=fc,fill=tc); cx+=tw+44+12; end=cy+a_+26
print('chips end y',end,'x',cx, 'head approx y', int(580*W/941)+SHIFT)
out='XF_PORTADA-SHORT_ferias-atardecer_9x16_20261122_v01.jpg'
im.convert('RGB').save(out,quality=95)
# safe-zone check overlay
g=im.copy(); gd=ImageDraw.Draw(g)
gd.rectangle((0,0,W,250),outline=(0,255,0),width=4); gd.rectangle((0,H-420,W,H),outline=(0,255,0),width=4); gd.rectangle((W-180,0,W,H),outline=(0,255,0),width=4)
g.convert('RGB').resize((540,960)).save('short2_check.jpg')
