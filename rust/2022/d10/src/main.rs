fn main() {
    let s = std::fs::read_to_string("../../../data/2022/10.input.txt").unwrap();
    let mut trace: [i32; 241] = [0; 241];
    let mut cycle = 1;
    let mut x = 1;
    for l in s.trim_end().lines() {
        let l = l.trim_end();
        match l {
            "noop" => {
                trace[cycle] = x;
                cycle += 1;
            }
            _ => {
                let v: i32 = l.split_whitespace().skip(1).next().unwrap().parse().unwrap();
                trace[cycle] = x;
                trace[cycle + 1] = x;
                x += v;
                cycle += 2;
            }
        }
    }
    println!("{}", (20..221).step_by(40).map(|i| i * trace[i as usize]).sum::<i32>());
    for i in 1..241 {
        print!("{}", if (trace[i] - (i - 1) as i32 % 40).abs() <= 1 {'#'} else {'.'});
        if i % 40 == 0 {
            println!("");
        }
    }
}
