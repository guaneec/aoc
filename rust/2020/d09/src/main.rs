use std::{fs::read_to_string, iter};

fn main() {
    let s = read_to_string("../../../data/2020/09.input.txt").unwrap();
    const M: usize = 25;
    let nums: Vec<u64> = s.trim_end().lines().map(|s|s.parse().unwrap()).collect();
    let p1 = nums[M + (0..).find(|&i| !(i..i+M).any(|j| (j+1..i+M).any(|k| nums[j] + nums[k] == nums[i + M]))).unwrap()];
    let n = nums.len();
    let partials: Vec<u64> = iter::once(0).chain(nums.iter().scan(0, |s, x| {*s += x; Some(*s)})).collect();
    let p2 = (||  {
        for i in 0..=n {
            for j in i+2..=n {
                if partials[j] - partials[i] == p1 {
                    return nums[i..j].iter().min().unwrap() + nums[i..j].iter().max().unwrap();
                }
            }
        }
        0
    })();    
    println!("{}", p1);
    println!("{}", p2);
}
