#include "Grid.h"

Grid::Grid(int width, int height):
	player(nullptr),
	tileSize(30)
{
	srand(time(NULL));
	generateTiles(width, height);
	randomizeTiles();
}

Tile* Grid::findAtPosition(Position pos)
{
	return nullptr;
}

void Grid::render(SDL_Renderer* renderer)
{
	for (int i = 0; i < grid.size(); i++)
	{
		grid[i].render(renderer, tileSize);
	}
}

void Grid::generateTiles(int width, int height)
{
	for (int i = 0; i < height; i++)
	{
		for (int j = 0; j < width; j++)
		{
			Position pos;
			pos.x = j;
			pos.y = i;
			Tile newTile(pos);
			grid.push_back(newTile);
		}
	}
}

void Grid::randomizeTiles()
{
	for (int i = 0; i < grid.size(); i++)
	{
		int normalChance = 10;
		int wallChance = 2;
		int swampChance = 3;
		int sandChance = 1;

		float randomNum = rand() % (normalChance + wallChance + sandChance + swampChance + 1);

		if (randomNum <= normalChance)
		{
			grid[i].setType(0);
		}
		else if (randomNum <= normalChance + wallChance)
		{
			grid[i].setType(1);
		}
		else if (randomNum <= normalChance + wallChance + swampChance)
		{
			grid[i].setType(2);
		}
		else if (randomNum <= normalChance + wallChance + swampChance + sandChance)
		{
			grid[i].setType(3);
		}
	}

}

void Grid::setNeighbours()
{
}

void Grid::setTileTypes()
{

}

void Grid::resetTiles()
{
}
