module AOC.Y2018.D01 where
import           Data.Function
import qualified Data.Set                      as Set

readSigned :: String -> Int
readSigned ('-' : n) = -read n
readSigned ('+' : n) = read n

getNums s = lines s & filter (not . null) & map readSigned

firstRepeat :: Ord a => [a] -> a
firstRepeat l =
    let sets = scanl (flip Set.insert) (Set.empty) l
    in  fst $ head $ dropWhile (uncurry Set.notMember) $ zip l sets

p1 :: String -> Int
p1 = sum . getNums

p2 :: String -> Int
p2 s = firstRepeat $ scanl (+) 0 $ cycle $ getNums s
