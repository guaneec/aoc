use std::fs::read_to_string;

fn enc(c: u8) -> u8 {
    c.to_ascii_lowercase() - b'a' + 26 * (c.is_ascii_uppercase() as u8)
}

fn pack<T: Iterator<Item = u8>>(it: T) -> u64 {
    let mut s: u64 = 0;
    for c in it {
        s |= 1 << enc(c);
    }
    s
}

fn extract(s: u64) -> u8 {
    for i in 0..64 {
        if s >> i & 1 == 1 {
            return i;
        }
    }
    panic!();
}

fn main() {
    let s = read_to_string("../../../data/2022/03.input.txt").unwrap();
    let lines: Vec<_> = s.split('\n').filter(|line| !line.is_empty()).map(|line| line.as_bytes()).collect();
    let p1: u32 = lines.iter().map(|line| {
        let n = line.len() / 2;
        (1 + extract(pack(line.iter().copied().take(n)) & pack(line.iter().copied().skip(n)))) as u32
    }).sum();
    let p2: u32 = (0..lines.len()).step_by(3).map(|i| {
        (1 + extract(
            pack(lines[i].iter().copied())
            & pack(lines[i+1].iter().copied())
            & pack(lines[i+2].iter().copied()))) as u32
    }).sum();
    println!("{}", p1);
    println!("{}", p2);
}
