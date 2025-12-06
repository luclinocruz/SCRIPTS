function checkCashRegister(price, cash, cid) {
  //calcule the ammount to change
  let change=cash-price;
  let cidOut=[
    ["ONE HUNDRED", 0],
    ["TWENTY", 0],
    ["TEN", 0],
    ["FIVE", 0],
    ["ONE", 0],
    ["QUARTER", 0],
    ["DIME", 0],
    ["NICKEL", 0],
    ["PENNY", 0]
]
  //creating an easy way know whitch reference i nead to focus and how mutch i must reduce for iteraction
  let reductor=0,id=0,cicle=change;
  let flag=1;//is there cash in draw
 
  do{ cicle=cicle.toFixed(2);
    
      if(cicle >=100 && cid[8][1]>=100){
        reductor=100;
        id=0;
        cidOut[id][1]+=reductor;
        cid[8][1]-=reductor;
        cicle=cicle-reductor;
        
      }else if(cicle >=20 && cid[7][1]>=20){
        reductor=20;
        id=1;
        cidOut[id][1]+=reductor;
        cid[7][1]-=reductor;
        cicle =cicle-reductor;
        
      }else if(cicle >=10 && cid[6][1]>=10){
        reductor=10;
        id=2;
        cidOut[id][1]+=reductor;
        cid[6][1]-=reductor;
        cicle=cicle-reductor;
          
      }else if(cicle >=5 && cid[5][1]>=5){
        reductor=5;
        id=3;
        cidOut[id][1]+=reductor;
        cid[5][1]-=reductor;
        cicle=cicle-reductor;
      }else if(cicle >=1 && cid[4][1]>=1){
        reductor=1;
        id=4;
        cidOut[id][1]+=reductor;
        cid[4][1]-=reductor;
        cicle=cicle-reductor;
      }else if(cicle >=0.25 && cid[3][1]>=0.25){
        reductor=0.25;
        id=5;
        cidOut[id][1]+=reductor;
        cid[3][1]-=reductor;
        cicle=cicle-reductor;
      }else if(cicle >=0.1 && cid[2][1]>=0.1){
        reductor=0.1;
        id=6;
        cidOut[id][1]+=reductor;
        cid[2][1]-=reductor;
        cicle=cicle-reductor;
      }else if(cicle >=0.05 && cid[1][1]>=0.05){
        reductor=0.05;
        id=7;
        cidOut[id][1]+=reductor;
        cid[1][1]-=reductor;
        cicle=cicle-reductor;
      }else if(cicle >= 0.01 && cid[0][1]>=0.01 &&cid[0][1]!=change){
        reductor=0.01;
        id=8;
        cidOut[id][1]+=reductor;
        cid[0][1]-=reductor;
        cicle= cicle-reductor;
        
      }else if(cicle>=0.01 && cid[0][1]==change){
        reductor=change;
        id=8;
        cidOut[id][1]+=reductor;
        cid[0][1]-=reductor;
        cicle= cicle-reductor;
        flag =-3
        break;
      }else if(cicle==0){
        flag=-2;break;
      }
      else{//there is no cash in draw
        flag=-1;break;
        }
    
  }while(flag > 0);
  
 if(flag==-3){
 }else{
   cidOut=cidOut.filter( i => { return i[1] > 0 })
   }

  if(flag==-1) {
    return {status: "INSUFFICIENT_FUNDS", change: []}
  }else if(cid[id][1]>=change){
    return {status: "OPEN", change: cidOut};
  }else if(cidOut!=undefined && cidOut[id][1] >= change){
    return {status: "CLOSED", change: cidOut.reverse()};
  } 
 
}
 
 
 
 
console.log(checkCashRegister(19.5, 20, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1], ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20], ["TWENTY", 60], ["ONE HUNDRED", 100]])); 
 
console.log(checkCashRegister(3.26, 100, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1], ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20], ["TWENTY", 60], ["ONE HUNDRED", 100]]))
 
console.log(checkCashRegister(3.26, 100, [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1], ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20], ["TWENTY", 60], ["ONE HUNDRED", 100]]))
 
 console.log(checkCashRegister(19.5, 20, [["PENNY", 0.5], ["NICKEL", 0], ["DIME", 0], ["QUARTER", 0], ["ONE", 0], ["FIVE", 0], ["TEN", 0], ["TWENTY", 0], ["ONE HUNDRED", 0]]))

 console.log(checkCashRegister(19.5, 20, [["PENNY", 0.01], ["NICKEL", 0], ["DIME", 0], ["QUARTER", 0], ["ONE", 0], ["FIVE", 0], ["TEN", 0], ["TWENTY", 0], ["ONE HUNDRED", 0]]))