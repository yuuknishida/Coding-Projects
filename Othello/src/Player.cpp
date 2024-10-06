#include "Player.hpp"

Player::Player()
{
    r = 20;
    player = '.';
}
void Player::set(int x_in, int y_in)
{
    x = x_in;
    y = y_in;
}

void Player::setColor(ofColor color_in)
{
    color.set(color_in);
}

void Player::drawStone()
{
    ofFill();
    ofSetColor(color);
    ofDrawCircle(x, y, r);
    
    ofNoFill();
    ofSetColor(0, 0, 0);
    ofDrawCircle(x, y, r);
}

void Player::print(string label)
{
    cout << "\n\nStone Object: " << label;
    cout << "\n             x: " << x;
    cout << "\n             y: " << y;
    cout << "\n             r: " << r;
    cout << "\n         color: " << color;
    cout << "\n        Player: " << player;
}
