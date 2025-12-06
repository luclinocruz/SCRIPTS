function rot13(str) {
  let base = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
  let index = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  let word="";
  for( let l in str){
    for(let i=0; i<index.length ; i++){
       if(str[l]===" " || str[l]==="!" || str[l]==="?" || str[l]==="."){  
         word=word.concat(str[l]);
         break;
       } else
       if(str[l]==index[i]){
         word=word.concat(base[i+13]);
       }
    }
   
  }

  return word;
}

console.log(rot13("SERR PBQR PNZC"))
console.log(rot13("SERR CVMMN!"))
console.log(rot13("SERR YBIR?"))
console.log(rot13("GUR DHVPX OEBJA SBK WHZCF BIRE GUR YNML QBT."));