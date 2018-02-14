//#define DEBUG
//
//********************************************************************************
//
//  Turnouts
//
//  Controls turnouts via LocoNet.  Each switch stand has a lantern that can be 
//  turned on/off.
//
//  Sensor address 800 centers all of the turnout servos.
//
//********************************************************************************
//
#include <LocoNet.h>
#include <SoftwareServo.h> 

const uint8_t ACTIVE = 16;
const uint8_t INACTIVE = 0;

const uint8_t CLOSED = 32;
const uint8_t THROWN = 0;

const uint8_t ON = 1;
const uint8_t OFF = 0;
const uint8_t DIM = 2;

//
// Function Address Controls
const int TURNOUT_0_LANTERN_CMD = 130;
const int TURNOUT_0_ADDR = 3;
const int TURNOUT_0_THROWN = 131;
const int TURNOUT_0_CLOSED = 132;

/*const int TURNOUT_1_LANTERN_CMD = 133;
const int TURNOUT_1_THROWN = 134;
const int TURNOUT_1_CLOSED = 135;
const int TURNOUT_1_ADDR = 1;*/

const int LEVEL_1_LIGHT_1_CMD = 136;
const int LEVEL_1_LIGHT_1_DIM = 137;
const int LEVEL_1_LIGHT_1_PIN = 5; // Pins 9 & 10 don't work as PWM with servo.

const int LEVEL_1_LIGHT_2_CMD = 138;
const int LEVEL_1_LIGHT_2_DIM = 139;
const int LEVEL_1_LIGHT_2_PIN = 6; // Pins 9 & 10 don't work as PWM with servo.

const int LEVEL_1_LIGHT_3_CMD = 133;
const int LEVEL_1_LIGHT_3_DIM = 134;
const int LEVEL_1_LIGHT_3_PIN = 4; // Pins 9 & 10 don't work as PWM with servo.

const int CENTER_SERVO_CMD = 800;

//
// Pin connections
const int TURNOUT_0_PIN = 3;
const int TURNOUT_0_LIGHT_PIN = 12;
const int TURNOUT_0_THROWN_RELAY_PIN=10;
const int TURNOUT_0_CLOSED_RELAY_PIN=11;

/*
const int TURNOUT_1_PIN = 9;
const int TURNOUT_1_LIGHT_PIN = 13;
const int TURNOUT_1_THROWN_RELAY_PIN=10;
const int TURNOUT_1_CLOSED_RELAY_PIN=11	;
*/
const int LN_TX_PIN = 7;
const int LN_RX_PIN = 8;

#define servo_start_delay 50
#define servo_init_delay 7

#define numTurnouts 1
#define numLights 3

struct LIGHT_DEF
{
  int pin;
  uint8_t currentIntensity;
  uint8_t maxIntensity;
  uint8_t dimIntensity;
  uint8_t targetIntensity;
  bool isDimmed = false;
  bool isOn = false;
  bool isDimming = false;
  bool isBrightening = false;
  int rate = 2;
  int counter = 0;
  int dimCmd;
  int onCmd;
};

struct SERVO_DEF
{
	String servoName;				// Name of the servo so we can identify the function
	uint16_t turnoutAddr;			// LocoNet turnout address
	bool moving = false;			// Indicates that the servo is currently moving
	int currentPosition;			// Current position of servo (angle)
	int direction;					// Direction servo is moving
	int increment;
	int thrownPosition;				// Position (angle) of servo
	int closedPosition;				// Position (angle) of servo
	int slowdown_rate = 10;				// Indicates how many times through LOOP to skip between moving servo - slows down movement
	int slowdown_counter = 0;		// Used with slowdown_rate to slow down movement...current counter
	SoftwareServo servo;			// Servo to move
	int servoPin;
	int lanternPin;
	uint8_t lanternState;
	uint16_t lanternCmd;
	uint16_t frogRelayThrownAddr;
	uint16_t frogRelayClosedAddr;
	uint8_t frogRelayThrownPin;
	uint8_t frogRelayClosedPin;
};
SERVO_DEF* turnout[numTurnouts];

LIGHT_DEF* light[numLights];

uint8_t level1Dim1 = INACTIVE;
uint8_t level1Dim2 = INACTIVE;

uint8_t level1Light1State = OFF;
uint8_t level1Light2State = OFF;

lnMsg  *LnPacket;          // pointer to a received LNet packet
//LocoNetThrottleClass  light1Dimmer ;
//LocoNetThrottleClass  light2Dimmer ;
//
//********************************************************************************
//
//  Arduino calls setup once on power-up.  Note that this usually happens before
//  JMRI has started.
//
//********************************************************************************
//
void setup()
{
#ifdef DEBUG
	Serial.begin(115200);
	Serial.println ("In setup");
#endif

  for (int i=0; i<numLights; i++)
  {
    light[i] = new LIGHT_DEF;
    light[i]->dimIntensity = 50;
    light[i]->maxIntensity = 255;
    light[i]->currentIntensity = 0;
    light[i]->targetIntensity = 0;
    light[i]->isDimming = false;
    light[i]->isBrightening = false;
    light[i]->counter = 0;
  }
  light[0]->pin = LEVEL_1_LIGHT_1_PIN;
  light[1]->pin = LEVEL_1_LIGHT_2_PIN;
  light[2]->pin = LEVEL_1_LIGHT_3_PIN;  
  light[0]->dimCmd = LEVEL_1_LIGHT_1_DIM;
  light[0]->onCmd = LEVEL_1_LIGHT_1_CMD;
  light[1]->dimCmd = LEVEL_1_LIGHT_2_DIM;
  light[1]->onCmd = LEVEL_1_LIGHT_2_CMD;
  light[2]->dimCmd = LEVEL_1_LIGHT_3_DIM;
  light[2]->onCmd = LEVEL_1_LIGHT_3_CMD;    

  for (int i=0; i<numLights; i++)
  {
    analogWrite (light[i]->pin, 0);
  }
  
	for(int i=0; i<numTurnouts; i++)
	{
		SERVO_DEF *s = new SERVO_DEF;
		turnout[i] = new SERVO_DEF;
		turnout[i]->thrownPosition = 55;
		turnout[i]->closedPosition = 145;
		turnout[i]->currentPosition = turnout[i]->closedPosition;
	}

	turnout[0]->lanternPin = TURNOUT_0_LIGHT_PIN;
	turnout[0]->servoPin = TURNOUT_0_PIN;
	turnout[0]->lanternCmd = TURNOUT_0_LANTERN_CMD;
	turnout[0]->turnoutAddr = TURNOUT_0_ADDR;
	turnout[0]->frogRelayThrownPin = TURNOUT_0_THROWN_RELAY_PIN;
	turnout[0]->frogRelayClosedPin = TURNOUT_0_CLOSED_RELAY_PIN;
	turnout[0]->frogRelayThrownAddr = TURNOUT_0_THROWN;
	turnout[0]->frogRelayClosedAddr = TURNOUT_0_CLOSED;
/*
	turnout[1]->lanternPin = TURNOUT_1_LIGHT_PIN;
	turnout[1]->servoPin = TURNOUT_1_PIN;
	turnout[1]->lanternCmd = TURNOUT_1_LANTERN_CMD;
	turnout[1]->turnoutAddr = TURNOUT_1_ADDR;
	turnout[1]->frogRelayThrownPin = TURNOUT_1_THROWN_RELAY_PIN;
	turnout[1]->frogRelayClosedPin = TURNOUT_1_CLOSED_RELAY_PIN;
	turnout[1]->frogRelayThrownAddr = TURNOUT_1_THROWN;
	turnout[1]->frogRelayClosedAddr = TURNOUT_1_CLOSED;
*/

	LocoNet.init(LN_TX_PIN);

	for (int t=0; t<servo_start_delay; t++)
	{
		SoftwareServo::refresh();
		delay(servo_init_delay);
	}

	for(int i=0; i<numTurnouts; i++)
	{
		pinMode(turnout[i]->lanternPin, OUTPUT);
		pinMode(turnout[i]->servoPin, OUTPUT);
    pinMode(turnout[i]->frogRelayThrownPin, OUTPUT);
    pinMode(turnout[i]->frogRelayClosedPin, OUTPUT);
		turnout[i]->lanternState = INACTIVE;
		digitalWrite(turnout[i]->lanternPin, LOW);	// Turn lanterns off...prevents unused pins from being hot
    digitalWrite(turnout[i]->frogRelayClosedPin, HIGH); // Turn both relays off (polarity is reversed on relay)
    digitalWrite(turnout[i]->frogRelayThrownPin, HIGH);
		LocoNet.requestSwitch(turnout[i]->turnoutAddr, 1, CLOSED);
	}

#ifdef DEBUG
	Serial.println ("Setup complete");
#endif
}

//
//********************************************************************************
//
//  Arduino calls loop over and over.  This is where we monitor for LocoNet messages
//  and adjust the servos.
//
//********************************************************************************
//
void loop()   
{
	// Check for any received LocoNet packets - Only one we get is to raise/lower spout
	LnPacket = LocoNet.receive() ;
	if ( LnPacket )
	{
    LocoNet.processSwitchSensorMessage(LnPacket);
	}

	SoftwareServo::refresh();
	delay(4);

	for (int i=0; i<numTurnouts; i++)
	{
		if (turnout[i]->moving)
		{
			moveTurnout(turnout[i]);
		}
	}

  for (int i=0; i<numLights; i++)
  {
    if (light[i]->isDimming)
    {
      dimLight(light[i], -1);
    }
    else if (light[i]->isBrightening)
    {
      dimLight(light[i], 1);
    }
  }
}

/**
 * dimLight
 */
void dimLight(LIGHT_DEF *light, int increment)
{

  if (light->counter++ > light->rate)
  {  
#ifdef DEBUG
    Serial.print ("In dimLight");
    Serial.print (" currentIntensity = ");
    Serial.print (light->currentIntensity);
    Serial.print (" targetIntensity = ");
    Serial.print (light->targetIntensity);
    Serial.print (" increment = ");
    Serial.print (increment);
    Serial.println(""); 
#endif   
    // Reset counter for next time through
    light->counter = 0;

    // Change light intensity 1 step
    light->currentIntensity = light->currentIntensity + increment;
    analogWrite(light->pin, light->currentIntensity);

    // Determine if we have reached the limit
    if (light->isDimming && light->currentIntensity <= light->targetIntensity)
    {
      light->isDimming = false;
      light->isBrightening = false;
    } 

    if (light->isBrightening && light->currentIntensity >= light->targetIntensity)
    {
      light->isDimming = false;
      light->isBrightening = false;
    }        
  }
}
 
/**
 * moveTurnout
 */
void moveTurnout(SERVO_DEF *servo)
{
#ifdef DEBUG
  Serial.print ("Moving Turnout");
  Serial.print (" slowdown_counter = ");
  Serial.print (servo->slowdown_counter);
  Serial.print (" slowdown_rate = ");
  Serial.print (servo->slowdown_rate);
  Serial.print (" direction = ");
  Serial.print (servo->direction);
 Serial.println ("");
#endif

	if (servo->slowdown_counter++ > servo->slowdown_rate)
	{
#ifdef DEBUG
  Serial.print (" currentPosition = ");
  Serial.print (servo->currentPosition);
  Serial.print (" increment = ");
  Serial.print (servo->increment);
  Serial.println ("");
#endif

		// Reset counter for next time through
		servo->slowdown_counter = 0;

		// Move the servo one degree
		servo->currentPosition = servo->currentPosition + servo->increment;
		servo->servo.write(servo->currentPosition);

		// Determine if we have reached the limit
		if (((servo->currentPosition > servo->closedPosition) && servo->increment > 0)
				|| ((servo->currentPosition < servo->thrownPosition) && servo->increment < 0))
		{
			servo->moving = false;
			servo->servo.detach();
			if (servo->direction == CLOSED)
			{
				digitalWrite(servo->frogRelayClosedPin, LOW);
				LocoNet.reportSensor(servo->frogRelayClosedAddr, ACTIVE);
			}
			else
			{
				digitalWrite(servo->frogRelayThrownPin, LOW);
				LocoNet.reportSensor(servo->frogRelayThrownAddr, ACTIVE);
			}
		}
	}
}

String showDirection(uint8_t direction)
{
  if (direction == CLOSED)
    return "CLOSED";
  else
    return "THROWN";
}

String showState(uint8_t state)
{
  if (state == INACTIVE)
    return "INACTIVE";
  else
    return "ACTIVE";
}
/**
 *
 */
void notifySwitchRequest( uint16_t address, uint8_t output, uint8_t direction )
{
	// Address: Switch Address.
	// Output: Value 0 for Coil Off, anything else for Coil On
	// Direction: Value 0 for Closed/GREEN, anything else for Thrown/RED
#ifdef DEBUG
	Serial.print ("In notifySwitchRequest, Address = ");
	Serial.print (address);
	Serial.print (" Output = ");
	Serial.print (output);
	Serial.print (" Direction = ");
	Serial.println (showDirection(direction));
#endif

	for (int i=0; i<numTurnouts; i++)
	{
		if (address == turnout[i]->turnoutAddr  && output != 0 && turnout[i]->moving == false)
		{
			if ((turnout[i]->direction != CLOSED) && (turnout[i]->currentPosition > turnout[i]->thrownPosition))
			{
				turnout[i]->increment = -1;
#ifdef DEBUG
				Serial.print ("THROWN ");
				Serial.print (" currentPosition = ");
				Serial.print (turnout[i]->currentPosition);
				Serial.print (" increment = ");
				Serial.print (turnout[i]->increment);
				Serial.print (" thrownPosition = ");
				Serial.println (turnout[i]->thrownPosition);
#endif
			}
			else if ((turnout[i]->direction == CLOSED) && (turnout[i]->currentPosition < turnout[i]->closedPosition))
			{
				turnout[i]->increment = 1;
#ifdef DEBUG
				Serial.print ("CLOSED ");
				Serial.print (" currentPosition = ");
				Serial.print (turnout[i]->currentPosition);
				Serial.print (" increment = ");
				Serial.print (turnout[i]->increment);
				Serial.print (" closedPosition = ");
				Serial.println (turnout[i]->closedPosition);
#endif
			}

			turnout[i]->moving = true;
			turnout[i]->direction = direction;
			turnout[i]->servo.attach(turnout[i]->servoPin);
			digitalWrite(turnout[i]->frogRelayThrownPin, HIGH);
			digitalWrite(turnout[i]->frogRelayClosedPin, HIGH);
			LocoNet.reportSensor(turnout[i]->frogRelayThrownAddr, INACTIVE);
			LocoNet.reportSensor(turnout[i]->frogRelayClosedAddr, INACTIVE);
		}
	}
}

void notifySwitchReport( uint16_t Address, uint8_t Output, uint8_t Direction )
{
#ifdef DEBUG
  Serial.print ("In notifySwitchReport...not doing anything, Address = ");
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
  Serial.print ("In notifySwitchState...not doing anything, Address = ");
  Serial.print (Address);
  Serial.print (" Output = ");
  Serial.print (Output);
  Serial.print (" Direction = ");
  Serial.println (Direction);
#endif
}
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
    LocoNet.reportSensor(CENTER_SERVO_CMD, INACTIVE);

    for (int i=0; i<numLights; i++)
    {
      if (light[i]->currentIntensity == light[i]->maxIntensity)
      {
        LocoNet.reportSensor(light[i]->onCmd, ACTIVE);
        LocoNet.reportSensor(light[i]->dimCmd, INACTIVE);
      }
      else if (light[i]->currentIntensity == light[i]->dimIntensity)
      {
        LocoNet.reportSensor(light[i]->onCmd, ACTIVE);
        LocoNet.reportSensor(light[i]->dimCmd, ACTIVE);
      }
      else if (light[i]->currentIntensity == 0)
      {
        LocoNet.reportSensor(light[i]->onCmd, INACTIVE);
        LocoNet.reportSensor(light[i]->dimCmd, INACTIVE) ;     
      }
    }
           
	  for (int i=0; i<numTurnouts; i++)
	  {
		  LocoNet.reportSensor(turnout[i]->lanternCmd, turnout[i]->lanternState);  // Report to JMRI      
		  LocoNet.reportSwitch(turnout[i]->turnoutAddr);
	  }
  }
}
//
//---------------------------------------------------------------------------------------
//
// notifySensor - Called by JMRI/LocoNet when a sensor changes on JMRI.
//
//---------------------------------------------------------------------------------------
//
void notifySensor( uint16_t address, uint8_t state )
{
#ifdef DEBUG
  Serial.print(" In notifySensor...");
  Serial.print(" address = ");
  Serial.print(address);
  Serial.print(" state = ");
  Serial.println(showState(state));
#endif
	for (int i=0; i<numTurnouts; i++)
	{
		//
		// Turn switch stand lantern on/off
		if (address == turnout[i]->lanternCmd)
		{
			if (state == INACTIVE)
				digitalWrite(turnout[i]->lanternPin, LOW);
			else
				digitalWrite(turnout[i]->lanternPin, HIGH);
			turnout[i]->lanternState = state;
		}
    else if (address == CENTER_SERVO_CMD && state != INACTIVE) // Center servos
    {
      turnout[i]->servo.attach(turnout[i]->servoPin);
      SoftwareServo::refresh();
      delay(4);      
      turnout[i]->servo.write(90);
      SoftwareServo::refresh();
      delay(4);
      turnout[i]->servo.detach();
  
      LocoNet.reportSensor(CENTER_SERVO_CMD, INACTIVE);
    }   
	}

  for (int i=0; i<numLights; i++)
  {
    if (address == light[i]->dimCmd)
    {
      light[i]->isDimming = (state == ACTIVE) && light[i]->isOn;
      light[i]->isBrightening = (state == INACTIVE) && light[i]->isOn;
      if (state == ACTIVE)
      {
        //Serial.println ("Setting dim");
        light[i]->targetIntensity = light[i]->dimIntensity;
      }
      else
      {
        //Serial.println ("Unsetting dim");
        light[i]->targetIntensity = light[i]->maxIntensity;        
      }
      light[i]->isDimmed = state == ACTIVE;
    }
    else if (address == light[i]->onCmd)
    {
      if (state == INACTIVE)
      {
        //Serial.println("Turning light off");
        light[i]->isDimming = true;
        light[i]->isBrightening = false;
        light[i]->targetIntensity = 0;
        light[i]->isOn = false;
      }
      else
      {
        //Serial.println("Turning light on");
        light[i]->isDimming = false;
        light[i]->isBrightening = true; 
        if (light[i]->isDimmed)
        {
          light[i]->targetIntensity = light[i]->dimIntensity;       
        }
        else
        {
          light[i]->targetIntensity = light[i]->maxIntensity;
        }
        light[i]->isOn = true;
      }
    }
  }
}
