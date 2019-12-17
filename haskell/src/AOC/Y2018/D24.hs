module AOC.Y2018.D24 where
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
import           Data.Ord
import           Data.Bits
import           Control.Lens
import           Control.Monad.State
import           Debug.Trace
import           Text.Megaparsec         hiding ( State )
import           Text.Megaparsec.Char
import qualified Text.Megaparsec.Char.Lexer    as L
import           Data.Void

type Parser = Parsec Void String

p1' :: () -> ()
p1' = id

p1 :: String -> ()
p1 _ = ()



p2' :: [Group] -> Int
p2' = undefined

p2 :: String -> ()
p2 _ = ()

data Group = Group { nUnit :: Int, hp :: Int, weaknesses :: Map String Int, dmg :: Int, tp :: String, ini :: Int, isInfection :: Bool } deriving (Show, Eq)
type Sys = Map Int Group


ep :: Group -> Int
ep g = nUnit g * (dmg g)

damage :: Group -> Group -> Int
damage attacker defender =
    let mul = fromMaybe 1 $ Map.lookup (tp attacker) (weaknesses defender)
    in  mul * ep attacker

tarSel :: Sys -> [(Int, Int)]
tarSel s =
    Map.assocs s
        & filter (\(_, g) -> nUnit g > 0)
        & sortOn (\(_, g) -> (ep g, ini g))
        & (\as -> foldr
              (\(i, g) (l, st) ->
                  let
                      es = as & filter
                          (\(i, g') ->
                              Set.notMember i st
                                  && (isInfection g' /= isInfection g)
                                  && (damage g g' > 0)
                          )
                      t = if null es
                          then Nothing
                          else
                              es
                              & maximumBy
                                    (comparing
                                        (\(i, g') ->
                                            (damage g g', ep g', ini g')
                                        )
                                    )
                              & fst
                              & Just
                  in
                      case t of
                          Nothing -> (l, st)
                          Just t  -> ((i, t) : l, Set.insert t st)
              )
              ([], Set.empty)
              as
          )
        & fst
        & reverse

doDamage :: Group -> Group -> Group
doDamage a d = d { nUnit = nUnit d - (damage a d) `div` (hp d) }

battle :: [(Int, Int)] -> Sys -> Sys
battle = flip $ foldl'
    (\s (ia, id) ->
        let d' = doDamage (s Map.! ia) (s Map.! id)
        in  if (Map.notMember ia s)
                then s
                else if nUnit d' <= 0
                    then Map.delete id s
                    else Map.insert id d' s
    )

fight :: Sys -> Sys
fight s = battle (tarSel s & sortOn (\(a, _) -> -ini (s Map.! a))) s

data Result = ImmWin | InfWin | Tie



end :: Sys -> Bool
end s = s == fight s

ss :: Sys -> IO ()
ss s = forM_
    (Map.assocs s)
    (\(i, g) ->
        (do
            print (i, hp g, nUnit g, isInfection g)
        )
    )

boost = 100

t :: IO ()
t = do
    f <- readFile "data/24.txt"
    let s =
            Map.fromList
                $ zip [0 ..]
                $ map
                      (\g -> if isInfection g
                          then g
                          else g { dmg = dmg g + boost }
                      )
                $ fromJust
                $ parseMaybe parser f
    let s' = until end fight s
    print $ Map.foldl' (\a g -> a + nUnit g) 0 s'
    ss s'
    return ()

t2 = do
    f <- readFile "data/24.txt"
    let gs = fromJust $ parseMaybe parser f
    let gss = map (\boost -> traceShow boost $ map (\g -> if isInfection g
                    then g
                    else g { dmg = dmg g + boost }
               ) gs) [31..]
    let os = map outcome gss
    let s = find wins os & fromJust
    print $ Map.foldl' (\a g -> a + nUnit g) 0 s
    ss s
    return ()

sumHp :: Sys -> Int
sumHp = Map.foldl' (\a g -> a + nUnit g) 0

outcome :: [Group] -> Sys
outcome gs = until end fight (Map.fromList $ zip [0 ..] gs)

wins :: Sys -> Bool
wins s = s & Map.elems & (not . any isInfection)

parserWI :: Parser (Map String Int)
parserWI =
    try
        $   (   Map.fromList
            <$> concatMap (\(l, m) -> map (\e -> (e, m)) l)
            <$> between
                    (string "(")
                    (string ")")
                    (do
                        l <- sepBy (try im <|> wk) (string "; ")
                        return l
                    )
            <*  space
            )
        <|> return (Map.empty)
  where
    im =
        (string "immune to ")
            >> ((\x -> (x, 0)) <$> ((many lowerChar) `sepBy1` (string ", ")))
    wk =
        string "weak to "
            >> ((\x -> (x, 2)) <$> ((many lowerChar) `sepBy1` (string ", ")))

-- 31 units each with 20064 hit points (immune to slashing, bludgeoning; weak to radiation) with an attack that does 1082 bludgeoning damage at initiative 10
parser :: Parser [Group]
parser = do
    string "Immune System:" <* space
    gg <- many g
    space >> string "Infection:" >> space
    ggg <- many g
    space
    eof
    return $ (($ False) <$> gg) ++ (($ True) <$> ggg)
  where
    g =
        (do
            (n, hp) <-
                (,)
                <$> L.decimal
                <*  string " units each with "
                <*> L.decimal
                <*  string " hit points "
            w <- parserWI
            string "with an attack that does "
            a <- L.decimal
            space
            t <- many lowerChar
            string " damage at initiative "
            init <- L.decimal
            space
            return $ Group n hp w a t init
        )
