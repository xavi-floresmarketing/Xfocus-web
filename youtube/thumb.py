from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='fonts/fontsource-montserrat/files/montserrat-latin-%d-normal.woff'
R='fonts/fontsource-roboto/files/roboto-latin-%d-normal.woff'
def mf(w,s): return ImageFont.truetype(F%w,s)
def rf(w,s): return ImageFont.truetype(R%w,s)
WHITE=(255,255,255);NUBE=(248,249,250);TINTA=(32,33,36);ROJO=(234,67,53);AZUL=(26,115,232);AMA=(251,188,4);VERDE=(24,128,56)

cut=Image.open('xavi_truck_cut.png')
bb=cut.getbbox(); cut=cut.crop(bb)
# keep head to mid-thigh
cut=cut.crop((0,0,cut.width,int(cut.height*0.62)))

def person_layer(h):
    p=cut.resize((int(cut.width*h/cut.height),h),Image.LANCZOS)
    a=p.split()[3]
    pad=40
    lay=Image.new('RGBA',(p.width+pad*2,p.height+pad),(0,0,0,0))
    big=Image.new('L',lay.size,0); big.paste(a,(pad,pad))
    stroke=big.filter(ImageFilter.MaxFilter(17))
    shadow=big.filter(ImageFilter.MaxFilter(17)).filter(ImageFilter.GaussianBlur(18))
    out=Image.new('RGBA',lay.size,(0,0,0,0))
    sh=Image.new('RGBA',lay.size,(0,0,0,110)); out.paste(sh,(14,10),shadow)
    out.paste(Image.new('RGBA',lay.size,WHITE+(255,)),(0,0),stroke)
    out.alpha_composite(p,(pad,pad))
    return out

def bg(W,H):
    im=Image.new('RGBA',(W,H),NUBE+(255,))
    d=ImageDraw.Draw(im)
    for x in range(0,W,32):
        for y in range(0,H,32): d.ellipse((x-1.5,y-1.5,x+1.5,y+1.5),fill=(218,220,224))
    return im

def chips(d,x,y,f,items,padx,pady,gap,r):
    for n,(txt,col,tc) in enumerate(items):
        w=d.textlength(txt,font=f); asc,desc=f.getmetrics(); h=asc
        d.rounded_rectangle((x,y,x+w+padx*2,y+h+pady*2),r,fill=col)
        d.text((x+padx,y+pady),txt,font=f,fill=tc)
        x+=w+padx*2+gap
    return y+h+pady*2

items=[('1 · Antes',AZUL,WHITE),('2 · Durante',AMA,TINTA),('3 · Después',VERDE,WHITE)]

# ---------- 16:9 ----------
W,H=1280,720
im=bg(W,H); d=ImageDraw.Draw(im)
d.ellipse((780,90,1300,610),fill=ROJO)
d.ellipse((835,145,1245,555),outline=WHITE,width=6)
p=person_layer(700); im.alpha_composite(p,(1240-p.width+60,H-p.height+40))
d=ImageDraw.Draw(im)
x=64
f=mf(800,30); t='FERIAS DE EMPRENDEDORES'
d.rounded_rectangle((x,56,x+d.textlength(t,font=f)+40,56+52),10,fill=TINTA)
d.text((x+20,64),t,font=f,fill=WHITE)
fh=mf(900,118)
d.text((x,128),'Tu feria',font=fh,fill=TINTA)
d.text((x,250),'empieza',font=fh,fill=TINTA)
w=d.textlength('antes',font=fh)
d.rounded_rectangle((x-14,384,x+w+18,512),14,fill=ROJO)
d.text((x,372),'antes',font=fh,fill=WHITE)
chips(d,x,560,mf(800,34),items,22,16,14,12)
im.convert('RGB').save('XF_MINIATURA_ferias-emprendedores_16x9_20261122_v01.jpg',quality=95)

# ---------- 9:16 Shorts ----------
W,H=1080,1920
im=bg(W,H); d=ImageDraw.Draw(im)
d.ellipse((90,1060,1010,1980),fill=ROJO)
d.ellipse((165,1135,935,1905),outline=WHITE,width=8)
p=person_layer(1000); im.alpha_composite(p,((W-p.width)//2-30,1010))
d=ImageDraw.Draw(im)
x=72
f=mf(800,38); t='FERIAS DE EMPRENDEDORES'
d.rounded_rectangle((x,270,x+d.textlength(t,font=f)+48,270+64),12,fill=TINTA)
d.text((x+24,280),t,font=f,fill=WHITE)
fh=mf(900,150)
d.text((x,360),'Tu feria',font=fh,fill=TINTA)
d.text((x,515),'empieza',font=fh,fill=TINTA)
w=d.textlength('antes',font=fh)
d.rounded_rectangle((x-16,690,x+w+22,852),18,fill=ROJO)
d.text((x,675),'antes',font=fh,fill=WHITE)
chips(d,x,885,mf(800,36),items,22,16,12,12)
im.convert('RGB').save('XF_PORTADA-SHORT_ferias-emprendedores_9x16_20261122_v01.jpg',quality=95)
