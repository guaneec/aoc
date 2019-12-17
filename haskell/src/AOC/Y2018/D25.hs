module AOC.Y2018.D25 where
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
import           Linear.V4

type I4 = V4 Int

type S = (Int, Map I4 Int, Set I4)

d :: I4 -> I4 -> Int
d (V4 x y z t) (V4 x' y' z' t') =
    abs (x - x') + abs (y - y') + abs (z - z') + abs (t - t')

adjs :: [I4] -> I4 -> [I4]
adjs ps p = filter (\p' -> d p p' <= 3) ps

tagNext :: S -> S
tagNext s@(i, tags, untouched)
    | Set.null untouched
    = s
    | otherwise
    = let (v, us'') = Set.deleteFindMin untouched
          vs        = adjs (Set.toList untouched) v & Set.fromList
          us'       = foldl' (flip Set.delete) us'' vs
          f (ts, us, vs) =
                  let (v, vs'') = Set.deleteFindMin vs
                      us'       = foldl' (flip Set.delete) us vs
                      vs'       = adjs (Set.toList us') v
                  in (Map.insert v i ts, us', foldl' (flip Set.insert) vs'' vs')
          (ts, us, _) = until (Set.null . (view _3)) f (tags, us', vs)
      in  (i + 1, ts, us)

t :: IO ()
t = do
    f <- readFile "data/25.txt"
    let ps = fromJust $ parseMaybe parser f
    let s =  (0, Map.empty :: Map I4 Int, Set.fromList ps)
    let s'@(i,t,u) = until (Set.null . (view _3)) tagNext s
    print i
    return ()

type Parser = Parsec Void String
parser :: Parser [I4]
parser = pl `sepEndBy` space <* eof
  where
    pl = V4 <$> sd <* char ',' <*> sd <* char ',' <*> sd <* char ',' <*> sd
    sd = L.signed space L.decimal
