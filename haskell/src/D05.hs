module D05 where

import           Data.Functor
import           Data.Function
import           Machine


pp :: String -> [Int]
pp f = read $ "[" ++ f ++ "]"

p1 :: String -> Int
p1 s = runInput [1] (makeCom $ pp s) & last

p2 :: String -> Int
p2 s = runInput [5] (makeCom $ pp s) & last
