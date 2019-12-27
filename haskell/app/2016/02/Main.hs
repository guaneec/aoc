module Main where

import           AOC.Common

import           Data.Set                       ( Set )
import qualified Data.Set                      as Set
import           Data.List.Split
import           Data.Function
import           Data.Foldable
import           Data.Monoid
import           Debug.Trace

f :: Char -> YX -> YX
f 'U' (y, x) = (y - 1, x)
f 'D' (y, x) = (y + 1, x)
f 'L' (y, x) = (y, x - 1)
f 'R' (y, x) = (y, x + 1)

f1 :: Char -> YX -> YX
f1 d = f d `but` (\(y, x) -> y `elem` [0 .. 2] && x `elem` [0 .. 2])

f2 :: Char -> YX -> YX
f2 d = f d `but` (\(y, x) -> abs y + abs x <= 2)

toKey :: YX -> Int
toKey (y, x) = 3 * y + x + 1

toKey2 :: YX -> Char
toKey2 (-2, 0 ) = '1'
toKey2 (-1, -1) = '2'
toKey2 (-1, 0 ) = '3'
toKey2 (-1, 1 ) = '4'
toKey2 (0 , -2) = '5'
toKey2 (0 , -1) = '6'
toKey2 (0 , 0 ) = '7'
toKey2 (0 , 1 ) = '8'
toKey2 (0 , 2 ) = '9'
toKey2 (1 , -1) = 'A'
toKey2 (1 , 0 ) = 'B'
toKey2 (1 , 1 ) = 'C'
toKey2 (2 , 0 ) = 'D'

but :: (a -> a) -> (a -> Bool) -> a -> a
but f p x = let x' = f x in if p x' then x' else x

main :: IO ()
main = do
    ls <- filter (not . null) . lines <$> getInput 2016 2
    putStrLn $ fmap (head . show . toKey) $ tail $ scanl (foldl' (flip f1))
                                                         (1, 1)
                                                         ls
    putStrLn $ fmap toKey2 $ tail $ scanl (foldl' (flip f2)) (0, -2) ls
