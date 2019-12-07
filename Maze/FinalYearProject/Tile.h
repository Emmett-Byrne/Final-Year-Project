#pragma once
#include "Position.h"
#include <vector>
#include <SDL.h>
#include <SDL_image.h>
class Tile
{
public:
	Tile(Position pos);
	void setPosition(Position pos);
	void setType(int val);
	std::vector<Tile*>* getNeightbours() { return &neighbours; };
	Tile* Up();
	Tile* Down();
	Tile* Left();
	Tile* Right();
	void reset();
	void render(SDL_Renderer* renderer, int size);
private:
	Position position;
	std::vector<Tile*> neighbours;
	int type; //0=nothing, 1=wall, 2=swamp, 3=sand

	SDL_Rect rect;
	int r;
	int g;
	int b;
};

