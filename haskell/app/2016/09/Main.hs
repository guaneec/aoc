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
import           Data.Set                       ( Set )
import qualified Data.Set                      as Set

dlen :: String -> Int
dlen ""        = 0
dlen ('(' : s) = a * b + dlen (drop a t)
  where
    (h, ')' : t) = span (/= ')') s
    [a, b      ] = map read $ splitOn "x" h
dlen s = length h + dlen t where (h, t) = span (/= '(') s

dlen2 :: String -> Int
dlen2 ""        = 0
dlen2 ('(' : s) = if length t < a
    then error "expansion exceeds substring"
    else b * (dlen2 $ take a t) + dlen2 (drop a t)
  where
    (h, ')' : t) = span (/= ')') s
    [a, b      ] = map read $ splitOn "x" h
dlen2 s = length h + dlen2 t where (h, t) = span (/= '(') s

main :: IO ()
main = do
    s <- takeWhile (not . isSpace) <$> getInput 2016 9
    print $ dlen s
    print $ dlen2 s
