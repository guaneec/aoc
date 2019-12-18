{-# LANGUAGE TupleSections #-}

module Main where

import           AOC.Common
import           Data.Set                       ( Set )
import qualified Data.Set                      as Set
import           Data.Map                       ( Map )
import qualified Data.Map                      as Map
import qualified Data.IntPSQ                   as PQ
import           Data.List
import           Debug.Trace
import           Data.Function
import           Data.Char

s = "#################\n#i.G..c...e..H.p#\n########.########\n#j.A..b...f..D.o#\n########@########\n#k.E..a...g..B.n#\n########.########\n#l.F..d...h..C.m#\n#################"


main :: IO ()
main = do
    f <- getInput 2019 18
    let vault = Map.fromList $ enum2D $ lines f
    let Just (entrance, _) = Map.toList vault & find ((=='@') . snd)
    let nKeys = countIf isLower f
    print entrance
    print $ dij (entrance, Set.empty) (neighborKey vault) & find (\(_, (_, s)) -> Set.size s == nKeys)
    return ()


neighborStep :: Map YX Char -> Set Char -> YX -> [(Int, YX)]
neighborStep vault keys yx = if isNewKey vault keys yx then [] else yx & adj4 & filter good & map (1,)
  where 
    good x = Map.member x vault && c /= '#' && not
        (isUpper c && Set.notMember (toLower c) keys)
        where c = vault Map.! x

type Vault = Map YX Char
type Keys = Set Char
type Node = (YX, Set Char)



isNewKey :: Vault -> Keys -> YX -> Bool
isNewKey vault keys yx = let k = vault Map.! yx in isLower k && Set.notMember k keys 

neighborKey :: Map YX Char -> Node -> [(Int, Node)]
neighborKey vault (yx, keys) = 
    dij yx (neighborStep vault keys)
    & filter (isNewKey vault keys . snd)
    & map f
    where f (d, yx) = (d, (yx, Set.insert (vault Map.! yx) keys))

dij :: Ord a => a -> (a -> [(Int, a)]) -> [(Int, a)]
dij n0 f =
    let
        q0 = PQ.singleton 0 0 n0
        m0 = Map.singleton n0 0
        g (q, dist, i)
            | PQ.null q = Nothing
            | otherwise = Just ((d0, n), foldr ff (q', dist, i) (f n))
          where
            Just (_, d, n, q') = PQ.minView q
            d0                 = dist Map.! n
            ff (d', n') s@(q, dist, i) = if Map.member n' dist && dPrev <= dNew
                then s
                else (PQ.insert i dNew n' q, Map.insert n' dNew dist, i + 1)
              where
                dPrev = dist Map.! n'
                dNew  = d' + d
    in
        unfoldr g (q0, m0, 1)

-- f null = Nothing
-- f q = a, q'
