//#define DEBUG
//
//********************************************************************************
//
//  WaterTower
//
//  Animates the spout on a water tower.  Monitors LocoNet for a JMRI sensor (currently set to #110) to change to 'active'.
//
//  -  When the sensor changes to active, the spout is lowered (via a servo).  When the spout is fully lowered, a second servo is activated
//     to change the level of the water gauge on the side of the tank.
//  -  When the sensor changes to inactive, the servo changing the water level is stopped and the spout is raised.  When the
//     spout is fully  raised, the water level servo is activated to refill the tank.
//  -  Sensor status is sent to JMRI for the following:
//     -  WaterFlowing (currently JMRI LocoNet sensor 111) - Indicates that water is flowing out of the tank to the locomotive.  The
//        gauge on the side of the tank will be changing.
//     -  SpoutMoving (currently JMRI LocoNet sensor 116) - Indicates that the spout is moving up/down (i.e. the servo is active).
//     -  TankFilling (currently JMRI LocoNet sensor 117) - Indicates that the tank is being refilled.  The gauge on the side of the tank
//        will change until the tank is "full".
//     - TankEmpty (JMRI LocoNet sensor 118) - Indicates that the tank is out of water.
//     - WaterLevel (JMRI LocoNet sensors 112-115) - Indicates the number of feet of water in the tank.  Each sensor represents
//       on bit of a four-bit value (0-15).  Sensor 112 is LSB.
//
//********************************************************************************
//
#include <LocoNet.h>
#include <SoftwareServo.h> 

const uint8_t ACTIVE = 16;
const uint8_t INACTIVE = 0;
const uint8_t DOWN = 16;
const uint8_t UP = 0;
const uint8_t EMPTY = 16;
const uint8_t FILL = 0;
const float TANK_CAPACITY = 12.0; // Number of feet of water in the tank.

//
// Function Address Controls
const int SPOUT_SENSOR = 110;
const int WATER_FLOWING = 111;
const int WATER_LEVEL_LSB = 112;
// Address 112-115 are the water level bits.
const int SPOUT_MOVING = 116;
const int TANK_FILLING = 117;
const int TANK_EMPTY = 118;
const int ROCK_RATE = 119;
const int ROCK_WOBBLE = 120;
const int ROCK_BOUNCE = 121;

//
// Pin connections
const int SPOUT_PIN = 2;
const int GAUGE_PIN = 3;
const int ROCK_PIN = 4;
const int LN_TX_PIN = 7;
const int LN_RX_PIN = 8;

bool tankFilling = false;
bool tankEmptying = false;
bool rockWobbling = false;
bool rockBouncing = false;

const int ROCK_WOBBLE_FAST = 200;
const int ROCK_WOBBLE_SLOW = 300;
const int ROCK_TOP_FAST = 25;
const int ROCK_TOP_SLOW = 30;
const int ROCK_BOTTOM_FAST = 15;
const int ROCK_BOTTOM_SLOW = 15;

int rockTopLimit = ROCK_TOP_FAST;
int rockBottomLimit = ROCK_BOTTOM_FAST;

#define servo_start_delay 50
#define servo_init_delay 7

struct MY_SERVO_DEF
{
	String servoName;				// Name of the servo so we can identify the function
	bool moving;					// Indicates that the servo is currently moving
	bool finishedMoving = false;  	// Use to identify transition at end of move
	int currentPosition;			// Current position of servo (angle)
	int direction;					// Direction servo is moving (UP or DOWN)
	int topPosition;				// Position (angle) of servo when spout is UP (tank is full)
	int bottomPosition;				// Position (angle) of servo when spout is DOWN (tank is empty)
	int slowdown_rate;				// Indicates how many times through LOOP to skip between moving servo - slows down movement
	int slowdown_counter = 0;		// Used with slowdown_rate to slow down movement...current counter
	SoftwareServo servo;			// Servo to move
};

MY_SERVO_DEF *spout = new MY_SERVO_DEF;
MY_SERVO_DEF *gauge = new MY_SERVO_DEF;
MY_SERVO_DEF *rock = new MY_SERVO_DEF;

lnMsg  *LnPacket;          // pointer to a received LNet packet

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

	LocoNet.init(LN_TX_PIN);

	tankFilling = false;
	tankEmptying = false;
	rockWobbling = false;
	rockBouncing = false;
	//
	// Initialize the two servos to the initial position
	spout->servo.attach(SPOUT_PIN);
	spout->servoName = "spout";
	spout->topPosition = 170; // Spout raised
	spout->currentPosition = 170;
	spout->bottomPosition = 70;
	spout->slowdown_rate = 10;
	spout->moving = false;
	spout-finishedMoving = false;

	gauge->servo.attach(GAUGE_PIN);
	gauge->servoName = "gauge";
	gauge->topPosition = 15; // Ball at bottom (Full tank) - Smaller number = lower ball
	gauge->currentPosition = 15;
	gauge->bottomPosition = 180; // Ball at top (Empty tank)
	gauge->slowdown_rate = 210;
	gauge->moving = false;
	gauge->finishedMoving = false;

	rock->servo.attach(ROCK_PIN);
	rock->servoName = "rock";
	rock->topPosition = ROCK_TOP_SLOW; // Ball at bottom (Full tank) - Smaller number = lower ball
	rock->bottomPosition = ROCK_BOTTOM_SLOW;
	rock->slowdown_rate = ROCK_WOBBLE_FAST;
	rock->currentPosition = rock->bottomPosition;
	rock->moving = false;
	rock->direction = UP;

	//
	//  Move the servos to the inital position.  We want the spout up and the tank full.
	spout->servo.write(spout->topPosition);
	gauge->servo.write(gauge->topPosition);
	rock->servo.write(rock->topPosition);

	//
	//  Wait for spout/gauge to move
	for (int t=0; t<servo_start_delay; t++)
	{
		SoftwareServo::refresh();
		delay(servo_init_delay);
	}
	spout->servo.detach();
	gauge->servo.detach();
	rock->servo.detach();

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

	if (spout->moving)
	{
		moveServo (spout);
	}

	if (spout->finishedMoving)
	{
		spout->finishedMoving = false;
		LocoNet.reportSensor(SPOUT_MOVING, INACTIVE);

		//
		//  If spout is up, we have finished filling the locomotive.  Now we need to refill
		//	the tank.  Attach the gauge servo and get ready to start stepping the servo.
		if (spout->currentPosition >= spout->topPosition)
		{
			LocoNet.reportSensor(WATER_FLOWING, INACTIVE);
			tankFilling = true;
			gauge->moving = true;
			gauge->direction = UP;
			gauge->finishedMoving = false;
			gauge->servo.attach(GAUGE_PIN);
			gauge->slowdown_counter = 0;
		}
		else if (spout->currentPosition <= spout->bottomPosition)
		{
			LocoNet.reportSensor(WATER_FLOWING, ACTIVE);
			tankEmptying = true;
			gauge->moving = true;
			gauge->direction = DOWN;
			gauge->finishedMoving = false;
			gauge->servo.attach(GAUGE_PIN);
			gauge->slowdown_counter = 0;
		}
	}

	//
	//  If we are changing the water level in the tank (filling the tank or emptying into the locomotive),
	//  we step the servo and report the water level.
	if (gauge->moving)
	{
		moveServo(gauge);
		if (gauge->slowdown_counter > gauge->slowdown_rate)
		{
			reportWaterLevel();
		}
	}
	else if (!gauge->moving && (tankFilling || tankEmptying))
	{
		tankFilling = false;
		tankEmptying = false;
		reportWaterLevel();
	}

	if (rockWobbling)
	{
		wobbleRock();
	}

	if (rockBouncing)
	{
		bounceRock();
	}
}
//
//**********************************************************************
//
void bounceRock()
{
	int increment = 1;
	int newDirection = rock->direction;

	if (rock->currentPosition < rockTopLimit && rock->direction == UP)
		increment = 1;
	else if (rock->currentPosition > rockBottomLimit && rock->direction == DOWN)
		increment = -1;

	if (rock->currentPosition >= rockTopLimit)
	{
		newDirection = DOWN;
	}
	else if (rock->currentPosition <= rockBottomLimit)
	{
		newDirection = UP;
	}

	if (rock->direction != newDirection)
	{
		rock->direction = newDirection;
		rockBottomLimit = rockBottomLimit + 1;
		rockTopLimit = rockTopLimit -1;
	}

	if (rock->slowdown_counter++ > rock->slowdown_rate)
	{
		rock->currentPosition = rock->currentPosition + increment;

		//  Serial.print (" current Position = ");
		//  Serial.print (rock->currentPosition);
		//  Serial.print (" rockTopLimit = ");
		//  Serial.print (rockTopLimit);
		//  Serial.print (" rockBottomLimit = ");
		//  Serial.print (rockBottomLimit);
		//  Serial.println (" ");

		rock->servo.write(rock->currentPosition);
		rock->slowdown_counter = 0;



		if (rockBottomLimit >= rockTopLimit)
		{
			rockBouncing = false;
			LocoNet.reportSensor(ROCK_BOUNCE, INACTIVE);
			rock->servo.detach();
		}
	}
}

//
//**********************************************************************
//
void wobbleRock()
{
	int increment = 1;
	if (rock->currentPosition < rock->topPosition && rock->direction == UP)
		increment = 1;
	else if (rock->currentPosition > rock->bottomPosition && rock->direction == DOWN)
		increment = -1;

	if (rock->currentPosition >= rock->topPosition)
		rock->direction = DOWN;
	else if (rock->currentPosition <= rock->bottomPosition)
		rock->direction = UP;

#ifdef DEBUG
	Serial.println (" ");
	Serial.print ("*** Moving servo ");
	Serial.print(rock->servoName);
	if (rock->direction == UP)
	{
		Serial.println (" UP");
	}
	else
	{
		Serial.println (" DOWN");
	}
	Serial.print (" current position = ");
	Serial.print (rock->currentPosition);  Serial.print (" increment = ");
	Serial.print (increment);
	Serial.print (" topPosition = ");
	Serial.print (rock->topPosition);
	Serial.print (" bottomPosition = ");
	Serial.print (rock->bottomPosition);
	Serial.print (" slowdown_counter = ");
	Serial.print (rock->slowdown_counter);
	Serial.print (" slowdown_rate = ");
	Serial.println (rock->slowdown_rate);
	Serial.println (" ");
#endif

	if (rock->slowdown_counter++ > rock->slowdown_rate)
	{
		rock->currentPosition = rock->currentPosition + increment;

		rock->servo.write(rock->currentPosition);
		rock->slowdown_counter = 0;
	}
}
//
//**********************************************************************
//
//  reportWaterLevel -- Report the water level in the tank to JMRI.
//
//**********************************************************************
//
void reportWaterLevel()
{
	//
	//  Determine the water level based on the tank capacity and the current servo position.
	int gaugeTravel = gauge->bottomPosition - gauge->topPosition;
	int waterLevel = TANK_CAPACITY - (int)(TANK_CAPACITY * 1.0/(float(gaugeTravel) / (float)(gauge->currentPosition - gauge->topPosition)));

#ifdef DEBUG
	Serial.print ("Water Level = ");
	Serial.println(waterLevel);
#endif

	//
	// We send the water level to JMRI as a 4-bit binary value using 4 consecutive JMRI sensors.
	for (int i=0; i<4; i++)
	{
		if ((waterLevel & 1<<i) == 0)
			LocoNet.reportSensor(WATER_LEVEL_LSB+i, INACTIVE);
		else
			LocoNet.reportSensor(WATER_LEVEL_LSB+i, ACTIVE);
	}

	//
	//  Set additional sensors to tell JMRI the state of the water tower.
	if (waterLevel == 0)
	{
		LocoNet.reportSensor(WATER_FLOWING, INACTIVE);
		LocoNet.reportSensor(TANK_EMPTY, ACTIVE);
	}
	else if (waterLevel > 0 && waterLevel < TANK_CAPACITY)
	{
		LocoNet.reportSensor(TANK_EMPTY, INACTIVE);
		if (gauge->direction == UP)
		{
			LocoNet.reportSensor(TANK_FILLING, ACTIVE);
			LocoNet.reportSensor(WATER_FLOWING, INACTIVE);
		}
		else
		{
			LocoNet.reportSensor(TANK_FILLING, INACTIVE);
			LocoNet.reportSensor(WATER_FLOWING, ACTIVE);
		}
	}
	else if (gauge->moving)
	{
		LocoNet.reportSensor(WATER_FLOWING, ACTIVE);
	}
	else
	{
		LocoNet.reportSensor(TANK_EMPTY, INACTIVE);
		LocoNet.reportSensor(TANK_FILLING, INACTIVE);
		LocoNet.reportSensor(WATER_FLOWING, INACTIVE);
	}
}
//
//**********************************************************************
//
//**********************************************************************
//
void moveServo(MY_SERVO_DEF *servo)
{
	int increment = 0;
	if ((servo->direction == UP) && (servo->topPosition > servo->bottomPosition))
	{
		increment = 1;
	}
	else if ((servo->direction == DOWN) && (servo->topPosition > servo->bottomPosition))
	{
		increment = -1;
	}
	else if ((servo->direction == UP) && (servo->topPosition < servo->bottomPosition))
	{
		increment = -1;
	}
	else
	{
		increment = 1;
	}

#ifdef DEBUG
	Serial.println (" ");
	Serial.print ("*** Moving servo ");
	Serial.print(servo->servoName);
	if (servo->direction == UP)
	{
		Serial.println ("UP");
	}
	else
	{
		Serial.println ("DOWN");
	}
	Serial.print (" current position = ");
	Serial.print (servo->currentPosition);  Serial.print (" increment = ");
	Serial.print (increment);
	Serial.print (" topPosition = ");
	Serial.print (servo->topPosition);
	Serial.print (" bottomPosition = ");
	Serial.print (servo->bottomPosition);
	Serial.print (" slowdown_counter = ");
	Serial.print (servo->slowdown_counter);
	Serial.print (" slowdown_rate = ");
	Serial.println (servo->slowdown_rate);
	Serial.println (" ");
#endif

	if (servo->slowdown_counter++ > servo->slowdown_rate)
	{
		servo->currentPosition = servo->currentPosition + increment;
		if (servo->direction == UP) 
		{
			if (((servo->currentPosition >= servo->topPosition) && increment > 0) || ((servo->currentPosition <= servo->topPosition) && increment < 0))
			{
				servo->currentPosition = servo->topPosition;
				servo->moving = false;
				servo->finishedMoving = true;
				servo->servo.detach();
#ifdef DEBUG
				Serial.print (" Finished moving servo ");
				Serial.print (servo->servoName);
				Serial.print (" Position = ");
				Serial.println (servo->currentPosition);
#endif
			}
		}
		else
		{
			if (((servo->currentPosition <= servo->bottomPosition) && increment < 0) || ((servo->currentPosition >= servo->bottomPosition) && increment > 0))
			{
				servo->currentPosition = servo->bottomPosition;
				servo->moving = false;
				servo->finishedMoving = true;
				servo->servo.detach();
#ifdef DEBUG
				Serial.print (" Finished moving servo ");
				Serial.print (servo->servoName);
				Serial.print (" Position = ");
				Serial.println (servo->currentPosition);
#endif
			}
		}
		servo->servo.write(servo->currentPosition);
		servo->slowdown_counter = 0;
	}
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
		reportWaterLevel();
	}
}
//
//---------------------------------------------------------------------------------------
//
// notifySensor - Called by JMRI/LocoNet when a sensor changes on JMRI.  We will see
// all LocoNet sensor notifications, but we only care about one...moving the spout up or down
//
//---------------------------------------------------------------------------------------
//
void notifySensor( uint16_t address, uint8_t state )
{
	//  Input from JMRI
	if (address == SPOUT_SENSOR)
	{
#ifdef DEBUG
		Serial.print ("In notifySensor State = ");
		Serial.print (state);
		Serial.print (" Address = ");
		Serial.println (address);
#endif  

		spout->servo.detach();
		gauge->servo.detach();
		SoftwareServo::refresh();

		if (!spout->moving)  
		{
			spout->servo.attach(SPOUT_PIN);
			spout->slowdown_counter = 0;
			spout->moving = true;
			LocoNet.reportSensor(SPOUT_MOVING, ACTIVE);
		}
		spout->finishedMoving = false;
		tankFilling = false;
		tankEmptying = false;
		gauge->moving = false;

		//  Active means lower spout and empty tank
		if (state != INACTIVE)
		{
			spout->direction = DOWN;
		}
		else // Inactive means raise spout & refill tank
		{
			spout->direction = UP;
		}
	}
	else if (address == ROCK_WOBBLE)
	{
		if (state != INACTIVE)
		{
			rockWobbling = true;
			//rockBouncing = false;
			//LocoNet.reportSensor(ROCK_BOUNCE, INACTIVE);
			rock->servo.attach(ROCK_PIN);
		}
		else
		{
			rockWobbling = false;
			rock->servo.detach();
		}

	}
	else if (address == ROCK_BOUNCE)
	{
		rockBouncing = (state != INACTIVE);
		if (state != INACTIVE)
		{
			rock->servo.attach (ROCK_PIN);
			rockTopLimit = ROCK_TOP_FAST;
			rockBottomLimit = ROCK_BOTTOM_FAST;
			rock->currentPosition = rockBottomLimit;

			//rockWobbling = false;
			//LocoNet.reportSensor(ROCK_WOBBLE, INACTIVE);
		}
		else
		{
			rock->servo.detach();
		}
	}
	else if (address == ROCK_RATE)
	{
		if (state != INACTIVE)
		{
			rock->slowdown_rate = ROCK_WOBBLE_FAST;
			rock->topPosition = ROCK_TOP_FAST;
			rock->bottomPosition = ROCK_BOTTOM_FAST;
		}
		else
		{
			rock->slowdown_rate = ROCK_WOBBLE_SLOW;
			rock->topPosition = ROCK_TOP_SLOW;
			rock->bottomPosition = ROCK_BOTTOM_SLOW;
		}
	}
}
