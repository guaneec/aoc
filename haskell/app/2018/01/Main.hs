module Main where

import AOC.Common
import AOC.Y2018.D01

main :: IO ()
main = do
    f <- getInput 2018 1
    print $ p1 f
    print $ p2 f
