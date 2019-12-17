module Main where

import AOC.Common
import AOC.Y2019.D02

main :: IO ()
main = do
    f <- getInput 2019 2
    print $ p1 f
    print $ p2 f
