use std::{fs::read_to_string, collections::HashMap};

type Color<'a> = (&'a str, &'a str);
type Map<'a> = HashMap<Color<'a>, Vec<(i32, Color<'a>)>>;

static GOLD: Color = ("shiny", "gold");

fn has_gold(c: Color, m: &Map) -> bool {
    m.get(&c).unwrap().iter().any(|&(_x, c)| c == GOLD || has_gold(c, m))
}

fn count_all(c: Color, m: &Map) -> i32 {
    m.get(&c).unwrap().iter().map(|&(x, c)| x + x * count_all(c, m)).sum::<i32>()
}

fn main() {
    let s = read_to_string("../../../data/2020/07.input.txt").unwrap();
    let mut m: Map = HashMap::new();
    for l in s.lines() {
        if l.is_empty() {
            break;
        }
        let words: Vec<_> = l.split_ascii_whitespace().collect();
        let mut v: Vec<_> = Vec::new();
        for i in (4..=words.len()-4).step_by(4) {
            let x = words[i].parse().unwrap();
            v.push((x, (words[i+1], words[i+2])))
        }
        m.insert((words[0], words[1]), v);
    }
    let p1 = m.keys().filter(|&&k| has_gold(k, &m)).count();
    let p2 = count_all(GOLD, &m);
    println!("{}", p1);
    println!("{}", p2);
}
