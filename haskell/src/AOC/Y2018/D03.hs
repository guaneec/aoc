module AOC.Y2018.D03 where

import           Text.Read
import           Data.Function
import           Data.List
import qualified Data.Set                      as Set
import qualified Data.Map                      as Map
import           Text.Regex.TDFA
import           Data.Array.Unboxed
import           Data.Time.Calendar
import           Data.Time.Format
import           Data.Time.Clock
import           Data.Maybe
import           Data.Char
import qualified Data.Vector.Unboxed           as V
import           Data.List.Split
import           Debug.Trace
import           Control.Monad.State
import           Data.Void

data Rect = Rect {
    x :: Int,
    y :: Int,
    w :: Int,
    h :: Int
}

data CRect = CRect {
    x1 :: Int,
    x2 :: Int,
    y1 :: Int,
    y2 :: Int
} deriving (Show)

rc (Rect x y w h) = (CRect x (x + w) y (y + h))


parseLine :: String -> (Int, Rect)
parseLine s =
    ( (read (g !! 0) :: Int)
    , Rect (read (g !! 1) :: Int)
           (read (g !! 2) :: Int)
           (read (g !! 3) :: Int)
           (read (g !! 4) :: Int)
    )
  where
    (_, _, _, g) =
        s =~ "#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)" :: ( String
            , String
            , String
            , [String]
            )



boundsr :: [CRect] -> CRect
boundsr = foldl1'
    (\(CRect ax1 ax2 ay1 ay2) (CRect x1 x2 y1 y2) ->
        (CRect (min ax1 x1) (max ax2 x2) (min ay1 y1) (max ay2 y2))
    )
-- 3.b

preproc :: String -> [(Int, CRect)]
preproc s =
    s & lines & filter (not . null) & map parseLine & map (\(x, r) -> (x, rc r))

p2 :: String -> [Int]
p2 s =
    let idrects             = preproc s
        ids                 = map fst idrects
        idSet               = Set.fromAscList ids
        rects               = map snd idrects
        (CRect x1 x2 y1 y2) = boundsr rects
        a =
                (array
                    ((0, 0), (x2 - x1, y2 - y1))
                    [ ((i, j), 0) | i <- [0 .. x2 - x1], j <- [0 .. y2 - y1] ] :: UArray
                        (Int, Int)
                        Int
                )
        (lonelies, _) = foldl'
            (\(s, counter) (id, (CRect rx1 rx2 ry1 ry2)) ->
                let coords =
                            [ (i, j)
                            | i <- [rx1 - x1 .. rx2 - 1 - x1]
                            , j <- [ry1 - y1 .. ry2 - 1 - y1]
                            ]
                    (newset, pairs, flag) = foldl'
                        (\(ss, pp, ff) coord ->
                            let c = counter ! coord
                            in  (Set.delete c ss, (coord, id) : pp, ff || c > 0)
                        )
                        (s, [], False)
                        coords
                in  ( if flag then (Set.delete id newset) else newset
                    , counter // pairs
                    )
            )
            (idSet, a)
            (zip ids rects)
    in  Set.toList lonelies


p1 :: String -> Int
p1 s =
    let idrects             = preproc s
        rects               = map snd idrects
        (CRect x1 x2 y1 y2) = boundsr rects
        a =
                (array
                    ((0, 0), (x2 - x1, y2 - y1))
                    [ ((i, j), 0) | i <- [0 .. x2 - x1], j <- [0 .. y2 - y1] ] :: UArray
                        (Int, Int)
                        Int
                )
        b = foldl'
            (\counter (CRect rx1 rx2 ry1 ry2) ->
                (  counter
                // [ ((i, j), (1 + counter ! (i, j)))
                   | i <- [rx1 - x1 .. rx2 - 1 - x1]
                   , j <- [ry1 - y1 .. ry2 - 1 - y1]
                   ] 
                )
            )
            a
            rects
    in  foldl' (\acc e -> (acc + (fromEnum $ e > 1))) 0 (elems b)
