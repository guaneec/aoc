module AOC.Common where 

import Text.Printf
import System.Directory
import Data.Array
import Data.Foldable
import Data.Map (Map)
import qualified  Data.Map as Map

getInput :: Int -> Int -> IO String
getInput year day = readFile (printf "../data/%d/%02d.input.txt" year day)

type YX = (Int, Int)

enumerate :: [a] -> [(Int, a)]
enumerate = zip [0 ..]

enum2D :: [[a]] -> [(YX, a)]
enum2D = (concatMap g) . (map f) . enumerate
  where
    f (i, x) = (i, enumerate x)
    h i (j, x) = ((i, j), x)
    g (i, jxs) = map (h i) jxs

arrayFromAA :: (Char -> a) -> String -> Array YX a
arrayFromAA f s =
    let ls = lines s
        n0 = length ls
        n1 = length $ head ls
    in  array ((0, 0), (n0 - 1, n1 - 1)) $ (\(i, e) -> (i, f e)) <$> enum2D ls



adj4 :: YX -> [YX]
adj4 (y, x) = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]


adj8 :: YX -> [YX]
adj8 (y, x) =
    (y + 1, x + 1)
        : (y - 1, x - 1)
        : (y - 1, x + 1)
        : (y + 1, x - 1)
        : (adj4 (y, x))

countIf :: Foldable t => (a -> Bool) -> t a -> Int
countIf f = length . (filter f) . toList

histogram :: Ord a => [a] -> Map a Int
histogram = Map.fromListWith (+) . (`zip` repeat 1)
