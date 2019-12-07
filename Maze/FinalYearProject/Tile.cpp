#include "Tile.h"

Tile::Tile(Position pos) : 
	position(pos),
	type(0),
	r(0),
	g(0),
	b(255)
{
	neighbours.resize(4);
}

void Tile::setPosition(Position pos)
{
	position = pos;
}

Position Tile::getPosition()
{
	return position;
}

void Tile::setType(int val)
{
	type = val;

	switch (type)
	{
	case 0:
		r = 25;
		g = 200;
		b = 20;
		break;
	case 1:
		r = 120;
		g = 120;
		b = 120;
		break;
	case 2:
		r = 240;
		g = 210;
		b = 150;
		break;
	case 3:
		r = 101;
		g = 67;
		b = 33;
		break;
	default:
		break;
	}
}

int Tile::getType()
{
	return type;
}

Tile* Tile::Up()
{
	return neighbours[0];
}

Tile* Tile::Down()
{
	return neighbours[1];
}

Tile* Tile::Left()
{
	return neighbours[2];
}

Tile* Tile::Right()
{
	return neighbours[3];
}

void Tile::reset()
{
}

void Tile::render(SDL_Renderer* renderer, int size)
{
	rect.x = position.x * size;
	rect.y = position.y * size;
	rect.w = size * .9f;
	rect.h = size * .9f; 

	SDL_SetRenderDrawColor(renderer, r, g, b, 255);
	SDL_RenderFillRect(renderer, &rect);
	SDL_RenderDrawRect(renderer, &rect);
	SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
}
