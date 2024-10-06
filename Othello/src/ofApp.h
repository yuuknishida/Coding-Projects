#pragma once

#include "ofMain.h"
#include "Game.hpp"
#include <istream>
#include <fstream>
#include <string>

#define N_MAX 100

class ofApp : public ofBaseApp{

	public:
        ofRectangle board[8][8];
        Player player[8][8];
        Game game;

        ofColor boardcolor;
        ofColor white;
        ofColor black;
        char playerTurn;
        char numturn[1][100];
        ofTrueTypeFont othello;
        ofTrueTypeFont instruction;
        ofTrueTypeFont scores;
        ofTrueTypeFont turn;
        int gameState;
        char text[10][100];
        int bPoints;
        int wPoints;
        
        int x[N_MAX];
        int y[N_MAX];
        int cx[N_MAX];
        int cy[N_MAX];
    
        int nx;
        int xmin;
        int xmax;
        int xstep;
        int ny;
        int ymin;
        int ymax;
        int ystep;
    
        int ncx;
        int cxmin;
        int cxmax;
        int cxstep;
        int ncy;
        int cymin;
        int cymax;
        int cystep;
    
        int index_j;
        int index_i;
    
        bool isEmpty;
        bool checkCanPlace;
        bool endgame = true;
    
		void setup();
		void update();
		void draw();

		void keyPressed(int key);
		void keyReleased(int key);
		void mouseMoved(int x, int y );
		void mouseDragged(int x, int y, int button);
		void mousePressed(int x, int y, int button);
		void mouseReleased(int x, int y, int button);
		void mouseEntered(int x, int y);
		void mouseExited(int x, int y);
		void windowResized(int w, int h);
		void dragEvent(ofDragInfo dragInfo);
		void gotMessage(ofMessage msg);
};
