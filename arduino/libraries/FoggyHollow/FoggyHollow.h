#include "Arduino.h"
#include "SoftwareServo.h"

const uint8_t ACTIVE = 16;
const uint8_t INACTIVE = 0;

const uint8_t SWITCH_ON = 32; // Light ON
const uint8_t SWITCH_OFF = 0; // Light OFF

const int ON_OFF = 0;
const int DIMMABLE = 1;
const int BLINKING = 2;
const int FLICKERING = 3;

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
		bool isFunctionOn = false;

		bool isInverted = false;

		int rate1 = 2;
		int rate2 = 2;
		int counter = 0;
		int functionCmd = -1;
		int onCmd = -1;
		int phase = LOW;
		int function = 0; // 0->onOff;
	};

class FoggyHollowClass
{
	public:
		FoggyHollowClass();
		void fadeOnOff(LIGHT_DEF *light, uint8_t state);
		void fadeLED(LIGHT_DEF *light, uint8_t requestedState);
		void blinkLED(LIGHT_DEF *light);
		void flickerLED(LIGHT_DEF *light);
		void loop (LIGHT_DEF *light);
		void fadeOn (LIGHT_DEF *light);
		void setState(LIGHT_DEF *light, bool state);
		void setFunctionState(LIGHT_DEF *light, bool state);

		LIGHT_DEF* createLight(int pin, int onCmd);
		LIGHT_DEF* createBlinkingLight(int pin, int onCmd, int blinkCmd);
		LIGHT_DEF* createDimmableLight(int pin, int onCmd, int dimCmd);
		LIGHT_DEF* createFlickeringLight(int pin, int onCmd, int rate);

};
extern  FoggyHollowClass FoggyHollow;
