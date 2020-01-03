module Main where

import AOC.Common
import Data.Char
import Data.List

react :: String -> String
react = go ""
    where 
        go (a:b:xs) ys | abs (ord a - ord b) == abs (ord 'a' - ord 'A') = go xs ys
        go xs (y:ys) = go (y:xs) ys
        go xs "" = reverse xs


main :: IO ()
main = do
    f <- takeWhile (not . isSpace) <$> getInput 2018 5
    print $ length $ react f
    let chars = nub $ toLower <$> f 
    print $ minimum $ map (length . react) $ map (\x -> filter (\y -> toLower y /= x) f) chars
