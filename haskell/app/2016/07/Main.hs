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

abba :: String -> Bool
abba [a, b, c, d] = c == b && d == a && a /= b
abba _            = False

sb :: String -> ([String], [String])
sb = sb' [] []
  where
    sb' o i "" = (o, i)
    sb' o i ('[' : s) =
        let (h , t ) = span (/= ']') s
            (o', i') = sb' o i (tail t)
        in  (o', h : i')
    sb' o i s =
        let (h , t ) = span (/= '[') s
            (o', i') = sb' o i t
        in  (h : o', i')

tls :: String -> Bool
tls s = any abba4 o && not (any abba4 i)
  where
    (o, i) = sb s
    abba4 x = any abba (divvy 4 1 x)

ssl :: String -> Bool
ssl s = not . Set.null $ Set.intersection aba bab  where
    (o, i) = sb s
    abas s = filter (\[a, b, c] -> a == c && a /= b) (divvy 3 1 s)
    aba = Set.fromList $ map (take 2) $ concatMap abas o
    bab = Set.fromList $ map (drop 1) $ concatMap abas i

main :: IO ()
main = do
    s <- getInput 2016 7
    print $ countIf tls $ lines s
    print $ countIf ssl $ lines s
    return ()
