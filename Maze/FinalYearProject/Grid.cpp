#include "Grid.h"

Grid::Grid(int width, int height):
	player(nullptr),
	tileSize(30)
{
	srand(time(NULL));
	generateTiles(width, height);
	setNeighbours();
	randomizeTiles();
	player = findAtPosition(Position(0, 0));
}

Tile* Grid::findAtPosition(Position pos)
{
	for (int i = 0; i < grid.size(); i++)
	{
		if (pos.x == grid[i].getPosition().x && pos.y == grid[i].getPosition().y)
		{
			return &grid[i];
		}
	}
	return nullptr;
}

void Grid::render(SDL_Renderer* renderer)
{
	for (int i = 0; i < grid.size(); i++)
	{
		grid[i].render(renderer, tileSize);
	}

	renderPlayer(renderer);
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

		float randomNum = rand() % (normalChance + wallChance + sandChance + swampChance);

		if (randomNum < normalChance)
		{
			grid[i].setType(0);
		}
		else if (randomNum < normalChance + wallChance)
		{
			grid[i].setType(1);
		}
		else if (randomNum < normalChance + wallChance + swampChance)
		{
			grid[i].setType(2);
		}
		else if (randomNum < normalChance + wallChance + swampChance + sandChance)
		{
			grid[i].setType(3);
		}
	}

	findAtPosition(Position(0, 0))->setType(0);
}

void Grid::setNeighbours()
{
	for (int i = 0; i < grid.size(); i++)
	{
		Position gridPos = grid[i].getPosition();
		std::vector<Tile*>* neighbours = grid[i].getNeightbours();

		//Up
		if (gridPos.y > 0)
		{
			neighbours->at(0) = findAtPosition(Position(gridPos.x, gridPos.y -1));
		}

		//left
		if (gridPos.x > 0)
		{
			neighbours->at(1) = findAtPosition(Position(gridPos.x - 1, gridPos.y));
		}

		//right
		if (gridPos.x < 50)
		{
			neighbours->at(2) = findAtPosition(Position(gridPos.x + 1, gridPos.y));
		}

		//Down
		if (gridPos.y < 50)
		{
			neighbours->at(3) = findAtPosition(Position(gridPos.x, gridPos.y + 1));
		}
	}
}

void Grid::setTileTypes()
{

}

void Grid::resetTiles()
{
}

void Grid::renderPlayer(SDL_Renderer* renderer)
{
	Position position = player->getPosition();
	playerRect.x = position.x * tileSize + tileSize * .1;
	playerRect.y = position.y * tileSize + tileSize * .1;
	playerRect.w = tileSize * .7f;
	playerRect.h = tileSize * .7f;

	SDL_SetRenderDrawColor(renderer, 230, 20, 30, 255);
	SDL_RenderFillRect(renderer, &playerRect);
	SDL_RenderDrawRect(renderer, &playerRect);
	SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
}

void Grid::movePlayer(int direction)
{
	Tile* newTile = nullptr;
	Position current = player->getPosition();
	if (direction == 0) //UP
	{
		newTile = findAtPosition(Position(current.x, current.y - 1));
	}
	if (direction == 1) //LEFT
	{
		newTile = findAtPosition(Position(current.x - 1, current.y));
	}
	if (direction == 2) //RIGHT
	{
		newTile = findAtPosition(Position(current.x + 1, current.y));
	}
	if (direction == 3) //DOWN
	{
		newTile = findAtPosition(Position(current.x, current.y + 1));
	}

	if (newTile != nullptr && newTile->getType() != 1)
	{
		player = newTile;
	}
}
