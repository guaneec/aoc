module AOC.Common where 

import Text.Printf
import System.Directory

getInput :: Int -> Int -> IO String
getInput year day = readFile (printf "../data/%d/%02d.input.txt" year day)
