from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='fonts/fontsource-montserrat/files/montserrat-latin-%d-normal.woff'
def mf(w,s): return ImageFont.truetype(F%w,s)
WHITE=(255,255,255);TINTA=(32,33,36);ROJO=(234,67,53);AZUL=(26,115,232);AMA=(251,188,4);VERDE=(24,128,56)
im=Image.open('/root/.claude/uploads/9d338d03-6138-591e-b5c2-abe75ccfc6ed/af08923b-image.png').convert('RGBA')
W,H=im.size
# soft shadow layer helper
def shadowed(draw_fn):
    sh=Image.new('RGBA',im.size,(0,0,0,0)); draw_fn(ImageDraw.Draw(sh),(0,0,0,150),True)
    sh=sh.filter(ImageFilter.GaussianBlur(10)); im.alpha_composite(sh,(0,6))
    draw_fn(ImageDraw.Draw(im),None,False)

# --- headline in bottom band ---
fh=mf(900,96); x=60; y=790
d=ImageDraw.Draw(im)
t1='Tu feria empieza '
w1=d.textlength(t1,font=fh); w2=d.textlength('antes',font=fh)
asc,_=fh.getmetrics()
d.text((x,y),t1,font=fh,fill=WHITE)
bx=x+w1
d.rounded_rectangle((bx-12,y+6,bx+w2+16,y+asc+14),14,fill=ROJO)
d.text((bx,y),'antes',font=fh,fill=WHITE)

# --- chips per panel ---
fc=mf(800,36)
def chip(x,y,txt,col,tc):
    w=d.textlength(txt,font=fc); a,_=fc.getmetrics()
    box=(x,y,x+w+48,y+a+30)
    def fn(dd,c,isshadow):
        dd.rounded_rectangle(box,14,fill=c if isshadow else col)
        if not isshadow: dd.text((x+24,y+15),txt,font=fc,fill=tc)
    shadowed(fn)
chip(36,640,'1 · Antes',AZUL,WHITE)
chip(530,640,'2 · Durante',AMA,TINTA)
chip(1112,640,'3 · Después',VERDE,WHITE)
d=ImageDraw.Draw(im)

# --- logo top-left ---
sym=Image.open('xfocus_symbol.png').convert('RGBA'); sym=sym.crop(sym.getbbox())
sh_=44; sym=sym.resize((int(sym.width*sh_/sym.height),sh_),Image.LANCZOS)
fl=mf(900,28); lx,ly=30,26
tw=d.textlength('XFOCUS',font=fl)
pill=Image.new('RGBA',im.size,(0,0,0,0)); pd=ImageDraw.Draw(pill)
pd.rounded_rectangle((lx-14,ly-12,lx+sym.width+16+tw+22,ly+sh_+12),16,fill=(32,33,36,170))
im.alpha_composite(pill)
im.alpha_composite(sym,(lx,ly))
d=ImageDraw.Draw(im)
d.text((lx+sym.width+16,ly+7),"XFOCUS",font=fl,fill=WHITE)

base='XF_MINIATURA_ferias-triptico_16x9_20261122_v01'
im.convert('RGB').save(base+'_full.jpg',quality=95)
im.convert('RGB').resize((1280,720),Image.LANCZOS).save(base+'.jpg',quality=95)
