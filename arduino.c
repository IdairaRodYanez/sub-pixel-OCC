/*
Arduino configuration to transmit all possible payloads in the frame
*/
void setup(){
  pinMode(6, OUTPUT);
}

void loop(){
  int trama[15] = {1,1,1,1,1,0,0,0,0,0,0,0,0,0,0};
  int cont, i, j, c;
  int binaryCont[8]; 
  
  /* Counter from 0 to 255*/
  for(cont=0; cont<=255;cont++){
    /*Convert Dec to Bin*/
    for(i=7; i>=0;i--){
      j = cont >>i;
      if(j & 1){
        binaryCont[i] = 1; 
      }else {
        binaryCont[i] = 0; 
      } 
    }
    /*Assign count to frame*/ 
    trama[6] = binaryCont[7];
    trama[7] = binaryCont[6];
    trama[8] = binaryCont[5];
    trama[9] = binaryCont[4];
    trama[11] = binaryCont[3];
    trama[12] = binaryCont[2];
    trama[13] = binaryCont[1];
    trama[14] = binaryCont[0];
    /*Turn on or off LED*/
    for(c=0; c<15;c++){
      if(trama[c]==1){
        digitalWrite(6, HIGH);
      }else{
        digitalWrite(6, LOW);
      }
      delayMicroseconds(133333); // 133.333 ms
    }  
  }
}