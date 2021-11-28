use std::{
    fs::File,
    io::{self, BufRead, BufReader},
};

fn main() -> io::Result<()> {
    let f = File::open("../../../data/2020/03.input.txt")?;
    let f = BufReader::new(f);
    let grid: Vec<_> = f.lines().map(|l| l.unwrap()).collect();
    let n = grid[0].len();
    let count_tree = |(right, down): &(usize, usize)| grid.iter()
        .step_by(*down)
        .enumerate()
        .filter(|(i, l)| l.as_bytes()[i * right % n] as char == '#')
        .count();
    let p1 = count_tree(&(3, 1));
    let p2: usize = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        .iter()
        .map(count_tree)
        .product();
    println!("{} {}", p1, p2);
    Ok(())
}
