module D01 where

import Data.Functor
import Data.Function

p1 :: String -> Int
p1 s = s & lines <&> read <&> fuel & sum

p2 :: String -> Int
p2 s = s & lines <&> read <&> realFuel & sum

fuel :: Int -> Int
fuel x = x `div` 3 - 2

realFuel :: Int -> Int
realFuel x = if f <= 0 then 0 else f + realFuel f where f = fuel x
