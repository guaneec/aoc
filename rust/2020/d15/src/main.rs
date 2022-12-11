fn main() {
    let s = String::from("9,6,0,10,18,2,1");
    let a: Vec<usize> = s.split(',').map(|x| x.parse().unwrap()).collect();
    for n in [2020, 30000000] {
        let mut hist = std::collections::HashMap::new();
        for (i, &x) in a[..a.len()-1].iter().enumerate() {
            hist.insert(x, i);
        }
        let mut p = a[a.len() - 1];
        for i in a.len()..n {
            let x = i - 1 - *hist.get(&p).unwrap_or(&(i - 1));
            hist.insert(p, i - 1);
            p = x;
        }
        println!("{}", p);
    }
}
