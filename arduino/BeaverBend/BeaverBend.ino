#define DEBUG


#include "SoftwareServo.h"
#include "LocoNet.h"
#include "FoggyHollow.h"

//int tim_delay = 500;
bool JMRI_ACTIVE = false;

uint8_t phase=LOW;
uint8_t trip=0;
uint8_t count=0;
uint8_t increment = 1;
int8_t angle = 45;

//
// Function Address Controls
const uint8_t CABIN_LIGHT_ADDR 			= 20;
const uint8_t TURNOUT_LEFT_ADDR 			= 21;
const uint8_t TURNOUT_LEFT_LANTERN_ADDR 	= 22;
const uint8_t TURNOUT_RIGHT_ADDR 			= 23;
const uint8_t TURNOUT_RIGHT_LANTERN_ADDR 	= 24;
const uint8_t STATION_MASTER_LIGHT_ADDR 	= 25;
const uint8_t STATION_MASTER_LIGHT_DIM_ADDR = 26;
const uint8_t TOWER_LIGHT_ADDR 			= 27;
const uint8_t TOWER_LIGHT_DIM_ADDR 		= 28;
const uint8_t ORDER_BOARD_LIGHT_ADDR 		= 29;
const uint8_t STATION_SIGN_LIGHTS_ADDR 	= 30;
const uint8_t RIGHT_TUNNEL_LIGHT_ADDR 		= 31;
const uint8_t MINE_TUNNEL_LIGHT_ADDR 		= 32;
const uint8_t CENTER_SERVOS_ADDR 			= 33;

const uint8_t CTC_SEND_INDICATOR_ADDR 		= 34;
const uint8_t CTC_RECEIVE_INDICATOR_ADDR 	= 35;
const uint8_t TURNOUT_LEFT_THROWN_INDICATOR_ADDR 	= 36;
const uint8_t TURNOUT_LEFT_CLOSED_INDICATOR_ADDR 	= 37;
const uint8_t TURNOUT_RIGHT_THROWN_INDICATOR_ADDR 	= 38;
const uint8_t TURNOUT_RIGHT_CLOSED_INDICATOR_ADDR 	= 39;

const uint8_t MIN_ADDR = 20;
const uint8_t MAX_ADDR = 39;


//
// Pin definitions

uint8_t ledPins [] = {3,5,6,9,10,11,12,13,14,15,16,18,19};
uint8_t turnoutPins[] = {2,4};

const uint8_t TURNOUT_LEFT_PIN 			= 2;
const uint8_t TURNOUT_RIGHT_PIN 		= 4;


const uint8_t TURNOUT_LEFT_LANTERN_PIN 	= 3;
const uint8_t TURNOUT_RIGHT_LANTERN_PIN = 5;
const uint8_t CABIN_LIGHT_PIN 			= 6;
const uint8_t LN_TX_PIN 				= 7;
const uint8_t LN_RX_PIN 				= 8;
const uint8_t STATION_MASTER_LIGHT_PIN 	= 14;  //A0
const uint8_t TOWER_LIGHT_PIN 			= 15; //A1
const uint8_t ORDER_BOARD_LIGHT_PIN 	= 16; //A2
const uint8_t STATION_SIGN_LIGHTS_PIN 	= 11; //A3

const uint8_t RIGHT_TUNNEL_LIGHT_PIN 	= 10;
const uint8_t MINE_TUNNEL_LIGHT_PIN 	= 13;

const uint8_t TURNOUT_LEFT_THROWN_INDICATOR_PIN 	= 9;
const uint8_t TURNOUT_LEFT_CLOSED_INDICATOR_PIN 	= 12;
const uint8_t TURNOUT_RIGHT_THROWN_INDICATOR_PIN 	= 18;
const uint8_t TURNOUT_RIGHT_CLOSED_INDICATOR_PIN 	= 19;

const uint8_t CABIN_LIGHT_IDX 				= 0;
const uint8_t TURNOUT_LEFT_LANTERN_IDX 		= 1;
const uint8_t TURNOUT_RIGHT_LANTERN_IDX 	= 2;
const uint8_t STATION_MASTER_LIGHT_IDX 		= 3;
const uint8_t TOWER_LIGHT_IDX 				= 4;
const uint8_t ORDER_BOARD_LIGHT_IDX 		= 5;
const uint8_t STATION_SIGN_LIGHTS_IDX 		= 6;
const uint8_t RIGHT_TUNNEL_LIGHT_IDX 		= 7;
const uint8_t MINE_TUNNEL_LIGHT_IDX 		= 8;

const uint8_t LEFT_THROWN_INDICATOR_IDX 	= 9;
const uint8_t LEFT_CLOSED_INDICATOR_IDX 	= 10;
const uint8_t RIGHT_THROWN_INDICATOR_IDX 	= 11;
const uint8_t RIGHT_CLOSED_INDICATOR_IDX 	= 12;

lnMsg  *LnPacket;          // pointer to a received LNet packet

const uint8_t numLights = sizeof(ledPins)/sizeof(ledPins[0]);
fh_light light[numLights];
fh_turnout turnouts[2];
SoftwareServo turnoutServos[2];

/**
 *  Setup - called once by Arduino on startup (power on?)
 */
void setup()
{
	#ifdef DEBUG
		Serial.begin(115200);
		Serial.println ("In setup");
	#endif

	JMRI_ACTIVE = false;

	LocoNet.init(LN_TX_PIN);
	// initialize the digital pins as outputs
	light[CABIN_LIGHT_IDX] = FoggyHollow.createLight(CABIN_LIGHT_PIN, CABIN_LIGHT_ADDR, FLICKERING, -1);

	light[RIGHT_TUNNEL_LIGHT_IDX] = FoggyHollow.createLight(RIGHT_TUNNEL_LIGHT_PIN, RIGHT_TUNNEL_LIGHT_ADDR, FLICKERING, -1);
	light[MINE_TUNNEL_LIGHT_IDX] = FoggyHollow.createLight(MINE_TUNNEL_LIGHT_PIN, MINE_TUNNEL_LIGHT_ADDR, FLICKERING, -1);

	light[STATION_SIGN_LIGHTS_IDX]= FoggyHollow.createLight(STATION_SIGN_LIGHTS_PIN, STATION_SIGN_LIGHTS_ADDR, ON_OFF, -1);
	light[ORDER_BOARD_LIGHT_IDX]= FoggyHollow.createLight(ORDER_BOARD_LIGHT_PIN, ORDER_BOARD_LIGHT_ADDR, ON_OFF, -1);
	light[TOWER_LIGHT_IDX] = FoggyHollow.createLight(TOWER_LIGHT_PIN, TOWER_LIGHT_ADDR, DIMMABLE, TOWER_LIGHT_DIM_ADDR);
	light[STATION_MASTER_LIGHT_IDX] = FoggyHollow.createLight(STATION_MASTER_LIGHT_PIN, STATION_MASTER_LIGHT_ADDR, DIMMABLE, STATION_MASTER_LIGHT_DIM_ADDR);

	light[LEFT_THROWN_INDICATOR_IDX] = FoggyHollow.createLight(TURNOUT_LEFT_THROWN_INDICATOR_PIN, TURNOUT_LEFT_THROWN_INDICATOR_ADDR, ON_OFF, -1);
	light[LEFT_CLOSED_INDICATOR_IDX] = FoggyHollow.createLight(TURNOUT_LEFT_CLOSED_INDICATOR_PIN, TURNOUT_LEFT_CLOSED_INDICATOR_ADDR, ON_OFF, -1);
	light[RIGHT_THROWN_INDICATOR_IDX] = FoggyHollow.createLight(TURNOUT_RIGHT_THROWN_INDICATOR_PIN, TURNOUT_RIGHT_THROWN_INDICATOR_ADDR, ON_OFF, -1);
	light[RIGHT_CLOSED_INDICATOR_IDX] = FoggyHollow.createLight(TURNOUT_RIGHT_CLOSED_INDICATOR_PIN, TURNOUT_RIGHT_CLOSED_INDICATOR_ADDR, ON_OFF, -1);

	turnouts[0] = FoggyHollow.createTurnout(TURNOUT_LEFT_PIN, TURNOUT_LEFT_ADDR,
			TURNOUT_LEFT_THROWN_INDICATOR_PIN, TURNOUT_LEFT_THROWN_INDICATOR_ADDR,
			TURNOUT_LEFT_CLOSED_INDICATOR_PIN, TURNOUT_LEFT_CLOSED_INDICATOR_ADDR);
	FoggyHollow.setCtcIndicators(&turnouts[0], CTC_SEND_INDICATOR_ADDR, CTC_RECEIVE_INDICATOR_ADDR);

  	turnouts[1] = FoggyHollow.createTurnout(TURNOUT_RIGHT_PIN, TURNOUT_RIGHT_ADDR,
			TURNOUT_RIGHT_THROWN_INDICATOR_PIN, TURNOUT_RIGHT_THROWN_INDICATOR_ADDR,
			TURNOUT_RIGHT_CLOSED_INDICATOR_PIN, TURNOUT_RIGHT_CLOSED_INDICATOR_ADDR);
	FoggyHollow.setCtcIndicators(&turnouts[1], CTC_SEND_INDICATOR_ADDR, CTC_RECEIVE_INDICATOR_ADDR);
    
	light[TURNOUT_LEFT_LANTERN_IDX]= FoggyHollow.createLight(TURNOUT_LEFT_LANTERN_PIN, TURNOUT_LEFT_LANTERN_ADDR, ON_OFF, -1);
	light[TURNOUT_RIGHT_LANTERN_IDX]= FoggyHollow.createLight(TURNOUT_RIGHT_LANTERN_PIN, TURNOUT_RIGHT_LANTERN_ADDR, ON_OFF, -1);

	for (int i = 0; i < numLights; i++)
	{
		FoggyHollow.setState(&light[i], false);
//		FoggyHollow.setFunctionState(light[i], false);
	}


//	reportSensors();
//	servo[0].attach(turnouts[0].servoPin);
//	servo[0].write(90);
//	SoftwareServo::refresh();
//	delay(4);
//	servo[0].detach();

	count = 0;
	phase = LOW;
	trip = 0;
#ifdef DEBUG
  	Serial.println ("turnouts[0]: ");
  	Serial.print ("turnouts[0].servoPin: ");
  	Serial.println (turnouts[0].servoPin);
  	Serial.print ("turnouts[0].turnoutAddr: ");
  	Serial.println (turnouts[0].turnoutAddr);
	Serial.println ("Setup complete 1");
#endif
}

/**
 * Reports all sensors we use to JMRI so they will populate the Sensor table.
 */
void reportSensors()
{
#ifdef DEBUG
	Serial.println ("Reporting sensors");
#endif
	//  Report initial state to JMRI...probably isn't listening

	for (uint8_t i=0; i<numLights; i++)
	{
		if (light[i].onCmd >= MIN_ADDR && light[i].onCmd <= MAX_ADDR)
		{
			LocoNet.reportSensor(light[i].onCmd, light[i].isOn ? ACTIVE : INACTIVE);
		}
	}
	LocoNet.reportSensor(CENTER_SERVOS_ADDR,  INACTIVE);
}

/**
 * Called over & over by Arduino to do things....
 */
void loop()
{

	// Check for any received LocoNet packets
	LnPacket = LocoNet.receive() ;
	if ( LnPacket )
	{
		LocoNet.processSwitchSensorMessage(LnPacket);
	}
	SoftwareServo::refresh();
	delay(4); // Milliseconds
	//
	//  Process turnouts.  We will check to see if any turnouts are in the process of moving.  If so,
	//  we will step the turnout one step.
	for (int i=0; i<2; i++)
	{
		FoggyHollow.moveTurnout(&turnouts[i], &turnoutServos[i]);
	}

	//
	//  Process lights ... we do this in the loop to handle flickering, fade on/off and dim (really fast flicker) lights.

	for (int i = 0; i < numLights; i++)
	{
		FoggyHollow.loop(&light[i]);
	}
}


// Callbacks from LocoNet.processSwitchSensorMessage() ...
// We tie into the ones connected to turnouts so we can capture anything
// that can change (or indicates change to) a turnout's position.
//

/**
*  Called when the user changes a turnout on JMRI
*/
void notifySwitchRequest( uint16_t address, uint8_t output, uint8_t direction )
{
#ifdef DEBUG1
	Serial.print ("In notifySwitchRequest, Address = ");
	Serial.print (address);
	Serial.print (" output = ");
	Serial.print (output);
	Serial.print (" direction = ");
	String tmp = " THROWN ";
	if (direction == 0)
	{
		tmp = " CLOSED";
	}
	Serial.println (tmp);
#endif
//	int idx = 0;
//	if (address >= MIN_ADDR && address <= MAX_ADDR)
//	{
//		for (int i=0; i<2; i++)
//		{
//			if (address == turnouts[i].turnoutAddr)
//			{
//#ifdef DEBUG
//					Serial.print ("In notifySwitchRequest, calling changeTurnout, direction = ");
//					Serial.println (direction);
//#endif
//				if (!turnouts[i].moving)
//				{
//					FoggyHollow.changeTurnout(&turnouts[i], direction, &turnoutServos[i]);
//				}
//				else
//				{
//#ifdef DEBUG
//					Serial.println ("In notifySwitchRequest, turnout already moving!!!");
//#endif
//				}
//			}
//		}

//		for (int i=0; i<numLights; i++)
//		{
//			if (address == light[i].onCmd)
//			{
//				FoggyHollow.setState(&light[i], direction == SWITCH_ON);
//			}
//			else if (address == light[i].functionCmd)
//			{
//				FoggyHollow.setFunctionState(&light[i], (direction == SWITCH_ON));
//			}
//		}
//	}
}
//---------------------------------------------------------------------------------------
//
// notifyPower - used to trigger reporting of sensor state when JMRI powers up.
//
//---------------------------------------------------------------------------------------
//
void notifyPower(uint8_t state)
{
#ifdef DEBUG
	Serial.println ("in notifyPower ");
#endif
	if (state)
	{
		//reportSensors();
		/*
		for (int i = 0; i < numLights; i++)
		{
			LocoNet.reportSwitch(light[i].onCmd);
			if (light[i].functionCmd >= 0)
			{
				LocoNet.reportSwitch(light[i].functionCmd);
			}
		}

		for (int i=0; i<numLights; i++)
		{
			if (light[i].isOn == ACTIVE)
				LocoNet.reportSensor(light[i].onCmd, ACTIVE);
			else
				LocoNet.reportSensor(light[i].onCmd, INACTIVE);

			if (light[i].functionCmd > 0)
			{
				if (light[i].isFunctionOn == ACTIVE)
					LocoNet.reportSensor(light[i].functionCmd, ACTIVE);
				else
					LocoNet.reportSensor(light[i].functionCmd, INACTIVE);
			}
		}
*/
	}
}

/**
 * Called when the user changes a sensor on JMRI
 */
void notifySensor(uint16_t address, uint8_t state)
{

	if (address >= MIN_ADDR && address <= MAX_ADDR)
	{
#ifdef DEBUG
		Serial.print ("In notifySensor, Address = ");
		Serial.print (address);
		Serial.print (" state = ");
		String outState = " INACTIVE";
		if (state == ACTIVE)
		{
			outState = " ACTIVE ";
		}
		Serial.println (outState);
#endif

		for (int i=0; i<2; i++)
		{
			//
			// Don't muck things up by changing a turnout that is already in the process of
			// moving.
			if ((address == turnouts[i].turnoutAddr) && (turnouts[i].currentState == IDLE))
			{
				FoggyHollow.changeTurnout(&turnouts[i], state, &turnoutServos[i]);
			}
		}
		for (int i=0; i<numLights; i++)
		{
			if (address == light[i].onCmd)
			{
				FoggyHollow.setState(&light[i], state != INACTIVE);
			}
			else if (address == light[i].functionCmd)
			{
				FoggyHollow.setFunctionState(&light[i], state != INACTIVE);
			}
		}
	}

}
