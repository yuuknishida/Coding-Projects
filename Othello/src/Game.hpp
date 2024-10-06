#include "ofMain.h"
#include "Player.hpp"

class Game : public Player
{
public:
    bool gameOver(Player p[][8]);
    int score(Player p[][8], char curPlayer);
    bool checkPieces(Player p[][8], int x, int y, int deltaX, int deltaY, char curPlayer, char opponent);
    void flipPieces(Player p[][8], int x, int y, int deltaX, int deltaY, char curPlayer, char opponent);
    bool checkMove(Player p[][8], int x, int y, char curPlayer);
    void makeMove(Player p[][8], int x, int y, char curPlayer);
};
