module AOC.Y2018.D18 where

import           AOC.Y2018.D00                            ( arrayFromAA
                                                , adj8
                                                , countIf
                                                )
import           Control.Arrow
import           Control.Monad
import           Data.Array
import           Data.Function
import           Data.Ix
import           Data.Maybe
import           Data.List
import qualified Data.Array                    as A
import Debug.Trace

data Acre = T | L | O deriving (Eq, Show)

type YX = (Int, Int)
type Field = Array YX Acre

p1' :: Field -> Int
p1' = iterate nextF >>> (!! 10) >>> (liftM2 (*) (countIf (== L)) (countIf (== T)))

p1 :: String -> Int
p1 = p1' . (arrayFromAA toAcre)

p2' :: Field -> Int
p2' f = decycle nextF f 1000000000 & (liftM2 (*) (countIf (== L)) (countIf (== T)))

p2 :: String -> Int
p2 = p2' . (arrayFromAA toAcre)

t :: IO ()
t = do
    s <- readFile "data/18.txt"
    let f  = (arrayFromAA toAcre) s
    let fs = iterate nextF f
    mapM_
        print
        (take 1000 $ zip [0 ..] $ map
            (liftM2 (,) (countIf (== L)) (countIf (== T)))
            fs
        )

toAcre :: Char -> Acre
toAcre '#' = L
toAcre '|' = T
toAcre _   = O

nextA :: Field -> YX -> Acre
nextA f yx =
    let a = map (f !) $ filter (inRange (bounds f)) $ adj8 yx
    in  case f ! yx of
            T -> if (countIf (== L) a) >= 3 then L else T
            O -> if (countIf (== T) a) >= 3 then T else O
            L -> if any (== L) a && any (== T) a then L else O

nextF :: Field -> Field
nextF f = array (bounds f) $ ap (,) (nextA f) <$> indices f

decycle :: Eq a => (a -> a) -> a -> Int -> a
decycle f a n =
    let
        as         = iterate f a
        as'        = fst $ foldr (\a ~(x, y) -> (a : y, x)) ([], []) as
        (i, a0, _) = fromJust $ find (\(i, x, y) -> x == y) $ zip3
            [1 ..]
            (tail as)
            (tail as')
    in
        as !! (if n <= i then n else i + (n - i) `mod` i)
