module Main where

import D01 (p1, p2)

main :: IO ()
main = do
    f <- readFile "../data/01.input.txt"
    print $ p1 f
    print $ p2 f
