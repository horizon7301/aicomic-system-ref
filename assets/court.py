import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
W,H=1280,720
cam=np.array([0.0,-11.0,11.0]); tgt=np.array([0.0,7.0,0.0])
f=(tgt-cam); f/=np.linalg.norm(f); up=np.array([0,0,1.0])
r=np.cross(f,up); r/=np.linalg.norm(r); u=np.cross(r,f)
foc=520
def P(x,y,z=0):
    v=np.array([x,y,z])-cam; d=np.array([v@r,v@u,v@f])
    return W/2+foc*d[0]/d[2], H*0.5-foc*d[1]/d[2]
def line(pts,c="white",lw=2.5,fill=None,ax=None):
    xy=[P(*p) for p in pts]
    if fill: ax.add_patch(Polygon(xy,closed=True,fc=fill,ec="none"))
    else: ax.plot(*zip(*xy),color=c,lw=lw,solid_capstyle="round")
def arc(cx,cy,rad,a0,a1,n=80):
    t=np.linspace(a0,a1,n); return list(zip(cx+rad*np.cos(t),cy+rad*np.sin(t)))
fig=plt.figure(figsize=(W/100,H/100),dpi=100); ax=fig.add_axes([0,0,1,1])
ax.set_xlim(0,W); ax.set_ylim(H,0); ax.axis("off")
ax.add_patch(plt.Rectangle((0,0),W,H,fc="#2a3550"))
line([(-17,-3),(17,-3),(17,18),(-17,18)],fill="#c9a06a",ax=ax)
line([(-14,0),(14,0),(14,15),(-14,15)],fill="#deb887",ax=ax)
for s in (-1,1):
    bx=s*14
    line([(bx,5.05),(bx-s*5.8,5.05),(bx-s*5.8,9.95),(bx,9.95)],fill="#b8323a",ax=ax)
    line([(bx,5.05),(bx-s*5.8,5.05),(bx-s*5.8,9.95),(bx,9.95)],ax=ax)
    line(arc(bx-s*5.8,7.5,1.8,0,2*np.pi),ax=ax)
    hx=bx-s*1.575
    a=np.arcsin((7.5-0.9)/6.75)
    pts=[(bx,0.9),(hx-s*np.sqrt(6.75**2-6.6**2),0.9)]
    t=np.linspace(-a,a,120) if s<0 else np.linspace(np.pi+a,np.pi-a,120)
    pts+= list(zip(hx+6.75*np.cos(t),7.5+6.75*np.sin(t)))
    pts+= [(bx,14.1)]
    line(pts,ax=ax)
    line(arc(hx,7.5,1.25,-np.pi/2,np.pi/2) if s<0 else arc(hx,7.5,1.25,np.pi/2,3*np.pi/2),ax=ax,lw=1.5)
    line([(bx-s*1.2,6.6,2.9),(bx-s*1.2,8.4,2.9),(bx-s*1.2,8.4,3.95),(bx-s*1.2,6.6,3.95),(bx-s*1.2,6.6,2.9)],c="#eeeeee",lw=2,ax=ax)
    line(arc(hx,7.5,0.23,0,2*np.pi,30),c="#ff6a00",lw=2,ax=ax)
    line([(bx+s*0.4,7.5,0),(bx+s*0.4,7.5,3.0),(bx-s*1.2,7.5,3.0)],c="#1f3c88",lw=4,ax=ax)
line([(-14,0),(14,0),(14,15),(-14,15),(-14,0)],ax=ax)
line([(0,0),(0,15)],ax=ax)
line(arc(0,7.5,1.8,0,2*np.pi),ax=ax)
line([(-3,-2.2,0.75),(3,-2.2,0.75),(3,-1.2,0.75),(-3,-1.2,0.75)],fill="#1f2d5c",ax=ax)
line([(-3,-1.2,0),(3,-1.2,0),(3,-1.2,0.75),(-3,-1.2,0.75)],fill="#162244",ax=ax)
fig.savefig("court-fiba-guide.png"); print("ok")
