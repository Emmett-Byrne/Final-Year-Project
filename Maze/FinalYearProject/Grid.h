#pragma once
#include <vector>
#include <stdlib.h>
#include <time.h> 
#include "Tile.h"
class Grid
{
public:
	Grid(int width, int height);

	Tile* findAtPosition(Position pos);

	void render(SDL_Renderer* renderer);
private:
	void generateTiles(int width, int height);
	void randomizeTiles();
	void setNeighbours();
	void setTileTypes();
	void resetTiles();

	std::vector<Tile> grid;
	std::vector<Tile*> path;

	int tileSize;

	Tile* player;
};

