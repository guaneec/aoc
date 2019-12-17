module AOC.Y2019.Machine where

import           Data.Map                       ( Map )
import qualified Data.Map                      as Map
import           Data.Functor
import           Data.Function
import           Data.Foldable
import           Data.Maybe

data Computer = Computer {
    memory :: Map Int Int,
    ip :: Int,
    halted :: Bool,
    input :: [Int],
    output :: [Int]
} deriving (Show)


step :: Computer -> Computer
step c@(Computer { memory = m, ip = i }) = ops (parseop $ m Map.! i) c


stepio :: Computer -> (Maybe Int, Computer)
stepio c =
    let o@(op : m1 : _) = parseop $ memory c Map.! (ip c)
        g 3 c@Computer { ip = i, memory = m, input = (i0 : is) } =
                ( Nothing
                , c { ip     = i + 2
                    , memory = Map.insert (comlv c m1 (i + 1)) i0 m
                    , input  = is
                    }
                )
        g 4 c@Computer { ip = i, memory = m } =
                (Just $ comrv c m1 (i + 1), c { ip = i + 2 })
        g _ c@Computer { ip = i, memory = m } = (Nothing, step c)
    in  g op c


makeCom :: [Int] -> Computer
makeCom code = Computer { memory = (Map.fromAscList (zip [0 ..] code))
                        , ip     = 0
                        , halted = False
                        , input  = []
                        , output = []
                        }

parseop :: Int -> [Int]
parseop o =
    [ o `mod` 100
    , o `div` 100 `mod` 10
    , o `div` 1000 `mod` 10
    , o `div` 10000 `mod` 10
    ]

comrv :: Computer -> Int -> Int -> Int
comrv c 0 v = (memory c) Map.! (memory c Map.! v)
comrv c 1 v = (memory c) Map.! v

comlv :: Computer -> Int -> Int -> Int
comlv c 0 v = (memory c) Map.! v

ops :: [Int] -> Computer -> Computer
ops [1, m1, m2, m3] c@(Computer { memory = m, ip = i }) =
    let i  = ip c
        r1 = comrv c m1 $ i + 1
        r2 = comrv c m2 $ i + 2
        r3 = comlv c m3 $ i + 3
        m' = Map.insert r3 (r1 + r2) m
    in  c { memory = m', ip = i + 4 }

ops [2, m1, m2, m3] c@(Computer { memory = m, ip = i }) =
    let i  = ip c
        r1 = comrv c m1 $ i + 1
        r2 = comrv c m2 $ i + 2
        r3 = comlv c m3 $ i + 3
        m' = Map.insert r3 (r1 * r2) m
    in  c { memory = m', ip = i + 4 }

ops [5, m1, m2, m3] c@(Computer { ip = i }) =
    let r1 = comrv c m1 $ i + 1
        r2 = comrv c m2 $ i + 2
    in  c { ip = if r1 /= 0 then r2 else i + 3 }

ops [6, m1, m2, m3] c@(Computer { ip = i }) =
    let r1 = comrv c m1 $ i + 1
        r2 = comrv c m2 $ i + 2
    in  c { ip = if r1 == 0 then r2 else i + 3 }

ops [7, m1, m2, m3] c@(Computer { memory = m, ip = i }) =
    let r1 = comrv c m1 $ i + 1
        r2 = comrv c m2 $ i + 2
        r3 = comlv c m3 $ i + 3
    in  c { memory = Map.insert r3 (fromEnum (r1 < r2)) $ m, ip = i + 4 }

ops [8, m1, m2, m3] c@(Computer { memory = m, ip = i }) =
    let r1 = comrv c m1 $ i + 1
        r2 = comrv c m2 $ i + 2
        r3 = comlv c m3 $ i + 3
    in  c { memory = Map.insert r3 (fromEnum (r1 == r2)) $ m, ip = i + 4 }

ops (99 : _) c = c { halted = True }


runInput :: [Int] -> Computer -> [Int]
runInput inp c =
    let ci = c { input = inp }
        (o, c') = stepio ci
        f c = let (o, c') = stepio c in (o, c):f c'
    in f ci & takeWhile (not.halted.snd) & fmap fst & catMaybes
