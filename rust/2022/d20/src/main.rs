fn main() {
    let s = std::fs::read_to_string("../../../data/2022/20.input.txt").unwrap();
    let a: Vec<i32> = s.split_terminator('\n').map(|x| x.parse().unwrap()).collect();
    let n = a.len();
    for (mult, rounds) in [(1, 1), (811589153, 10)] {
        let a: Vec<i64> = a.iter().map(|&x| x as i64 * mult).collect();
        let mut ixs: Vec<i64> = (0..n as i64).collect();
        for _ in 0..rounds {
            for (i, x) in a.iter().enumerate() {
                let j = ixs[i];
                let nn = n as i64 - 1;
                let jj = ((j + x) % nn + nn) % nn;
                if j < jj {
                    for k in 0..n {
                        ixs[k] -= if j < ixs[k] && ixs[k] <= jj {1} else if ixs[k] == j {j - jj} else {0};
                    }
                } else {
                    for k in 0..n {
                        ixs[k] += if jj <= ixs[k] && ixs[k] < j {1} else if ixs[k] == j {jj - j} else {0};
                    }
                }
            }
        }
        let i0 = ixs[a.iter().position(|&x| x == 0).unwrap()];
        let targets: [i64; 3] = [1000, 2000, 3000].map(|di| (i0+di) % n as i64);
        println!("{}", (0..n).filter(|&i| targets.contains(&ixs[i])).map(|i| a[i]).sum::<i64>());
    }
}
