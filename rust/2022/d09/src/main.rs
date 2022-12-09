fn main() {
    let s = String::from(
"R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"
    );
    let s = std::fs::read_to_string("../../../data/2022/09.input.txt").unwrap();
    for n in [2, 10] {
        let mut knots = Vec::new();
        let mut tails = std::collections::HashSet::new();
        for _ in 0..n {
            knots.push((0, 0));
        }
        for l in s.trim_end().lines() {
            let (dx, dy) = match l.as_bytes()[0] {
                b'R' => (1, 0),
                b'L' => (-1, 0),
                b'U' => (0, 1),
                b'D' => (0, -1),
                _ => panic!(),
            };
            for _ in 0..std::str::from_utf8(&l.as_bytes()[2..]).unwrap().parse().unwrap() {
                knots[0] = (knots[0].0 + dx, knots[0].1 + dy);
                for i in 0..knots.len()-1 {
                    let (hx, hy) = knots[i];
                    let (mut tx, mut ty): (i32, i32) = knots[i+1];
                    while (hx-tx).abs() > 1 || (hy-ty).abs() > 1 {
                        tx += (hx-tx).signum();
                        ty += (hy-ty).signum();
                    }
                    knots[i+1] = (tx, ty);
                }
                tails.insert(knots[knots.len() - 1]);
            }
        }
        println!("{}", tails.len());
    }
}
