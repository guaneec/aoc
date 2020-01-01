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
import           Data.Bits

tf '1' = True
tf '0' = False

weave :: [a] -> [a] -> [a]
weave l1 l2 = concatMap (\(a, b) -> [a, b]) $ zip l1 l2

drag :: [Bool]
drag = f <$> [(1 :: Int) ..]
  where f n = (/= 0) $ (.&. n) $ (`shiftL` 1) $ n .&. (-n)

drags l =
  concat $ weave (cycle [l, map not $ reverse l]) (map (\x -> [x]) $ drag)

fromba :: String -> [Bool]
fromba = map tf . takeWhile isDigit

toba :: [Bool] -> String
toba = concatMap (show . fromEnum)

checksum :: [Bool] -> String
checksum l = toba $ if b == 1 then l else map (foldl' (/=) True) (chunksOf b l)
 where
  (_, b) = until (odd . fst) (\(a, b) -> (a `div` 2, b * 2)) (length l, 1)

main :: IO ()
main = do
  s <- fromba <$> getInput 2016 16
  putStrLn $ checksum $ take 272 $ drags s
  putStrLn $ checksum $ take 35651584 $ drags s
  return ()
