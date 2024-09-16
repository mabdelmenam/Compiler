#include <stdio.h>
int main(void){
float x;
float y;
float result;
float counter;
/* THIS CODE IS TO TEST FUNCTIONALITY OF OUR COMPILER!! */
x = 10;
y = 5;
/* Test variable declaration, initialization, and arithmetic */
result = x+y*2-3;
printf("The result of x + y * 2 - 3 is:\n");
printf("%.2f\n", (float)(result));
/* Test IF, ELSE IF, ELSE conditionals */
if(result>20){
printf("Result is greater than 20\n");
}
else if(result==17){
printf("Result is exactly 17\n");
}
else{printf("Result is less than 17\n");
}
/* Test WHILE loop */
counter = 0;
while(counter<5){
printf("Counter value is:\n");
printf("%.2f\n", (float)(counter));
counter = counter+1;
}
/* Test reassigning variables and additional calculations */
x = x+3;
y = y*2;
result = x+y;
printf("After updating x and y, the new result is:\n");
printf("%.2f\n", (float)(result));
printf("HELLO\n");
printf("HI\n");
printf("BOY\n");
return 0;
}
