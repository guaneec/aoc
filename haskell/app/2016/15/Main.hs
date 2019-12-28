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

dropi :: Int -> [a] -> [a]
dropi i l = take i l ++ drop (i + 1) l

parse :: String -> [[Integer]]
parse s = map (dropi 2 . map read . wordsBy (not . isDigit)) . lines $ s

modInv :: Integer -> Integer -> Integer
modInv a n = go 0 1 n a
 where
  go t nt r 0  = if r > 1 then error "no inv" else (t + n) `rem` n
  go t nt r nr = go nt (t - q * nt) nr (r - q * nr) where q = r `div` nr

solve :: [[Integer]] -> Integer
solve discs = (`mod` pp) $ sum $ map
  (\(k, p) -> let a = pp `div` p in modInv a p * a * (p - k))
  ds
 where
  pp = product $ map snd ds
  ds = map (\[a, b, c] -> (a + c, b)) discs

main :: IO ()
main = do
  discs <- parse <$> getInput 2016 15
  print $ solve $ discs
  let d = [fromIntegral $ 1 + length discs, 11, 0]
  print $ solve $ d : discs
  return ()
