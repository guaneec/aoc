module AOC.Y2019.D07 where

import Data.Functor
import Data.Function
import Data.Foldable
import Data.List
import Data.Ord

import AOC.Y2019.Machine


p1 s = maximum $ f <$> permutations [0..4]
    where
        m = makeCom (pp s)
        f = foldl' (\o i -> runInput (i:o) m) [0]

p2 s = maximum $ f <$> permutations [5..9]
    where
        m = makeCom (pp s)
        g xs = fmap (\x -> [x]) xs & (\(x:xs) -> xs ++ [x ++ [0]])
        f y = let
            x = foldl (\acc inp -> inp ++ runInput acc m) x (g y)
            in last x

pp :: String -> [Int]
pp f = read $ "[" ++ f ++ "]"
