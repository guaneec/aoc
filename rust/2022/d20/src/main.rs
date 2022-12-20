fn main() {
    let s = std::fs::read_to_string("../../../data/2022/20.input.txt").unwrap();
    let a: Vec<i32> = s.split_terminator('\n').map(|x| x.parse().unwrap()).collect();
    let n = a.len();
    let nn = (n - 1) as i64;
    for (mult, rounds) in [(1, 1), (811589153, 10)] {
        let a: Vec<i64> = a.iter().map(|&x| x as i64 * mult).collect();
        let mut ixs: Vec<i64> = (0..n as i64).collect();
        for _ in 0..rounds {
            for (i, x) in a.iter().enumerate() {
                let j = ixs.iter().position(|&ii| ii == i as i64).unwrap() as i64;
                let jj = ((x + j) % nn + nn) % nn;
                if j < jj { ixs[j as usize..=jj as usize].rotate_left(1); }
                else { ixs[jj as usize..=j as usize].rotate_right(1); }
            }
        }
        let i0 = ixs.iter().position(|&i| i as usize == a.iter().position(|&x| x == 0).unwrap()).unwrap();
        println!("{}", [1000, 2000, 3000].map(|di| a[ixs[(i0 + di) % n] as usize]).iter().sum::<i64>());
    }
}
