/*
      Loconet on pins 8 (RX on UNO) and 7 (TX) (via a LocoShield or similar)
 */
/*
 * S3
 * S2
 * Surface
 * L1
 * L2
 * L3
 * L4
 */

#include <LocoNet.h>

#define DEBUG
#define ESTOP_PIN 6 // Use NC switch so we can put several switches in series.  Stop if circuit is broken.
#define LN_TX_PIN 7 // LocoNet
#define LN_RX_PIN 8 // LocoNet

//
//  Stepper motor controls
#define MOTOR_PIN 11
#define DIRECTION_PIN 12
#define ENB 13
#define SLP 14
#define SECOND_FLOOR_LIGHT_PIN 17
#define SIDE_LIGHT_PIN 18
#define DECK_LIGHT_PIN 19

#define PULSE_DELAY 2
#define MOTOR_DELAY 5
#define COMMAND_DELAY 5

#define LIGHT_CMD 74 	// JMRI sensor/light to turn lights on/off
#define LIGHT_DIM_CMD 75
#define SIDE_LIGHT_CMD 76
#define DECK_LIGHT_CMD 77
#define SECOND_FLOOR_LIGHT_CMD 78
#define FIRE_CMD 79
#define FIRE_INTENSITY_CMD 80
#define SEEK_LEVEL_CMD 81

#define ORANGE_FIRE_IDX 0
#define YELLOW_FIRE_IDX 1

#define FLICKER_RATE 500	// Defines how fast the firebox flickers

int flickerCount = 0;
int lightIntensity = 0;
int fireIntensity = HIGH;

bool areLightsDimmed = false;
bool areLightsOn = false;
bool isFireOn = true;

int numSensorPins = 4;
byte sensorPins [] = {2, 3, 4, 5}; // These will be HIGH when the switch is open; LOW when it is closed.
byte lightPins[2] = {9, 10};
byte flickerPins[2] = {15, 16};

int numInAddrs = 7;
uint16_t inAddrs [] = {60, 61, 62, 63, 64, 65, 66}; // JMRI Sensor address used as a button to select which level to move to

int numOutAddrs = 7;
int outAddrs[] = {67, 68, 69, 70, 71, 72, 73}; // JMRI sensor address to report when move is complete

bool flickerPhase[] = {false, false};

bool moving = false;
bool initialized = false;

int lastOutState [] = {LOW, LOW, LOW, LOW, LOW, LOW, LOW};
int currentLevel;
int	requestedLevel;
int stepsBetweenLevels[7];
bool hasSensor[7];

lnMsg  *LnPacket;          // pointer to a received LNet packet

void setup()
{
	pinMode(MOTOR_PIN, OUTPUT);
	pinMode(DIRECTION_PIN, OUTPUT);
	pinMode(ENB, OUTPUT);
	pinMode(SLP, OUTPUT);
	pinMode(ESTOP_PIN, INPUT_PULLUP);
	pinMode(DECK_LIGHT_PIN, OUTPUT);
	pinMode(SIDE_LIGHT_PIN, OUTPUT);

	for (int i=0; i<sizeof(flickerPins); i++)
		pinMode(flickerPins[i], OUTPUT);

	for (int i=0; i<sizeof(lightPins); i++)
		pinMode(lightPins[i], OUTPUT);

	int steps;
	hasSensor[0] = false;
	hasSensor[1] = true;
	hasSensor[2] = false;
	hasSensor[3] = false;
	hasSensor[4] = false;
	hasSensor[5] = true;
	hasSensor[6] = true;

	stepsBetweenLevels[0] = 2000; // Steps between level 4 & level 3 (should use reed switchs)
	stepsBetweenLevels[1] = 3000; // Steps between level 3 & level 2
	stepsBetweenLevels[2] = 3000; // Steps between level 2 & level 1
	stepsBetweenLevels[3] = 10700; // Steps between level 1 & level S1
	stepsBetweenLevels[4] = 3200; // Steps between level S1 & level S2
	stepsBetweenLevels[5] = 50; // Steps between level S2 & level S3

	digitalWrite(ENB, HIGH); //Pull low to allow motor control
	digitalWrite(SLP, HIGH); //Pull low to sleep

	currentLevel = -1;
	requestedLevel = -1;

	Serial.begin(115200);
	LocoNet.init(LN_TX_PIN);

	for (int i=0; i<numOutAddrs; i++)
		lastOutState[i] = LOW;


	//  Read all of the reed switches to see if we can find which level the cage is at.
	for (int i = 1; i < numSensorPins; i++)
	{
		pinMode(sensorPins[i], INPUT_PULLUP);
		int value = digitalRead(sensorPins[i]);
		if (value == LOW)
			value = HIGH;
		else
			value = LOW;
#ifdef DEBUG
		Serial.print (" Reading switch ");
		Serial.print (i);
		Serial.print (" value = ");
		if (value == LOW)
			Serial.println (" LOW ");
		else
			Serial.println (" HIGH ");
#endif

		lastOutState[mapSwitchToLevel(i)] = value;

		LocoNet.reportSensor(inAddrs[i], LOW);

		if (digitalRead(sensorPins[i]) == LOW)
		{
			currentLevel = mapSwitchToLevel(i);
		}
	}
	if (currentLevel < 0)
	{
#ifdef DEBUG
		Serial.println ("Hoist setup searching for cage level");
#endif

		seekAnyLevel();

		for (int i = 1; i < numSensorPins; i++)
		{
			if (digitalRead(sensorPins[i]) == LOW)
			{
				currentLevel = mapSwitchToLevel(i);
			}
		}
	}
	else
	{
		Serial.print ("Hoist setup found cage at Level ");
		Serial.println (currentLevel);
	}
	reportLevels();
}

void reportLevels()
{

  for (int i=0; i<numOutAddrs; i++)
  {
#ifdef DEBUG
    Serial.print ("At end of setup, lastOutState[");
    Serial.print (i);
    Serial.print ("] = ");
    Serial.println (lastOutState[i]);
#endif
    LocoNet.reportSensor(outAddrs[i], lastOutState[i]);
  }
#ifdef DEBUG
  Serial.println ("Setup complete");  
#endif
}

/**
 *
 *
 */
int mapLevelToSwitch(int level)
{
	int sw = -1;
	if (level == 0 || level == 1)
		sw = level;
	else if (level == 5)
		sw = 3;
	else if (level == 6)
		sw = 2;
	return sw;
}

/**
 *
 *
 */
int mapSwitchToLevel(int i)
{
	int level = -1;
	if (i==0 || i==1)
		level = i;
	else if (i==2)
		level = 6;
	else if (i == 3)
		level = 5;
	return level;
}

/**
 *
 *
 */
int getCurrentLevel()
{
  int idx = 1; // Skip sump level...reed switch doesn't work
  int lvl = -1;
  while(idx < 4 && lvl < 0)
  {
    if (digitalRead(sensorPins[idx]) == LOW)
    {
      lvl = mapSwitchToLevel(idx);
    }
    idx++;
  }
  return lvl;  
}

/**
 *  Initialize so we know which level the cage is on.
 */
void seekAnyLevel()
{
  digitalWrite(DIRECTION_PIN, HIGH);
  digitalWrite(SLP, HIGH);
  delay(COMMAND_DELAY);
  //
  // Start by moving down about 1/4 floor
  digitalWrite(DIRECTION_PIN, LOW);
  delay(COMMAND_DELAY);
  digitalWrite(ENB, LOW);
  delay(COMMAND_DELAY);  

  int count = 0;
  while ( (count++ < 500) && (digitalRead(ESTOP_PIN) == LOW)  && ( (digitalRead(sensorPins[1]) & digitalRead(sensorPins[2]) & digitalRead(sensorPins[3])) == HIGH))
  {
    digitalWrite(MOTOR_PIN, LOW);
    delay(PULSE_DELAY);
    digitalWrite(MOTOR_PIN, HIGH);
    delay(MOTOR_DELAY);    
  }


	currentLevel = getCurrentLevel();

   #ifdef DEBUG
    Serial.print (" after initial lowering, current level = ");
    Serial.println (currentLevel);
   #endif

  //
  //  If we didn't find a reed switch, move up until we do
  if (currentLevel < 0)
  {
    digitalWrite(DIRECTION_PIN, HIGH);
    delay(COMMAND_DELAY);

    count = 0;
    
    while ( (count++ < 2000) && (digitalRead(ESTOP_PIN) == LOW)  && ( (digitalRead(sensorPins[1]) & digitalRead(sensorPins[2]) & digitalRead(sensorPins[3])) == HIGH))
    {
      digitalWrite(MOTOR_PIN, LOW);
      delay(PULSE_DELAY);
      digitalWrite(MOTOR_PIN, HIGH);
      delay(MOTOR_DELAY);
    }

    currentLevel = getCurrentLevel();
   #ifdef DEBUG
    Serial.print (" after raising, current level = ");
    Serial.println (currentLevel);
   #endif    
  }
  digitalWrite(ENB, HIGH);
}

//
//---------------------------------------------------------------------------------------
//
// loop
//
//---------------------------------------------------------------------------------------
//
void loop() {


	// Check if any of the reed switches have changed.  If so, report new state

	for (int i = 1; i < numSensorPins; i++)
	{
		int level = mapSwitchToLevel(i);
		int value = digitalRead(sensorPins[i]);
		if (value == LOW)
			value = HIGH;
		else
			value = LOW;
		if (value != lastOutState[level])
		{

#ifdef DEBUG
			Serial.print ("Sensor Pin ");
			Serial.print (i);
			Serial.print (" corresponds to level ");
			Serial.print (level);
			Serial.print (" state = ");
			if (lastOutState[level] == LOW)
				Serial.print (" LOW ");
			else
				Serial.print (" HIGH ");
			Serial.print (" reporting to output address ");
			Serial.println(outAddrs[level]);
#endif
			lastOutState[level] = value;
			if (lastOutState[level] == LOW)
			{
				LocoNet.reportSensor(outAddrs[level], LOW);
			}
			else
			{
				LocoNet.reportSensor(outAddrs[level], HIGH);
				currentLevel = level; // In case bridge was manually moved
			}
		}
	}

	// Check for any received LocoNet packets
	LnPacket = LocoNet.receive() ;
	if ( LnPacket ) {
		LocoNet.processSwitchSensorMessage(LnPacket);
		// this function will call the specially named functions below...
	}

	//
	//  Flicker
	flicker(false);
}

//
//---------------------------------------------------------------------------------------
//
// moveMotor
//
//---------------------------------------------------------------------------------------
//
void moveMotor(int steps, bool moveUp, int sensorIdx)
{
	int count = 0;
	int direction = 0;

#ifdef DEBUG
	Serial.print ("MoveMotor, steps = ");
	Serial.print (steps);
	Serial.print (" sensorIdx = ");
	Serial.print (sensorIdx);
	if (moveUp)
	{
		Serial.println (" Moving UP");
	}
	else
	{
		Serial.println (" Moving DOWN");
	}
#endif

	if (moveUp)
	{
		digitalWrite(DIRECTION_PIN, HIGH);
		direction = 0;
	}
	else
	{
		digitalWrite(DIRECTION_PIN, LOW);
		direction = 1;
	}
	delay(COMMAND_DELAY);

  digitalWrite(SLP, HIGH);
  delay(COMMAND_DELAY);
	digitalWrite(ENB, LOW);
	delay(COMMAND_DELAY);
	if (sensorIdx < 0)
	{
#ifdef DEBUG
		Serial.print ("In moveMotor, steps = ");
		Serial.println(steps);
#endif
		for (int i=0; i<steps; i++)
		{
			if (digitalRead(ESTOP_PIN) == LOW)
			{
				digitalWrite(MOTOR_PIN, LOW);
				delay(PULSE_DELAY);
				digitalWrite(MOTOR_PIN, HIGH);
				delay(MOTOR_DELAY);
				flicker(true);  //  Keep firebox flickering
			}
			else
			{
#ifdef DEBUG
				Serial.print ("In Move Motor, ESTOP triggered");
#endif
				i = steps+2;
			}
		}
	}
	else
	{
#ifdef DEBUG
		Serial.print ("In moveMotor, sensorIdx = ");
		Serial.println(sensorIdx);
#endif

		while (digitalRead(sensorPins[sensorIdx]) == HIGH && digitalRead(ESTOP_PIN) == LOW)
		{
			digitalWrite(MOTOR_PIN, LOW);
			delay(PULSE_DELAY);
			digitalWrite(MOTOR_PIN, HIGH);
			delay(MOTOR_DELAY);
			flicker(true);  //  Keep firebox flickering
		}
	}
	digitalWrite(ENB, HIGH);
}


// Callbacks from LocoNet.processSwitchSensorMessage() ...
// We tie into the ones connected to turnouts so we can capture anything
// that can change (or indicatea change to) a turnout's position.

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
#ifdef DEBUG
	Serial.print ("In NotifySensor, address = ");
	Serial.print (address);
	if (state == LOW)
		Serial.println (" State = LOW ");
	else
		Serial.println (" State = HIGH ");
#endif

	// Notify JMRI of initial state.  We have to wait for JMRI to get started to report this, so we
	// report all sensor positions on the first one of "our" commands from JMRI.
	if ((address >= inAddrs[0]) && (address <= outAddrs[6]) && !initialized)
	{
		initialized = true;

		for (int i=0; i<numOutAddrs; i++)
		{
			LocoNet.reportSensor(outAddrs[i], lastOutState[i]);
			LocoNet.reportSensor(inAddrs[i], LOW);
#ifdef DEBUG
			Serial.print ("Reporting initial sensor state to JMRI, i = ");
			Serial.print (i);
			Serial.print (" outAddr = " );
			Serial.print (outAddrs[i]);
			if (lastOutState[i] == LOW)
				Serial.println (" lastOutState = LOW");
			else
				Serial.println (" lastOutState = HIGH");
#endif
		}
	}

	// Turn side door on/off if requested
	if (address == SIDE_LIGHT_CMD)
	{
		fadeOnOff(SIDE_LIGHT_PIN, state);
	}

	// Turn deck door on/off if requested
	if (address == DECK_LIGHT_CMD)
	{
		fadeOnOff(DECK_LIGHT_PIN, state);
	}

  if (address == SECOND_FLOOR_LIGHT_CMD)
  {
    fadeOnOff(SECOND_FLOOR_LIGHT_PIN, state);
  }
	if (address == LIGHT_DIM_CMD)
	{
		areLightsDimmed = (state != LOW);
		toggleMainLights();
	}
	//
	// Turn on interior lights
	if (address == LIGHT_CMD)
	{
		areLightsOn = (state != LOW);
		toggleMainLights();
	}

	//
	// Turn on boiler fire
	if (address == FIRE_CMD)
	{
		isFireOn = (state != LOW);
    // Force a report of the current level status
    reportLevels();
	}


  // 
  // Find a current level by wiggling the cage down then up
  if (address == SEEK_LEVEL_CMD && state != LOW)
  {
    #ifdef DEBUG
      Serial.println ("Manually seeking initial level");
    #endif
    seekAnyLevel();
  }

	//
	// Adjust intensity of boiler fire.
	if (address == FIRE_INTENSITY_CMD)
	{
		if (state != LOW)
		{
			fireIntensity = HIGH;
		}
		else
		{
			fireIntensity = LOW;
		}
	}

	// Request to move hoist cage...and we're not already moving it.
     requestedLevel = address - inAddrs[0];
  #ifdef DEBUG
    Serial.print ("In notifySensor, State changed, new State = ");
    if (state == LOW)
      Serial.print( " LOW ");
    else
      Serial.print (" HIGH ");
    Serial.print (" currentLevel = ");
    Serial.print (currentLevel);
    Serial.print (" requestedLevel = ");
    Serial.print (requestedLevel);
    Serial.print (" address = ");
    Serial.println(address);
  #endif 
	if (((address >= inAddrs[0]) && (address <= inAddrs[6])) && (state != 0) && !moving && (requestedLevel != currentLevel))
	{
    requestedLevel = address - inAddrs[0];
  #ifdef DEBUG
    Serial.print ("In notifySensor, State changed, new State = ");
    if (state == LOW)
      Serial.print( " LOW ");
    else
      Serial.print (" HIGH ");
    Serial.print (" currentLevel = ");
    Serial.print (currentLevel);
    Serial.print (" requestedLevel = ");
    Serial.print (requestedLevel);
    Serial.print (" address = ");
    Serial.println(address);
  #endif   
		// Turn lights in winding house on bright while moving.  Remember the current state so we can
		// restore the lights to that state when we are done moving.
		bool wereLightsOn = areLightsOn;
		bool wereLightsDim = areLightsDimmed;
		areLightsOn = true;
		areLightsDimmed = false;
		toggleMainLights();

		moving = true;
		LocoNet.reportSensor(outAddrs[currentLevel], LOW);


		//  Move motor

		bool isMovingUp = false;
		if (currentLevel < requestedLevel)
		{
			isMovingUp = true;
		}

		//
		// Levels 2, 3, 4 don't have magnetic sensors.  we do steps from above/below
		int nearestSensor = -1;
		int steps = 0;

		//
		// Simple case, move until reed switch triggers.
		if (hasSensor[requestedLevel])
		{
			// Wait for appropriate magnetic sensor to trigger
			moveMotor(0, isMovingUp, mapLevelToSwitch(requestedLevel));
		}
		else // Move based on number of steps between levels
		{
			if (isMovingUp)
			{
				for (int i=currentLevel; i<requestedLevel; i++)
				{
					steps += stepsBetweenLevels[i];
				}
			}
			else
			{
				for (int i=currentLevel; i>requestedLevel; i--)
				{
					steps += stepsBetweenLevels[i-1];
				}
			}
			// Wait for nearest sensor to trip.  We also stop if either the top or bottom sensor trips (safety)
			moveMotor(steps, isMovingUp, -1);
		}

#ifdef DEBUG
		Serial.print ("Moved motor ");
		Serial.print (steps);
		Serial.print (" steps from Level ");
		Serial.print (currentLevel);
		Serial.print (" to ");
		Serial.println (requestedLevel);
#endif

		currentLevel = requestedLevel;
		LocoNet.reportSensor(outAddrs[currentLevel], HIGH);  // Turn on JMRI sensor
		LocoNet.reportSensor(address, LOW);  // Turn off the sensor on the UI that activated this move

		moving = false;

		// Restore the lights to the state they were in before the request to move the cage
		areLightsDimmed = wereLightsDim;
		areLightsOn = wereLightsOn;
		toggleMainLights();
	}
}

/**
 *
 */
void toggleMainLights()
{
	if (!areLightsDimmed && areLightsOn)
	{
		lightIntensity = 255;
		analogWrite(lightPins[1], lightIntensity);
		delay(2000);
		analogWrite(lightPins[0], lightIntensity);
	}
	else if (areLightsDimmed && areLightsOn)
	{
		lightIntensity = 255;
		analogWrite(lightPins[1], lightIntensity);
		delay(2000);
		analogWrite(lightPins[0], 0);
	}
	else
	{
		lightIntensity = 128;
		analogWrite(lightPins[1], lightIntensity);
		delay(2000);
		analogWrite(lightPins[0], lightIntensity);
	}
}

/**
 *
 */
void fadeOnOff(int lightPin, uint8_t state)
{
#define fadedelay 24
#define fadestep 12

#ifdef DEBUG
    Serial.print("In FadeOnOff, state = ");
    Serial.println(state);
#endif
	if (state != LOW)
	{
#ifdef DEBUG
		Serial.print("Turning fade ON, pin = ");
		Serial.println(lightPin);
#endif
		for (int t = 0; t < fadestep; t += 1)
		{
			digitalWrite( lightPin, HIGH);
			delay(fadedelay * (t / fadestep));
			digitalWrite( lightPin, LOW);
			delay(fadedelay - (fadedelay * (t / fadestep)));
		}
		digitalWrite( lightPin,  HIGH );
	} else if (state == LOW) {
#ifdef DEBUG
		Serial.print("Turning fade OFF, pin = ");
		Serial.println(lightPin);
#endif
		for (int t = 0; t < fadestep; t += 1)
		{
			digitalWrite( lightPin, LOW);
			delay(fadedelay * (t / fadestep));
			digitalWrite( lightPin, HIGH);
			delay(fadedelay - (fadedelay * (t / fadestep)));
		}
		digitalWrite(lightPin, LOW);
	}
}

/**
 *
 */
void flicker(bool isMoving)
{
	if (isFireOn)
	{
    int rate = FLICKER_RATE;
    int phaseRate = 50;
    int phase = LOW;
    
    if (fireIntensity == LOW)
    {
      rate = rate / 3; // Higher number = slower flicker
      phaseRate = 90;
      digitalWrite(flickerPins[YELLOW_FIRE_IDX], LOW); // Turn off yellow LED
    }  
		if (flickerCount++ > rate  || isMoving)
		{
			flickerCount = 0;
			for (int i=0; i<sizeof(flickerPins); i++)
			{
				if (random(1,100) > phaseRate) // Change phase (on/off) of LED to randomly keep the LED on longer or shorter
				{
          phase = HIGH;
				}
        else
        {
          phase = LOW;
        }

        //
        // Flicker both LEDS on high intensity.  Only flicker the orange LED on low intensity.
        if (fireIntensity == HIGH || (fireIntensity == LOW && i == ORANGE_FIRE_IDX))
					  digitalWrite(flickerPins[i], phase);
			}
		}
	}
	else // Turn Fire Off
	{
		for (int i=0; i<sizeof(flickerPins); i++)
		{
			digitalWrite(flickerPins[i], LOW);
		}
	}
}

/**
 *
 */
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
