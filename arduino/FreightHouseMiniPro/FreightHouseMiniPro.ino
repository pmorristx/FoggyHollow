// ******** UNLESS YOU WANT ALL CV'S RESET UPON EVERY POWER UP
// ******** AFTER THE INITIAL DECODER LOAD REMOVE THE "//" IN THE FOLLOWING LINE!!
#define DECODER_LOADED

//#define DEBUG


#define SET_CV_Address       120	// THIS ADDRESS IS FOR SETTING CV'S Like a Loco
#define Accessory_Address    120	// THIS ADDRESS IS THE START OF THE SWITCHES RANGE
									// WHICH WILL EXTEND FOR 6 MORE SWITCH ADDRESSES
//  Function 0 turns stove on/off
//  Function 1 turns platform lights on/off
//  Function 2 turns inside light on/off
//  Function 3 turns deck light on/off
//  Function 4 dims platform lights
//  Function 5 dims inside light
//  Function 6 dims deck light
//  CV30 = Platform diming value
//  CV31 = Inside diming value
//  CV32 = Dock diming value

#include <NmraDcc.h>

// Analog pins = 3, 5, 6, 9, 10, 11
byte stovePins [] = {5, 6};
byte platformPins [] = {10, 11};
byte dockPin = 3;
byte insidePin = 9; 

int platformIterationLimit = 20;
int platformIteration = 0;
boolean platformTriggered = false;

boolean stoveOn = true; // On/Off flag for stove flicker set by function 0

boolean platformDim = true;
boolean insideDim = true;
boolean dockDim = true;
boolean platformOn = true;
boolean insideOn = true;
boolean dockOn = true;

boolean dimPhase = false;
int dimIter = 0;

byte fpins [] = {3,5,6,9,10, 11};

NmraDcc  Dcc ;
DCC_MSG  Packet ;

int t;                                    // temp

uint8_t CV_DECODER_MASTER_RESET =   30;  // THIS IS THE CV ADDRESS OF THE FULL RESET
#define CV_To_Store_SET_CV_Address	30
#define CV_Accessory_Address CV_ACCESSORY_DECODER_ADDRESS_LSB

struct CVPair
{
  uint16_t  CV;
  uint8_t   Value;
};
CVPair FactoryDefaultCVs [] =
{
  {CV_ACCESSORY_DECODER_ADDRESS_LSB, Accessory_Address & 0x00ff},
  {CV_ACCESSORY_DECODER_ADDRESS_MSB, Accessory_Address & 0xff00},
  {CV_MULTIFUNCTION_EXTENDED_ADDRESS_MSB, 0},
  {CV_MULTIFUNCTION_EXTENDED_ADDRESS_LSB, 0},
  {CV_DECODER_MASTER_RESET, 0},
  {CV_To_Store_SET_CV_Address, SET_CV_Address},
  {CV_To_Store_SET_CV_Address + 1, 0},
  {30,240}, // Platform dim
  {31,245}, // Inside dim
  {32,250}  // Dock dim
};

uint8_t FactoryDefaultCVIndex = sizeof(FactoryDefaultCVs) / sizeof(CVPair);
void notifyCVResetFactoryDefault()
{
  // Make FactoryDefaultCVIndex non-zero and equal to num CV's to be reset
  // to flag to the loop() function that a reset to Factory Defaults needs to be done
  FactoryDefaultCVIndex = sizeof(FactoryDefaultCVs) / sizeof(CVPair);
};

void setup()   //******************************************************
{
#ifdef DEBUG
  Serial.begin(115200);
  Serial.println ("Starting Setup");
#endif
  int i;
  uint8_t cv_value;

  // initialize the digital pins as outputs
  for (int i = 0; i < sizeof(fpins); i++) {
    pinMode(fpins[i], OUTPUT);
  }

  // Setup which External Interrupt, the Pin it's associated with that we're using
  Dcc.pin(0, 2, 0);
  // Call the main DCC Init function to enable the DCC Receiver
  Dcc.init( MAN_ID_DIY, 100, FLAGS_OUTPUT_ADDRESS_MODE | FLAGS_DCC_ACCESSORY_DECODER, CV_To_Store_SET_CV_Address);
  delay(800);
#ifdef DEBUG
  Serial.println ("Setup finished DCC init");
#endif 

#if defined(DECODER_LOADED)
  if ( Dcc.getCV(CV_DECODER_MASTER_RESET) == CV_DECODER_MASTER_RESET )
#endif

  {
    for (int j = 0; j < sizeof(FactoryDefaultCVs) / sizeof(CVPair); j++ )
      Dcc.setCV( FactoryDefaultCVs[j].CV, FactoryDefaultCVs[j].Value);
    digitalWrite(17, 1);
    delay (1000);
    digitalWrite(17, 0);
  }

  // Initialize lights on & dim
  
  exec_function(0, true); // Turn stove on
  exec_function(1, true); // Turn platform lights on
  exec_function(4, true); // Dim platform lights

  exec_function(2, true); // Turn inside lights on
  exec_function(5, true); // Dim inside lights

  exec_function(3, true); // Turn inside lights on
  exec_function(6, true); // Dim inside lights  
#ifdef DEBUG
  Serial.println ("Setup Complete");
#endif  
}

void loop()   //**********************************************************************
{
  //MUST call the NmraDcc.process() method frequently
  // from the Arduino loop() function for correct library operation
  Dcc.process();
  delay(8);

  //
  //  Flicker the stove -- stoveState is set by execFunction when function changes.  
  //  Turning off the function turns off the stove.  If the flag is HIGH, the stove
  //  will flicker here in the loop.
  if (stoveOn)
  {
    for (int i=0; i<sizeof(stovePins); i++)
    {
      int r = random(10);
  		if (r > 5)
  		{
  		  analogWrite(stovePins[i], random(0, 255));
  		}
    }
  }

  if (platformTriggered)
  {
    platformIterationLimit = int (random (20, 40));
    if (platformIteration++ > platformIterationLimit)
    {
      platformTriggered = false;
      FadeOnOff (platformPins[1], 1, platformDim, platformOn);
    }
  }

  if (stoveOn)
  {
      if (dimPhase)
      {
        analogWrite(5, 255);
        analogWrite(6, 255);
        dimPhase = !dimPhase;
      }
      else
      {
        if (dimIter++ > 1)
        {
          dimIter = 0;
          analogWrite (5,0);
          analogWrite (6,0);
          dimPhase = !dimPhase;
        }
        else
        {
          delay (int (random(8)));
        }
      }
  }
}

extern void notifyDccAccState( uint16_t Addr, uint16_t BoardAddr, uint8_t OutputAddr, uint8_t State) {
  uint16_t Current_Decoder_Addr;
  uint8_t Bit_State;
  uint8_t Bit_State_Orig;
  boolean functionIsOn;

  #ifdef DEBUG
      Serial.println ("In notifyDccAccState");
  #endif
  
  functionIsOn = (OutputAddr & 0x01) == 1;
  Current_Decoder_Addr = Dcc.getAddr();

#ifdef DEBUG
    Serial.print("Addr = ");
    Serial.println(Addr);
    Serial.print("Output Addr = ");
    Serial.println(OutputAddr);    
    Serial.print("Current Decoder Addr = ");
    Serial.println(Current_Decoder_Addr);
    Serial.print("BoardAddr = ");
    Serial.println(BoardAddr);
   
    Serial.print("State = ");
    Serial.println(State);

    Serial.print("FunctionIsOn = ");
    Serial.println(functionIsOn);    
#endif  


  
  Bit_State_Orig = OutputAddr & 0x01;
  if (Bit_State_Orig == 1) {
    Bit_State = LOW;
  } else {
    Bit_State = HIGH;
  }

  if ( Addr >= Current_Decoder_Addr && Addr < Current_Decoder_Addr + 17) { //Controls Accessory_Address+16
#ifdef DEBUG
    Serial.print("Addr = ");
    Serial.println(Addr);
    Serial.print("BoardAddr = ");
    Serial.println(BoardAddr);
    Serial.print("Bit_State_Orig = ");
    Serial.println(Bit_State_Orig);    
    Serial.print("Bit_State = ");
    Serial.println(Bit_State);
    Serial.print("FunctionIsOn = ");
    Serial.println(functionIsOn);    
#endif
    exec_function(Addr - Current_Decoder_Addr, functionIsOn );
  }
}

//
// Fade lights on/off.  Light may be dimmed by F4-6.
void FadeOnOff(int pinNo, int fNum, boolean isDim, boolean turnLightOn)
{
#define fadedelay 24
#define fadeSteps 5
#define increment 1
int maxBrightness;

	maxBrightness = 0;
	if (isDim)
	{
		maxBrightness = int(Dcc.getCV(29 + fNum));
	}

#ifdef DEBUG
	Serial.println ("Fade on/off...");
	Serial.print("pin = ");
	Serial.println(pinNo);
	Serial.print("isDim = ");
	Serial.println(isDim);
	Serial.print("turnLightOn = ");
	Serial.println(turnLightOn);
	Serial.print("maxBrightness = ");
	Serial.println(maxBrightness);
#endif 

	if (turnLightOn) // Turn on
	{
    int range = 255 - maxBrightness;
    int fadeStep = int(range / 4.);
    for (int i=4; i>=1; i--)
    {
      analogWrite(pinNo, max(maxBrightness, i*fadeStep));
      delay(5);
    }        
		analogWrite(pinNo, maxBrightness);
	}
	else // Turn off
	{
    int range = 255 - maxBrightness;
    int fadeStep = int(range / 4.);
    for (int i=1; i<=5; i++)
    {
      analogWrite(pinNo, maxBrightness + (i*fadeStep));
      delay(5);
    }   
		analogWrite(pinNo, 255);
	}
}

  
//  Function 0 turns stove on/off
//  Function 1 turns platform lights on/off
//  Function 2 turns inside light on/off
//  Function 3 turns deck light on/off
//  Function 4 dims platform lights
//  Function 5 dims inside light
//  Function 6 dims deck light

void exec_function(int function, boolean isFunctionOn)
{
#ifdef DEBUG
  Serial.println ("In Exec Function");
  Serial.print ("...function = ");
  Serial.println (function);
  Serial.print ("...isFunctionOn = ");
  Serial.println (isFunctionOn);
#endif
	switch (function)
	{
	case 0:   // Stove flicker on/off.  Turn off flickering or set flag and let loop maintain
    stoveOn = isFunctionOn;
		if (!stoveOn)
		{
		  for (int i=0; i<sizeof(stovePins); i++)
		  {
			  digitalWrite(stovePins[i], HIGH);
		  }
		}
		break;

  case 1 : // Platform lights on/off
    platformOn = isFunctionOn;
    platformIteration = 0;
    platformTriggered = true;
    FadeOnOff (platformPins[0], function, platformDim, platformOn);
    break;

  case 2 : // Inside Light on/off
    insideOn = isFunctionOn;  
    FadeOnOff (insidePin, function, insideDim, isFunctionOn);
    break;

  case 3 : // Deck Light on/off
    dockOn = isFunctionOn;  
    FadeOnOff (dockPin, function, dockDim, isFunctionOn);
    break;
    
	case 4 : // Platform lights dim
    platformDim = isFunctionOn; 
    if (platformOn)
    {
      for (int i=0; i<sizeof(platformPins); i++)
      {
        FadeOnOff (platformPins[i], 1, platformDim, true);
        delay (2000);
      }
    }
    break;    
  case 5 :
    insideDim = isFunctionOn; 
    FadeOnOff (insidePin, 2, insideDim, insideOn);        
    break;
  case 6 :
    dockDim = isFunctionOn;
    if (dockOn)
    {
      FadeOnOff (dockPin, 3, dockDim, true);        
    }    
		break;
   
	default:
		break;
	}
}
