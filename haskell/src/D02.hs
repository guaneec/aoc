module D02 where

import           Data.Functor
import           Data.Function
import           Data.Map                       ( Map )
import qualified Data.Map                      as Map
import           Data.Foldable
import           Data.Char
import           Data.Maybe

p1 :: String -> Int
p1 s =
    let com  = s & pp & makeCom & pa1202
        com' = until halted step com
    in  com' & memory & (Map.! 0)

p2 :: String -> Maybe Int
p2 s = f $ (,) <$> [0 .. 99] <*> [0 .. 99]
  where
    f nvs = (\(n, v) -> 100 * n + v) <$> find g nvs
    g (n, v) =
        let com  = s & pp & makeCom & panv n v
            com' = until halted step com
        in  com' & memory & (Map.! 0) & (== 19690720)

data Computer = Computer {
    memory :: Map Int Int,
    ip :: Int,
    halted :: Bool
} deriving (Show)


pp :: String -> [Int]
pp "" = []
pp s =
    let (d, nd) = span isDigit s
    in  (read d) : (pp $ dropWhile (not . isDigit) nd)


ops :: Int -> Computer -> Computer
ops 1 c@(Computer m i _) =
    let i  = ip c
        r1 = (m Map.!) . (m Map.!) $ (i + 1)
        r2 = (m Map.!) . (m Map.!) $ (i + 2)
        r3 = m Map.! (i + 3)
        m' = Map.insert r3 (r1 + r2) m
    in  Computer m' (i + 4) False

ops 2 c@(Computer m i _) =
    let i  = ip c
        r1 = (m Map.!) . (m Map.!) $ (i + 1)
        r2 = (m Map.!) . (m Map.!) $ (i + 2)
        r3 = m Map.! (i + 3)
        m' = Map.insert r3 (r1 * r2) m
    in  Computer m' (i + 4) False

ops 99 c = c { halted = True }

step :: Computer -> Computer
step c@(Computer m i _) = ops (m Map.! i) c


makeCom :: [Int] -> Computer
makeCom code = Computer (Map.fromAscList (zip [0 ..] code)) 0 False

pa1202 :: Computer -> Computer
pa1202 c = c { memory = memory c & Map.insert 1 12 & Map.insert 2 2 }


panv :: Int -> Int -> Computer -> Computer
panv n v c = c { memory = memory c & Map.insert 1 n & Map.insert 2 v }
