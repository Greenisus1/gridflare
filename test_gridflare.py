import unittest,tempfile
from pathlib import Path
from unittest.mock import patch
import gridflare as a

class Tests(unittest.TestCase):
 def test_initial(self):
  g=a.Puzzle(1);self.assertEqual(len(g.offer),3);self.assertEqual(g.score,0);self.assertFalse(g.over)
 def test_place(self):
  g=a.Puzzle();g.offer=[(((0,0),(0,1)),0)];self.assertTrue(g.place(0,3,3));self.assertEqual(g.score,2)
  self.assertEqual(g.grid[3][3],0);self.assertEqual(g.grid[3][4],0)
 def test_bounds(self):
  g=a.Puzzle();g.offer=[(((0,0),(0,1)),0)];self.assertFalse(g.place(0,0,8));self.assertFalse(g.place(0,-1,0))
 def test_occupied(self):
  g=a.Puzzle();g.grid[2][2]=1;g.offer=[(((0,0),),0)];self.assertFalse(g.place(0,2,2))
 def test_row_clear(self):
  g=a.Puzzle();g.grid[0]=[0]*8;g.grid[0][7]=None;g.offer=[(((0,0),),0)]
  self.assertTrue(g.place(0,0,7));self.assertEqual(g.score,101);self.assertTrue(all(v is None for v in g.grid[0]))
 def test_col_clear(self):
  g=a.Puzzle()
  for y in range(8):g.grid[y][3]=0
  g.grid[7][3]=None;g.offer=[(((0,0),),0)]
  self.assertTrue(g.place(0,7,3));self.assertTrue(all(g.grid[y][3] is None for y in range(8)))
 def test_multi_clear(self):
  g=a.Puzzle();g.grid[0]=[0]*8;g.grid[0][0]=None
  for y in range(8):g.grid[y][0]=g.grid[y][0] if y==0 else 1
  g.grid[0][0]=None;g.offer=[(((0,0),),0)]
  sc=g.score;g.place(0,0,0);self.assertEqual(g.score-sc,1+100*2+50*2)
 def test_refill(self):
  g=a.Puzzle(2);g.offer=[(((0,0),),0)];g.place(0,0,0);self.assertEqual(len(g.offer),3)
 def test_over(self):
  g=a.Puzzle(3)
  for y in range(8):
   for x in range(8):g.grid[y][x]=0 if (x+y)%2==0 else None  # checkerboard: no full line, no adjacent empties
  g.refill=lambda:g.offer.extend([(((0,0),(0,1)),0) for _ in range(3)])  # deterministic: only 1x2 pieces
  g.offer=[(((0,0),),0)]
  self.assertTrue(g.place(0,0,1))
  self.assertTrue(g.over)  # refilled with 1x2 pieces; no two adjacent empty cells
 def test_fits(self):
  g=a.Puzzle()
  for y in range(8):
   for x in range(8):g.grid[y][x]=0
  self.assertFalse(g.fits_anywhere(((0,0),)))
 def test_record(self):
  with tempfile.TemporaryDirectory() as d,patch.object(a,'RECORD',Path(d)/'best.json'):
   self.assertTrue(a.save(500));a.save(2);self.assertEqual(a.best(),500)
 def test_frame(self):
  import sprites
  self.assertIn('38;2;',sprites.frame(a.Puzzle(1),4,2,2,3,0,0,0))
 def test_shapes(self):
  for shape in a.SHAPES:
   self.assertTrue(all(y>=0 and x>=0 for y,x in shape));self.assertEqual(len(shape),len(set(shape)))
if __name__=='__main__':unittest.main()
