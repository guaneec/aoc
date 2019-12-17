module AOC.Y2018.D19 where
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
import           Control.Monad
import           Control.Monad.State
import           Debug.Trace
import           Text.Megaparsec         hiding ( State )
import           Text.Megaparsec.Char
import qualified Text.Megaparsec.Char.Lexer    as L
import           Data.Void
import           Data.Vector                    ( Vector
                                                , (!?)
                                                )
import qualified Data.Vector                   as V

import           AOC.Y2018.D16                            ( ops )

type Parser = Parsec Void String

p1' :: (Int, Vector [Int]) -> Int
p1' (ip, p) =
    let f = step ip p
    in  head $ last $ unfoldr (\r -> (,) <$> f r <*> f r) (replicate 6 0)

p1 :: String -> Int
p1 = p1' . pp



p2' :: (Int, Vector [Int]) -> Int
p2' (ip, p) =
    let f = step ip p
    in  head $ last $ unfoldr (\r -> (,) <$> f r <*> f r) [1, 0, 0, 0, 0, 0]

p2 :: String -> Int
p2 = p2' . pp

toCode :: String -> Int
toCode s = fromJust $ L.findIndex
    (== s)
    [ "addr"
    , "addi"
    , "mulr"
    , "muli"
    , "banr"
    , "bani"
    , "borr"
    , "bori"
    , "setr"
    , "seti"
    , "gtir"
    , "gtri"
    , "gtrr"
    , "eqir"
    , "eqri"
    , "eqrr"
    ]

step :: Int -> Vector [Int] -> [Int] -> Maybe [Int]
step ip p regs =
    let ins = p !? (regs !! ip)
    in  case ins of
            Nothing -> Nothing
            Just [o, a, b, c] ->
                Just $ (ops !! o) a b c regs & over (ix ip) succ


mxn :: Monad m => Int -> (a -> m a) -> (a -> m a)
mxn n f = foldr (>=>) return (replicate n f)

t :: IO ()
t = do
    f <- readFile "data/19.txt"
    let (ip, p) = pp f
    let r       = 1 : (replicate 5 0)
    let f       = step ip p
    mapM print $ take 100 $  unfoldr (\r -> (,) <$> f r <*> f r) r
    return ()

pp :: String -> (Int, Vector [Int])
pp s = s & parseMaybe ps & fromJust

pins :: Parser [Int]
pins = do
    s <- (many letterChar)
    space
    a <- L.decimal
    space
    b <- L.decimal
    space
    c <- L.decimal
    return ([toCode s, a, b, c])

ps :: Parser (Int, Vector [Int])
ps = do
    string "#ip" >> space
    ip <- L.decimal
    space
    is <- pins `sepEndBy` space1
    return (ip, V.fromList is)
