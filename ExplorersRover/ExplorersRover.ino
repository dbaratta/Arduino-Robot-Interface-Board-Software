/******************************************************************************
 * Engineering Explorers Rover
 * 2013 - 2014
 *
 * Author: Dominic Baratta <dominic.baratta@lmco.com / dbaratta@buffalo.edu>
 *
 * CHANGE LOG
 * DATE     DEVELOPER     DESCRIPTION
 * 10/11/13 D. Baratta    Created
 *****************************************************************************/

#include <string.h>

#define M1_EN   2
#define M1_FWD  5
#define M1_REV  3
#define M2_EN   4
#define M2_FWD  9
#define M2_REV  6

void drive_motor(int motor_id, int direction, int speed);
void serial_rcv(void);
void process_cmd_string(void);

char cmd_string[128];
int index = 0;

void setup()
{
  /* Setup pin-modes */
  pinMode(M1_EN, OUTPUT);
  pinMode(M2_EN, OUTPUT);
  pinMode(M1_FWD, OUTPUT);
  pinMode(M1_REV, OUTPUT);
  pinMode(M2_FWD, OUTPUT);
  pinMode(M2_REV, OUTPUT);

  /* DISABLE both drive motors */
  digitalWrite(M1_EN, LOW);
  digitalWrite(M2_EN, LOW);

  Serial.begin(9600);
}

void loop()
{
serial_rcv();

}

void drive_motor(int motor_id, int direction, int speed)
{
  switch(direction)
  {
  case 0:
    // Forward
    if(motor_id == 1)
    {
      digitalWrite(M1_EN, HIGH);
      analogWrite(M1_REV, 0);
      analogWrite(M1_FWD, speed);
    }
    else if (motor_id == 2)
    {
      digitalWrite(M2_EN, HIGH);
      analogWrite(M2_REV, 0);
      analogWrite(M2_FWD, speed);
    }
    break;

  case 1:
    // Reverse
    if(motor_id == 1)
    {
      digitalWrite(M1_EN, HIGH);
      analogWrite(M1_FWD, 0);
      analogWrite(M1_REV, speed);
    }
    else if (motor_id == 2)
    {
      digitalWrite(M2_EN, HIGH);
      analogWrite(M2_FWD, 0);
      analogWrite(M2_REV, speed);
    }
    break;
  }
}

void serial_rcv()
{
  int is_done = 0;
  char c;
  while(is_done == 0)
  {
  //Serial.println("here2");
    if(Serial.available())
    {
      c = Serial.read();

          if(c == '\n')
          {
            is_done = 1;
          }
          else
          {
            cmd_string[index] = c;
            index++;
          }
    }


  }

  process_cmd_string();

  for(int i = 0; i < index; i++)
  {
    cmd_string[i] = NULL;
  }

  index = 0;

}

void process_cmd_string()
{
  char *tkn_p;
  int motor_idx;
  int direction;
  int speed;
  tkn_p = strtok(cmd_string, " ");

  motor_idx = atoi(&tkn_p[1]);
  if(tkn_p[2] == '+'){
    direction = 0;
  }
  else
  {
    direction = 1;
  }

  speed = (atoi(&tkn_p[3]) * 100);
  speed = speed + (atoi(&tkn_p[4]) * 10);
  speed = speed + atoi(&tkn_p[5]);
  
  drive_motor(motor_idx, direction, map(speed, 0, 100, 0, 255));

  tkn_p = strtok(NULL, " ");
    motor_idx = atoi(&tkn_p[1]);
    if(tkn_p[2] == '+'){
      direction = 0;
    }
    else
    {
      direction = 1;
    }

    speed = (atoi(&tkn_p[3]) * 100);
    speed = speed + (atoi(&tkn_p[4]) * 10);
    speed = speed + atoi(&tkn_p[5]);
    
    drive_motor(motor_idx, direction, map(speed, 0, 100, 0, 255));
}
