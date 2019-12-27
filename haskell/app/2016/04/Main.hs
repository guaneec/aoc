module Main where

import           AOC.Common
import           Data.List
import           Data.Function
import           Data.List.Split
import           Data.Char
import           Data.Ord
import           Data.Map                       ( Map )
import qualified Data.Map                      as Map

data Room = Room {
    name :: String,
    sid :: Int,
    checksum :: String
    } deriving Show

parse :: String -> Room
parse s = Room a (read c) (d & drop 1 & take 5)
  where
    (a, b) = break isDigit s
    (c, d) = break (== '[') b

real :: Room -> Bool
real Room { name = s, checksum = cs } =
    Map.assocs h & sortOn (\(k, v) -> (Down v, k)) & map fst & take 5 & (== cs)
    where h = histogram $ filter isLower s

rot :: Int -> Char -> Char
rot i c = let a = ord 'a' in chr $ (ord c + i - a) `mod` 26 + a

decrypt :: Room -> Room
decrypt r = r
    { name =
        map
            (\c -> (if isLower c then rot $ (sid r) `mod` 26 else const ' ') c)
            (name r)
    }

main :: IO ()
main = do
    rooms <- map parse . lines <$> getInput 2016 4
    print $ rooms & filter real & map sid & sum
    print $ sid . head $ filter (\r -> "north" `isInfixOf` (name r)) $ map
        decrypt
        rooms
    return ()
