module AOC.Y2018.D23 where
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
import           Data.Functor
import           Data.Ord
import           AOC.Y2018.D00                            ( countIf )

type Parser = Parsec Void String
type Sphere = (XYZ, Int)
type XYZ = (Int, Int, Int)

data RNode = RL [R4] | RNL [RNode]

pairs xs = zip xs (tail xs)

p1 :: String -> Int
p1 s =
    s
        & parseMaybe parser
        & fromJust
        & ap (,) (maximumBy (comparing snd))
        & (\(bots, (xyz, r)) -> countIf (\(xyz', _) -> d xyz xyz' <= r) bots)


p2' :: () -> ()
p2' = id

p2 :: String -> ()
p2 _ = ()

t = do
    f <- readFile "data/23.txt"
    let bots = fromJust $ parseMaybe parser f
        pois = pairs bots & concatMap (uncurry poi)
        mp = maximumBy (comparing (\p -> countIf (inSp p) bots)) pois
        in print (mp, d mp (0,0,0))
    return ()

d (x, y, z) (x', y', z') = abs (x - x') + abs (y - y') + abs (z - z')


type STUV = (Int, Int, Int, Int)
type R4 = (STUV, STUV)

fromXYZ :: XYZ -> STUV
fromXYZ (x, y, z) = (x + y + z, x + y - z, x - y + z, x - y - z)

sp :: Sphere -> [XYZ]
sp ((x, y, z), r) =
    [ (x + r, y    , z)
    , (x - r, y    , z)
    , (x    , y + r, z)
    , (x    , y - r, z)
    , (x    , y    , z + r)
    , (x    , y    , z - r)
    ]


inSp :: XYZ  -> Sphere -> Bool
inSp p' (p, r) = (d p p') <= r

fromSp :: Sphere -> R4
fromSp ((x, y, z), r) = (fromXYZ (x - r, y, z), fromXYZ (x + r + 1, y, z))

goodR4 :: R4 -> Bool
goodR4 ((s1, t1, u1, v1), (s2, t2, u2, v2)) =
    s1 < s2 && t1 < t2 && u1 < u2 && v1 < v2

inR4 :: XYZ -> R4 -> Bool
inR4 xyz ((s1, t1, u1, v1), (s2, t2, u2, v2)) =
    let (s, t, u, v) = fromXYZ xyz
    in  (  (s1 <= s && s < s2)
        && (t1 <= t && t < t2)
        && (u1 <= u && u < u2)
        && (v1 <= v && v < v2)
        )

cut4 :: R4 -> R4 -> [R4]
cut4 ((s1, t1, u1, v1), (s2, t2, u2, v2)) ((s1', t1', u1', v1'), (s2', t2', u2', v2'))
    = [ ((s1, t1, u1, v1)    , (s1', t2, u2, v2))
      , ((s2', t1, u1, v1)   , (s2, t2, u2, v2))
      , ((s1', t1, u1, v1)   , (s2', t1', u2, v2))
      , ((s1', t2', u1, v1)  , (s2', t2, u2, v2))
      , ((s1', t1', u1, v1)  , (s2', t2', u1', v2))
      , ((s1', t1', u2', v1) , (s2', t2', u2, v2))
      , ((s1', t1', u1', v1) , (s2', t2', u2', v1'))
      , ((s1', t1', u1', v2'), (s2', t2', u2', v2))
      ]
        & filter goodR4

sect4 :: R4 -> R4 -> ([R4], [R4], [R4])
sect4 r@((s1, t1, u1, v1), (s2, t2, u2, v2)) r'@((s1', t1', u1', v1'), (s2', t2', u2', v2'))
    = let ru =
                  ( (max s1 s1', max t1 t1', max u1 u1', max v1 v1')
                  , (min s2 s2', min t2 t2', min u2 u2', min v2 v2')
                  )
      in  if goodR4 ru then (cut4 r ru, [ru], cut4 r' ru) else ([r], [], [r'])

poi :: Sphere -> Sphere -> [XYZ]
poi s@(p@(x,y,z),r) s'@(p'@(x',y',z'), r') 
    | z > z' = poi s' s
    | otherwise = 
    let 
        a = (r + r' - d p p') `div` 2
        fromUv (u, v) = ((u + v) `div` 2, (u - v) `div` 2)
        fromXy (x, y) = (x + y, x - y)
        poi2 (x, y, r) (x', y', r') = if abs (x-x') + abs (y-y') > r + r' then [] else  let
            (u1, v1) = fromXy (x-r, y)
            (u2, v2) = fromXy (x+r, y)
            (u1', v1') = fromXy (x'-r', y')
            (u2', v2') = fromXy (x'+r', y')
            maxu = max u1 u1'
            minu = min u2 u2'
            maxv = max v1 v1'
            minv = min v2 v2'
             in  [
                (maxu, maxv),
                (minu, minv),
                (minu, maxv),
                (maxu, minv)
            ] <&> fromUv
        s | z + r >= z' + r' = [z-r, z, z+r, z'-r', z', z'+r']
          | otherwise = [z - a, z, z', z' + a]
        in s & concatMap (\zz -> (\(x,y) -> (x,y,zz)) <$> poi2 (x, y, r - abs (z-zz)) (x', y', r' - abs (z' -zz ))) & filter (\pp -> (d p pp == r) || (d p' pp == r')) & nub

parser :: Parser [(XYZ, Int)]
parser =
    many
            (do
                string "pos=<"
                x <- L.signed space L.decimal
                char ','
                y <- L.signed space L.decimal
                char ','
                z <- L.signed space L.decimal
                string ">, r="
                r <- L.signed space L.decimal
                space
                return ((x, y, z), r)
            )
        <* eof
