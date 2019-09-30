object Main extends App {

  sealed trait Expr
  case class Lit(num: Int) extends Expr
  case class Add(e1: Expr, e2: Expr) extends Expr

  def eval(e: Expr): Int = {
    e match {
      case Lit(num) => num
      case Add(e1, e2) => eval(e1) + eval(e2)
    }
  }

  val e1 = Lit(10)
  println(e1)
  println(eval(e1))

  val e2 = Add(Lit(10), Lit(15))
  println(e2)
  println(eval(e2))

  val e3 = Add(e2, e2)
  println(e3)
  println(eval(e3))
}