#!/usr/bin/env python3
"""Original offline block-placement puzzle. Python standard library only."""
import curses,os,json,random,time,sys
from pathlib import Path
from ui import put,run
import sprites
VERSION='1.0.0'
RECORD=Path.home()/'.local/share/gridflare/best.json'
BOARD=8
SHAPES=(
 ((0,0),),((0,0),(0,1)),((0,0),(1,0)),((0,0),(0,1),(0,2)),((0,0),(1,0),(2,0)),
 ((0,0),(0,1),(0,2),(0,3)),((0,0),(1,0),(2,0),(3,0)),
 ((0,0),(0,1),(0,2),(0,3),(0,4)),((0,0),(1,0),(2,0),(3,0),(4,0)),
 ((0,0),(0,1),(1,0),(1,1)),
 ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)),
 ((0,0),(1,0),(1,1)),((0,0),(0,1),(1,0)),((0,1),(1,0),(1,1)),((0,0),(0,1),(1,1)),
 ((0,0),(1,0),(2,0),(2,1)),((0,1),(1,1),(2,0),(2,1)),((0,0),(0,1),(1,0),(2,0)),((0,0),(0,1),(1,1),(2,1)),
 ((0,0),(0,1),(0,2),(1,1)),((0,1),(1,0),(1,1),(1,2)),((0,0),(1,0),(1,1),(2,0)),((0,1),(1,0),(1,1),(2,1)),
 ((0,1),(0,2),(1,0),(1,1)),((0,0),(0,1),(1,1),(1,2)),
 ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2)),((0,0),(0,1),(1,0),(1,1),(2,0),(2,1)))
class Puzzle:
 def __init__(self,seed=None):
  self.rng=random.Random(seed);self.grid=[[None]*BOARD for _ in range(BOARD)];self.score=0;self.over=False;self.message='Place all three pieces to draw three more.';self.offer=[];self.refill()
 def refill(self):
  self.offer=[(self.rng.choice(SHAPES),self.rng.randrange(6)) for _ in range(3)]
 def shape_dims(self,shape):
  return max(y for y,x in shape)+1,max(x for y,x in shape)+1
 def can_place(self,shape,r,c):
  for dy,dx in shape:
   y,x=r+dy,c+dx
   if not (0<=y<BOARD and 0<=x<BOARD) or self.grid[y][x] is not None:return False
  return True
 def fits_anywhere(self,shape):
  h,w=self.shape_dims(shape)
  return any(self.can_place(shape,r,c) for r in range(BOARD-h+1) for c in range(BOARD-w+1))
 def place(self,slot,r,c):
  if self.over:return False
  if not (0<=slot<len(self.offer)):return False
  shape,color=self.offer[slot]
  if not self.can_place(shape,r,c):self.message='No room there.';return False
  for dy,dx in shape:self.grid[r+dy][c+dx]=color
  self.score+=len(shape);self.offer.pop(slot)
  lines=0
  rows=[y for y in range(BOARD) if all(self.grid[y][x] is not None for x in range(BOARD))]
  cols=[x for x in range(BOARD) if all(self.grid[y][x] is not None for y in range(BOARD))]
  for y in rows:
   for x in range(BOARD):self.grid[y][x]=None
  for x in cols:
   for y in range(BOARD):self.grid[y][x]=None
  lines=len(rows)+len(cols)
  if lines:self.score+=100*lines+50*lines*(lines-1);self.message='Flare! '+str(lines)+' line'+('s' if lines>1 else '')+' cleared.'
  else:self.message='Placed.'
  if not self.offer:self.refill()
  if not any(self.fits_anywhere(s) for s,c in self.offer):self.over=True;self.message='No moves left. R restarts.'
  return True
def best():
 try:
  if RECORD.is_symlink():return 0
  return max(0,int(json.loads(RECORD.read_text()).get('best',0)))
 except (OSError,ValueError,TypeError,AttributeError):return 0
def save(score):
 try:
  if any(p.is_symlink() for p in [RECORD,*RECORD.parents]):return False
  RECORD.parent.mkdir(parents=True,exist_ok=True,mode=0o700);tmp=RECORD.with_suffix('.tmp');fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_TRUNC|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'w') as f:json.dump({'best':max(score,best())},f)
  tmp.replace(RECORD);return True
 except OSError:return False
def palette():
 if not curses.has_colors():return False
 curses.start_color();curses.use_default_colors()
 values=[(220,-1),(81,-1),(201,-1),(208,-1),(46,-1),(196,-1),(255,-1),(245,-1)] if curses.COLORS>=256 else [(3,-1),(6,-1),(5,-1),(1,-1),(2,-1),(1,-1),(7,-1),(7,-1)]
 for i,(fg,bg) in enumerate(values,1):curses.init_pair(i,fg,bg)
 return True
def play(s):
 g=Puzzle();row=0;col=0;slot=0;recorded=False;high=best();pixels=sprites.supported() and '--ascii' not in sys.argv;colors=palette()
 def color(i):return curses.color_pair(i) if colors else 0
 while True:
  s.timeout(120);key=s.getch();h,w=s.getmaxyx();s.erase()
  if key in (27,ord('q'),ord('Q')):return
  if key in (ord('v'),ord('V')):pixels=not pixels;s.clear()
  if key in (ord('r'),ord('R')):g=Puzzle();row=0;col=0;slot=0;recorded=False
  if h<24 or w<64:put(s,1,1,'Resize to 64x24. Game paused. Q quits.');s.refresh();continue
  if key in (ord('1'),ord('2'),ord('3')) and ord('1')<=key<ord('1')+len(g.offer):slot=key-ord('1')
  slot=min(slot,max(0,len(g.offer)-1))
  if not g.over and g.offer:
   shape,pcol=g.offer[slot]
   sh,sw=g.shape_dims(shape)
   if key in (curses.KEY_UP,ord('w'),ord('W')):row=max(0,row-1)
   if key in (curses.KEY_DOWN,ord('s'),ord('S')):row=min(BOARD-sh,row+1)
   if key in (curses.KEY_LEFT,ord('a'),ord('A')):col=max(0,col-1)
   if key in (curses.KEY_RIGHT,ord('d'),ord('D')):col=min(BOARD-sw,col+1)
   if key in (ord(' '),10,13):
    if g.place(slot,row,col):slot=min(slot,max(0,len(g.offer)-1));row=0;col=0
  row=max(0,min(row,BOARD-1));col=max(0,min(col,BOARD-1))
  if g.over and not recorded:g.message+=' Best saved.' if save(g.score) else ' Save unavailable.';recorded=True;high=max(high,best())
  cw=4;rh=2;ox=max(2,(w-cw*BOARD)//2);oy=3
  if not pixels:
   for y in range(BOARD):
    for x in range(BOARD):
     cell=g.grid[y][x]
     put(s,oy+y*rh,ox+x*cw,'.'*(cw-1),color(8))
     if cell is not None:
      for yy in range(rh):put(s,oy+y*rh+yy,ox+x*cw,'['+' '*(cw-2)+']',color(cell+1))
   if g.offer and not g.over:
    shape,pcol=g.offer[slot]
    ok=g.can_place(shape,row,col)
    for dy,dx in shape:
     for yy in range(rh):put(s,oy+(row+dy)*rh+yy,ox+(col+dx)*cw,'<'+' '*(cw-2)+'>',color(pcol+1)|(curses.A_BOLD if ok else curses.A_DIM))
  tx=ox;ty=oy+BOARD*rh+2
  for i,(shape,pcol) in enumerate(g.offer):
   put(s,ty-1,tx,('>' if i==slot else ' ')+str(i+1),color(7))
   for dy,dx in shape:put(s,ty+dy,tx+2+dx*3,'[]',color(pcol+1))
   tx+=g.shape_dims(shape)[1]*3+6
  put(s,0,2,'GRIDFLARE | SCORE '+str(g.score)+' | BEST '+str(high),color(7)|curses.A_BOLD)
  put(s,1,2,g.message,color(2))
  put(s,h-2,2,'1-3 choose piece | Arrows/WASD move | Space place | V pixel/text | R restart | Q quit',color(7))
  put(s,h-1,2,'Fill a full row or column to flare it clear. No fitting piece ends the run.',color(8));s.refresh()
  if pixels:sys.stdout.write(sprites.frame(g,cw,rh,ox,oy,slot,row,col));sys.stdout.flush()
if __name__=='__main__':
 if '--version' in sys.argv:print(VERSION)
 else:raise SystemExit(run(play))
