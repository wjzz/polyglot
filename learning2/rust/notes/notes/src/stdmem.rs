pub fn swap_example() {
    let mut a = 10;
    let mut b = 5;
    std::mem::swap(&mut a, &mut b);
    assert_eq!(a, 5);
    assert_eq!(b, 10);
}

pub fn sizeof_examples() {
    let a: i32 = 123;
    println!("sizeof(i32) = {}", 
        std::mem::size_of_val(&a));
    println!("sizeof(usize) = {}",
        std::mem::size_of::<bool>())
}

pub fn example() {
    swap_example();
    sizeof_examples();
}