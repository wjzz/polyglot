object MyExample {
  val PI: Double = 3.1415918
}

object Main extends App {
  def square(x: Int) = x * x

  def square(x: Double) = x * x

  def area(x: Double): Double = 3.1415918 * x * x

  def sum_of_squares(x: Double, y: Double): Double = square(x) + square(y)

  def abs(x: Double) = if (x >= 0) x else -x

  println(abs(11))
  println(abs(-11))

  val b2 = 12 > 10 && !(10 == 10)
  println(b2)

  def sqrt(x: Double) = {
    // recursive functions need an explicit return value in Scala
    def sqrtIter(guess: Double): Double =
      if (isGoodEnough(guess)) guess
      else sqrtIter(improve(guess))

    def improve(guess: Double) = 
      (guess + x / guess) / 2

    def isGoodEnough(guess: Double) = 
      abs(guess * guess - x) < 0.00001

    sqrtIter(1.0)
  }

  def printMany(limit: Int): Unit = {
    def printIter(current: Int): Unit = 
        if (current < limit) {
          print("Sqrt of ")
          print(current)
          print(" is ")
          println(sqrt(current))
          printIter(current+1)
        }

    printIter(0)
  }
  
  printMany(10)

  val n = 123
  val b = true
  val d = 10.0

  // literals are overloaded
  val n2 : Int = 10
  val d2 : Double = 10

  println(square(11))
  println(area(10.0))

  // blocks are expressions!
  val x = {
    val a = 123
    a + 1
  }
  println(x)

  // semicolons are optional, but they can be used to group many expressions
  // on one line
  val aa = 11; val zz = aa * aa
  print("aa = ")
  println(aa)

  println("Hello, Tokyo!")

  // operators should be put on a trailing position if they don't fit on a single line
  val a = 12 +
    10
  print("a = ")
  println(a)

  def addPI(x: Double) = MyExample.PI + x

  // Automatic imports
  //   These are:

  // All members of package scala
  // All members of package java.lang
  // All members of the singleton object scala.Predef.
  // Here are the fully qualified names of some types and functions which you have seen so far:

  // Int                            scala.Int
  // Boolean                        scala.Boolean
  // Object                         java.lang.Object
  // String                         java.lang.String
}
