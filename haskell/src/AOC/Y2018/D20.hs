module AOC.Y2018.D20 where
import           Data.Function
import           Data.Foldable
import           Data.Maybe
import           Data.Char
import           Control.Arrow
import           Data.Containers.ListUtils
import           Data.Ord
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
import           Data.Tree
import           AOC.Y2018.D00                            ( adj4 )
import           Data.Graph

type Parser = Parsec Void String
data E = E [O] deriving Show
data O = OS String | OO [E] deriving Show
type YX = (Int, Int)

p1' :: E -> Int
p1' e =
    let (v0, g) = ge e
        [t]     = dfs g [v0]
    in  height t

p1 :: String -> Int
p1 s = parseMaybe pr s & fromJust & p1'



p2' :: E -> Int
p2' e =
    let (v0, g) = ge e
        [t]     = dfs g [v0]
        h n (Node v ts) s = if n == 0 then s else foldr (h (n-1)) (Set.delete v s) ts
        s = Set.fromAscList (vertices g)
    in  length $ h 1000 t s

p2 :: String -> Int
p2 s = parseMaybe pr s & fromJust & p2'

ge e = (v0, g)  where
    (vs, es) = foo e (Set.singleton (0, 0), Set.empty)
    vall     = Set.toList es & concatMap (\(e1, e2) -> [e1, e2]) & Set.fromList
    es'      = es & Set.toAscList & groupBy (\x y -> fst x == fst y) & map
        (\es@((v1, _) : _) -> (v1, v1, map snd es))
    (g, nfv, vfk) = graphFromEdges es'
    v0            = fromJust $ vfk (0, 0)

go :: Char -> YX -> YX
go c (y, x) = case c of
    'N' -> (y - 1, x)
    'S' -> (y + 1, x)
    'E' -> (y, x + 1)
    'W' -> (y, x - 1)


height :: Tree a -> Int
height (Node _ []) = 0
height (Node _ ts) = 1 + (maximum $ height <$> ts)

t = do
    let s = "^(SSS|EEESSSWWW)ENNES$"
    print $ p1 s



type S = (Set YX, Set (YX, YX))
foo :: E -> S -> S
foo (E os) (vs, es) = foldl' g1 (vs, es) os  where
    g1 (vs, es) (OS s) = foldr (g4 s) (Set.empty, es) vs
    g1 (vs, es) (OO oes) =
        let (vss, ess) = unzip $ ($ (vs, es)) <$> (map foo oes)
        in  (Set.unions vss, Set.unions ess)
    g2 s yx = foldl' g3 (yx, []) s
    g3 (yx, l) c = let yx' = go c yx in (yx', (yx, yx') : (yx', yx) : l)
    g4 s yx (vs, es) =
        let (yx', l) = g2 s yx in (Set.insert yx' vs, foldr Set.insert es l)



parserToks :: Parser O
parserToks = do
    s <- some (oneOf "NSEW")
    return $ OS s

parserParen :: Parser O
parserParen = do
    single '('
    t <- (try parserE <|> (return $ E [])) `sepBy` (single '|')
    single ')'
    return $ OO t

parserE :: Parser E
parserE = do
    s <- many (try parserParen <|> try parserToks)
    return $ E s

pr :: Parser E
pr = char '^' *> parserE <* char '$' <* space <* eof
