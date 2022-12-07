use std::{fs::read_to_string, collections::HashMap};

fn main() {
    let s = read_to_string("../../../data/2022/07.input.txt").unwrap();
    let mut path = Vec::new();
    let mut files = HashMap::new();
    let mut dirs: HashMap<Vec<&str>, u32> = HashMap::new();
    s.lines().filter(|&line| !line.is_empty()).for_each(|line| {
        let parts: Vec<_> = line.split_ascii_whitespace().collect();
        match parts[..] {
            ["$", "cd", p] => {
                if p == "/" {
                    path.clear();
                } else if p == ".." {
                    path.pop();
                } else {
                    path.push(p);
                }
            }
            ["$", "ls"] | ["dir", _] => {}
            [sz, file] => {
                let sz: u32 = sz.parse().unwrap();
                path.push(file);
                files.insert(path.clone(), sz);
                path.pop();
            }
            _ => {}
        }
    });
    for (p, size) in files {
        for i in 0..=p.len()-1 {
            *dirs.entry(p.iter().take(i).copied().collect()).or_insert(0) += size;
        }
    }
    let empty: Vec<&str> = vec!();
    let all = dirs.get(&empty).unwrap();
    println!("{}", dirs.values().filter(|&&v| v <= 100000).sum::<u32>());
    println!("{}", dirs.values().filter(|&&v| 70000000 - all + v >= 30000000).min().unwrap());
}
