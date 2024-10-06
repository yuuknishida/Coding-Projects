#include "ofMain.h"
class Player
{
public:
    int x;
    int y;
    int r;
    char player;
    ofColor color;
    
    Player();
    
    void set(int x_in, int y_in);
    void setColor(ofColor color_in);
    void print(string label);
    void drawStone();
};

