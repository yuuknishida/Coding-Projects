#include "ofApp.h"

using namespace std;

//--------------------------------------------------------------
void ofApp::setup(){
    Player();
    ofSetBackgroundColor(169, 169, 169);
    boardcolor.set(0, 255, 0);
    white.set(255, 255, 255);
    black.set(0, 0, 0);
    playerTurn = '.';
    othello.load("Roboto-Light.ttf", 50);
    instruction.load("Roboto-Light.ttf", 18);
    scores.load("Roboto-Light.ttf", 18);
    turn.load("Roboto-Light.ttf", 30);
    strcpy(text[0], "------------------------Rules of Gameplay------------------------");
    strcpy(text[1], "1. Each Player will each get a turn by clicking on a square on the board to place a stone.");
    strcpy(text[2], "2. To place a stone of your corresponding color it must follow the rules.");
    strcpy(text[3], "Rules- before you place a stone there must be a stone vertically, horizontally");
    strcpy(text[4], "and/or diagonally from the place you click.");
    strcpy(text[5], "To start press space.");
    
    //Board
    xmin = 100;
    xmax = 450;
    xstep = 50;
    ymin = 100;
    ymax = 450;
    ystep = 50;
    
    //Stones
    cxmin = 125;
    cxmax = 475;
    cxstep = 50;
    cymin = 125;
    cymax = 475;
    cystep = 50;
    
    //For the board
    nx = (xmax - xmin) / xstep + 1;
    for(int j=0;j<nx;j++)
    {
        x[j] = xmin + j * xstep;
    }
    
    ny = (ymax - ymin) / ystep + 1;
    for(int i=0;i<ny;i++)
    {
        y[i] = ymin + i * ystep;
    }
    //For the stones
        
    ncx = (cxmax - cxmin) / cxstep + 1;
    for(int j=0;j<ncx;j++)
    {
        cx[j] = cxmin + j * cxstep;
        
    }
    ncy = (cymax - cymin) / cystep + 1;
    for(int i=0;i<ncy;i++)
    {
        cy[i] = cymin + i * cystep;
    }
    
    for(int j=0;j<nx;j++)
    {
        for(int i=0;i<ny;i++)
        {
            board[j][i].set(x[j], y[i], xstep, ystep);
            player[j][i].set(cx[j], cy[i]);
        }
    }
}

//--------------------------------------------------------------
void ofApp::update(){
    bPoints = game.score(player, 'B');
    wPoints = game.score(player, 'W');
}

//--------------------------------------------------------------
void ofApp::draw()
{
    if(gameState == 0)
    {
        othello.drawString("Othello", 600, 100);
        instruction.drawString(text[0], 600, 200);
        instruction.drawString(text[1], 600, 220);
        instruction.drawString(text[2], 600, 240);
        instruction.drawString(text[3], 600, 260);
        instruction.drawString(text[4], 600, 280);
        instruction.drawString(text[5], 600, 300);
        scores.drawString(ofToString(bPoints), 220, 535);
        scores.drawString(ofToString(wPoints), 370, 535);
        if(playerTurn == 'B')
        {
            strcpy(numturn[0], "Black Player's Turn");
            turn.drawString(numturn[0], 200, 50);
        }
        if(playerTurn == 'W')
        {
            strcpy(numturn[0], "White Player's Turn");
            turn.drawString(numturn[0], 200, 50);
        }
        ofFill();
        ofSetColor(0, 0, 0);
        ofDrawCircle(175, 525, 20);
        
        ofFill();
        ofSetColor(255, 255, 255);
        ofDrawCircle(325, 525, 20);
        ofNoFill();
        ofSetColor(0, 0, 0);
        ofDrawCircle(325, 525, 20);
        
        for(int j=0;j<nx;j++)
        {
            for(int i=0;i<ny;i++)
            {
                ofFill();
                ofSetColor(boardcolor);
                ofDrawRectangle(x[j], y[i], xstep, ystep);
                ofNoFill();
                ofSetColor(0, 0, 0);
                ofDrawRectangle(x[j], y[i], xstep, ystep);
                
                if(player[j][i].player == 'B')
                {
                    player[j][i].setColor(black);
                    player[j][i].drawStone();
                }
                
                if(player[j][i].player == 'W')
                {
                    player[j][i].setColor(white);
                    player[j][i].drawStone();
                }
                
                if(game.checkMove(player, j, i, playerTurn) == true)
                {
                    if(playerTurn == 'B')
                    {
                        ofNoFill();
                        ofSetColor(0, 0, 0);
                        ofDrawCircle(player[j][i].x, player[j][i].y, player[j][i].r);
                    }
                    if(playerTurn == 'W')
                    {
                        ofNoFill();
                        ofSetColor(0, 0, 0);
                        ofDrawCircle(player[j][i].x, player[j][i].y, player[j][i].r);
                    }
                }
            }
        }
        
        if(game.gameOver(player) == true)
        {
            gameState = 1;

        }
    }
    if(gameState == 1)
    {
        if(bPoints > wPoints) turn.drawString("Black Player Wins", ofGetWidth()/2, ofGetHeight()/2);
        if(bPoints < wPoints) turn.drawString("White Player Wins", ofGetWidth()/2, ofGetHeight()/2);
    }
}

//--------------------------------------------------------------
void ofApp::keyPressed(int key){
    if(key == 32)
    {
        player[3][3].player = 'W';
        player[4][4].player = 'W';
        player[3][4].player = 'B';
        player[4][3].player = 'B';
        playerTurn = 'B';
    }
}

//--------------------------------------------------------------
void ofApp::keyReleased(int key){
}

//--------------------------------------------------------------
void ofApp::mouseMoved(int x, int y ){
}

//--------------------------------------------------------------
void ofApp::mouseDragged(int x, int y, int button)
{
    
}

//--------------------------------------------------------------
void ofApp::mousePressed(int x, int y, int button)
{
    if(game.gameOver(player) != true)
    {
        char piece, opponent;
        for(int j=0;j<nx;j++)       //xAxis
        {
            for(int i=0;i<ny;i++)   //yAxis
            {
                bool result = board[j][i].inside(x, y);
                if(result == true)
                {
                    index_i = i;
                    index_j = j;
                }
            }
        }
        checkCanPlace = game.checkMove(player, index_j, index_i, playerTurn);
        if(checkCanPlace == true)
        {
            game.makeMove(player, index_j, index_i, playerTurn);
            if(playerTurn == 'B') playerTurn = 'W';
            else playerTurn = 'B';
        }
        else
            cout << "\nInvalid move";
        if(game.gameOver(player) == true)
        {
            if(bPoints < wPoints)
                cout << " White Player Wins";
            if(wPoints > bPoints)
                cout << "Black Player wins";
        }
    }
}

//--------------------------------------------------------------
void ofApp::mouseReleased(int x, int y, int button){

}

//--------------------------------------------------------------
void ofApp::mouseEntered(int x, int y){

}

//--------------------------------------------------------------
void ofApp::mouseExited(int x, int y){

}

//--------------------------------------------------------------
void ofApp::windowResized(int w, int h){

}

//--------------------------------------------------------------
void ofApp::gotMessage(ofMessage msg){

}

//--------------------------------------------------------------
void ofApp::dragEvent(ofDragInfo dragInfo){
}
