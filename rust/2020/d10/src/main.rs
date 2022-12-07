use std::fs::read_to_string;

fn main() {
    let s = read_to_string("../../../data/2020/10.input.txt").unwrap();
    let mut nums: Vec<i32> = [0, 0, 0].into_iter().chain(s.trim_end().lines().map(|s| s.parse().unwrap())).collect();
    nums.sort();
    nums.push(nums[nums.len() - 1] + 3);
    let mut js = [0, 0, 0, 0];
    for i in 0..nums.len() - 1 {
        js[(nums[i+1] - nums[i]) as usize] += 1;
    }
    let mut p2: [u64; 3] = [0, 0, 1];
    println!("{}", js[1] * js[3]);
    for i in 3..nums.len() {
        p2 = [p2[1], p2[2], (0..3).filter(|j| nums[i] - nums[i-3+j] <= 3).map(|i| p2[i]).sum()];
    }
    println!("{}", p2[2]);
}
