module D02 where

import           Data.Functor
import           Data.Function
import           Data.Map                       ( Map )
import qualified Data.Map                      as Map
import           Data.Foldable
import           Data.Char
import           Data.Maybe
import Machine

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


pp :: String -> [Int]
pp "" = []
pp s =
    let (d, nd) = span isDigit s
    in  (read d) : (pp $ dropWhile (not . isDigit) nd)



pa1202 :: Computer -> Computer
pa1202 c = c { memory = memory c & Map.insert 1 12 & Map.insert 2 2 }


panv :: Int -> Int -> Computer -> Computer
panv n v c = c { memory = memory c & Map.insert 1 n & Map.insert 2 v }
