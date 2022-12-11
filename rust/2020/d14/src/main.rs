fn main() {
    let s = std::fs::read_to_string("../../../data/2020/14.input.txt").unwrap();
    for part1 in [true, false] {
        let mut zero: u64 = 0;
        let mut one: u64 = 0;
        let mut mem = std::collections::HashMap::new();
        for l in s.trim_end().lines() {
            if l.as_bytes()[1] == b'a' {
                (zero, one) = l.as_bytes().iter().rev().take(36).enumerate().fold((0, 0), |(zero, one), (i, &c)| 
                (zero | ((c == b'0') as u64) << i, (one | ((c == b'1') as u64) << i)));
            } else {
                let i: usize = l.split('[').skip(1).next().unwrap().split(']').next().unwrap().parse().unwrap();
                let v: u64 = l.split("= ").skip(1).next().unwrap().parse().unwrap();
                if part1 {
                    mem.insert(i, v & !zero | one);
                } else {
                    let i = i as u64 & zero | one;
                    let mut vec = vec![i];
                    for b in 0..36 {
                        if (zero | one) >> b & 1 == 0 {
                            vec.extend(vec.clone().iter().map(|x| x | 1 << b));
                        }
                    }
                    for i in vec {
                        mem.insert(i as usize, v);
                    }
                }
            }
        }
        println!("{}", mem.values().sum::<u64>());
    }
}
