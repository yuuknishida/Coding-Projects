#include "Game.hpp"
 
bool Game::gameOver(Player p[][8])
{
    for(int j=0;j<8;j++)
    {
        for(int i=0;i<8;i++)
        {
            if (p[j][i].player == '.') return false;
        }
    }
    return true;
}
int Game::score(Player p[][8], char curPlayer)
{
    int total = 0;
    for(int x=0;x<8;x++)
    {
        for(int y=0;y<8;y++)
        {
            if (p[x][y].player == curPlayer) total++;
        }
    }
    return total;
}
bool Game::checkPieces(Player p[][8], int x, int y, int deltaX, int deltaY, char curPlayer, char opponent)
{
    if(p[x][y].player == opponent)
    {
        while ((x >= 0) && (x < 8) && (y >= 0) && (y < 8))
        {
            x = x + deltaX;
            y = y + deltaY;
            if ((x >= 0) && (x < 8) && (y >= 0) && (y < 8))
            {
                if (p[x][y].player == '.') return false;
                if (p[x][y].player == curPlayer) return true;
            }
        }
    }
    return false;
}
void Game::flipPieces(Player p[][8], int x, int y, int deltaX, int deltaY, char curPlayer, char opponent)
{
    while (p[x][y].player == opponent)
    {
        p[x][y].player = curPlayer;
        x = x + deltaX;
        y = y + deltaY;
    }
}
bool Game::checkMove(Player p[][8], int x, int y, char curPlayer)
{
    char opponent;
    if (p[x][y].player != '.') return false;
    if(curPlayer == 'B') opponent = 'W';
    if(curPlayer == 'W') opponent = 'B';
    //Left
    if(checkPieces(p, x-1, y, -1, 0, curPlayer, opponent) == true) return true;
    //Right
    if(checkPieces(p, x+1, y, 1, 0, curPlayer, opponent) == true) return true;
    //Up
    if(checkPieces(p, x, y-1, 0, -1, curPlayer, opponent) == true) return true;
    //Down
    if(checkPieces(p, x, y+1, 0, 1, curPlayer, opponent) == true) return true;
    //Lower Right
    if(checkPieces(p, x+1, y+1, 1, 1, curPlayer, opponent) == true) return true;
    //Upper Left
    if(checkPieces(p, x-1, y-1, -1, -1, curPlayer, opponent) == true) return true;
    //Lower Left
    if(checkPieces(p, x-1, y+1, -1, 1, curPlayer, opponent) == true) return true;
    //Upper Right
    if(checkPieces(p, x+1, y-1, 1, -1, curPlayer, opponent) == true) return true;
    
    return false;
}
void Game::makeMove(Player p[][8], int x, int y, char curPlayer)
{
    char opponent;
    if(curPlayer == 'B') opponent = 'W';
    if(curPlayer == 'W') opponent = 'B';
    
    //Left
    if(checkPieces(p, x-1, y, -1, 0, curPlayer, opponent) == true)
    {
        p[x][y].player = curPlayer;
        flipPieces(p, x-1, y, -1, 0, curPlayer, opponent);
    }
    //Right
    if(checkPieces(p, x+1, y, 1, 0, curPlayer, opponent) == true)
    {
        p[x][y].player = curPlayer;
        flipPieces(p, x+1, y, 1, 0, curPlayer, opponent);
    }
    //Up
    if(checkPieces(p, x, y-1, 0, -1, curPlayer, opponent) == true)
    {
        p[x][y].player = curPlayer;
        flipPieces(p, x, y-1, 0, -1, curPlayer, opponent);
    }
    //Down
    if(checkPieces(p, x, y+1, 0, 1, curPlayer, opponent) == true)
    {
        p[x][y].player = curPlayer;
        flipPieces(p, x, y+1, 0, 1, curPlayer, opponent);
    }
    //Lower Right
    if(checkPieces(p, x+1, y+1, 1, 1, curPlayer, opponent) == true)
    {
        p[x][y].player = curPlayer;
        flipPieces(p, x+1, y+1, 1, 1, curPlayer, opponent);
    }
    //Upper Left
    if(checkPieces(p, x-1, y-1, -1, -1, curPlayer, opponent) == true)
    {
        p[x][y].player = curPlayer;
        flipPieces(p, x-1, y-1, -1, -1, curPlayer, opponent);
    }
    //Lower Left
    if(checkPieces(p, x-1, y+1, -1, 1, curPlayer, opponent) == true)
    {
        p[x][y].player = curPlayer;
        flipPieces(p, x-1, y+1, -1, 1, curPlayer, opponent);
    }
    //Upper Right
    if(checkPieces(p, x+1, y-1, 1, -1, curPlayer, opponent) == true)
    {
        p[x][y].player = curPlayer;
        flipPieces(p, x+1, y-1, 1, -1, curPlayer, opponent);
    }
}
