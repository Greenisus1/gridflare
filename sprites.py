"""Colored block rendering with ANSI RGB half blocks. Original art."""
import os
COLORS=((255,211,56),(87,200,220),(192,118,220),(230,127,44),(83,189,77),(225,68,71))
GHOST=(120,120,120);BOARD_BG=(24,28,36);GRID_LINE=(44,50,62)
def supported():return os.environ.get('COLORTERM','').lower() in ('truecolor','24bit') or 'direct' in os.environ.get('TERM','').lower()
def frame(g,cw,rh,ox,oy,slot,row,col):
 width=cw*8;height=rh*8*2
 canvas=[[BOARD_BG for _ in range(width)] for _ in range(height)]
 for y in range(8):
  for x in range(8):
   for yy in range(rh*2):canvas[y*rh*2+yy][x*cw]=GRID_LINE;canvas[y*rh*2+yy][(x+1)*cw-1]=GRID_LINE
   for xx in range(cw):canvas[y*rh*2][x*cw+xx]=GRID_LINE;canvas[(y+1)*rh*2-1][x*cw+xx]=GRID_LINE
   cell=g.grid[y][x]
   if cell is not None:
    c=COLORS[cell]
    for yy in range(1,rh*2-1):
     for xx in range(1,cw-1):canvas[y*rh*2+yy][x*cw+xx]=c
 if g.offer and not g.over:
  shape,pcol=g.offer[min(slot,len(g.offer)-1)]
  ok=g.can_place(shape,row,col)
  tint=COLORS[pcol] if ok else GHOST
  for dy,dx in shape:
   for yy in range(1,rh*2-1):
    for xx in range(1,cw-1):
     y=(row+dy)*rh*2+yy;x=(col+dx)*cw+xx
     if 0<=y<height and 0<=x<width:
      bg=canvas[y][x]
      canvas[y][x]=tuple((a+b)//2 for a,b in zip(tint,bg)) if ok else tint
 out=[]
 for y in range(0,height,2):
  out.append(f'\x1b[{oy+y//2+1};{ox+1}H');fg=bg=None
  for x in range(width):
   a,b=canvas[y][x],canvas[y+1][x]
   if a!=fg:out.append('\x1b[38;2;'+';'.join(map(str,a))+'m');fg=a
   if b!=bg:out.append('\x1b[48;2;'+';'.join(map(str,b))+'m');bg=b
   out.append('▀')
 out.append('\x1b[0m');return ''.join(out)
