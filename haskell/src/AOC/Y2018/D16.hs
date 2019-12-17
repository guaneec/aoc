module AOC.Y2018.D16 where
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
import           Debug.Trace
import           Text.ParserCombinators.ReadP


data OpLog = OpLog { before :: [Int], after::[Int], code :: [Int] } deriving Show
type Regs = [Int]
type Op = Int -> Int -> Int -> Regs -> Regs

pp1 :: String -> [OpLog]
pp1 s = readP_to_S pf s & head & fst & fst

tryop :: OpLog -> Op -> Bool
tryop l@(OpLog b a c) op = op (c !! 1) (c !! 2) (c !! 3) b == a

p1' :: [OpLog] -> Int
p1' = map f >>> filter (>= 3) >>> length
  where f log = filter (tryop log) ops & length

p1 :: String -> Int
p1 = p1' . pp1

pp2 :: String -> ([OpLog], [Int])
pp2 = readP_to_S pf >>> head >>> fst

p2' :: ([OpLog], [Int]) -> Int
p2' (logs, p) =  head $ runProgram (solveOps logs) p

p2 :: String -> Int
p2 = p2' . pp2


-- operations


addr :: Op
addr a b c regs = regs & ix c .~ (regs !! a + regs !! b)
addi :: Op
addi a b c regs = regs & ix c .~ (regs !! a + b)
mulr :: Op
mulr a b c regs = regs & ix c .~ (regs !! a * regs !! b)
muli :: Op
muli a b c regs = regs & ix c .~ (regs !! a * b)
banr :: Op
banr a b c regs = regs & ix c .~ (regs !! a .&. regs !! b)
bani :: Op
bani a b c regs = regs & ix c .~ (regs !! a .&. b)
borr :: Op
borr a b c regs = regs & ix c .~ (regs !! a .|. regs !! b)
bori :: Op
bori a b c regs = regs & ix c .~ (regs !! a .|. b)
setr :: Op
setr a _ c regs = regs & ix c .~ regs !! a
seti :: Op
seti a _ c regs = regs & ix c .~ a
gtir :: Op
gtir a b c regs = regs & ix c .~ fromEnum (a > regs !! b)
gtri :: Op
gtri a b c regs = regs & ix c .~ fromEnum (regs !! a > b)
gtrr :: Op
gtrr a b c regs = regs & ix c .~ fromEnum (regs !! a > regs !! b)
eqir :: Op
eqir a b c regs = regs & ix c .~ fromEnum (a == regs !! b)
eqri :: Op
eqri a b c regs = regs & ix c .~ fromEnum (regs !! a == b)
eqrr :: Op
eqrr a b c regs = regs & ix c .~ fromEnum (regs !! a == regs !! b)

ops :: [Op]
ops =
  [ addr
  , addi
  , mulr
  , muli
  , banr
  , bani
  , borr
  , bori
  , setr
  , seti
  , gtir
  , gtri
  , gtrr
  , eqir
  , eqri
  , eqrr
  ]

solveOps :: [OpLog] -> [Op]
solveOps logs =
  let m = foldl' (flip Set.delete)
                 (Set.fromList $ (,) <$> [0 .. 15] <*> [0 .. 15])
                 l'
      l' = concatMap g logs
      g l = map (\i -> (i, (head $ code l)))
        $ filter (\i -> not $ tryop l (ops !! i)) [0 .. 15]
      is = shake m
  in  (ops !!) <$> is

runProgram :: [Op] -> [Int] -> [Int]
runProgram ops program = r ops program [0, 0, 0, 0]
 where
  r ops []                  regs = regs
  r ops (o : a : b : c : p) regs = r ops p ((ops !! o) a b c regs)

histogram :: Ord a => [a] -> Map a Int
histogram = Map.fromListWith (+) . (`zip` repeat 1)

shake :: Set (Int, Int) -> [Int]
shake s = shake' s []

shake' :: Set (Int, Int) -> [(Int, Int)] -> [Int]
shake' s acc | Set.null s = acc & nubOrd & sortOn snd & map fst
shake' s acc =
  let ls    = Set.toList s
      freqx = histogram $ map fst ls
      freqy = histogram $ map snd ls
      onexs = Map.assocs freqx & filter ((1 ==) . snd) & map fst
      oneys = Map.assocs freqy & filter ((1 ==) . snd) & map fst
      xx    = ls & filter (\e -> (fst e `elem` onexs))
      yy    = ls & filter (\e -> (snd e `elem` oneys))
      s'    = Set.filter
        (\(x0, y0) ->
          not (any (\(_, y) -> y == y0) xx) && not (any (\(x, _) -> x == x0) xx)
        )
        s
  in  shake' s' (xx ++ yy ++ acc)


-- parsing stuff

num :: ReadP Int
num = do
  v <- many1 (satisfy isDigit)
  return (read v)

numcs :: ReadP [Int]
numcs = do
  char '['
  v <- sepBy num commas
  char ']'
  return v

commas :: ReadP ()
commas = do
  skipSpaces
  char ','
  skipSpaces

bef :: ReadP [Int]
bef = do
  string "Before:"
  skipSpaces
  numcs

aft = do
  string "After:"
  skipSpaces
  numcs

plog :: ReadP OpLog
plog = do
  b <- bef
  skipSpaces
  c <- num `sepBy` (skipMany1 (satisfy isSpace))
  skipSpaces
  a <- aft
  return (OpLog b a c)

pf :: ReadP ([OpLog], [Int])
pf = do
  logs <- plog `sepBy` skipSpaces
  skipSpaces
  program <- num `sepBy` (skipMany1 (satisfy isSpace))
  skipSpaces
  eof
  return (logs, program)
