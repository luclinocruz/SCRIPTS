function palindrome(str) {
  let word=str.split(/[\W_]/g).join("").toLowerCase()
  let flag=-1;
  console.log(str)
  console.log(str.length)
  console.log(word)
  console.log(word.length)
  if(word.length%2 != 0){ //sz impar
    let mid= Math.round( (word.length/2));
    for( let x=0, y=word.length-1 ; x!=y; x++ ,y-- ){
      if(word[x]!=word[y]){
        flag=0;
        }
    }
} else{ //sz par
    let mid= str.length/2 ;
    for( let x=0, y=word.length-1 ; x<mid && y>=mid; x++, y--){
      if(word[x]!=word[y]){
        flag=0;
        }
    }
}

  
  
    if(flag == -1){
      return true;
    }
    else{
      return false;
    }
  
}

console.log(palindrome("eye"));
console.log(palindrome("_eye"));
console.log(palindrome("race car"));
console.log(palindrome("not a palindrome"));
console.log(palindrome("My age is 0, 0 si ega ym."));
console.log(palindrome("0_0 (: /-\ :) 0-0"));
console.log(palindrome("five|\_/|four"));
console.log(palindrome("1 eye for of 1 eye."));
console.log(palindrome("A man, a plan, a canal. Panama"));