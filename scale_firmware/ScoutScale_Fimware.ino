//-------------------------------------------------------------------------------------
// ScoutScale_Firmware.ino
// Alex Lueddecke 
// Version 1.0
// February 2024
//-------------------------------------------------------------------------------------

/*
Hardware Parameters
  Pins for load cells
  - 3
  - 4
  - 8
  - 12

  Clock Pin
  - 2
*/

#include <HX711_ADC.h>

// Used for debugging code
#define DEBUGGING_ACTIVE false

#define CELL1_ACTIVE true
#define CELL2_ACTIVE true
#define CELL3_ACTIVE true
#define CELL4_ACTIVE true

// Pin declarations
#define CLOCK 2
#define DATA1 3
#define DATA2 4
#define DATA3 8
#define DATA4 12

#define NO_BROKEN_CELLS '0'

/* 
number of calibration points of reference
- make sure to include the zero value
- E.g. if you are calibrating using the table and a 25 lb weight NUMBER_OF_CAL_POR should be 2
- The interface code needs to reflect for this to work
*/
#define NUMBER_OF_CAL_POR 2

//HX711 constructor (dout pin, sck pin)
HX711_ADC LoadCell_1(DATA1, CLOCK); 
HX711_ADC LoadCell_2(DATA2, CLOCK); 
HX711_ADC LoadCell_3(DATA3, CLOCK); 
HX711_ADC LoadCell_4(DATA4, CLOCK);

unsigned long t = 0;

void initializeCells(){
  #if (CELL1_ACTIVE)
  LoadCell_1.begin();
  LoadCell_1.setReverseOutput();
  #endif

  #if (CELL2_ACTIVE)
  LoadCell_2.begin();
  LoadCell_2.setReverseOutput();
  #endif

  #if (CELL3_ACTIVE)
  LoadCell_3.begin();
  LoadCell_3.setReverseOutput();
  #endif

  #if (CELL4_ACTIVE)
  LoadCell_4.begin();
  LoadCell_4.setReverseOutput();
  #endif
}

int getNumberOfActiveLoadCells(){
  int numberOfCells = 0;

  #if (CELL1_ACTIVE)
  numberOfCells++;
  #endif

  #if (CELL2_ACTIVE)
  numberOfCells++;
  #endif

  #if (CELL3_ACTIVE)
  numberOfCells++;
  #endif

  #if (CELL4_ACTIVE)
  numberOfCells++;
  #endif

  return numberOfCells;
}

void startCells(){
  // tare preciscion can be improved by adding a few seconds of stabilizing time
  unsigned long stabilizingtime = 2000;
  
  // tare cells
  boolean _tare = true;

  byte loadcell1Rdy = 0;
  byte loadcell2Rdy = 0;
  byte loadcell3Rdy = 0;
  byte loadcell4Rdy = 0;

  int numberOfActiveLoadcells = getNumberOfActiveLoadCells();

  //run startup, stabilization and tare, all modules simultaniously
  while ((loadcell1Rdy + loadcell2Rdy + loadcell3Rdy + loadcell4Rdy) < numberOfActiveLoadcells) {
    #if (CELL1_ACTIVE)
    if (!loadcell1Rdy) loadcell1Rdy = LoadCell_1.startMultiple(stabilizingtime, _tare);
    #endif

    #if (CELL2_ACTIVE)
    if (!loadcell2Rdy) loadcell2Rdy = LoadCell_2.startMultiple(stabilizingtime, _tare);
    #endif

    #if (CELL3_ACTIVE)
    if (!loadcell3Rdy) loadcell3Rdy = LoadCell_3.startMultiple(stabilizingtime, _tare);
    #endif

    #if (CELL4_ACTIVE)
    if (!loadcell4Rdy) loadcell4Rdy = LoadCell_4.startMultiple(stabilizingtime, _tare);
    #endif
  }
}

char brokenCell(){
  char brokenCellNumber = NO_BROKEN_CELLS;

  #if (CELL1_ACTIVE)
  if (LoadCell_1.getTareTimeoutFlag()){
    brokenCellNumber = '1';
    #if (DEBUGGING_ACTIVE)
    Serial.println("Timeout, check MCU>HX711 no.1 wiring and pin designations");
    #endif
  }
  #endif

  #if (CELL2_ACTIVE)
  if (LoadCell_2.getTareTimeoutFlag()){
    brokenCellNumber = '2';
    #if (DEBUGGING_ACTIVE)
    Serial.println("Timeout, check MCU>HX711 no.2 wiring and pin designations");
    #endif
  }
  #endif

  #if (CELL3_ACTIVE)
  if (LoadCell_3.getTareTimeoutFlag()){
    brokenCellNumber = '3';
    #if (DEBUGGING_ACTIVE)
    Serial.println("Timeout, check MCU>HX711 no.3 wiring and pin designations");
    #endif
  }
  #endif

  #if (CELL4_ACTIVE)
  if (LoadCell_4.getTareTimeoutFlag()){
    brokenCellNumber = '4';
    #if (DEBUGGING_ACTIVE)
    Serial.println("Timeout, check MCU>HX711 no.4 wiring and pin designations");
    #endif
  }
  #endif

  return brokenCellNumber;
}

void setCellCalFactor(float calibrationValue1, float calibrationValue2, float calibrationValue3, float calibrationValue4){
  #if (CELL1_ACTIVE)
  LoadCell_1.setCalFactor(calibrationValue1);
  #endif

  #if (CELL2_ACTIVE)
  LoadCell_2.setCalFactor(calibrationValue2);
  #endif

  #if (CELL3_ACTIVE)
  LoadCell_3.setCalFactor(calibrationValue3);
  #endif

  #if (CELL4_ACTIVE)
  LoadCell_4.setCalFactor(calibrationValue4);
  #endif
}

float calculateTotal(float unitConversionRatio, float cell1Value, float cell2Value, float cell3Value, float cell4Value){
  return(cell1Value + cell2Value + cell3Value + cell4Value)/unitConversionRatio;
}

void tareCells(){
  #if (DEBUGGING_ACTIVE)
  Serial.println("Taring...");
  #endif

  #if (CELL1_ACTIVE)
  LoadCell_1.tare();
  #endif

  #if (CELL2_ACTIVE)
  LoadCell_2.tare();
  #endif

  #if (CELL3_ACTIVE)
  LoadCell_3.tare();
  #endif

  #if (CELL4_ACTIVE)
  LoadCell_4.tare();
  #endif

  #if (DEBUGGING_ACTIVE)
  Serial.println("Tare Complete");
  #endif

  Serial.println("t");
}

bool cellEnabled(){
  bool enabled = false;

  #if (CELL1_ACTIVE)
  enabled = true;
  #endif

  #if (CELL2_ACTIVE)
  enabled = true;
  #endif

  #if (CELL3_ACTIVE)
  enabled = true;
  #endif

  #if (CELL4_ACTIVE)
  enabled = true;
  #endif

  return enabled;
}

bool newDataReady(){
  bool ready = false;

  #if (CELL1_ACTIVE)
  if (LoadCell_1.update()) ready = true;
  #endif

  #if (CELL2_ACTIVE)
  if (LoadCell_2.update()) ready = true;
  #endif

  #if (CELL3_ACTIVE)
  if (LoadCell_3.update()) ready = true;
  #endif

  #if (CELL4_ACTIVE)
  if (LoadCell_4.update()) ready = true;
  #endif

  return ready;
}

void getCellValues(float &cell1Value, float &cell2Value, float &cell3Value, float &cell4Value){
  #if (CELL1_ACTIVE)
  cell1Value = LoadCell_1.getData();
  #endif
  
  #if (CELL2_ACTIVE)
  cell2Value = LoadCell_2.getData();
  #endif

  #if (CELL3_ACTIVE)
  cell3Value = LoadCell_3.getData();
  #endif

  #if (CELL4_ACTIVE)
  cell4Value = LoadCell_4.getData();
  #endif
}

float calculateWeightRatio(float zeroValue){
  bool resume = false;
  float totalWeightValue;
  float knownMass;
  float cell1Value, cell2Value, cell3Value, cell4Value;

  #if(DEBUGGING_ACTIVE)
  Serial.println("Place known weight on the scale and send the character 'w'");
  #endif

  while (!resume)
  {
    newDataReady();
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'w') {
        delay(5000);
        newDataReady();
        getCellValues(cell1Value, cell2Value, cell3Value, cell4Value);
        totalWeightValue = cell1Value + cell2Value + cell3Value + cell4Value;
        Serial.println("w");
        resume = true;
      }
    }
  }

  resume = false;

  #if (DEBUGGING_ACTIVE)
  Serial.print("Zero Value: ");
  Serial.print(zeroValue);
  Serial.print(" | Weight Value: ");
  Serial.println(totalWeightValue);
  Serial.println("Enter in the known weight (lbs)");
  #endif

  while (!resume)
  {
    if (Serial.available() > 0) {
      knownMass = Serial.parseFloat();
      if (knownMass != 0) {
        resume = true;
      }
    }
  }

  return ((totalWeightValue - zeroValue)/knownMass);
}

float averageListVal(float list[], int length){
  float total = 0;
  for (int i = 0; i < length; i++){
    total += list[i];
  }
  return total/length;
}

float calibrate()
{
  bool resume = false;
  float totalZeroValue;
  float totalWeightValue;
  float knownMass;
  float cell1Value, cell2Value, cell3Value, cell4Value;
  float calWeightRatios[NUMBER_OF_CAL_POR - 1];
  float avgWeightRatio;

  #if (DEBUGGING_ACTIVE)
  Serial.println("Clear the scale and send the character 'z'");
  #endif

  while (!resume)
  {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'z') {
        tareCells();
        newDataReady();
        getCellValues(cell1Value, cell2Value, cell3Value, cell4Value);
        totalZeroValue = cell1Value + cell2Value + cell3Value + cell4Value;
        resume = true;
      }
    }
  }

  resume = false;

  for (int i = 0; i < NUMBER_OF_CAL_POR - 1; i++)
  {
    calWeightRatios[i] = calculateWeightRatio(totalZeroValue);
  }

  avgWeightRatio = averageListVal(calWeightRatios, NUMBER_OF_CAL_POR - 1);

  #if (DEBUGGING_ACTIVE)
  Serial.print("Ratio: ");
  Serial.println(avgWeightRatio);
  #endif

  Serial.println("c");

  return avgWeightRatio;
}

void setup(){

  Serial.begin(57600); delay(10);

  #if (DEBUGGING_ACTIVE)
  Serial.println();
  Serial.println("Starting...");
  #endif

  if (!cellEnabled()){
    #if (DEBUGGING_ACTIVE)
    Serial.println("No Cells Active, please activate a cell");
    #endif
    Serial.println("a");
    delay(5000);
    exit(0);
  }
  else{

    char brokenCellNumber;

    // old value = 733.0; 
    float calibrationValue1 = 18704.12; 
    float calibrationValue2 = 18704.12; 
    float calibrationValue3 = 18704.12; 
    float calibrationValue4 = 18704.12; 

    initializeCells();

    startCells();

    brokenCellNumber = brokenCell();

    if (brokenCellNumber != NO_BROKEN_CELLS){
      Serial.print("Cell Start Failed: ");
      Serial.println(brokenCellNumber);
    }

    setCellCalFactor(calibrationValue1, calibrationValue2, calibrationValue3, calibrationValue4);

    #if DEBUGGING_ACTIVE
    Serial.println("Startup is complete");
    #endif
  }
}

void loop() {
  static bool dataReady = false;
  static float unitConversionRatio = 1;

  //increase value to slow down serial print activity
  const int serialPrintInterval = 100; 

  float cell1Value;
  float cell2Value;
  float cell3Value;
  float cell4Value;
  float totalValue;

  dataReady = newDataReady();

  if (dataReady) {
    if (millis() > t + serialPrintInterval) {
      
      getCellValues(cell1Value, cell2Value, cell3Value, cell4Value);

      #if (DEBUGGING_ACTIVE)
      Serial.print("1: ");
      Serial.print(cell1Value);
      Serial.print("  2: ");
      Serial.print(cell2Value);
      Serial.print("  3: ");
      Serial.print(cell3Value);
      Serial.print("  4: ");
      Serial.print(cell4Value);
      Serial.print("  Total: ");
      #endif

      totalValue = calculateTotal(unitConversionRatio, cell1Value, cell2Value, cell3Value, cell4Value);
      Serial.println(totalValue);

      dataReady = false;

      t = millis();
    }
  }

  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 't') {
      tareCells();
    }
    if (inByte == 'c') {
      unitConversionRatio = calibrate();
    }
  }

  #if (DEBUGGING_ACTIVE)
    
    #if (CELL1_ACTIVE)
    if (LoadCell_1.getTareStatus() == true) {
      Serial.println("Tare load cell 1 complete");
    }
    #endif

    #if (CELL2_ACTIVE)
    if (LoadCell_2.getTareStatus() == true) {
      Serial.println("Tare load cell 2 complete");
    }
    #endif

    #if (CELL3_ACTIVE)
    if (LoadCell_3.getTareStatus() == true) {
      Serial.println("Tare load cell 3 complete");
    }
    #endif

    #if (CELL4_ACTIVE)
    if (LoadCell_4.getTareStatus() == true) {
      Serial.println("Tare load cell 4 complete");
    }
    #endif
  #endif
}


