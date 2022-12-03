use std::fs::read_to_string;

fn main() {
    let s = read_to_string("../../../data/2020/05.input.txt").unwrap();
    let mut ids: Vec<i32> = s.lines().into_iter().map(|line| {
        let mut row = 0;
        let mut col = 0;
        for i in 0..7 {
            if line.as_bytes()[i as usize] == b'B' {
                row += 1 << (6 - i);
            }
        }
        for i in 0..3 {
            if line.as_bytes()[(i + 7) as usize] == b'R' {
                col += 1 << (2 - i);
            }
        }
        row * 8 + col
    }).collect();
    ids.sort();
    let p1 = ids.last().unwrap();
    let p2 = ids.windows(2).filter(|w| {w[0] + 2 == w[1]}).next().unwrap()[0] + 1;
    println!("{}", p1);
    println!("{}", p2);
}
