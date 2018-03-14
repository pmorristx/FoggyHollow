#include "Arduino.h"
#include "SoftwareServo.h"

const uint8_t ACTIVE = 16;
const uint8_t INACTIVE = 0;

const uint8_t SWITCH_ON = 32; // Light ON
const uint8_t SWITCH_OFF = 0; // Light OFF

	struct MY_SERVO_DEF
	{
	//	String servoName;		// Name of the servo so we can identify the function
		bool moving;				// Indicates that the servo is currently moving
		bool finishedMoving = false;  	// Use to identify transition at end of move
		int currentPosition;			// Current position of servo (angle)
		int direction;					// Direction servo is moving (UP or DOWN)
		int topPosition;// Position (angle) of servo when spout is UP (tank is full)
		int bottomPosition;	// Position (angle) of servo when spout is DOWN (tank is empty)
		int slowdown_rate;// Indicates how many times through LOOP to skip between moving servo - slows down movement
		int slowdown_counter = 0;// Used with slowdown_rate to slow down movement...current counter
		SoftwareServo servo;			// Servo to move
	};

	struct LIGHT_DEF
	{
		int pin = -1;
		uint8_t currentIntensity = 0;
		uint8_t maxIntensity = 255;
		uint8_t dimIntensity = 70;
		uint8_t targetIntensity = 0;
		bool isDimmed = false;
		bool isOn = false;
		bool isDimming = false;
		bool isBrightening = false;
		bool isPWM = false;
		int rate = 2;
		int counter = 0;
		int dimCmd = -1;
		int onCmd = -1;
	};

class FoggyHollowClass
{
	public:
		FoggyHollowClass();
		void fadeOnOff(LIGHT_DEF *light, uint8_t state);
		void fadeLED(LIGHT_DEF *light, uint8_t requestedState);
};
extern  FoggyHollowClass FoggyHollow;
