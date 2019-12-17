module AOC.Y2018.D02 where
import           Data.Function
import qualified Data.Map                      as Map
import           Data.List
import           Data.Maybe




has23 :: String -> (Bool, Bool)
has23 s =
    foldr (\v (h2, h3) -> (h2 || (v == 2), h3 || (v == 3))) (False, False)
        $ foldl' (\s c -> Map.insertWith (+) c 1 s) Map.empty
        $ s

pairs :: [a] -> [(a, a)]
pairs l = [ (x, y) | (x : ys) <- tails l, y <- ys ]

dist :: String -> String -> (String, Int)
dist = dist' ("", 0)

dist' :: (String, Int) -> String -> String -> (String, Int)
dist' i      "" "" = i
dist' (s, 2) _  _  = (s, 2)
dist' (s, i) (a : as) (b : bs) =
    let ss = s ++ (if a == b then [a] else "")
        ii = fromEnum (a /= b) + i
    in  dist' (ss, ii) as bs


preproc :: String -> [String]
preproc = lines


p1 :: String -> Int
p1 s =
    preproc s
        & map has23
        & foldl'
              (\(a2, a3) (h2, h3) -> (a2 + fromEnum h2, a3 + fromEnum h3))
              (0, 0)
        & uncurry (*)

p2 :: String -> String
p2 s =
    preproc s
        & pairs
        & map (\x -> (x, (uncurry dist x)))
        & find (\(_, (s, d)) -> d == 1)
        & fromJust
        & snd
        & fst
