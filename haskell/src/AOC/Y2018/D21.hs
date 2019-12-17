module AOC.Y2018.D21 where
import           Data.Function
import           Data.Foldable
import           Data.Maybe
import           Data.Char
import           Control.Arrow
import           Data.Containers.ListUtils
import           Data.List                     as L
import           Data.List.Lens
import           Data.Set                       ( Set )
import qualified Data.Set                      as Set
import           Data.Map                       ( Map )
import qualified Data.Map                      as Map
import           Data.Bits
import           Control.Lens
import           Control.Monad.State
import           Debug.Trace
import           Text.Megaparsec         hiding ( State )
import           Text.Megaparsec.Char
import qualified Text.Megaparsec.Char.Lexer    as L
import           Data.Void


p1 :: String -> Integer
p1 _ = snd $ g (65536, 11469373)



p2 :: String -> Integer
p2 _ =
    let (_ : h, l) = dord g (65536, 11469373) in lastUniq $ fmap snd $ (h ++ l)


f :: (Integer, Integer) -> (Integer, Integer)
f (r3, r4) =
    let (r3', r4') =
                if 256 > r3 then (r4 .|. 65536, 3730679) else (r3 `div` 256, r4)
    in  ( r3'
        , (r4' + (r3' .&. 255)) & (.&. 16777215) & (* 65899) & (.&. 16777215)
        )
g (a, b) = let (c, d) = f (a, b) in if c < 256 then (c, d) else g (c, d)

d :: Eq a => (a -> a) -> a -> ([a], [a])
d f a =
    let
        as         = iterate f a
        as'        = fst $ foldr (\a ~(x, y) -> (a : y, x)) ([], []) as
        (i, a0, _) = fromJust $ find (\(i, x, y) -> x == y) $ zip3
            [1 ..]
            (tail as)
            (tail as')
        (h, (t : ts)) = span (/= a0) as
    in
        (h, t : (takeWhile (/= a0) ts))

dord :: Ord a => (a -> a) -> a -> ([a], [a])
dord f a =
    let as            = iterate f a
        ss            = scanl (flip Set.insert) Set.empty as
        l             = length $ takeWhile (uncurry Set.notMember) $ zip as ss
        a0            = as !! l
        (h, (t : ts)) = span (/= a0) as
    in  (h, t : (takeWhile (/= a0) ts))

decr :: Ord a => [a] -> [a]
decr []       = []
decr (x : xs) = x : (decr $ filter (< x) xs)


lastUniq :: Ord a => [a] -> a
lastUniq l =
    let ss = scanl (flip Set.insert) Set.empty l
    in  fst $ last $ takeWhile (uncurry Set.notMember) $ zip l ss
