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
import           Data.Bifunctor
import           Control.Monad
import           Data.Maybe
import           Crypto.Hash
import           Crypto.Hash.Algorithms
import           Data.ByteString.Char8          ( pack )

md5 :: String -> String
md5 s = show (hash . pack $ s :: Digest MD5)

md52016 :: String -> String
md52016 s = iterate md5 s !! 2017

hashes :: String -> (String -> String) -> [String]
hashes salt f = map (\x -> f $ salt ++ show x) [0 ..]

trips :: String -> Set Char
trips s = divvy 3 1 s & map f & catMaybes & take 1 & Set.fromList
  where
    f [a, b, c] | a == b && b == c = Just a
                | otherwise        = Nothing


quints :: String -> Set Char
quints s = divvy 5 1 s & map f & catMaybes & Set.fromList
  where
    f v@[a, b, c, d, e] | all (== a) (tail v) = Just a
                        | otherwise           = Nothing

l5 = (map quints .) . hashes
l3 = (map trips .) . hashes

otp salt hf = zip3 [0..] (l3 salt hf) (tail $ divvy 1000 1 (l5 salt hf)) & filter f & map (\(i, _, _) -> i)
    where f (_, t, qs) = any (\q -> not $ Set.null (t `Set.intersection` q)) qs


main :: IO ()
main = do
    s <- takeWhile (not . isSpace) <$> getInput 2016 14
    print $ otp s md5 !! 63
    print $ otp s md52016 !! 63
    return ()

