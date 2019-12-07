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
	Position getPosition();
	void setType(int val);
	int getType();
	std::vector<Tile*>* getNeightbours() { return &neighbours; };
	Tile* Up();
	Tile* Down();
	Tile* Left();
	Tile* Right();
	void reset();
	void render(SDL_Renderer* renderer, int size);
private:
	Position position;
	std::vector<Tile*> neighbours; //[0] UP, [1]LEFT, [2]RIGHT, [3]DOWN
	int type; //0=nothing, 1=wall, 2=swamp, 3=sand

	SDL_Rect rect;
	int r;
	int g;
	int b;
};

