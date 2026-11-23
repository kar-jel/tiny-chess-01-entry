import json,os
import urllib.request as R

U=os.environ.get('MAKEFUN_ENV_URL') or 'http://127.0.0.1:8080'
MT=90000
W=(33,31,18,14,-14,-18,-31,-33)
D=(15,17,-15,-17)
L=(1,-1,16,-16)
K=D+L
KV=(0,100,320,330,500,900,0)
SQ=tuple(x for x in range(128) if not x&136)


def pst(t,r,f):
 c=min(f,7-f)+min(r,7-r)
 if t==1:return(0,0,4,8,14,24,40,0)[r]+(10 if f==3 or f==4 else 0)
 if t==2:return 6*c-20
 if t==3:return 4*c-8
 if t==4:return 15 if r==6 else 0
 if t==5:return 2*c-6
 return(20,25,10,0,0,10,25,20)[f] if r==0 else max(-50,-15*r)


V=[0]*2048
for _p in range(1,16):
 _t=_p&7
 if _t in(0,7):continue
 for _s in SQ:
  _r=_s>>4
  if _p>8:_r=7-_r
  V[_p*128+_s]=(1 if _p<8 else -1)*(KV[_t]+pst(_t,_r,_s&7))

ST=[0]*239
for _d in K:
 for _k in range(1,8):ST[119+_k*_d]=_d

M64=(1<<64)-1
_x=0x9E3779B97F4A7C15


def _n():
 global _x
 _x=(_x+0x9E3779B97F4A7C15)&M64
 z=_x
 z=((z^(z>>30))*0xBF58476D1CE4E5B9)&M64
 z=((z^(z>>27))*0x94D049BB133111EB)&M64
 return z^(z>>31)


Z=[_n() for _ in range(2048)]
ZC=[_n() for _ in range(16)]
ZE=[_n() for _ in range(8)]
ZS=_n()

CK=[15]*128
CK[0]=13;CK[7]=14;CK[4]=12;CK[112]=7;CK[119]=11;CK[116]=3

b=[0]*128
side=0;cr=0;ep=-1;ks=[4,116];ss=0;hm=0;h=0;ck=0
stk=[];hs=[]
tt={}
nd=0;lim=0;ab=0
kil=[0]*128
hist=[0]*128


def ld(f):
 global b,side,cr,ep,ks,ss,hm,h,ck,stk,hs
 w=f.split()
 b=[0]*128
 for i,row in enumerate(w[0].split('/')):
  fl=0
  for ch in row:
   if ch<='9':fl+=int(ch)
   else:
    b[(7-i)*16+fl]='.pnbrqk'.index(ch.lower())+(0 if ch.isupper() else 8)
    fl+=1
 side=0 if w[1]=='w' else 1
 cr=0
 for i,ch in enumerate('KQkq'):
  if ch in w[2]:cr|=1<<i
 ep=-1 if w[3]=='-' else (int(w[3][1])-1)*16+'abcdefgh'.index(w[3][0])
 ks=[b.index(6),b.index(14)]
 hm=int(w[4]) if len(w)>4 else 0
 ss=0
 h=0
 for x in SQ:
  p=b[x]
  if p:
   ss+=V[p*128+x]
   h^=Z[p*128+x]
 if side:h^=ZS
 h^=ZC[cr]
 if ep>=0:h^=ZE[ep&7]
 stk=[]
 hs=[]
 ck=atk(ks[side],side^1)


def atk(sq,c):
 bb=b
 o=c*8
 for d in((-15,-17),(15,17))[c]:
  t=sq+d
  if t&136==0 and bb[t]==1+o:return 1
 for d in W:
  t=sq+d
  if t&136==0 and bb[t]==2+o:return 1
 for d in K:
  t=sq+d
  if t&136==0 and bb[t]==6+o:return 1
 for ds,ts in((D,(3,5)),(L,(4,5))):
  for d in ds:
   t=sq+d
   while t&136==0:
    p=bb[t]
    if p:
     if p&7 in ts and p>>3==c:return 1
     break
    t+=d
 return 0


def lin(k,f,by):
 d=ST[f-k+119]
 if not d:return 0
 di=d in D
 t=k+d
 while t&136==0:
  p=b[t]
  if p:
   if p>>3!=by:return 0
   q=p&7
   return q==5 or q==(3 if di else 4)
  t+=d
 return 0


def gen(cp):
 bb=b
 ms=[]
 ad=16-side*32
 lr=7-side*7
 for f in SQ:
  p=bb[f]
  if not p or p>>3!=side:continue
  t=p&7
  if t==1:
   x=f+ad
   if not bb[x]:
    if x>>4==lr:ms+=[f|x<<7|q<<14 for q in(5,4,3,2)]
    elif not cp:
     ms.append(f|x<<7)
     if f>>4==(1,6)[side] and not bb[f+2*ad]:ms.append(f|(f+2*ad)<<7)
   for d in(ad-1,ad+1):
    x=f+d
    if x&136:continue
    y=bb[x]
    if y:
     if y>>3!=side:
      if x>>4==lr:ms+=[f|x<<7|q<<14 for q in(5,4,3,2)]
      else:ms.append(f|x<<7)
    elif x==ep:ms.append(f|x<<7)
  elif t==2 or t==6:
   for d in(W if t==2 else K):
    x=f+d
    if x&136:continue
    y=bb[x]
    if y:
     if y>>3!=side:ms.append(f|x<<7)
    elif not cp:ms.append(f|x<<7)
   if t==6 and not cp:
    z=112*side
    if cr&1<<(2*side) and not bb[z+5] and not bb[z+6]:ms.append(f|(z+6)<<7)
    if cr&2<<(2*side) and not bb[z+3] and not bb[z+2] and not bb[z+1]:ms.append(f|(z+2)<<7)
  else:
   for d in(D if t==3 else L if t==4 else K):
    x=f+d
    while x&136==0:
     y=bb[x]
     if y:
      if y>>3!=side:ms.append(f|x<<7)
      break
     if not cp:ms.append(f|x<<7)
     x+=d
 return ms


def mk(m):
 global side,cr,ep,ss,hm,h
 bb=b
 f=m&127
 t=m>>7&127
 q=m>>14&7
 p=bb[f]
 u=p>>3
 cs=t
 if p&7==1 and t==ep and not bb[t]:cs=t-16+u*32
 cap=bb[cs]
 o=[m,cap,cr,ep,ss,h,hm,ck,ks[u],cs]
 hh=h^Z[p*128+f]
 if cap:
  hh^=Z[cap*128+cs]
  bb[cs]=0
  ss-=V[cap*128+cs]
 bb[f]=0
 ss-=V[p*128+f]
 n=p if not q else q|u*8
 bb[t]=n
 ss+=V[n*128+t]
 hh^=Z[n*128+t]
 isk=p&7==6
 if isk:
  ks[u]=t
  if t-f==2 or f-t==2:
   r1=f+3 if t>f else f-4
   r2=f+1 if t>f else f-1
   r=bb[r1]
   bb[r1]=0
   bb[r2]=r
   ss+=V[r*128+r2]-V[r*128+r1]
   hh^=Z[r*128+r1]^Z[r*128+r2]
 nc=cr&CK[f]&CK[t]
 if nc!=cr:
  hh^=ZC[cr]^ZC[nc]
  cr=nc
 if ep>=0:hh^=ZE[ep&7]
 ep=-1
 if p&7==1 and abs(t-f)==32 and ((t+1&136)==0 and bb[t+1]==(9,1)[u] or (t-1&136)==0 and bb[t-1]==(9,1)[u]):
  ep=f+t>>1
  hh^=ZE[ep&7]
 hm=0 if p&7==1 or cap else hm+1
 stk.append(o)
 side=u^1
 if isk or ck or cs!=t:
  bad=atk(ks[u],u^1)
  if not bad and isk and (t-f==2 or f-t==2):bad=ck or atk(f+t>>1,u^1)
  if bad:
   h=hh
   um()
   return 0
 else:
  if lin(ks[u],f,u^1):
   h=hh
   um()
   return 0
 h=hh
 return 1


def um():
 global side,cr,ep,ss,hm,h,ck
 m,cap,cr0,ep0,ss0,h0,hm0,ck0,ku,cs=stk.pop()
 f=m&127
 t=m>>7&127
 u=side^1
 p=b[t] if m>>14&7==0 else 1|u*8
 b[f]=p
 b[t]=0
 if cap:b[cs]=cap
 if p&7==6:
  ks[u]=f
  if t-f==2 or f-t==2:
   r1=f+3 if t>f else f-4
   r2=f+1 if t>f else f-1
   b[r1]=b[r2]
   b[r2]=0
 cr=cr0
 ep=ep0
 ss=ss0
 h=h0
 hm=hm0
 ck=ck0
 side=u


def ev():
 return ss if not side else -ss


def ordr(ms,pl,tm):
 bb=b
 out=[]
 for m in ms:
  f=m&127
  t=m>>7&127
  q=m>>14&7
  if m==tm:v=1000000
  elif q:v=200000+q
  elif bb[t]:v=100000+10*KV[bb[t]&7]-(bb[f]&7)
  elif m==kil[2*pl]:v=90
  elif m==kil[2*pl+1]:v=80
  else:v=hist[t]
  out.append((v,m))
 out.sort(reverse=True)
 return [m for v,m in out]


def qs(a,be,pl):
 global nd,ab,ck
 nd+=1
 if ab or(lim and nd>lim):ab=1;return 0
 if pl>48:return ev()
 ck=atk(ks[side],side^1)
 if ck:
  ms=gen(0)
  best=-MT-1
 else:
  v=ev()
  if v>=be:return v
  best=v
  if v>a:a=v
  ms=gen(1)
 lg=0
 sp=best
 for m in ordr(ms,pl,0):
  if not mk(m):continue
  if sp>-MT+1000 and b[m>>7&127] and sp+KV[b[m>>7&127]&7]+150<a:um();continue
  lg+=1
  v=-qs(-be,-a,pl+1)
  um()
  if ab:return 0
  if v>best:best=v
  if v>=be:break
  if v>a:a=v
 if ck and not lg:return -MT+pl
 return best


def sr(d,a,be,pl):
 global nd,ab,ck
 if pl and(hm>=100 or h in hs):return 0
 hs.append(h)
 try:
  ck=atk(ks[side],side^1)
  if ck:d+=1
  if d<1:return qs(a,be,pl)
  nd+=1
  if ab or(lim and nd>lim):ab=1;return 0
  al=a
  e=tt.get(h)
  tm=0
  if e:
   tm=e[3]
   if e[0]>=d:
    v=e[2]
    if v>MT-500:v-=pl
    elif v<-MT+500:v+=pl
    fg=e[1]
    if fg==1 or(fg==2 and v>=be)or(fg==3 and v<=a):return v
  lg=0
  best=-MT-1
  bm=0
  for m in ordr(gen(0),pl,tm):
   if not mk(m):continue
   lg+=1
   v=-sr(d-1,-be,-a,pl+1)
   um()
   if ab:return 0
   if v>best:
    best=v
    bm=m
   if v>a:a=v
   if a>=be:
    if not b[m>>7&127] and not m>>14&7:
     if kil[2*pl]!=m:
      kil[2*pl+1]=kil[2*pl]
      kil[2*pl]=m
    else:
     t=m>>7&127
     if hist[t]<60:hist[t]+=1
    break
  if not lg:return -MT+pl if ck else 0
  sv=best+pl if best>MT-500 else(best-pl if best<-MT+500 else best)
  tt[h]=(d,3 if best<=al else(2 if best>=be else 1),sv,bm)
  return best
 finally:
  hs.pop()


def legal():
 global ck
 ck=atk(ks[side],side^1)
 return [m for m in gen(0) if mk(m) and not um()]


def go(dep,bud):
 global nd,lim,ab,ck,h
 ms=legal()
 if not ms:return 0
 ck=atk(ks[side],side^1)
 tt.clear()
 sc={m:-MT for m in ms}
 best=ms[0]
 for d in range(1,dep+1):
  nd=0
  ab=0
  lim=bud if d>1 else 0
  a=-MT-1
  ns={}
  bm=best
  for m in sorted(ms,key=lambda m:-sc[m]):
   mk(m)
   v=-sr(d-1,-MT-1,-a,1)
   um()
   if ab:break
   ns[m]=v
   if v>a:a=v;bm=m
  if ab:break
  sc=ns
  ms=list(ns)
  best=bm
  if a>MT-1000:break
 return best


def uci(m):
 f=m&127
 t=m>>7&127
 q=m>>14&7
 return 'abcdefgh'[f&7]+str((f>>4)+1)+'abcdefgh'[t&7]+str((t>>4)+1)+(' pnbrq'[q] if q else '')


def pmv(s):
 f=(int(s[1])-1)*16+'abcdefgh'.index(s[0])
 t=(int(s[3])-1)*16+'abcdefgh'.index(s[2])
 return f|t<<7|(' pnbrq'.index(s[4])<<14 if len(s)>4 else 0)


def gh(sf,mvs):
 global ck
 ld(sf)
 o=[h]
 for x in mvs:
  ck=atk(ks[side],side^1)
  mk(pmv(x))
  o.append(h)
 return o


def call(p,o):
 return json.load(R.urlopen(R.Request(U+p,json.dumps(o).encode(),{'content-type':'application/json'}),timeout=60))


def send(n,mv,lm):
 for x in [mv]+[y for y in lm if y!=mv][:3]:
  try:return call('/move',{'game':n,'move':x})
  except Exception:pass
 return None


DEP=64
BUD=25000

if __name__=='__main__':
 bad=0
 g=call('/game',{})
 while g.get('status')!='done':
  if g['status']=='your_move':
   try:
    hs[:]=gh(g['start_fen'],g['moves'])
   except Exception:pass
   ld(g['fen'])
   m=go(DEP,BUD)
   mv=uci(m) if m else g['legal_moves'][0]
   r=send(g['game'],mv,g['legal_moves'])
   if r is None:
    bad+=1
    if bad>3:break
    r=call('/game',{})
   g=r
  else:
   g=call('/game',{})
