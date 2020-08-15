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
const uint16_t GATE_LIGHT_CMD = 89;
const uint16_t CHUTE_LEFT_CMD = 90;
const uint16_t CHUTE_RIGHT_CMD = 91;
const uint16_t BRIDGE_LEFT_CMD = 92;
const uint16_t BRIDGE_RIGHT_CMD = 93;
const uint16_t INSIDE_LIGHTS_CMD = 94;
const uint16_t CHUTE_LIGHT_CMD = 95;
const uint16_t EOT_LANTERN_WHITE_CMD = 96;
const uint16_t EOT_LANTERN_RED_CMD = 97;
const uint16_t ORE_BIN_SENSOR_CMD = 98;
const uint16_t EOT_SENSOR_CMD = 99;



uint8_t EOTState;
uint8_t OreBinState;

//
// Pin definitions

uint8_t ledPins [] = {4,5,6,9,10,11,12,16};
uint8_t chutePins[] = {2,3};

const int CHUTE_LEFT_PIN = 2;
const int CHUTE_RIGHT_PIN = 3;

const int BRIDGE_RIGHT_PIN = 4;
const int INSIDE_LEFT_PIN = 5;
const int INSIDE_RIGHT_PIN = 6;
const int LN_TX_PIN = 7;
const int LN_RX_PIN = 8;
const int EOT_LANTERN_WHITE_PIN = 9;
const int EOT_LANTERN_RED_PIN = 10;
const int BRIDGE_LEFT_PIN = 11;
const int CHUTE_LIGHT_PIN = 12;

const int EOT_SENSOR_PIN = 14;
const int ORE_BIN_SENSOR_PIN = 15;
const int GATE_LIGHT_PIN = 16;

lnMsg  *LnPacket;          // pointer to a received LNet packet

const int numLights = 8;
LIGHT_DEF* light[numLights];

void setup()   //******************************************************
{

#ifdef DEBUG
	Serial.begin(115200);
	//Serial.println ("In setup");
#endif



	JMRI_ACTIVE = false;
	// initialize the digital pins as outputs


	for (int i = 0; i < numLights; i++)
	{
		light[i] = new LIGHT_DEF;
	}

	light[0]->pin = BRIDGE_RIGHT_PIN;
	light[0]->onCmd = BRIDGE_RIGHT_CMD;

	light[1]->pin = INSIDE_LEFT_PIN;
	light[1]->onCmd = INSIDE_LIGHTS_CMD;

	light[2]->pin = INSIDE_RIGHT_PIN;

	light[3]->pin = EOT_LANTERN_WHITE_PIN;
	light[3]->onCmd = EOT_LANTERN_WHITE_CMD;

	light[4]->pin = EOT_LANTERN_RED_PIN;
	light[4]->onCmd = EOT_LANTERN_RED_CMD;

	light[5]->pin = BRIDGE_LEFT_PIN;
	light[5]->onCmd = BRIDGE_LEFT_CMD;

	light[6]->pin = CHUTE_LIGHT_PIN;
	light[6]->onCmd = CHUTE_LIGHT_CMD;

	light[7]->pin = GATE_LIGHT_PIN;
	light[7]->onCmd = GATE_LIGHT_CMD;

	for (int i = 0; i < numLights; i++)
	{
		pinMode(light[i]->pin, OUTPUT);
		digitalWrite(light[i]->pin, LOW);
		light[i]->isOn = false;
	}


	pinMode(EOT_SENSOR_PIN, INPUT_PULLUP);
	pinMode(ORE_BIN_SENSOR_PIN, INPUT_PULLUP);

	EOTState = -1;
	OreBinState = -1;

	LocoNet.init(LN_TX_PIN);

	// Init left chute
	servoParams[0].current_position = 0;
	servoParams[0].stop_value = 270;
	servoParams[0].start_value = 0;
	servoParams[0].increment = -1;

	// Init right chute
	servoParams[1].current_position = 0;
	servoParams[1].stop_value = 270;
	servoParams[1].start_value = 0;
	servoParams[1].increment = -1;
	for (int i=0; i<2; i++)
	{
		// attaches servo on pin to the servo object
		servo[i].attach(chutePins[i]);

		servo[i].write(servoParams[i].start_value);
		for (int t=0; t<servo_start_delay; t++)
		{
			SoftwareServo::refresh();
			delay(servo_init_delay);
		}
		servoParams[i].inuse = 0;
		servo[i].detach();
	}

	reportSensors();

#ifdef DEBUG
	Serial.println ("Setup complete");
#endif
}

void reportSensors()
{
	//  Report initial state to JMRI...probably isn't listening
	for (uint8_t i=0; i<numLights; i++)
	{
		LocoNet.reportSensor(light[i]->onCmd, light[i]->isOn ? ACTIVE : INACTIVE);
	}
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
						/*
						if (i == 0)
							LocoNet.reportSensor(CHUTE_LEFT_CMD, ACTIVE);
						else
							LocoNet.reportSensor(CHUTE_RIGHT_CMD, ACTIVE);
						*/
					}
				}
				if (servoParams[i].increment < 0) {
					if (servoParams[i].current_position < servoParams[i].start_value) 
					{
						servoParams[i].current_position = servoParams[i].start_value;
						servoParams[i].inuse = 0;
						servo[i].detach();
						/*
						if (i == 0)
							LocoNet.reportSensor(CHUTE_LEFT_CMD, INACTIVE);
						else
							LocoNet.reportSensor(CHUTE_RIGHT_CMD, INACTIVE);
							*/
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
}

/**
 *
 */
/*
void FoggyHollow.fadeLED(int lightPin, uint8_t state)
{
	//#define fadedelay 36
#define fadestep 8

	int fadedelay = fadestep * fadestep;
#ifdef DEBUG
	Serial.print("In FoggyHollow.fadeLED, state = ");
	Serial.println(state);
#endif
	if (state != LOW)
	{
#ifdef DEBUG
		Serial.print("Turning fade ON, pin = ");
		Serial.println(lightPin);
#endif

		for (int t = 1; t <= fadestep; t += 1)
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
		for (int t = 1; t <= fadestep; t += 1)
		{
			digitalWrite( lightPin, HIGH);
			delay(fadedelay - (fadedelay * (t / fadestep)));
			digitalWrite( lightPin, LOW);
			delay(fadedelay * (t / fadestep));
		}
		digitalWrite(lightPin, LOW);
	}
}
*/
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
		reportSensors();
	}
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

#ifdef DEBUG
	Serial.print ("In notifySensor State = ");
	Serial.print (state);
	Serial.print (" Address = ");
	Serial.println (address);
#endif
}
/**
*
*/
void notifySwitchRequest( uint16_t address, uint8_t output, uint8_t state )
{
#ifdef DEBUG
	Serial.print ("In notifySwitchRequest, Address = ");
	Serial.print (address);
	Serial.print (" Output = ");
	Serial.print (output);
	Serial.print (" state = ");
	Serial.println (state);
#endif
	int idx = 0;
	if (address >= GATE_LIGHT_CMD && address <= EOT_LANTERN_RED_CMD)
	{
		if (address == CHUTE_RIGHT_CMD || address == CHUTE_LEFT_CMD)
		{
			idx = address - CHUTE_LEFT_CMD;
			if (servoParams[idx].inuse == 0)  {
				servoParams[idx].inuse = 1;
				if (address == CHUTE_LEFT_CMD)
				{
					servo[idx].attach(CHUTE_LEFT_PIN);
					if (state != INACTIVE)
					{
						servoParams[idx].increment = 1;
						servoParams[idx].stop_value = 180; // Stop
					}
					else
					{
						servoParams[idx].increment = -1;
						servoParams[idx].stop_value = 0;  // Start
					}
				}
				else
				{
					servo[idx].attach(CHUTE_RIGHT_PIN);
					if (state != INACTIVE)
					{
						servoParams[idx].increment = 1;
						servoParams[idx].stop_value = 180; // Stop
					}
					else
					{
						servoParams[idx].increment = -1;
						servoParams[idx].stop_value = 0;  // Start
					}
				}
			}
		}

		for (int l=0; l<numLights; l++)
		{
			if (address == light[l]->onCmd)
			{
				if (address == INSIDE_LIGHTS_CMD)
				{
					FoggyHollow.fadeLED(light[l], state);
					delay(2000);
					FoggyHollow.fadeLED(light[l+1], state);
				}
				else if (address == EOT_LANTERN_WHITE_CMD)
				{
					if (state != INACTIVE)
					{
						FoggyHollow.fadeLED(light[3], ACTIVE);
						FoggyHollow.fadeLED(light[4], INACTIVE);
						LocoNet.reportSensor(EOT_LANTERN_RED_CMD, INACTIVE);
						LocoNet.requestSwitch(EOT_LANTERN_RED_CMD, output, INACTIVE);
					}
					else
					{
						FoggyHollow.fadeLED(light[3], INACTIVE);
					}
				}
				else if (address == EOT_LANTERN_RED_CMD)
				{
					if (state != INACTIVE)
					{
						FoggyHollow.fadeLED(light[l-1], INACTIVE);
						FoggyHollow.fadeLED(light[l], ACTIVE);
						LocoNet.reportSensor(EOT_LANTERN_WHITE_CMD, INACTIVE);
						//LocoNet.requestSwitch(EOT_LANTERN_WHITE_CMD, output, INACTIVE);
					}
					else
					{
						FoggyHollow.fadeLED(light[l], INACTIVE);
					}
				}
				else
				{
					FoggyHollow.fadeLED(light[l], state);
				}
			}
		}
	}
}
