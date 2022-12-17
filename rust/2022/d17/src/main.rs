use std::collections::HashSet;

const ROCKS: &str = "####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##";

fn main() {
    let rocks: Vec<Vec<(i32, i32)>> = ROCKS
        .split("\n\n")
        .map(|g| {
            g.lines()
                .rev()
                .enumerate()
                .flat_map(|(y, l)| {
                    l.bytes()
                        .enumerate()
                        .filter(|&(_x, c)| c == b'#')
                        .map(move |(x, _c)| (x as i32, y as i32))
                })
                .collect()
        })
        .collect();
    let s = std::fs::read_to_string("../../../data/2022/17.input.txt").unwrap();
    let mut itdx = s
        .trim()
        .bytes()
        .map(|c| if c == b'>' { 1 } else { -1 })
        .cycle();
    let mut top = 0;
    let mut board = HashSet::new();
    for i in 0..2022 {
        let mut rock: Vec<_> = rocks[i % rocks.len()]
            .iter()
            .map(|&(x, y)| (x, top + 4 + y))
            .collect();
        loop {
            let dx = itdx.next().unwrap();
            if !rock
                .iter()
                .any(|&(x, y)| x + dx == -3 || x + dx == 5 || board.contains(&(x + dx, y)))
            {
                rock.iter_mut().for_each(|(x, _y)| *x += dx);
            }
            if !rock
                .iter()
                .any(|&(x, y)| y - 1 == 0 || board.contains(&(x, y - 1)))
            {
                rock.iter_mut().for_each(|(_x, y)| *y -= 1);
            } else {
                for &(x, y) in rock.iter() {
                    board.insert((x, y));
                    top = top.max(y);
                }
                break;
            }
        }
    }
    println!("{}", top);
}
