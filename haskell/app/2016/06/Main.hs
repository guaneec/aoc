module Main where

import           AOC.Common
import           Data.List
import           Data.Functor
import           Control.Arrow
import           Data.Function
import           Data.List.Split
import           Data.Char
import           Data.Ord
import           Data.Map                       ( Map )
import qualified Data.Map                      as Map

main :: IO ()
main = do
    s <- getInput 2016 6
    putStrLn 
        $   lines s
        &   transpose
        <&> (histogram >>> Map.assocs >>> maximumBy (comparing snd) >>> fst)
    putStrLn 
        $   lines s
        &   transpose
        <&> (histogram >>> Map.assocs >>> minimumBy (comparing snd) >>> fst)
    return ()
