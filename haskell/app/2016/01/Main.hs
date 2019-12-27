module Main where

import           AOC.Common

import           Data.Set                       ( Set )
import qualified Data.Set                      as Set
import           Data.List.Split
import           Data.Function
import           Data.Foldable
import           Data.Monoid
import           Debug.Trace

dist :: YX -> Int
dist (y, x) = abs y + abs x

p1 :: String -> Int
p1 s = s & wordsBy (`elem` ", ") & foldr f ((1, 0), (0, 0)) & snd & dist
  where
    f (lr : ints) ((dy, dx), (y, x)) = ((dy', dx'), (i * dy + y, i * dx + x))
      where
        (dy', dx') = if lr == 'L' then (dx, -dy) else (-dx, dy)
        i          = read ints

p2 :: String -> Int
p2 s =
    s
        & wordsBy (`elem` ", ")
        & foldl' f ((1, 0), ((0, 0), Set.singleton (0, 0), First Nothing))
        & (\(_, (_, _, First (Just a))) -> dist a)
  where
    f ((dy, dx), ((y, x), s, rep)) (lr : ints) =
        ((dy', dx'), foldl' g ((y, x), s, rep) [1, 2 .. i])
      where
        g ((y, x), s, rep) _ =
            let yx' = (y + dy', x + dx')
            in  ( yx'
                , Set.insert yx' s
                , rep <> First (if Set.member yx' s then Just yx' else Nothing)
                )

        (dy', dx') = if lr == 'L' then (dx, -dy) else (-dx, dy)
        i          = read ints

main :: IO ()
main = do
    f <- getInput 2016 1
    print $ p1 f
    print $ p2 f
