from PIL import Image, ImageFilter
import numpy as np
bg=Image.open('/workspace/aicomic/assets/bg-s03-arena-final.jpg').convert('RGBA')
W,H=bg.size; s=W/1024
def key(p):
    im=Image.open(p).convert('RGB'); a=np.array(im).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]
    m=((g-np.maximum(r,b))>40)
    al=np.where(m,0,255).astype('uint8')
    a[...,1]=np.minimum(g,np.maximum(r,b)+10)  # despill
    out=Image.fromarray(np.dstack([a.clip(0,255).astype('uint8'),al]),'RGBA')
    out.putalpha(out.getchannel('A').filter(ImageFilter.GaussianBlur(1)))
    return out.crop(out.getbbox())
def place(img,h,cx,fy):
    h=int(h*s); w=int(img.width*h/img.height); img=img.resize((w,h),Image.LANCZOS)
    sh=Image.new('RGBA',(w,int(h*0.12)),(0,0,0,0))
    from PIL import ImageDraw; d=ImageDraw.Draw(sh); d.ellipse([0,0,w,sh.height],fill=(0,0,0,90))
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)),(int(cx*s-w/2),int(fy*s-sh.height/2)))
    bg.alpha_composite(img,(int(cx*s-w/2),int(fy*s-h)))
place(key('cut-collision.jpg'),95,770,318)
place(key('cut-chenyu.jpg'),120,965,345)
bg.convert('RGB').save('p01-v4-wide.jpg',quality=92)
x0=W-int(H*9/16); bg.crop((x0,0,x0+int(H*9/16),H)).convert('RGB').resize((1080,1920),Image.LANCZOS).save('p01-v4.jpg',quality=92)
