//-------------------------------------------------------------------------------------
// ScoutScale_Firmware.ino
// Alex Lueddecke February 2024
//-------------------------------------------------------------------------------------

#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

const bool debugging_active = true;

const bool HX711_cell1_active = true;
const bool HX711_cell2_active = true;
const bool HX711_cell3_active = true;
const bool HX711_cell4_active = true;

// Pins for table 3, 4, 8, 12
// Clock Pin 2

//pins:
const int common_clock = 2;

const int HX711_data1 = 3;
const int HX711_data2 = 4;
const int HX711_data3 = 8;
const int HX711_data4 = 12; 

//HX711 constructor (dout pin, sck pin)
HX711_ADC LoadCell_1(HX711_data1, common_clock); 
HX711_ADC LoadCell_2(HX711_data2, common_clock); 
HX711_ADC LoadCell_3(HX711_data3, common_clock); 
HX711_ADC LoadCell_4(HX711_data4, common_clock); 

// // eeprom adress for calibration value load cell 1 (4 bytes)
// const int calVal_eepromAdress_1 = 0; 
// const int calVal_eepromAdress_2 = 4; 
// const int calVal_eepromAdress_3 = 8; 
// const int calVal_eepromAdress_4 = 12; 

// weight ratio
float weight_ratio = 1;


unsigned long t = 0;

void setup() {
  Serial.begin(57600); delay(10);
  if (debugging_active){ 
    Serial.println();
    Serial.println("Starting...");
  }

  float calibrationValue_1; // calibration value load cell 1
  float calibrationValue_2; // calibration value load cell 2
  float calibrationValue_3; // calibration value load cell 1
  float calibrationValue_4; // calibration value load cell 2

  // if these values are 0 then it outputs infinite
  // uncomment this if you want to set this value in the sketch
  calibrationValue_1 = 18704.12; 
  calibrationValue_2 = 18704.12; 
  calibrationValue_3 = 18704.12; 
  calibrationValue_4 = 18704.12;

  // calibrationValue_1 = 733.0; 
  // calibrationValue_2 = 733.0; 
  // calibrationValue_3 = 733.0; 
  // calibrationValue_4 = 733.0;

  if (HX711_cell1_active)
  {
    LoadCell_1.begin();
    LoadCell_1.setReverseOutput();
  }

  if (HX711_cell2_active)
  {
    LoadCell_2.begin();
    LoadCell_2.setReverseOutput();
  }

  if (HX711_cell3_active)
  {
    LoadCell_3.begin();
    LoadCell_3.setReverseOutput();
  }

  if (HX711_cell4_active)
  {
    LoadCell_4.begin();
    LoadCell_4.setReverseOutput();
  }

  unsigned long stabilizingtime = 2000; // tare preciscion can be improved by adding a few seconds of stabilizing time

  boolean _tare = true; //set this to false if you don't want tare to be performed in the next step

  byte loadcell_1_rdy = 0;
  byte loadcell_2_rdy = 0;
  byte loadcell_3_rdy = 0;
  byte loadcell_4_rdy = 0;

  int number_of_active_loadcells = 0;

  if (HX711_cell1_active)
  {
    number_of_active_loadcells++;
  }

  if (HX711_cell2_active)
  {
    number_of_active_loadcells++;
  }

  if (HX711_cell3_active)
  {
    number_of_active_loadcells++;
  }

  if (HX711_cell4_active)
  {
    number_of_active_loadcells++;
  }

  while ((loadcell_1_rdy + loadcell_2_rdy + loadcell_3_rdy + loadcell_4_rdy) < number_of_active_loadcells) { //run startup, stabilization and tare, both modules simultaniously
    if (HX711_cell1_active)
    {
      if (!loadcell_1_rdy) loadcell_1_rdy = LoadCell_1.startMultiple(stabilizingtime, _tare);
    }

    if (HX711_cell2_active)
    {
      if (!loadcell_2_rdy) loadcell_2_rdy = LoadCell_2.startMultiple(stabilizingtime, _tare);
    }

    if (HX711_cell3_active)
    {
      if (!loadcell_3_rdy) loadcell_3_rdy = LoadCell_3.startMultiple(stabilizingtime, _tare);
    }

    if (HX711_cell4_active)
    {
      if (!loadcell_4_rdy) loadcell_4_rdy = LoadCell_4.startMultiple(stabilizingtime, _tare);
    }
  }

  if (HX711_cell1_active)
  {
    if (LoadCell_1.getTareTimeoutFlag()) {
      if (debugging_active) {Serial.println("Timeout, check MCU>HX711 no.1 wiring and pin designations");}
    }
    LoadCell_1.setCalFactor(calibrationValue_1); // user set calibration value (float)
  }

  if (HX711_cell2_active)
  {
    if (LoadCell_2.getTareTimeoutFlag()) {
      if (debugging_active) {Serial.println("Timeout, check MCU>HX711 no.2 wiring and pin designations");}
    }
    LoadCell_2.setCalFactor(calibrationValue_1); // user set calibration value (float)
  }

  if (HX711_cell3_active)
  {
    if (LoadCell_3.getTareTimeoutFlag()) {
      if (debugging_active) {Serial.println("Timeout, check MCU>HX711 no.3 wiring and pin designations");}
    }
    LoadCell_3.setCalFactor(calibrationValue_3); // user set calibration value (float)
  }

  if (HX711_cell4_active)
  {
    if (LoadCell_4.getTareTimeoutFlag()) {
      if (debugging_active) {Serial.println("Timeout, check MCU>HX711 no.4 wiring and pin designations");}
    }
    LoadCell_4.setCalFactor(calibrationValue_4); // user set calibration value (float)
  }

  if (debugging_active) {Serial.println("Startup is complete");}
}

float weight_lbs(float cell1_value, float cell2_value, float cell3_value, float cell4_value)
{
  float total = 0;

  // if (cell1_value > 0)
  // {
  //   total += cell1_value;
  // }
  
  // if (cell2_value > 0)
  // {
  //   total += cell2_value;
  // }

  // if (cell3_value > 0)
  // {
  //   total += cell3_value;
  // }

  // if (cell4_value > 0)
  // {
  //   total += cell4_value;
  // } 

  total =  cell1_value + cell2_value + cell3_value + cell4_value;
  
  return total/weight_ratio;
}

void update_load_cells()
{
  if (HX711_cell1_active)
  {
    LoadCell_1.update();
  }

  if (HX711_cell2_active)
  {
    LoadCell_2.update();
  }

  if (HX711_cell3_active)
  {
    LoadCell_3.update();
  }

  if (HX711_cell4_active)
  {
    LoadCell_4.update();
  }
}

void tare_loadcells()
{
  if (HX711_cell1_active)
  {
    LoadCell_1.tare();
  }

  if (HX711_cell2_active)
  {
    LoadCell_2.tare();
  }
  if (HX711_cell3_active)
  {
    LoadCell_3.tare();
  }

  if (HX711_cell4_active)
  {
    LoadCell_4.tare();
  }
}

float calibrate()
{
  bool resume = false;
  float total_zero_value = 0;
  float total_weight_value = 0;
  float known_mass = 0;
  float cell1_value, cell2_value, cell3_value, cell4_value;

  tare_loadcells();

  if (debugging_active)
  {
    Serial.println("Clear the scale and send the character 'z'");
  }

  while (!resume)
  {
    update_load_cells();
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'z') {
        // check for new data/start next conversion

        if (HX711_cell1_active)
        {
          cell1_value = LoadCell_1.getData();

          if(cell1_value > 0)
          {
            total_zero_value += cell1_value;
          }

        }

        if (HX711_cell2_active)
        {
          cell2_value = LoadCell_2.getData();
          if(cell2_value > 0)
          {
            total_zero_value += cell2_value;
          }
        }
        if (HX711_cell3_active)
        {
          cell3_value = LoadCell_3.getData();
          if(cell3_value > 0)
          {
            total_zero_value += cell3_value;
          }
        }

        if (HX711_cell4_active)
        {
          cell4_value = LoadCell_4.getData();
          if(cell4_value > 0)
          {
            total_zero_value += cell4_value;
          }
        }
        resume = true;
      }
    }
  }

  resume = false;

  if (debugging_active)
  {
    Serial.println("Place known weight on the scale and send the character 'w'");
  }

  while (!resume)
  {
    update_load_cells();
    //Serial.print(LoadCell_4.getData();
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'w') {
        // check for new data/start next conversion
        if (HX711_cell1_active)
        {

          cell1_value = LoadCell_1.getData();
          if(cell1_value > 0)
          {
            total_weight_value += cell1_value;
          }
        }

        if (HX711_cell2_active)
        {
          cell2_value = LoadCell_2.getData();
          if(cell2_value > 0)
          {
            total_weight_value += cell2_value;
          }
        }

        if (HX711_cell3_active)
        {
          cell3_value = LoadCell_3.getData();
          if(cell3_value > 0)
          {
            total_weight_value += cell3_value;
          }
        }

        if (HX711_cell4_active)
        {
          cell4_value = LoadCell_4.getData();
          if(cell4_value > 0)
          {
            total_weight_value += cell4_value;
          }
        }
        resume = true;
      }
    }
  }

  resume = false;

  if (debugging_active)
  {
    Serial.print("Zero Value: ");
    Serial.print(total_zero_value);
    Serial.print(" | Weight Value: ");
    Serial.println(total_weight_value);
    Serial.println("Enter in the known weight (lbs)");
  }

  while (!resume)
  {
    if (Serial.available() > 0) {
      known_mass = Serial.parseFloat();
      if (known_mass != 0) {
        Serial.println("c");
        resume = true;
      }
    }

  }

  weight_ratio = ((total_weight_value - total_zero_value)/known_mass);

  if (debugging_active)
  {
    Serial.print("Ratio: ");
    Serial.println(weight_ratio);
  }
}



void loop() {
  static boolean newDataReady = 0;
  const int serialPrintInterval = 100; //increase value to slow down serial print activity
  float cell1_value = 0;
  float cell2_value = 0;
  float cell3_value = 0;
  float cell4_value = 0;
  float total_value;


  // check for new data/start next conversion
  if (HX711_cell1_active)
  {
    if (LoadCell_1.update()) newDataReady = true;
  }

  if (HX711_cell2_active)
  {
    if (LoadCell_2.update()) newDataReady = true;
  }

  if (HX711_cell3_active)
  {
    if (LoadCell_3.update()) newDataReady = true;
  }

  if (HX711_cell4_active)
  {
    if (LoadCell_4.update()) newDataReady = true;
  }

  //get smoothed value from data set
  if ((newDataReady)) {
    if (millis() > t + serialPrintInterval) {
      
      total_value  = 0;

      if (HX711_cell1_active)
      {
        cell1_value = LoadCell_1.getData();
        //total_value += cell1_value;
        if (debugging_active){
          Serial.print("1: ");
          Serial.print(cell1_value);
        }
      }

      if (HX711_cell2_active)
      {
        cell2_value = LoadCell_2.getData();
        //total_value += cell2_value;
        if (debugging_active){
          Serial.print("  2: ");
          Serial.print(cell2_value);
        }
      }
            
      if (HX711_cell3_active)
      {
        cell3_value = LoadCell_3.getData();
        //total_value += cell3_value;
        if (debugging_active){
          Serial.print("  3: ");
          Serial.print(cell3_value);
        }
      }
      
      if (HX711_cell4_active)
      {
        cell4_value = LoadCell_4.getData();
        //total_value += cell4_value;
        if (debugging_active){
          Serial.print("  4: ");
          Serial.print(cell4_value);
        }
      }

      if (debugging_active) 
      {
        Serial.print("  Total: ");
      }
      
      total_value = weight_lbs(cell1_value, cell2_value, cell3_value, cell4_value);
      Serial.print(total_value);

      if (debugging_active) 
      {
        Serial.print(" | Weight Ratio: ");
        Serial.println(weight_ratio);
      }

      newDataReady = 0;

      t = millis();
    }
  }

  // receive command from serial terminal, send 't' to initiate tare operation:
  if (Serial.available() > 0) {
    char inByte = Serial.read();
    if (inByte == 't') {
      tare_loadcells();
    }
    if (inByte == 'c') {
      calibrate();
    }
  }

  if (debugging_active){
    //check if last tare operation is complete
    if (HX711_cell1_active)
    {
      if (LoadCell_1.getTareStatus() == true) {
        Serial.println("Tare load cell 1 complete");
      }
    }

    if (HX711_cell2_active)
    {
      if (LoadCell_2.getTareStatus() == true) {
        Serial.println("Tare load cell 2 complete");
      }
    }
    if (HX711_cell3_active)
    {
      if (LoadCell_3.getTareStatus() == true) {
        Serial.println("Tare load cell 3 complete");
      }
    }

    if (HX711_cell4_active)
    {
      if (LoadCell_4.getTareStatus() == true) {
        Serial.println("Tare load cell 4 complete");
      }
    }
  }
}


