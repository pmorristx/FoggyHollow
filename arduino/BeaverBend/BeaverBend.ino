//#define DEBUG

#include <LocoNet.h>
#include <SoftwareServo.h> 
#include <FoggyHollow.h>

//const uint8_t ACTIVE = 16;
//const uint8_t INACTIVE = 0;

SoftwareServo servo[2];
#define servo_start_delay 50
#define servo_init_delay 7
#define servo_slowdown  3   //servo loop counter limit
int servo_slow_counter = 1; //servo loop counter to slowdown servo transit

struct SERVO_DEF
{
  int inuse;
  int current_position;
  int increment;
  int stop_value;
  int start_value;
};
SERVO_DEF *servoParams = new SERVO_DEF[2];

int tim_delay = 500;
bool JMRI_ACTIVE = false;

//
// Function Address Controls (lights on/off or chute up/down)
const uint16_t CABIN_LIGHT_CMD = 20;
const uint16_t TURNOUT_LEFT_CMD = 21;
const uint16_t TURNOUT_LEFT_LANTERN_CMD = 22;
const uint16_t TURNOUT_RIGHT_CMD = 23;
const uint16_t TURNOUT_RIGHT_LANTERN_CMD = 24;
const uint16_t STATION_MASTER_LIGHT_CMD = 25;
const uint16_t STATION_MASTER_LIGHT_DIM_CMD = 26;
const uint16_t TOWER_LIGHT_CMD = 27;
const uint16_t TOWER_LIGHT_DIM_CMD = 28;
const uint16_t ORDER_BOARD_LIGHT_CMD = 29;
const uint16_t STATION_SIGN_LIGHTS_CMD = 30;
const uint16_t RIGHT_TUNNEL_LIGHT_CMD = 31;
const uint16_t MINE_TUNNEL_LIGHT_CMD = 32;
const uint16_t CENTER_SERVOS_CMD = 33;

const uint16_t MIN_CMD = 20;
const uint16_t MAX_CMD = 33;


//
// Pin definitions

uint8_t ledPins [] = {4,5,6,9,10,11,12,16};
uint8_t turnoutPins[] = {2,3};

const int TURNOUT_LEFT_PIN = 2;
const int TURNOUT_RIGHT_PIN = 3;

const int CABIN_LIGHT_PIN = 4;
const int TURNOUT_LEFT_LANTERN_PIN = 5;
const int TURNOUT_RIGHT_LANTERN_PIN = 6;
const int LN_TX_PIN = 7;
const int LN_RX_PIN = 8;
const int STATION_MASTER_LIGHT_PIN = 14;  //A0
const int TOWER_LIGHT_PIN = 15; //A1
const int ORDER_BOARD_LIGHT_PIN = 16; //A2
const int STATION_SIGN_LIGHTS_PIN = 11; //A3

const int RIGHT_TUNNEL_LIGHT_PIN = 10;
const int MINE_TUNNEL_LIGHT_PIN = 11;

const int CABIN_LIGHT_IDX = 0;
const int TURNOUT_LEFT_LANTERN_IDX = 1;
const int TURNOUT_RIGHT_LANTERN_IDX = 2;
const int STATION_MASTER_LIGHT_IDX = 3;
const int TOWER_LIGHT_IDX = 4;
const int ORDER_BOARD_LIGHT_IDX = 5;
const int STATION_SIGN_LIGHTS_IDX = 6;
const int RIGHT_TUNNEL_LIGHT_IDX = 7;
const int MINE_TUNNEL_LIGHT_IDX = 8;

lnMsg  *LnPacket;          // pointer to a received LNet packet

const int numLights = 9;
LIGHT_DEF* light[numLights];


void setup()   //******************************************************
{

#ifdef DEBUG
	Serial.begin(115200);
	Serial.println ("In setup");
#endif



	JMRI_ACTIVE = false;
	// initialize the digital pins as outputs

#ifdef DEBUG
  Serial.println ("Starting pin assignment");
#endif
	light[CABIN_LIGHT_IDX] = FoggyHollow.createFlickeringLight(CABIN_LIGHT_PIN, CABIN_LIGHT_CMD, 40);

	light[RIGHT_TUNNEL_LIGHT_IDX] = FoggyHollow.createFlickeringLight(RIGHT_TUNNEL_LIGHT_PIN, RIGHT_TUNNEL_LIGHT_CMD, 65);
	light[MINE_TUNNEL_LIGHT_IDX] = FoggyHollow.createFlickeringLight(MINE_TUNNEL_LIGHT_PIN, MINE_TUNNEL_LIGHT_CMD, 65);
#ifdef DEBUG
  Serial.println ("Pin assignment complete for tunnel lights");
#endif 
	light[STATION_SIGN_LIGHTS_IDX]= FoggyHollow.createLight(STATION_SIGN_LIGHTS_PIN, STATION_SIGN_LIGHTS_CMD);
	light[ORDER_BOARD_LIGHT_IDX]= FoggyHollow.createLight(ORDER_BOARD_LIGHT_PIN, ORDER_BOARD_LIGHT_CMD);
  light[TOWER_LIGHT_IDX] = FoggyHollow.createDimmableLight(TOWER_LIGHT_PIN, TOWER_LIGHT_CMD, TOWER_LIGHT_DIM_CMD);
  light[STATION_MASTER_LIGHT_IDX] = FoggyHollow.createDimmableLight(STATION_MASTER_LIGHT_PIN, STATION_MASTER_LIGHT_CMD, STATION_MASTER_LIGHT_DIM_CMD);
#ifdef DEBUG
  Serial.println ("Pin assignment complete for station lights");
#endif 
    
	light[TURNOUT_LEFT_LANTERN_IDX]= FoggyHollow.createLight(TURNOUT_LEFT_LANTERN_PIN, TURNOUT_LEFT_LANTERN_CMD);
	light[TURNOUT_RIGHT_LANTERN_IDX]= FoggyHollow.createLight(TURNOUT_RIGHT_LANTERN_PIN, TURNOUT_RIGHT_LANTERN_CMD);


#ifdef DEBUG
  Serial.println ("Pin assignment complete for turnout lanterns");
#endif 
	for (int i = 0; i < numLights; i++)
	{
		FoggyHollow.setState(light[i], false);
		FoggyHollow.setFunctionState(light[i], false);
	}
#ifdef DEBUG
  Serial.println ("Pin assignment complete");
#endif
	LocoNet.init(LN_TX_PIN);

	// Init left turnout
	servoParams[0].current_position =  135; // was 0;
	servoParams[0].stop_value = 135; // was 270
	servoParams[0].start_value = 45; // was 0
	servoParams[0].increment = -1;
	//turnout[i]->thrownPosition = 45;
	//turnout[i]->closedPosition = 135;

	// Init right turnout
	servoParams[1].current_position = 135; // was 0;
	servoParams[1].stop_value = 135; // was 270
	servoParams[1].start_value = 45; // was 0;
	servoParams[1].increment = -1;
	for (int i=0; i<2; i++)
	{
		// attaches servo on pin to the servo object
		servo[i].attach(turnoutPins[i]);

		servo[i].write(servoParams[i].start_value);
		for (int t=0; t<servo_start_delay; t++)
		{
			SoftwareServo::refresh();
			delay(servo_init_delay);
		}
		servoParams[i].inuse = 0;
		servo[i].detach();
	}
#ifdef DEBUG
  Serial.println ("Servo setup complete");
#endif
	reportSensors();

#ifdef DEBUG
	Serial.println ("Setup complete");
#endif
}

void reportSensors()
{
#ifdef DEBUG
	Serial.println ("Reporting sensors");
#endif
	//  Report initial state to JMRI...probably isn't listening
	for (uint8_t i=0; i<numLights; i++)
	{
		//LocoNet.reportSensor(light[i]->onCmd, light[i]->isOn ? ACTIVE : INACTIVE);
		LocoNet.reportSwitch(light[i]->onCmd);
		if (light[i]->functionCmd >= 0)
		{
			LocoNet.reportSwitch(light[i]->functionCmd);
		}
	}
	//LocoNet.reportSensor(CENTER_SERVOS_CMD,  INACTIVE);
	LocoNet.reportSwitch(CENTER_SERVOS_CMD);
}

void loop()   //**********************************************************************
{
	// Check for any received LocoNet packets
	LnPacket = LocoNet.receive() ;
	if ( LnPacket )
	{
		//Serial.println ("Loconet message received");
		LocoNet.processSwitchSensorMessage(LnPacket);
		// this function will call the specially named functions below...
	}

	SoftwareServo::refresh();
	delay(4);

	for (int i=0; i<2; i++)
	{
		if (servoParams[i].inuse==1)
		{
			if (servo_slow_counter++ > servo_slowdown)
			{
				servoParams[i].current_position = servoParams[i].current_position + servoParams[i].increment;
				if (servoParams[i].increment > 0) {
					if (servoParams[i].current_position > servoParams[i].stop_value) 
					{
						servoParams[i].current_position = servoParams[i].stop_value;
						servoParams[i].inuse = 0;
						servo[i].detach();
					}
				}
				if (servoParams[i].increment < 0) {
					if (servoParams[i].current_position < servoParams[i].start_value) 
					{
						servoParams[i].current_position = servoParams[i].start_value;
						servoParams[i].inuse = 0;
						servo[i].detach();
					}
				}

#ifdef DEBUG       
				Serial.print (" Start position = ");
				Serial.print (servoParams[i].start_value);
				Serial.print (" Stop position = ");
				Serial.print (servoParams[i].stop_value);
				Serial.print (" Servo position = ");
				Serial.println(servoParams[i].current_position);
#endif        
				servo[i].write(servoParams[i].current_position);
				servo_slow_counter = 0;
			}
		}
	}

	for (int i = 0; i < numLights; i++)
	{
		FoggyHollow.loop(light[i]);
	}
}

// Callbacks from LocoNet.processSwitchSensorMessage() ...
// We tie into the ones connected to turnouts so we can capture anything
// that can change (or indicates change to) a turnout's position.
//
//---------------------------------------------------------------------------------------
//
// notifyPower - used to trigger reporting of sensor state when JMRI powers up.
//
//---------------------------------------------------------------------------------------
//
void notifyPower(uint8_t state)
{
	if (state)
	{
		//reportSensors();
		for (int i = 0; i < numLights; i++)
		{
#ifdef DEBUG
			Serial.print ("In notifyPower, Address = ");
			Serial.print (light[i]->onCmd);
#endif
			LocoNet.reportSwitch(light[i]->onCmd);
			if (light[i]->functionCmd >= 0)
			{
				LocoNet.reportSwitch(light[i]->functionCmd);
			}
		}

		for (int i=0; i<numLights; i++)
		{
			if (light[i]->isOn == ACTIVE)
				LocoNet.reportSensor(light[i]->onCmd, ACTIVE);
			else
				LocoNet.reportSensor(light[i]->onCmd, INACTIVE);

			if (light[i]->functionCmd > 0)
			{
				if (light[i]->isFunctionOn == ACTIVE)
					LocoNet.reportSensor(light[i]->functionCmd, ACTIVE);
				else
					LocoNet.reportSensor(light[i]->functionCmd, INACTIVE);
			}
		}

	}
}


void notifySensor(uint16_t address, uint8_t state)
{
#ifdef DEBUG
	Serial.print ("In notifySensor, Address = ");
	Serial.print (address);
	Serial.print (" state = ");
	Serial.println (state);
#endif

	//  Center the turnout servos to set the arm....kinda one-time use.
	if (address == CENTER_SERVOS_CMD)
	{
		for (int i=0; i<2; i++)
		{
			servo[i].attach(turnoutPins[i]);
			servo[i].write(90);
			servo[i].detach();
		}
	}
}
/**
*
*/


void notifySwitchRequest( uint16_t address, uint8_t output, uint8_t state )
{
#ifdef DEBUG
	Serial.print ("In notifySwitchRequest, Address = ");
	Serial.print (address);
	Serial.print (" output = ");
	Serial.print (output);
	Serial.print (" state = ");
	Serial.println (state);
#endif
	int idx = 0;
	if (address >= MIN_CMD && address <= MAX_CMD)
	{
		if (address == TURNOUT_RIGHT_CMD || address == TURNOUT_LEFT_CMD)
		{

			if (address == TURNOUT_RIGHT_CMD)
			{
				idx = 1;
			}
			if (servoParams[idx].inuse == 0)  {
				servoParams[idx].inuse = 1;
				if (address == TURNOUT_LEFT_CMD)
				{
					servo[idx].attach(TURNOUT_LEFT_PIN);
					if (state != INACTIVE)
					{
						servoParams[idx].increment = 1;
						servoParams[idx].stop_value = 135; // Stop
					}
					else
					{
						servoParams[idx].increment = -1;
						servoParams[idx].stop_value = 45;  // Start
					}
				}
				else
				{
					servo[idx].attach(TURNOUT_RIGHT_PIN);
					if (state != INACTIVE)
					{
						servoParams[idx].increment = 1;
						servoParams[idx].stop_value = 135; // Stop
					}
					else
					{
						servoParams[idx].increment = -1;
						servoParams[idx].stop_value = 45;  // Start
					}
				}
			}
		}
		else if (address == CENTER_SERVOS_CMD)
		{
			//  Center the turnout servos to set the arm....kinda one-time use.

			for (int i=0; i<2; i++)
			{
#ifdef DEBUG
				Serial.print ("In notifySwitchRequest, resetting servo = ");
				Serial.println (i);
#endif
				servo[i].attach(turnoutPins[i]);
				servo[i].write(90);
				SoftwareServo::refresh();
				delay(4);
				servo[i].detach();
			}
		}

		for (int i=0; i<numLights; i++)
		{
			if (address == light[i]->onCmd)
			{
				FoggyHollow.setState(light[i], state == SWITCH_ON);
			}
			else if (address == light[i]->functionCmd)
			{
				FoggyHollow.setFunctionState(light[i], (state == SWITCH_ON));
			}
		}
/*
		for (int l=0; l<numLights; l++)
		{
			if (address == light[l]->onCmd)
			{
				FoggyHollow.fadeLED(light[l], state);
			}
		}
*/
	}
}
