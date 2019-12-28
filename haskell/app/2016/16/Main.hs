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

tf '1' = True
tf '0' = False

drag :: [Bool] -> [Bool]
drag [] = []
drag l = l ++ dt l
  where dt l = let o = False:(map not $ reverse l) in o ++ dt (l ++ o)

fromba :: String -> [Bool]
fromba = map tf . takeWhile isDigit

toba :: [Bool] -> String
toba = concatMap (show . fromEnum)

checksum :: [Bool] -> String
checksum l | length l `mod` 2 == 1 = toba l
           | otherwise = checksum $ map (\[a,b] -> a == b) (chunksOf 2 l)

main :: IO ()
main = do
  s <- fromba <$> getInput 2016 16
  putStrLn $ checksum $ take 272 $ drag s
  putStrLn $ checksum $ take 35651584 $ drag s
  return ()
