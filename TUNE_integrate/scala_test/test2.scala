// list of complex objects

case class Stud( rollno : Int, name : String, marks : Int)

val students  = List(Stud(1,"Kir",40), Stud(2,"A",55), Stud(5,"hi",89), Stud(5,"hi5",91))

println(students)

val first = students.head
val rest = students.tail
val headOfTail = students.tail.head

val toppers = students.filter(s => s.marks>=56)

println(toppers)

val parts = students.partition(s => s.marks>=60)
println(parts)


// Tuples

val part1 = parts._1
println(part1)





