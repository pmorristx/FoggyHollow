#include <NmraDcc.h>

// ******** UNLESS YOU WANT ALL CV'S RESET UPON EVERY POWER UP
// ******** AFTER THE INITIAL DECODER LOAD REMOVE THE "//" IN THE FOOLOWING LINE!!
//#define DECODER_LOADED

//  Function 0 turns stove on/off
//  Function 1 turns platform lights on/off
//  Function 2 turns waiting room lights on/off
//  Function 3 turns office light on/off
//  Function 4 turns sign lights on/off
//  Function 5 turns indicators on/off
//  Function 6 dims platform lights
//  Function 7 dims waiting room lights;
//  CV30 = Platform dimming value
//  CV31 = Inside dimming value

#define DEBUG

#include <NmraDcc.h>


// Analog pins = 3, 5, 6, 9, 10, 11
byte signPins [] = {8,16};
byte officePin = 4;
byte waitingRoomPins [] = {10, 11};
byte stovePins [] = {12, 13, 14, 15};
byte platformPins [] = {3,9};

boolean stoveOn = true;
boolean stovePhase[] = {false, false, false, false};

long indicatorTimer = 0;
boolean indicatorsOn = true; 	// on/off flag for GH indicators set by function 1
int indicatorState = 0; 		// 0-> off; 1-> one on; 2-> red on
byte bluePin1 = 5;
byte bluePin2 = 6;
byte redPin = 7;
byte activeBluePin = bluePin1;
byte inactiveBluePin = bluePin2;
boolean indicatorBlinkState = false;
byte indicatorPins[] = {5,6,7};
long timerLimit = 3000;

boolean platformOn = false;
boolean platformDim = false;

boolean waitingRoomOn = false;
boolean waitingRoomDim = false;

boolean gh1Blink = false;
boolean gh2Blink = false;
boolean ghrBlink = false;
uint16_t gh1Timer = 0;
uint16_t gh2Timer = 0;
uint16_t ghrTimer = 0;
boolean gh1BlinkState = false;
boolean gh2BlinkState = false;
boolean ghrBlinkState = false;

int flickerState = HIGH; // On/Off flag for stove flicker set by function 0

byte fpins [] = {3,4,5,6,7,8, 9,12, 13, 14, 15, 16, 17, 18, 19};

NmraDcc  Dcc ;
DCC_MSG  Packet ;

int t;                                    // temp
#define SET_CV_Address       100           // THIS ADDRESS IS FOR SETTING CV'S Like a Loco - default was 24
#define Accessory_Address    100           // THIS ADDRESS IS THE START OF THE SWITCHES RANGE - default was 40
// WHICH WILL EXTEND FOR 16 MORE SWITCH ADDRESSES
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
  {CV_ACCESSORY_DECODER_ADDRESS_LSB, Accessory_Address},
  {CV_ACCESSORY_DECODER_ADDRESS_MSB, 0},
  {CV_MULTIFUNCTION_EXTENDED_ADDRESS_MSB, 0},
  {CV_MULTIFUNCTION_EXTENDED_ADDRESS_LSB, 0},
  {CV_DECODER_MASTER_RESET, 0},
  {CV_To_Store_SET_CV_Address, SET_CV_Address},
  {CV_To_Store_SET_CV_Address + 1, 0},
  {30,200}, // Platform dim
  {31,200} // Inside dim  
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
    digitalWrite(fpins[i], HIGH);
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
#ifdef DEBUG
  Serial.println ("Setup Complete");
#endif  
}
void doIndicators()
{
	indicatorTimer++;  
	switch (indicatorState)
	{
	case 0: // Indicators off.  Randomly turn one of the blue LEDs on
		if (indicatorTimer*8 > timerLimit )
		{
      // Randomly pick which blue LED to light
			activeBluePin = bluePin1;
      inactiveBluePin = bluePin2;
			if ((int(random(100)) % 2) == 0)  
			{
				activeBluePin = bluePin2;
        inactiveBluePin = bluePin1;
			}
			digitalWrite (activeBluePin, LOW); // Turn blue indicator on steady
     
			timerLimit = random (1000,2000) * 60;  // Random wait time between 1 & 2 minutes
			indicatorTimer = 0;
			indicatorState = 1;
      indicatorBlinkState = true;
		}
		break;

  case 1:  // Change the steady blue indicator to blinking on 1 second interval.
    if (indicatorTimer*8 > timerLimit) // Move to next state
    {
      indicatorState = 2;
    }
    else
    {
      if (indicatorTimer % 128 == 0) // Blink the LED.  Every 8 times through the loop turn the LED on or off
      {
        if (!indicatorBlinkState)
        {
          digitalWrite(activeBluePin, HIGH);
        }
        else
        {
          digitalWrite(activeBluePin, LOW);
        }
        indicatorBlinkState = !indicatorBlinkState;
      }
    }
    break;

  case 2: // Turn other blue indicator on.
    digitalWrite(inactiveBluePin, LOW);
    indicatorTimer = 0;
    timerLimit = random (2000, 10000);
    indicatorState = 3;
  
	case 3:
		if (indicatorTimer*8 > timerLimit ) // Turn both blue indicators off.  Turn red indicator on
		{
			digitalWrite (bluePin1, HIGH);
			digitalWrite (bluePin2, HIGH);
			digitalWrite (redPin, LOW);
      indicatorTimer = 0;
			timerLimit = random (5000,8000) * 30;  // Random wait time between 5 & 8 minutes
			indicatorState = 4;
		}
		break;
    
	case 4: // Turn all indicators off.
		if (indicatorTimer*8 > timerLimit )
		{
			digitalWrite (bluePin1, HIGH);
			digitalWrite (bluePin2, HIGH);
			digitalWrite (redPin, HIGH);
      indicatorTimer = 0;
			timerLimit = random (3000,8000) * 30;  // Random wait time between 5 & 8 minutes
			indicatorState = 0;
		}
		break;
	}
}

void loop()   //**********************************************************************
{
  //MUST call the NmraDcc.process() method frequently
  // from the Arduino loop() function for correct library operation
  Dcc.process();
  delay(8);

  if (stoveOn)
  {
    for (int i=0; i<sizeof(stovePins); i++)
    {
      if (random(1,100) > 50) // Change phase (on/off) of LED
      {
        if (stovePhase[i])
        {
    		  digitalWrite(stovePins[i], HIGH);
        }
        else
        {
          digitalWrite(stovePins[i], LOW);          
        }
        stovePhase[i] = !stovePhase[i];
      }
    }
  }

  if (indicatorsOn)
  {
	  doIndicators();
  }

  if (gh1Blink)
  {
	  if (gh1Timer++ % 128 == 0) // Blink the LED.  Every 8 times through the loop turn the LED on or off
	  {
		  if (!gh1BlinkState)
		  {
			  digitalWrite(bluePin1, HIGH);
		  }
		  else
		  {
			  digitalWrite(bluePin1, LOW);
		  }
		  gh1BlinkState = !gh1BlinkState;
		  gh1Timer = 0;
	  }
  }

  if (gh2Blink)
  {
	  if (gh2Timer++ % 128 == 0) // Blink the LED.  Every 8 times through the loop turn the LED on or off
	  {
		  gh2Timer = 0;
		  if (!gh2BlinkState)
		  {
			  digitalWrite(bluePin2, HIGH);
		  }
		  else
		  {
			  digitalWrite(bluePin2, LOW);
		  }
		  gh2BlinkState = !gh2BlinkState;
	  }
  }

  if (ghrBlink)
  {
	  if (ghrTimer++ % 128 == 0) // Blink the LED.  Every 8 times through the loop turn the LED on or off
	  {
		  ghrTimer = 0;
		  if (!ghrBlinkState)
		  {
			  digitalWrite(redPin, HIGH);
		  }
		  else
		  {
			  digitalWrite(redPin, LOW);
		  }
		  ghrBlinkState = !ghrBlinkState;
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
    executeDccFunction(Addr - Current_Decoder_Addr, functionIsOn );
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


//
//  Execute the DCC function sent...
void executeDccFunction(int function, boolean isFunctionOn)
{
#ifdef DEBUG
  Serial.println ("In Exec Function");
  Serial.print ("...function = ");
  Serial.println (function);
  Serial.print ("...isFunctionOn = ");
  Serial.println (isFunctionOn);
#endif

#define fadedelay 24
#define fadestop 5
#define increment 1

	byte pin;

	byte state = HIGH;
	if (isFunctionOn)
	{
		state = LOW;
	}

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

	case 1: // Platform lights
	    platformOn = isFunctionOn;
      for (int i=0; i<sizeof(platformPins); i++)
      {
	      FadeOnOff (platformPins[i], function, platformDim, platformOn);
        //delay (random(500, 3000));
      }
		break;

	case 2: // Waiting room lights
      waitingRoomOn = isFunctionOn;
      for (int i=0; i<sizeof(waitingRoomPins); i++)
      {
        FadeOnOff (waitingRoomPins[i], function, waitingRoomDim, waitingRoomOn);
        //delay (random(500, 3000));
      }  
		break;

	case 3: // Office light
		digitalWrite(officePin, state);
		break;

	case 4: // Sign lights
		for (int i=0; i<sizeof(signPins); i++)
		{
			digitalWrite(signPins[i], state);
		}
		break;

	case 5: // GH Indicators on/off
		indicatorsOn = isFunctionOn;

		if (!indicatorsOn)
		{
		  for (int i=0; i<sizeof(indicatorPins); i++)
		  {
			  digitalWrite(indicatorPins[i], HIGH);
		  }
      indicatorState = 0;
      indicatorTimer = 0;
		}
		else
		{
			indicatorState = 0;
			indicatorTimer = 0;
			timerLimit = random (3000,5000);  // Random wait time between 3 & 5 minutes
		}
		break;

  case 6 : // Platform lights dim
    platformDim = isFunctionOn; 
    if (platformOn)
    {
      for (int i=0; i<sizeof(platformPins); i++)
      {
        FadeOnOff (platformPins[i], 1, platformDim, true);
        //delay (2000);
      }
    }
    break;  
    
  case 7 : // Waiting room lights dim
    waitingRoomDim = isFunctionOn; 
    if (waitingRoomOn)
    {
      for (int i=0; i<sizeof(waitingRoomPins); i++)
      {
        FadeOnOff (waitingRoomPins[i], 2, waitingRoomDim, true);
        //delay (2000);
      }
    }
    break;    

  case 8: // GH1 Indicator
    digitalWrite(bluePin1, state);
    break;

  case 9: // GHR Indicator
    digitalWrite(redPin, state);
    break;

  case 10: // GH2 Indicator
    digitalWrite(bluePin2, state);
    break;
  case 11: // GH1 Blink
	  gh1Blink = isFunctionOn;
	  if (isFunctionOn)
	  {
		  gh1Timer = 0;
		  gh1BlinkState = false;
	  }
	  else
	  {
		  digitalWrite(bluePin1, HIGH);
	  }
	  break;
  case 12: // GHR Blink
	  ghrBlink = isFunctionOn;
	  if (isFunctionOn)
	  {
		  ghrTimer = 0;
		  ghrBlinkState = false;
	  }
	  else
	  {
		  digitalWrite(redPin, HIGH);
	  }
	  break;
  case 13: // GH2 Blink
	  gh2Blink = isFunctionOn;
	  if (isFunctionOn)
	  {
		  gh2Timer = 0;
		  gh2BlinkState = false;
	  }
	  else
	  {
		  digitalWrite(bluePin2, HIGH);
	  }

	  break;
	default:
    #ifdef DEBUG
      Serial.print ("Unhandled function in Depot...function = ");
      Serial.println (function);
    #endif  
    break;
	}
}
