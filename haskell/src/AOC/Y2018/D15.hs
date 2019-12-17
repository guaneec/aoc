module AOC.Y2018.D15 where
import           Data.Function
import           Data.Foldable
import           Data.Maybe
import           Data.Char
import           Control.Arrow
import           Data.Containers.ListUtils
import           Data.List                     as L
import           Data.Set                       ( Set )
import qualified Data.Set                      as Set
import           Data.Map                       ( Map )
import qualified Data.Map                      as Map
import           Control.Lens
import           Debug.Trace

type YX = (Int, Int)
data Actor = Actor { hp :: Int, atk :: Int, isElf :: Bool } deriving Show
data World = World { actors :: Map YX Actor, tiles :: Set YX } deriving Show
type Game = (World, [YX], Int)


enumerate :: [a] -> [(Int, a)]
enumerate = zip [0 ..]

enum2D :: [[a]] -> [((Int, Int), a)]
enum2D = (concatMap g) . (map f) . enumerate
 where
  f (i, x) = (i, enumerate x)
  h i (j, x) = ((i, j), x)
  g (i, jxs) = map (h i) jxs

adjs :: YX -> [YX]
adjs (y, x) = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]

actorAt :: World -> YX -> Actor
actorAt w xy = actors w & Map.lookup xy & fromJust

isNone :: World -> YX -> Bool
isNone (World a t) c = (Set.member c t) && (Map.notMember c a)

-- 
flood
  :: Ord a
  => Show a
  => (YX -> Bool)
  -> (YX -> Bool)
  -> (Set YX)
  -> [(YX, a)]
  -> Maybe a
flood _ _ _ [] = Nothing
flood islegal isend visited seeds =
  let f yx = islegal yx && (Set.notMember yx visited)
      g (yx, a) = map (\yx -> (yx, a)) $ filter f $ adjs yx
      seeds'   = seeds & concatMap g & sort & nubOrdOn fst
      ends     = filter (isend . fst) seeds & sort
      visited' = foldl' (flip Set.insert) visited (map fst $ toList seeds')
  in  if null ends
        then flood islegal isend visited' seeds'
        else Just (snd $ head ends)


-- where to move next
move :: World -> YX -> Maybe YX
move w yx =
  let ie = isElf $ fromJust $ Map.lookup yx $ actors w
      ends =
          actors w
            & Map.assocs
            & filter (\(_, a) -> ie /= isElf a)
            & map fst
            & concatMap adjs
            & Set.fromList
      f x = (x, x)
  in  flood (isNone w)
            (`Set.member` ends)
            (Set.singleton yx)
            (map f $ filter (isNone w) $ (adjs yx))


preproc1 s = preproc s 3

preproc :: String -> Int -> World
preproc s i = s & lines & enum2D & foldl' wa e
 where
  e = (World Map.empty Set.empty)
  wa (World a n) (yx, 'E') =
    World (Map.insert yx (Actor 200 i True) a) (Set.insert yx n)
  wa (World a n) (yx, 'G') =
    World (Map.insert yx (Actor 200 3 False) a) (Set.insert yx n)
  wa (World a n) (yx, '.') = World a (Set.insert yx n)
  wa w           _         = w

tickAttack :: Game -> YX -> YX -> Game
tickAttack (w, yxs, i) c0 c1 =
  let me  = actorAt w c0
      him = actorAt w c1
      hp' = hp him - atk me
  in  if hp' > 0
        then
          let him' = (Actor (hp') (atk him) (isElf him))
              w'   = World (actors w & Map.insert c1 him') (tiles w)
          in  (w', yxs, i)
        else
          let yxs' = delete c1 yxs
              w'   = World (Map.delete c1 (actors w)) (tiles w)
          in  (w', yxs', i)

dg (w, _, i) = trace
  (  "\n"
  ++ showGame w (0, 0) (9, 9)
  ++ ( show
     $ ( i + 1
       , (toList >>> map hp >>> sum) $ actors w
       , length $ actors w
       , actors w & toList & map hp
       )
     )
  )

tick :: Game -> Game
tick (w, [], i) = (w, yxs, i + 1)
  where yxs = Set.toAscList $ Map.keysSet $ actors w
tick (w, yx : yxs, i) =
  let
    a = actors w & Map.lookup yx & fromJust
    f w a yx =
      actors w
        & Map.assocs
        & filter (\(yx', a') -> yx' `elem` adjs yx && (isElf a /= isElf a'))
        & sortOn (\(yx', a') -> (hp a', yx'))
    es     = f w a yx
    target = fst $ head es
  in
    if not (null es)
      then tickAttack (w, yxs, i) yx target
      else
        let yx' = move w yx
        in
          case yx' of
            Nothing -> (w, yxs, i)
            Just j ->
              let w' = World (actors w & Map.delete yx & Map.insert j a)
                             (tiles w)
                  a'     = actors w' & Map.lookup j & fromJust
                  es'    = f w' a j
                  target = fst $ head es'
              in  if (null es')
                    then (w', yxs, i)
                    else tickAttack (w', yxs, i) j target



gameOver :: Game -> Bool
gameOver (w, _, _) =
  actors w & Map.elems & (\x -> all isElf x || not (any isElf x))

score :: Game -> Int
score (w, l, n) = (n + fromEnum (null l)) * (getHpSum $ actors w)
  where getHpSum = Map.elems >>> map hp >>> sum

countElf :: World -> Int
countElf w = Map.elems (actors w) & filter isElf & length

elvesWin :: (Int -> World) -> Int -> Bool
elvesWin makeworld n =
  let w0 = makeworld n
      n0 = countElf w0
  in  (\w -> countElf w == n0) $ view _1 $ fromJust $ find gameOver $ iterate
        tick
        (w0, [], -1)


findInt :: (Int -> Bool) -> Int -> Int
findInt f l = if f l then l else findInt f (l + 1)


gc w yx = case a of
  Just (Actor _ _ False) -> 'G'
  Just (Actor _ _ True ) -> 'E'
  Nothing                -> if Set.member yx (tiles w) then '.' else '#'
  where a = Map.lookup yx (actors w)

showGame :: World -> YX -> YX -> String
showGame w (y0, x0) (y1, x1) =
  [ [ gc w (y, x) | x <- [x0 .. x1] ] | y <- [y0 .. y1] ] & unlines

endGame :: World -> Game
endGame w = fromJust $ find gameOver $ iterate tick (w, [], -1)

p1' :: World -> Int
p1' w = score $ endGame w

p1 :: String -> Int
p1 = p1' . preproc1

p2' :: (Int -> World) -> Int
p2' mw =
  let a = findInt (elvesWin mw) 4 in score $ endGame $ mw a

p2 :: String -> Int
p2 = p2' . preproc
