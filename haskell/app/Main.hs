module Main where

import Text.Printf
import Control.Arrow
import System.Environment

import qualified D01 (p1, p2)
import qualified D02 (p1, p2)

pns :: [Int]
pns = [1..2]

parts :: Int -> [String -> String]
parts 1 = [show . D01.p1, show . D01.p2]
parts 2 = [show . D02.p1, show . D02.p2]


getInput :: Int -> IO String
getInput n = readFile $ printf "../data/%02d.input.txt" n

runDay :: Int -> IO ()
runDay n = do
    f <- getInput n
    printf "Day %02d:\n" n
    mapM_ putStrLn $ map ($ f) (parts n)
    putChar '\n'


main :: IO ()
main = do
    days' <- fmap read <$> getArgs
    let days = if null days' then pns else days'
    mapM_ runDay days
    return ()
