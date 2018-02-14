/*

    Circuit:
      Loconet on pins 8 (RX on UNO) and 7 (TX) (via a LocoShield or similar)
 	  JMRI Sensors 52-56 input signal to move bridge to appropriate track (sensor number - 50)
 	  JMRI Sensors 57-61 output current position of bridge
*/

#include <LocoNet.h>

#define DEBUG


#define LN_TX_PIN 7 // Pro Mini
#define LN_RX_PIN 8

#define MOTOR_PIN 10
#define DIRECTION_PIN 11
#define MS1 12
// Skip LED pin 13
#define ENB 14
#define MS2 15
#define SLP 16

#define MANUAL_MOVE 17

byte sensorPins [] = {2, 3, 4, 5, 6}; // These will be HIGH when the switch is open; LOW when it is closed.

uint16_t inAddrs [] = {50, 51, 52, 53, 54}; // JMRI Sensor address used as a button to select which track to move to
uint16_t outAddrs[] = {55, 56, 57, 58, 59}; // JMRI sensor address to report when move is complete

byte lightPins[]      = {A5, A6, A7};
uint16_t lightAddrs[] = {60, 61, 62, 63}; 

boolean moving = false;

uint16_t lastOutState [] = {LOW, LOW, LOW, LOW, LOW, LOW};

// Loconet turnout position definitions to make code easier to read
#define TURNOUT_NORMAL     1  // aka closed
#define TURNOUT_DIVERGING  0  // thrown

int currentTrack;
int	requestedTrack;
#define halfCircle 800
uint16_t stepsBetweenTracks[5];

int cwSteps[5][5];
int ccwSteps[5][5];

int sensorOffset[5][2]; //  Number of steps to keep moving after reed switch activates 0->clockwise; 1->counterClockwise

lnMsg  *LnPacket;          // pointer to a received LNet packet

// Construct a Loconet packet that requests a turnout to set/change its state
void sendOPC_SW_REQ(int address, byte dir, byte on) {
  lnMsg SendPacket ;

  int sw2 = 0x00;
  if (dir == TURNOUT_NORMAL) {
    sw2 |= B00100000;
  }
  if (on) {
    sw2 |= B00010000;
  }
  sw2 |= (address >> 7) & 0x0F;

  SendPacket.data[ 0 ] = OPC_SW_REQ ;
  SendPacket.data[ 1 ] = address & 0x7F ;
  SendPacket.data[ 2 ] = sw2 ;

  LocoNet.send( &SendPacket );
}

// Some turnout decoders (DS54?) can use solenoids, this code emulates the digitrax
// throttles in toggling the "power" bit to cause a pulse
void setLNTurnout(int address, byte dir) {
  sendOPC_SW_REQ(address - 1, dir, 1);
  sendOPC_SW_REQ(address - 1, dir, 0);
}

void setup()
{
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(DIRECTION_PIN, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(SLP, OUTPUT);

  pinMode(MANUAL_MOVE, INPUT_PULLUP);

  for (int i=0; i<sizeof(lightPins); i++)
  {
    pinMode (lightPins[i], OUTPUT);
  }

  int stepsPerRevolution[4];
  stepsPerRevolution[0] = 200; // Full Step
  stepsPerRevolution[1] = 400; // Half Step
  stepsPerRevolution[2] = 800; // Quarter Setp
  stepsPerRevolution[3] = 1600; // Eight Step

  int stepMode = 2;
  int steps = 20/360 * stepsPerRevolution[stepMode];
  
  stepsBetweenTracks[0] = 68; // 18/360 * stepsPerRevolution[stepMode]; // Track 2 -> Track 3
  stepsBetweenTracks[1] = 72; // 18/360 * stepsPerRevolution[stepMode]; // Track 3 -> Track 4
  stepsBetweenTracks[2] = 76; // 18/360 * stepsPerRevolution[stepMode]; // Track 4 -> Track 5
  stepsBetweenTracks[3] = 952; // 238/360 * stepsPerRevolution[stepMode]; // Track 5 -> Track 6
  stepsBetweenTracks[4] = 462; // 114/360 * stepsPerRevolution[stepMode]; // Track 6 -> Track 2


  cwSteps[0][0] = halfCircle; // 180 degree rotate
  cwSteps[0][1] = stepsBetweenTracks[0];
  cwSteps[0][2] = stepsBetweenTracks[0] + stepsBetweenTracks[1];
  cwSteps[0][3] = stepsBetweenTracks[0] + stepsBetweenTracks[1] + stepsBetweenTracks[2]; 
  cwSteps[0][4] = stepsBetweenTracks[0] + stepsBetweenTracks[1] + stepsBetweenTracks[2] + stepsBetweenTracks[3];  

  cwSteps[1][0] = stepsBetweenTracks[4] + stepsBetweenTracks[1] + stepsBetweenTracks[2] + stepsBetweenTracks[3];  
  cwSteps[1][1] = halfCircle; // 180 degree rotate
  cwSteps[1][2] = stepsBetweenTracks[1];
  cwSteps[1][3] = stepsBetweenTracks[1] + stepsBetweenTracks[2]; 
  cwSteps[1][4] = stepsBetweenTracks[1] + stepsBetweenTracks[2] + stepsBetweenTracks[3];   

  cwSteps[2][0] = stepsBetweenTracks[2] + stepsBetweenTracks[3] + stepsBetweenTracks[4];
  cwSteps[2][1] = stepsBetweenTracks[2] + stepsBetweenTracks[3] +  stepsBetweenTracks[4] + stepsBetweenTracks[0]; 
  cwSteps[2][2] = halfCircle; // 180 degree rotate
  cwSteps[2][3] = stepsBetweenTracks[2]; 
  cwSteps[2][4] = stepsBetweenTracks[2] + stepsBetweenTracks[3]; 

  cwSteps[3][0] = stepsBetweenTracks[3] + stepsBetweenTracks[4];
  cwSteps[3][1] = stepsBetweenTracks[3] +  stepsBetweenTracks[4] + stepsBetweenTracks[0]; 
  cwSteps[3][2] = stepsBetweenTracks[3] +  stepsBetweenTracks[4] + stepsBetweenTracks[0] + stepsBetweenTracks[1];
  cwSteps[3][3] = halfCircle; // 180 degree rotate 
  cwSteps[3][4] = stepsBetweenTracks[3];  

  cwSteps[4][0] = stepsBetweenTracks[4];
  cwSteps[4][1] = stepsBetweenTracks[4] + stepsBetweenTracks[0]; 
  cwSteps[4][2] = stepsBetweenTracks[4] + stepsBetweenTracks[0] + stepsBetweenTracks[1];
  cwSteps[4][3] = stepsBetweenTracks[4] + stepsBetweenTracks[0] + stepsBetweenTracks[1] + stepsBetweenTracks[2];
  cwSteps[4][4] = halfCircle; // 180 degree rotate    

  ccwSteps[0][0] = halfCircle; // 180 degree rotate
  ccwSteps[0][1] = stepsBetweenTracks[4] + stepsBetweenTracks[3] + stepsBetweenTracks[2] + stepsBetweenTracks[1];
  ccwSteps[0][2] = stepsBetweenTracks[4] + stepsBetweenTracks[3] + stepsBetweenTracks[2];
  ccwSteps[0][3] = stepsBetweenTracks[4] + stepsBetweenTracks[3]; 
  ccwSteps[0][4] = stepsBetweenTracks[4];  

  ccwSteps[1][0] = stepsBetweenTracks[1]; 
  ccwSteps[1][1] = halfCircle; // 180 degree rotate
  ccwSteps[1][2] = stepsBetweenTracks[0] + stepsBetweenTracks[4] + stepsBetweenTracks[3] + stepsBetweenTracks[2]; 
  ccwSteps[1][3] = stepsBetweenTracks[0] + stepsBetweenTracks[4] + stepsBetweenTracks[3]; 
  ccwSteps[1][4] = stepsBetweenTracks[0] + stepsBetweenTracks[4];   

  ccwSteps[2][0] = stepsBetweenTracks[1] + stepsBetweenTracks[0];
  ccwSteps[2][1] = stepsBetweenTracks[1]; 
  ccwSteps[2][2] = halfCircle; // 180 degree rotate
  ccwSteps[2][3] = stepsBetweenTracks[1] +  stepsBetweenTracks[0] + stepsBetweenTracks[4] + stepsBetweenTracks[3]; 
  ccwSteps[2][4] = stepsBetweenTracks[1] +  stepsBetweenTracks[0] + stepsBetweenTracks[4]; 

  ccwSteps[3][0] = stepsBetweenTracks[2] + stepsBetweenTracks[1] + stepsBetweenTracks[0];
  ccwSteps[3][1] = stepsBetweenTracks[2] +  stepsBetweenTracks[1]; 
  ccwSteps[3][2] = stepsBetweenTracks[2];
  ccwSteps[3][3] = halfCircle; // 180 degree rotate 
  ccwSteps[3][4] = stepsBetweenTracks[2] + stepsBetweenTracks[1] + stepsBetweenTracks[0] + stepsBetweenTracks[4];  

  ccwSteps[4][0] = stepsBetweenTracks[3] + stepsBetweenTracks[2] + stepsBetweenTracks[1] + stepsBetweenTracks[0];
  ccwSteps[4][1] = stepsBetweenTracks[3] + stepsBetweenTracks[2] + stepsBetweenTracks[1]; 
  ccwSteps[4][2] = stepsBetweenTracks[3] + stepsBetweenTracks[2];
  ccwSteps[4][3] = stepsBetweenTracks[3];
  ccwSteps[4][4] = halfCircle; // 180 degree rotate 

  sensorOffset[0][0] = 4;
  sensorOffset[0][1] = 15;
  sensorOffset[1][0] = 0;
  sensorOffset[1][1] = 15;
  sensorOffset[2][0] = 5;
  sensorOffset[2][1] = 22;
  sensorOffset[3][0] = 0;
  sensorOffset[3][1] = 0;
  sensorOffset[4][0] = 6;
  sensorOffset[4][1] = 10;

  //
  // Microstep mode
  // MS1   MS2
  //  L     L    Full Step
  //  H     L    Half Step
  //  L     H    Quarter Step
  //  H     H    Eighth Step

  digitalWrite(MS1, LOW); // Set MS1 & MS2 High for eighth step mode
  digitalWrite(MS2, HIGH);
  digitalWrite(ENB, LOW); //Pull low to allow motor control
  digitalWrite(SLP, LOW); //Pull low to sleep

  currentTrack = 0;
  requestedTrack = -1;

  Serial.begin(115200);
  LocoNet.init(LN_TX_PIN);

  //  Read all of the reed switches to see if we can find the initial orientation of the turntable
  for (int i = 0; i < sizeof(sensorPins); i++)
  {
    pinMode(sensorPins[i], INPUT_PULLUP);
#ifdef DEBUG
    Serial.print (" Reading switch ");
    Serial.print (i);
    Serial.print (" value = ");
    Serial.println (digitalRead(sensorPins[i]));
#endif
    lastOutState[i] = digitalRead(sensorPins[i]);
//    digitalWrite (trackLEDPins[i], lastOutState[i]);

    // Report initial state of sensors to JMRI
    if (lastOutState[i] == LOW)
      LocoNet.reportSensor(outAddrs[i], HIGH);
    else
      LocoNet.reportSensor(outAddrs[i], LOW);
          
    LocoNet.reportSensor(inAddrs[i], LOW);

    if (digitalRead(sensorPins[i]) == LOW)
    {
      currentTrack = i;
    }
  }

  // None of the reed switches are active.  We need to move the bridge until one of them activates
  if (currentTrack == 0)
  {
    Serial.println ("Turntable setup searching for bridge orientation");

    digitalWrite(DIRECTION_PIN, LOW);
    digitalWrite(SLP, HIGH);
    delay(80);
    seekAnyTrack();
            
    digitalWrite(SLP, LOW);
    for (int i = 0; i < sizeof(sensorPins); i++)
    {
      if (digitalRead(sensorPins[i]) == LOW)
      {
        currentTrack = i;
      }
    }
  }
  else
  {
    Serial.print ("Turntable setup found bridge at track ");
    Serial.println (currentTrack);
  }

#ifdef DEBUG
  Serial.println ("Setup complete");
#endif
}


void seekAnyTrack()
{
    while ((digitalRead(sensorPins[0]) & digitalRead(sensorPins[1]) & digitalRead(sensorPins[2]) & digitalRead(sensorPins[3]) & digitalRead(sensorPins[4])) == HIGH)
    {
      digitalWrite(MOTOR_PIN, LOW);
      delay(2);
      digitalWrite(MOTOR_PIN, HIGH);
      delay(80);
    }

    int idx = 0;
    currentTrack = -1;
    while(idx < 5 && currentTrack < 0)
    {
      if (digitalRead(sensorPins[idx]) == LOW)
      {
        currentTrack = idx;
      }
      idx++;
    }

    for (int i=0; i<sensorOffset[idx][0]; i++)
    {
      digitalWrite(MOTOR_PIN, LOW);
      delay(2);
      digitalWrite(MOTOR_PIN, HIGH);
      delay(100);
    }
}

void seekTrack(byte sensorPin, int fudge)
{
    while (digitalRead(sensorPin) == HIGH)
    {
      digitalWrite(MOTOR_PIN, LOW);
      delay(2);
      digitalWrite(MOTOR_PIN, HIGH);
      delay(80);
    }

    for (int i=0; i<fudge; i++)
    {
      digitalWrite(MOTOR_PIN, LOW);
      delay(2);
      digitalWrite(MOTOR_PIN, HIGH);
      delay(100);
    }
}
//
//---------------------------------------------------------------------------------------
//
// loop
//
//---------------------------------------------------------------------------------------
//
void loop() {
  // Check for any received LocoNet packets
  LnPacket = LocoNet.receive() ;
  if ( LnPacket ) {
    LocoNet.processSwitchSensorMessage(LnPacket);
    // this function will call the specially named functions below...
  }

  // Check if any of the reed switches have changed.  If so, report new state
  for (int i = 0; i < sizeof(sensorPins); i++)
  {  
    if (digitalRead(sensorPins[i]) != lastOutState[i])
    {
      lastOutState[i] = digitalRead(sensorPins[i]);
      if (lastOutState[i] == LOW)
      {
        LocoNet.reportSensor(outAddrs[i], HIGH);
        currentTrack = i; // In case bridge was manually moved
      }
      else
      {
        LocoNet.reportSensor(outAddrs[i], LOW);  
      }    
    }
  }

  //
  // Manually move motor to count steps
  if (digitalRead(MANUAL_MOVE) == LOW)
  {
	  int count = 0;
	  while (digitalRead(MANUAL_MOVE) == LOW)
	  {
		  moveMotor(1, true, -1);
		  count = count + 1;
	  }
	  Serial.print ("--- MOVED MOTOR ");
	  Serial.print (count);
	  Serial.print (" steps ---- ");
  }
}

//
//---------------------------------------------------------------------------------------
//
// moveMotor
//
//---------------------------------------------------------------------------------------
//
void moveMotor(int steps, boolean rotateClockWise, int sensorIdx)
{
  int count = 0;


  int direction = 0;
  if (rotateClockWise)
  {
    digitalWrite(DIRECTION_PIN, LOW);
    direction = 0;
  }
  else
  {
    digitalWrite(DIRECTION_PIN, HIGH);
    direction = 1;
  }
  delay(500);
  
  Serial.print ("In moveMotor, steps = ");
  Serial.println(steps);

  digitalWrite(SLP, HIGH);
  delay(500);
  if (sensorIdx < 0 || steps == halfCircle)
  {
    for (int i=0; i<steps; i++)
    {
      digitalWrite(MOTOR_PIN, LOW);
      delay(2);
      digitalWrite(MOTOR_PIN, HIGH);
      delay(80);
    }
  }
  else
  {
    seekTrack(sensorPins[sensorIdx], sensorOffset[sensorIdx][direction]);
  }
  digitalWrite(SLP, LOW);
}


// Callbacks from LocoNet.processSwitchSensorMessage() ...
// We tie into the ones connected to turnouts so we can capture anything
// that can change (or indicatea change to) a turnout's position.

//
//---------------------------------------------------------------------------------------
//
// notifyPower - used to trigger reporting of sensor state when JMRI powers up.
//
//---------------------------------------------------------------------------------------
//
void notifyPower (uint8_t state)
{
  if (state)
  {
  for (int i = 0; i < sizeof(sensorPins); i++)
  {
      LocoNet.reportSensor(outAddrs[currentTrack], LOW);  // Turn off inactive track sensors
  }
  LocoNet.reportSensor(outAddrs[currentTrack], HIGH);  // Turn on JMRI sensor on turntable
}

//
//---------------------------------------------------------------------------------------
//
// notifySensor
//
//---------------------------------------------------------------------------------------
//
void notifySensor( uint16_t address, uint8_t state )
{
  //  Input from JMRI
  // Request to move turntable; otherwise an output sensor changed.
/*
  if (address >= lightAddrs[0] && address <= lightAddrs[3])
  {
    if (address == lightAddrs[0])
    {
      // Turn on/off all three turntable lights
      fadeAllLightsOnOff(state);
    }
    else
    {
      // Turn on/off a specified turntable light
      fadeOnOff(lightPins[address-lightAddrs[1]], state);
    }
  }
  */
  if (((address >= inAddrs[0]) && (address <= inAddrs[4])) && (state != 0) && !moving)
  {
    moving = true;
    // fadeAllLightsOnOff(LOW);
    requestedTrack = address - inAddrs[0];

#ifdef DEBUG
    Serial.print ("In notifySensor, State changed, new State = ");
    Serial.print (state);
    Serial.print (" currentTrack = ");
    Serial.print (currentTrack);
    Serial.print (" requestedTrack = ");
    Serial.print (requestedTrack);
    Serial.print (" address = ");
    Serial.println(address);
#endif

    LocoNet.reportSensor(outAddrs[currentTrack], LOW);
   

    //  Move motor the shorter direction
    int steps = 0;

    if (cwSteps[currentTrack][requestedTrack] < ccwSteps[currentTrack][requestedTrack])
    {
      moveMotor(cwSteps[currentTrack][requestedTrack], true, requestedTrack);
      steps = cwSteps[currentTrack][requestedTrack];
    }
    else
    {
      moveMotor(ccwSteps[currentTrack][requestedTrack], false, requestedTrack);
      steps = ccwSteps[currentTrack][requestedTrack];
    }
    
    #ifdef DEBUG
        Serial.print ("Moved motor ");
        Serial.print (steps);
        Serial.print (" steps from Track ");
        Serial.print (currentTrack);
        Serial.print (" to ");
        Serial.print (requestedTrack);

        Serial.print (" --- CW Steps = ");
        Serial.print (cwSteps[currentTrack][requestedTrack]);
        Serial.print (" CCW Steps = ");
        Serial.println (ccwSteps[currentTrack][requestedTrack]);
    #endif
    
    currentTrack = requestedTrack;
    LocoNet.reportSensor(outAddrs[currentTrack], HIGH);  // Turn on JMRI sensor on turntable
    LocoNet.reportSensor(address, LOW);  // Turn off the sensor on the UI that activated this move

    // fadeAllLightsOnOff(HIGH);
    moving = false;
  }
}

void notifySwitchRequest( uint16_t Address, uint8_t Output, uint8_t Direction )
{
#ifdef DEBUG
  Serial.print ("In notifySwitchRequest, Address = ");
  Serial.print (Address);
  Serial.print (" Output = ");
  Serial.print (Output);
  Serial.print (" Direction = ");
  Serial.println (Direction);
#endif
}

void notifySwitchReport( uint16_t Address, uint8_t Output, uint8_t Direction )
{
#ifdef DEBUG
  Serial.print ("In notifySwitchReport, Address = ");
  Serial.print (Address);
  Serial.print (" Output = ");
  Serial.print (Output);
  Serial.print (" Direction = ");
  Serial.println (Direction);
#endif
}

void notifySwitchState( uint16_t Address, uint8_t Output, uint8_t Direction )
{
#ifdef DEBUG
  Serial.print ("In notifySwitchState, Address = ");
  Serial.print (Address);
  Serial.print (" Output = ");
  Serial.print (Output);
  Serial.print (" Direction = ");
  Serial.println (Direction);
#endif
}

void fadeAllLightsOnOff(int state)
{
  for (int l=0; l<sizeof(lightPins); l++)
  {
    fadeOnOff(lightPins[l], state);
    delay(3000);
  }
}

void fadeOnOff(int lightPin, int state)
{
  #define fadedelay 24
  if (state == LOW) 
  {
    #ifdef DEBUG
        Serial.print("Turning fade ON, pin = ");
        Serial.println(lightPin);
    #endif
    for (int t = 0; t < 3; t += 1)
    {
      digitalWrite( lightPin, LOW);         
      delay(fadedelay * (t / 3));
      digitalWrite( lightPin, HIGH);          
      delay(fadedelay - (fadedelay * (t / 3)));
    }
    digitalWrite( lightPin,  LOW );
  } else {
    #ifdef DEBUG
        Serial.print("Turning fade OFF, pin = ");
        Serial.println(lightPin);
    #endif        
    if (state == HIGH)
    {
      for (int t = 0; t < 3; t += 1)
      {
        digitalWrite( lightPin, HIGH);          
        delay(fadedelay * (t / 3));
        digitalWrite( lightPin, LOW);           
        delay(fadedelay - (fadedelay * (t / 3)));
      }
      digitalWrite(lightPin, HIGH);
    }
  }  
}

