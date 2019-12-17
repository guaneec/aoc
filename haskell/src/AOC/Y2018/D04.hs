module AOC.Y2018.D04 where

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


data Action = Sleep | Wake | Shift Int deriving (Show)



getAction :: String -> Action
getAction "wakes up"     = Wake
getAction "falls asleep" = Sleep
getAction s              = Shift $ read $ takeWhile isDigit $ drop 7 $ s

parseLine :: String -> (UTCTime, Action)
parseLine s =
    ( s
        & drop 1
        & take 16
        & parseTimeM False defaultTimeLocale "%Y-%m-%d %H:%M"
        & fromJust
    , getAction (drop 19 s)
    )

tDiff a b = realToFrac $ nominalDiffTimeToSeconds $ diffUTCTime a b

consume (guards, i, t0) (t, Sleep) = (guards, i, t)
consume (guards, i, t0) (t, Wake) =
    (Map.insertWith (+) i (tDiff t t0) guards, i, t)
consume (guards, i, t0) (_, (Shift ii)) = (guards, ii, t0)

minCounts t0 t1 =
    let
        (UTCTime d0 dt0) = t0
        (UTCTime d1 dt1) = t1
        m0 =
            (diffTimeToPicoseconds dt0)
            `div` 60
            `div` 1000000000000
            &     fromInteger :: Int
        m1 =
            ((toModifiedJulianDay d1) - (toModifiedJulianDay d0))
            *     24
            *     60
            +     (diffTimeToPicoseconds dt1)
            `div` 60
            `div` 1000000000000
            &     fromInteger :: Int
        mm0 = m0 `rem` 60
        mm1 = m1 `rem` 60
    in
        [ (i, ((fromEnum (i >= mm0)) + (fromEnum (i < mm1)))) | i <- [0 .. 59] ]

cl
    :: Int
    -> (Array Int Int, Bool, UTCTime)
    -> (UTCTime, Action)
    -> (Array Int Int, Bool, UTCTime)
cl i (freqs, isi , t0) (_, (Shift ii)) = (freqs, i == ii, t0)
cl _ (freqs, True, t0) (t, Sleep     ) = (freqs, True, t)
cl _ (freqs, True, t0) (t, Wake) = (accum (+) freqs (minCounts t0 t), True, t)
cl _ acc               _               = acc

getFreq entries i =
    let t0            = parseTimeOrError False defaultTimeLocale "%Y" "2000"
        (freqs, _, _) = entries & foldl'
            (cl i)
            ( array (0, 59) [ (i, 0) | i <- [0 .. 59] ] :: Array Int Int
            , False
            , t0
            )
    in  last $ sortOn snd $ assocs freqs


preproc :: String -> [(UTCTime, Action)]
preproc s = s & lines & sort & map parseLine

p1 :: String -> Int
p1 s = 
    let
        entries = preproc s
        t0 = fst $ head entries
        (guardsTotalSleep, _, _) = foldl' consume (Map.empty, 0, t0) entries
        mostSleptGuard = Map.assocs guardsTotalSleep & sortOn (negate . snd) & head & fst
    in (fst $ getFreq entries mostSleptGuard) * mostSleptGuard

p2 :: String -> Int
p2 s =
    let
        entries = preproc s
        guards  = Map.empty :: Map.Map Int Double
        t0 = fst $ head entries
        is      = entries & foldl' consume (guards, 0, t0) & \(g, j, t) ->
            g & Map.keys
    in
        (\(i, (m, f)) -> i * m) $ head $ reverse $ sortOn
            (\(i, (m, f)) -> f)
            [ (i, getFreq entries i) | i <- is ]



