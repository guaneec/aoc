module AOC.Y2019.D05 where

import           Data.Functor
import           Data.Function
import           AOC.Y2019.Machine


pp :: String -> [Int]
pp f = read $ "[" ++ f ++ "]"

p1 :: String -> Int
p1 s = runInput [1] (makeCom $ pp s) & last

p2 :: String -> Int
p2 s = runInput [5] (makeCom $ pp s) & last
