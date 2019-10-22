// example of a simple recursive data structure in Rust

pub enum Tree {
    Empty,
    Node(i32, Box<Tree>, Box<Tree>),
}

impl Tree {
    fn sum(t: &Tree) -> i32 {
        use Tree::*;

        match t {
            Empty => 0,
            Node(n, l, r) => 
                n + Self::sum(l) + Self::sum(r)
        }
    }
}

pub fn example() -> i32 {
    use Tree::*;

    let t = Box::new(
        Node(5,
        Box::new(Empty),
        Box::new(Empty)));

    Tree::sum(&t)
}