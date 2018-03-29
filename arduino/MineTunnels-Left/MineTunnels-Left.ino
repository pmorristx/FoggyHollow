//#define DEBUG

#include <LocoNet.h>
#include <FoggyHollow.h>

const int baseAddr = 212;

const int LN_TX_PIN = 7; // LocoNet
const int LN_RX_PIN = 8; // LocoNet

int pins[] = {3,4,5,6, 10,11,12,13, 14,15,16,17};
int numLights = sizeof(pins) / sizeof(int);
LIGHT_DEF* light[12];

lnMsg  *LnPacket;          // pointer to a received LNet packet

void setup()
{
	Serial.begin(115200);

	for (int i=0; i<numLights; i++)
	{
		light[i] = new LIGHT_DEF;
		light[i]->pin = pins[i];
		light[i]->onCmd = baseAddr + i;
		light[i]->isOn = false;
		pinMode(light[i]->pin, OUTPUT);
		digitalWrite(light[i]->pin, LOW);
		Serial.print ("initialized ");
		Serial.print (light[i]->onCmd);
		Serial.print (" pin #");
		Serial.println (light[i]->pin);
	}

	LocoNet.init(LN_TX_PIN);

}

void loop()
{
	// Check for any received LocoNet packets
	LnPacket = LocoNet.receive() ;
	if ( LnPacket )
	{
		LocoNet.processSwitchSensorMessage(LnPacket);
	}
}

void notifyPower(uint8_t state)
{
	for (int i=0; i<numLights; i++)
	{
		LocoNet.reportSensor(light[i]->onCmd, INACTIVE);
	}
}

void notifySwitchRequest( uint16_t address, uint8_t output, uint8_t state )
{
	for (int i=0; i<numLights; i++)
	{
		if (address == light[i]->onCmd)
		{
			Serial.print (" Address = ");
			Serial.print (address);
			Serial.print (" state = ");
			Serial.println (state);

			light[i]->isOn = state != INACTIVE;
			digitalWrite(light[i]->pin, light[i]->isOn ? HIGH : LOW);
		}
	}
}
