module Main where

import           AOC.Common
import           Data.List
import           Data.Function
import           Data.List.Split

good :: [Int] -> Bool
good v@[a, b, c] = a' + b' > c' where [a', b', c'] = sort v

main :: IO ()
main = do
    nums <- map (map read . words) . lines <$> getInput 2016 3 :: IO [[Int]]
    print $ countIf good nums
    print $ nums & chunksOf 3 & map transpose & map (countIf good) & sum

