fn int_literals() -> i32 {
    let a = 43; //int32
    let b = 33i32 + a;
    let c = b + 100_i32;
    let d = 1_i16;
    let e = c + (d as i32);
    e
}

fn character_literals() {
    let a: char = 'a';
    let b: u8 = b'a';
    let c: String = String::from("hello");
    let d: String = "hello".to_string();
    let e: &str = "hello";
    let f = b"hello there bytestring!";
}

fn tuples() {
    let a = (5, "hello");
    let (b, c) = a;
    assert_eq!(b, 5);
}

fn change_first(s: &mut [bool]) {
    s[0] = !s[0];
}

fn arrays() {
    let mut a: [bool; 10] = [true; 10];
    assert_eq!(a.len(), 10);

    // array slice
    let b: &[bool] = &a[..];

    println!("a = {:?}", a);
    change_first(&mut a);
    println!("a = {:?}", a);
}

fn vectors() {
    let mut v = vec![];
    for _i in 0..10 {
        v.push(false);
    }
    println!("v = {:?}", v);
    change_first(&mut v);
    println!("v = {:?}", v);
}

mod tree;
mod stdmem;

fn main() {
    tuples();
    arrays();
    vectors();
    tree::example();
    stdmem::example();
}
