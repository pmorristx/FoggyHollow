//#define DEBUG

#include <LocoNet.h>
#include <SoftwareServo.h> 

const uint8_t ACTIVE = 16;
const uint8_t INACTIVE = 0;

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

//
// Function Address Controls (lights on/off or chute up/down)
const int GATE_LIGHT = 89;
const int CHUTE_LEFT = 90;
const int CHUTE_RIGHT = 91;
const int BRIDGE_LEFT = 92;
const int BRIDGE_RIGHT = 93;
const int INSIDE_LIGHTS = 94;
const int CHUTE_LIGHT = 95;
const int EOT_LANTERN_WHITE = 96;
const int EOT_LANTERN_RED = 97;
const int ORE_BIN_SENSOR = 98;
const int EOT_SENSOR = 99;



uint8_t EOTState;
uint8_t OreBinState;

uint8_t sensorState[9];

//
// Pin definitions

uint8_t ledPins [] = {4,5,6,9,10,11,12,16};

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

void setup()   //******************************************************
{
#ifdef DEBUG
	Serial.begin(115200);
	//Serial.println ("In setup");
#endif

	// initialize the digital pins as outputs
	for (uint8_t i=0; i < sizeof(ledPins); i++)
	{
		pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
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
		servo[i].attach(ledPins[i]);

		servo[i].write(servoParams[i].start_value);
		for (int t=0; t<servo_start_delay; t++)
		{
			SoftwareServo::refresh();delay(servo_init_delay);
		}
		servoParams[i].inuse = 0;
		servo[i].detach();
	}

    for (uint8_t i=0; i<sizeof(sensorState); i++)
    {
    	sensorState[i] = 0;
    }
    reportSensors();
    
#ifdef DEBUG
	Serial.println ("Setup complete");
#endif
}

void reportSensors()
{
	//  Report initial state to JMRI...probably isn't listening
	for (uint8_t i=0; i<sizeof(sensorState); i++)
	{
	  LocoNet.reportSensor(i+89, sensorState[i]);
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


  uint8_t newState = digitalRead(EOT_SENSOR_PIN);
  //Serial.print (" new State = ");
  //Serial.println (newState);  
  if (newState != EOTState)
  {
    EOTState = newState;
    //  Have to flip the state from what hardware reads
    if (EOTState != LOW)
    {
      //  If the room is dark, the EOT sensors keep flipping
      if (sensorState[3] == ACTIVE && sensorState[4] == ACTIVE)
      {      
        LocoNet.reportSensor(EOT_SENSOR, ACTIVE); 
        LocoNet.reportSensor(EOT_LANTERN_RED, ACTIVE);
      }
    }
    else
    {
      if (sensorState[3] == ACTIVE && sensorState[4] == ACTIVE)
      {
        LocoNet.reportSensor(EOT_SENSOR, INACTIVE);              
        LocoNet.reportSensor(EOT_LANTERN_RED, INACTIVE);
      }
    }
  }

  newState = digitalRead(ORE_BIN_SENSOR_PIN);
  //Serial.print (" new State = ");
  //Serial.println (newState);
  if (newState != OreBinState)
  {
#ifdef DEBUG
  Serial.print (" OreBin State = ");
  Serial.print (OreBinState);
  Serial.print (" LOW = ");
  Serial.print (LOW);
  Serial.print (" newState = ");
  Serial.println (newState);  
#endif  
    OreBinState = newState;
    //  Have to flip the state from what hardware reads
    if (OreBinState != LOW)
    {
      //Serial.println ("Changing sensor state to ACTIVE");

      if (sensorState[2] == ACTIVE && sensorState[4] == ACTIVE)
      {
        LocoNet.reportSensor(ORE_BIN_SENSOR, ACTIVE);        
        LocoNet.reportSensor(EOT_LANTERN_WHITE, ACTIVE);
      }
    }
    else
    {
      //Serial.println ("Changing sensor state to INACTIVE");

      if (sensorState[2] == ACTIVE && sensorState[4] == ACTIVE)
      { 
        LocoNet.reportSensor(ORE_BIN_SENSOR, INACTIVE);                   
        LocoNet.reportSensor(EOT_LANTERN_WHITE, INACTIVE);
      } 
    }   
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
}

/**
 *
 */
void fadeOnOff(int lightPin, uint8_t state)
{
//#define fadedelay 36
#define fadestep 8

int fadedelay = fadestep * fadestep;
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
	Serial.print ("In notifySensor State = ");
	Serial.print (state);
	Serial.print (" Address = ");
	Serial.println (address);
#endif

	int idx = address - GATE_LIGHT;
  
	if (address >= GATE_LIGHT && address <= EOT_LANTERN_RED)
	{
		sensorState[idx] = state;
		reportSensors();
	}

	switch (address)
	{
	case CHUTE_RIGHT :
	case CHUTE_LEFT :
		if (servoParams[idx].inuse == 0)  {
			servoParams[idx].inuse = 1;
			if (address == CHUTE_LEFT)
			{
				servo[idx].attach(2);
				if (state == ACTIVE)
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
				servo[idx].attach(3);
				if (state == ACTIVE)
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

		break;

	case BRIDGE_LEFT :
		fadeOnOff(BRIDGE_LEFT_PIN, state);
		break;
	case BRIDGE_RIGHT :
		fadeOnOff(BRIDGE_RIGHT_PIN, state);
		break;
	case CHUTE_LIGHT :
		fadeOnOff(CHUTE_LIGHT_PIN, state);
		break;
  case GATE_LIGHT :
    fadeOnOff(GATE_LIGHT_PIN, state);
    break;    
    
	case INSIDE_LIGHTS :
		fadeOnOff(INSIDE_LEFT_PIN, state);
		delay(2000);
		fadeOnOff(INSIDE_RIGHT_PIN, state);
		break;

  //
  // EOT Lantern only allow one LED on at a time....but both can be off.
	case EOT_LANTERN_WHITE :
    if (state == ACTIVE)
    {
      //digitalWrite(EOT_LANTERN_RED_PIN, 0);     
      fadeOnOff(EOT_LANTERN_WHITE_PIN, state);
      LocoNet.reportSensor(EOT_LANTERN_RED, INACTIVE);   
    }
    else
    {
      digitalWrite(EOT_LANTERN_WHITE_PIN, 0);      
    }
		break;
  case EOT_LANTERN_RED :
    if (state == ACTIVE)
    {
      //digitalWrite(EOT_LANTERN_WHITE_PIN, 0);
      LocoNet.reportSensor(EOT_LANTERN_WHITE, INACTIVE);     
      fadeOnOff(EOT_LANTERN_RED_PIN, state);      
    }
    else
    {
      digitalWrite(EOT_LANTERN_RED_PIN, 0);      
    }
    break;
	}
}
