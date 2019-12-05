case class Student(var rollno : Int = 1, var name : String = "Kiran", var marks: Int = 90)
{
    //create class
    def show() = //method
    {
        println("hii")
    }

    def >(s2 : Student) : Boolean =
    {
        marks > s2.marks

    }

}

var s1 = Student(4, "Rahul") //creating object
var s2 = Student(name = "Tim", marks = 88) 

s1.show() //hii
println(s1>s2) //true

var nums = List(4,8,5,6)

for (n <- nums)
{
    println(n)
}

// reverse nums
var reverseNums = nums.reverse

var dropped = reverseNums.drop(2).take(1) //removes first 2 elements, takes the next one

// Lambda expression
dropped.foreach{i: Int => println(i) }
reverseNums.foreach{i: Int => println(i) }

//create list[AnyVal]
var lis = List(4,5,true)
//creat list[Any] top in hierarchy
var lis1 = List(4,5,true,"Kiran")



