module AOC.Y2018.D17 where
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

type Parser = Parsec Void String

data Tile = Clay | Sand | Flowing | Still deriving (Show, Eq)
type XY = (Int, Int)
data Board = Board { clay :: Set XY, flowing :: Set XY , still :: Set XY} deriving Show


d :: IO ()
d = do
    f <- readFile "data/17.txt"
    let b = pp f
    let (maxx, maxy) =
            liftM2 (,) maximum minimum $ map snd $ Set.toList $ clay b
    let b' = execState (flow maxy DDown (500, 1)) b
    print (length (clay b'), length (clay b))
    show (toList $ clay b') & writeFile "clay.txt"
    show (toList $ flowing b') & writeFile "flowing.txt"
    show (toList $ still b') & writeFile "still.txt"

pp :: String -> Board
pp s =
    parseMaybe mpf s
        & fromJust
        & concatMap (\(x1, y1, x2, y2) -> (,) <$> [x1 .. x2] <*> [y1 .. y2])
        & Set.fromList
        & \s -> Board s Set.empty Set.empty

p1' :: Board -> Int
p1' b =
    let (maxy, miny) =
                liftM2 (,) maximum minimum $ map snd $ Set.toList $ clay b
        b' = execState (flow maxy DDown (500, 1)) b
        f  = flowing b' & toList & filter (\x -> (snd x) >= miny)
    in  length f + length (still b')

p1 :: String -> Int
p1 = p1' . pp

p2' :: Board -> Int
p2' b =
    let maxy = maximum $ map snd $ Set.toList $ clay b
        b'   = execState (flow maxy DDown (500, 1)) b
    in  length (still b')

p2 :: String -> Int
p2 = p2' . pp


tileAt :: Board -> XY -> Tile
tileAt b xy | xy `Set.member` (still b)   = Still
            | xy `Set.member` (flowing b) = Flowing
            | xy `Set.member` (clay b)    = Clay
            | otherwise                   = Sand

blocked :: Board -> XY -> Bool
blocked b xy = tileAt b xy `elem` [Clay, Still]

data Direction = DDown | DLeft | DRight deriving (Show, Eq)

flow :: Int -> Direction -> XY -> State Board Bool
flow n dir (x, y) = do
    b <- get
    if blocked b (x, y) -- || (traceShow ("flow", x, y) False)
        then return True
        else if y > n
            then return False
            else do
                if (tileAt b (x, y) == Flowing)
                    then return False
                    else do
                        d   <- flow n DDown (x, y + 1)
                        out <- if not d
                            then return False
                            else do
                                l <- if dir /= DRight
                                    then flow n DLeft (x - 1, y)
                                    else return True
                                r <- if dir /= DLeft
                                    then flow n DRight (x + 1, y)
                                    else return True
                                return $ l && r
                        if out && dir == DDown then freeze (x, y) else return ()
                        if dir == DDown && not out
                            then if d
                                then cover DDown (x, y)
                                else
                                    modify
                                        (\b -> b
                                            { flowing = Set.insert
                                                            (x, y)
                                                            (flowing b)
                                            }
                                        )
                            else return ()
                        return out

freeze :: XY -> State Board ()
freeze (x, y) = do
    return () -- &  traceShow ("freeze", x, y)
    b <- get
    let
        f = \x ->
            ( x
            & map (\x -> (x, y))
            & takeWhile (not . (blocked b))
            & mapM
                  (\xy ->
                      modify (\b -> b { still = Set.insert xy (still b) })
                  )
            )
    f [x ..]
    f [x - 1, x - 2 ..]
    return ()

cover :: Direction -> XY -> State Board ()
cover d (x, y) = do
    b <- get
    if (blocked b (x, y))
        then return ()
        else do
            return () -- & traceShow ("cover", x, y)
            modify (\b -> b { flowing = Set.insert (x, y) (flowing b) })
            if (not (blocked b (x, y + 1)))
                then return ()
                else do
                    if (d == DDown || d == DRight)
                        then cover DRight (x + 1, y)
                        else return ()
                    if (d == DDown || d == DLeft)
                        then cover DLeft (x - 1, y)
                        else return ()



mp :: Parser (Int, Int, Int, Int)
mp = do
    xy <- single 'x' <|> single 'y'
    single '='
    i0 <- L.decimal
    string ", "
    single (if xy == 'x' then 'y' else 'x')
    single '='
    i1 <- L.decimal
    string ".."
    i2 <- L.decimal
    return (if xy == 'x' then (i0, i1, i0, i2) else (i1, i0, i2, i0))

mpf = mp `sepEndBy` space
