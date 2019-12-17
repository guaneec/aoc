module AOC.Y2018.D22 where
import           Data.Function
import           Data.Foldable
import           Data.Maybe
import           Data.Char
import           Control.Arrow
import           Data.Containers.ListUtils
import           Data.List                     as L
import           Data.List.Lens
import           Data.Set                       ( Set )
import qualified Data.Set                      as Set
import           Data.Map                       ( Map )
import qualified Data.Map                      as Map
import           Data.Bits
import           Control.Lens
import           Control.Monad.State
import           Debug.Trace
import           Text.Megaparsec         hiding ( State )
import           Text.Megaparsec.Char
import qualified Text.Megaparsec.Char.Lexer    as L
import           Data.Void
import           Data.MemoTrie
import qualified Data.OrdPSQ                   as PQ
import           Data.OrdPSQ                    ( OrdPSQ )

import AOC.Y2018.D00 (adj4)

p1' :: () -> ()
p1' = id

p1 :: String -> Int
p1 _ = sum $ (`mod` 3) <$> el <$> ((,) <$> [0 .. 778] <*> [0 .. 14])



p2' :: () -> ()
p2' = id

p2 :: Int
p2 =  evalState pathDist (let p = (0,0,I) in (PQ.singleton p (h p) (), Map.singleton p 0))


data G = O | I | T deriving (Show, Enum, Ord, Eq)
type P3 = (Int, Int, G)
type S = (OrdPSQ P3 Int (), Map P3 Int)

d :: P3 -> P3 -> Int
d (y1, x1, e1) (y2, x2, e2) = abs (y1 - y2) + abs (x1 - x2) + 7 * fromEnum (e1 /= e2)

h :: P3 -> Int
h (y, x, _) = abs (fst yx - y) + abs (snd yx - x)

adjs :: P3 -> [P3]
adjs p@(y,x,e) = adj4 (y,x) 
    & map (\(y, x) -> (y,x,e))
    & (\l -> (y,x,O):(y,x,I):(y,x,T):l )
    & filter (\p'@(y, x, e) -> y>=0 && x >= 0 && (rt (y,x) /= e) && p' /= p)

pathDist :: State S Int
pathDist = do
    (pq, gs) <- get
    let v@(p, f, _) = fromJust $ PQ.findMin pq
    let g = (Map.!) gs p
    -- traceShow (p, f, g) $ return ()
    if p == (fst yx, snd yx, I) then return g else do        
        forM (adjs p) (\n -> do
            let 
                g' = Map.lookup n gs
                gNew = g + d n p
                in if (isJust g' && gNew >= fromJust g') then return () else do
                    modify (over _1 $ PQ.insert n (gNew + h n) ())
                    modify (over _2 $ Map.insert n gNew))
        modify (over _1 $ PQ.delete p)
        pathDist






depth = 11541
yx = (778, 14)

-- depth = 510
-- yx = (10, 10)


rt :: (Int, Int) -> G
rt yx = [O,I,T] !! (el yx `mod` 3)

el :: (Int, Int) -> Int
el = memo el' where el' (y, x) = (gi (y, x) + depth) `mod` 20183

gi :: (Int, Int) -> Int
gi = memo gi'  where
    gi' (y, x) | yx == (y, x) || (y, x) == (0, 0) = 0
               | x == 0                           = y * 48271
               | y == 0                           = x * 16807
               | otherwise = (el (y - 1, x)) * (el (y, x - 1))

