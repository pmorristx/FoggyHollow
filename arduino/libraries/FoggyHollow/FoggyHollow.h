#ifndef FoggyHollow_h
#define FoggyHollow_h

#include "Arduino.h"
#include <SoftwareServo.h>

	// Sensor states
	const uint8_t ACTIVE = 16;
	const uint8_t INACTIVE = 0; // Check this value....note value is the same as "THROWN" and "SWITCH_OFF"

	// Turnout states
	const uint8_t CLOSED = 32;
	const uint8_t THROWN = 0;

	// Light states
	const uint8_t SWITCH_ON = 32; // Light ON
	const uint8_t SWITCH_OFF = 0; // Light OFF

	//
	// Light functions
	const uint8_t ON_OFF = 0;
	const uint8_t DIMMABLE = 1;
	const uint8_t BLINKING = 2;
	const uint8_t FLICKERING = 3;

	//
	// Turnout states
	const uint8_t IDLE = 0;		// Turnout is not moving...waiting for a command
	const uint8_t SENDING = 1;  // CTC is sending request to turnout to move
	const uint8_t MOVING = 2;	// Turnout is responding to CTC message to change
	const uint8_t RECEIVING = 3; // Turnout is responding to CTC that it has changed

	struct fh_light
	{
		uint8_t pin = -1;		// Arduino pin controlling LED
		uint8_t onCmd = -1;		// JMRI Sensor Address (command)
		uint8_t function = 0; 	// Function type of this light.  0->onOff;
		uint8_t functionCmd = -1; // JMRI Sensor Address of function command (dimming, etc.)
		uint16_t rate1 = 2;		// Blink/Flicker rate 1
		uint16_t rate2 = 2;		// Blink/Flicker rate 2

		uint8_t currentIntensity = 0;
		uint8_t maxIntensity = 255;
		uint8_t dimIntensity = 70;
		uint8_t targetIntensity = 0;

		bool isDimmed = false;
		bool isOn = false;
		bool isDimming = false;
		bool isBrightening = false;
		bool isPWM = false;
		bool isFunctionOn = false;
		bool isInverted = false;

		uint16_t counter = 0;
		uint8_t phase = LOW;
	};

	struct fh_turnout
	{
		uint8_t turnoutAddr;			// LocoNet turnout address
		uint8_t servoPin;				// Arduino servo control pin
		bool moving = false;			// Indicates that the servo is currently moving
		int8_t currentPosition;			// Current position of servo (angle)
		int8_t direction;				// Direction servo is moving
		int8_t increment=1;				// Current position increment to move servo
		uint8_t thrownPosition = 55;	// Position (angle) of servo
		uint8_t closedPosition = 145;	// Position (angle) of servo
		uint8_t currentState = IDLE;

        uint8_t servoSlowdown = 8;   	//servo loop counter limit
		uint8_t servoSlowCounter = 1; 	//servo loop counter to slowdown servo transit

		uint8_t thrownIndicatorPin;		// Arduino pin to activate when turnout is THROWN
		uint8_t thrownIndicatorAddr;	// Loconet address to report back to JMRI
		uint8_t closedIndicatorPin;		// Arduino pin to activate when turnout is CLOSED
		uint8_t closedIndicatorAddr;	// Loconet address to report back to JMRI

		uint8_t frogRelayThrownAddr;
		uint8_t frogRelayClosedAddr;
		uint8_t frogRelayThrownPin;
		uint8_t frogRelayClosedPin;

		uint8_t ctcSendIndicatorAddr;		// JMRI Sensor Address of CTC Send Relay
		uint8_t ctcReceiveIndicatorAddr;	// JMRI Sensor Address of CTC Receive Relay
		bool hasCtcIndicators = false;
		uint16_t ctcReceiveCount = 0;		// Counter used to keep CTC lights on
	};

	class FoggyHollowClass
	{
		public:
			FoggyHollowClass();
			void fadeOnOff(fh_light light, uint8_t state);
			void fadeLED(fh_light light, uint8_t requestedState);
			void blinkLED(fh_light *light);
			void flickerLED(fh_light *light);
			void loop (fh_light *light);
			void fadeOn (fh_light *light);
			void setState(fh_light *light, bool state);
			void setFunctionState(fh_light *light, bool state);

			fh_light createLight( uint8_t pin, uint8_t onCmd, uint8_t function, uint8_t functionCmd);

			fh_turnout createTurnout(uint8_t servoPin, uint8_t turnoutAddr,
					uint8_t thrownIndicatorAddr, uint8_t thrownIndicatorPin,
					uint8_t closedIndicatorAddr, uint8_t closedIndicatorPin);

			void changeTurnout(fh_turnout *turnout, uint8_t direction, SoftwareServo *turnoutServo);
			void setCtcIndicators(fh_turnout *turnout, uint8_t sendAddr, uint8_t receiveAddr);
			void moveTurnout(fh_turnout *turnout, SoftwareServo *turnoutServo);
	};
	extern  FoggyHollowClass FoggyHollow;

#endif
