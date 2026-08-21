
import math;

def computepi(n):
    
    total = 0;
    pom = 1.0; 

    for k in range (n):
        # 2 * count + 1 = always odd 
        total += (pom * 1.0/(2 * k + 1)); 
        #flips sign every iteration
        pom *= -1; 

    return total * 4;



def compute_sqrt(x):
    #because if zero the first iteration will be undef 
    last = 1.0;

    for k in range (10):
        
        #formula for sqrt
        next_guess = .5 * (last + x / last);
        last = next_guess;
    

    return last;



def is_prime(n):
   if (n < 2):
       return False;
        
   for k in range (2, n):  
        if (n % k == 0):
           return False;
       
   return True;



def display_prime(n):
    
    for k in range (2, n + 1): 
        
        #use what we had before
        if (is_prime(k)):
            print(k);
    
    print("\n");




def process_scores():

    total = 0;
    count = 0;
    score = 0;
    avg = 0.0;
    quit = 'h';
    min_student = [];
    max_student = [];
   
    #while not quitting keep going
    while (quit != 'q' and quit != 'Q'):
                      
            student = input("Enter Student's name: ");
            score = int(input("Enter Student's score: "));

            total += score;
            #at 0 we set everything up for the rest of the increments
            if (count == 0):
                minimum = score;
                maximum = score; 
                max_student = [student];
                min_student = [student]; 
                            
            if (score > maximum):           
                maximum = score;
                max_student = [student];
            
            if (score < minimum):
                minimum = score;
                min_student = [student];       

            count = count + 1;

            quit = input("quit (q or Q)?: ");
    
    avg = total / float(count);
    print("\nStudents who scored the minimum: ",min_student);
    print("\nStudents who scored the maximum: ", max_student);
    print("\nStudent average: ", avg);




def compute_tax(income, status, state):

    if income <= 0:
        return False

    if (status != 'single' and status != 'married' and
        status != 'Single' and status != 'Married'):
        return False

    if (state != 'i' and state != 'I' and
        state != 'o' and state != 'O'):
        return False

    if (state == 'i' or state == 'I'):

        if (status == 'single' or status == 'Single'):

            if income < 30000:
                rate = 0.20;
            else:
                rate = 0.25;
        #if married
        else:

            if income < 50000:
                rate = 0.10;
            else:
                rate = 0.15;
    #o or O
    else:

        if (status == 'single' or status == 'Single'):

            if income < 30000:
                rate = 0.17; 
            else:
                rate = 0.22;   
        #if married
        else: 

            if income < 50000:
                rate = 0.07;   
            else:
                rate = 0.12;  

    return income * rate;



def quadratic(a, b, c):
        answer = 0.0;

        #this checks if a is zero because you cant divide by 0
        if (a == 0):
            return 0, 0;
        
        answer = (b * b) - (4 * a * c);

        #this checks if real solutions exist 
        if (answer < 0):      
            return 0, 0;
        

        #this computes the solutions 
        solution1 = (-b + math.sqrt(answer)) / (2 * a);
        solution2 = (-b - math.sqrt(answer)) / (2 * a);

        return solution1, solution2;



def sort(list):

    #list2 is now a copy of list without affecting list
    list2 = list.copy();
    a = len(list2);

    for i in range(a - 1):
        #minimum index
        minimumI = i;

        for k in range(i + 1, a):
            if list2[k] < list2[minimumI]:
                minimumI = k;

        #swap in the loop
        #temp holder so we can swap
        swap = list2[i];
        list2[i] = list2[minimumI];
        list2[minimumI] = swap;

    return list2



def id_password(first, last):
    #makes sure its always uppercase
    first = first.upper();
    last = last.upper();

    #assigning
    id = first[0] + last;
    pw = first[0] + first[len(first)-1] + last[0] + last[1] + last[2] + str(len(first)) + str(len(last));

    return id, pw;




def file_sort(infile, outfile):

    f = open(infile, "r");
    
    #this reads the number of students
    n = int(f.readline().strip());
    
    students = [];
    
    #this reads the student data
    for i in range(n):
        line = f.readline().strip();
        ls = line.split();
        
        student_id = int(ls[0]);
        name = ls[1];
        gpa = float(ls[2]);
        
        students.append([student_id, name, gpa]);
    
    f.close();
    
    #the selection Sort by student_id
    length = len(students);
    
    for i in range(length - 1):
        
        minimumI = i;
        
        for k in range(i + 1, length):
            if students[k][0] < students[minimumI][0]:
                minimumI = k;
        
        #swap with temp
        temp = students[i];
        students[i] = students[minimumI];
        students[minimumI] = temp;
    
    #this writes to output file
    f = open(outfile, "w");
    
    f.write(str(n) + "\n");
    
    for i in range(len(students)):
        student = students[i];
        f.write(str(student[0]) + " " + student[1] + " " + str(student[2]) + "\n");
    
    f.close();



def main():
    
   choice = 0

   while choice != 10:
       #print prompt and choices
        print("This is the Menu (hi!!)");
        print("1 = Compute Pi");
        print("2 = Compute Square Root");
        print("3 = Check Prime");
        print("4 = Display Primes");
        print("5 = Process Scores");
        print("6 = Compute Tax");
        print("7 = Quadratic Solver");
        print("8 = Sort List");
        print("9 = File Sort");
        print("10 = Quit");

        #make sure choice is between 1 and 10
        choice = int(input("What will you choose? (1-10): "));

        if choice == 1:
            n = int(input("Enter number of terms: "));
            result = computepi(n);
            print("your Pi: ", result);

        elif choice == 2:
            x = float(input("Enter number: "));
            result = compute_sqrt(x);
            print("square root is: ", result);

        elif choice == 3:
            n = int(input("Enter number: "));
            result = is_prime(n);
            print("Is this prime?: ", result);

        elif choice == 4:
            n = int(input("display the primes up to: "));
            display_prime(n);

        elif choice == 5:
            process_scores();

        elif choice == 6:
            income = float(input("Enter income: "));
            status = input("Enter mairital status (single/married): ");
            state = input("Enter state (i/o): ");
            tax = compute_tax(income, status, state);
            print("Tax: ", tax);

        elif choice == 7:
            a = float(input("Enter a: "));
            b = float(input("Enter b: "));
            c = float(input("Enter c: "));
            sol1, sol2 = quadratic(a, b, c);
            print("the solutions are: ", sol1, sol2);

        elif choice == 8:
            nums = input("Enter numbers: ");
            nums_list = nums.split();
            nums_list = [int(x) for x in nums_list];
            sorted_list = sort(nums_list);
            print("sorted list: ", sorted_list);

        elif choice == 9:
            infile = input("Enter input file name: ");
            outfile = input("Enter output file name: ");
            file_sort(infile, outfile);
            print("File sorted successfully.");

        elif choice == 10:
            print("Peace!");

        else:
            print("Try again....");

main();

class Rectangle:

    #Constructors
    def __init__(self, length, width):
        self.length = length;
        self.width = width;

    #Setters
    def slength(self, length):
        self.length = length;

    def swidth(self, width):
        self.width = width;

    #Getters
    def glength(self):
        return self.length;

    def gwidth(self):
        return self.width;

    #area method
    def area(self):
        return self.length * self.width;

    #convert to string method
    def __str__(self):
       return "Rectangle: length = " + str(self.length) +  ", width = " + str(self.width);




   