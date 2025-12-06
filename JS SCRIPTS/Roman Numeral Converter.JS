\\function convertToRoman(num) {
  let romNum=[];
 
  do{
      
    if(num >= 1000){
      romNum=romNum.concat("M");
      num=num-1000;
      }else if(num >= 900){
      romNum=romNum.concat("CM");
      num=num-900;
      }else if(num >= 500){
      romNum=romNum.concat("D");
      num=num-500;
      }else if(num >= 400){
      romNum=romNum.concat("CD");
      num=num-400;
      }else if(num >= 100){
      romNum=romNum.concat("C");
      num=num-100;
      }else if(num >= 90){
      romNum=romNum.concat("XC");
      num=num-90;
      }else if(num >= 50){
      romNum=romNum.concat("L");
      num=num-50;
      }else if(num >= 40){
      romNum=romNum.concat("XL");
      num=num-40;
      }else if(num >= 10){
      romNum=romNum.concat("X");
      num=num-10;
      }else if(num == 9){
      romNum=romNum.concat("IX");
      num=num-9;
      }else if(num >= 5){
      romNum=romNum.concat("V");
      num=num-5;
      }else if(num == 4){
      romNum=romNum.concat("IV");
      num=num-4;
      } else {
      romNum=romNum.concat("I");
      num=num-1;
      }

  }while(num > 0);

  
 return romNum.join("");
}

console.log(convertToRoman(400));
console.log(convertToRoman(2))Roman Numeral Converter