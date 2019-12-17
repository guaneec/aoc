module AOC.Y2018.D14 where
import           Data.Function
import           Data.Foldable
import           Data.Maybe
import           Data.Char
import           Data.List                     as L
import qualified Data.Set                      as Set
import           Data.Sequence                 as S

preproc1 = read :: (String -> Int)

preproc2 :: String -> [Int]
preproc2 s = read <$> pure <$> L.filter (not . isSpace) s

type S a = (Seq a, Int, Int)

infixl 5 ||>
(||>) :: Foldable f => Seq a -> f a -> Seq a
(||>) s l = foldl (|>) s l


step :: S Int -> S Int
step (s, i, j) =
    let x  = fromJust $ s !? i
        y  = fromJust $ s !? j
        ds = digits $ x + y
        s' = s ||> ds
        l  = S.length s'
        i' = (x + i + 1) `mod` l
        j' = (y + j + 1) `mod` l
    in  (s', i', j')

digits :: Int -> [Int]
digits i = read <$> pure <$> show i

s0 = (fromList [3, 7], 0, 1)

p1' :: Int -> String
p1' n =
    iterate step s0
        & map (\(s, _, _) -> s)
        & find (\s -> S.length s > n + 10)
        & fromJust
        & toList
        & L.drop n
        & L.take 10
        & map show
        & concat

p1 :: String -> String
p1 = p1' . preproc1

takeR :: Int -> Seq a -> Seq a
takeR i s = S.drop (max 0 $ S.length s - i) s

p2' :: [Int] -> Int
p2' ds =
    let ln = L.length ds
    in  iterate step s0
            & map (\(s, _, _) -> s)
            & map
                  (\s ->
                      let l  = S.length s
                          p  = toList $ takeR ln s
                          p' = toList $ S.take ln $ takeR (ln + 1) s
                      in  if p' == ds
                              then Just (l - ln - 1)
                              else if p == ds then Just (l - ln) else Nothing
                  )
            & catMaybes
            & head


p2 :: String -> Int
p2 = p2' . preproc2
