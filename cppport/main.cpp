#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <vector>
#include <iostream>
#include <map>
#define SHAPE_SIZE_W 4
#define SHAPE_SIZE_H 6
#define WINDOW_W 640
#define WINDOW_H 480

const int SCALE_FACTOR = 5;
std::vector<SDL_Rect> srcRectList; 
std::vector<SDL_Rect> destRectList; 
//const char text[] = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvqxyz{|}~~"; 
const char text[] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque posuere, est eu finibus posuere, velit nunc faucibus orci, eget congue ligula erat eu nisi. Mauris sed accumsan risus. Nulla pretium urna eu ante consequat lobortis. Suspendisse non arcu porta, aliquam ante eu, ornare tellus. Ut vestibulum vel ex quis consequat. Phasellus auctor fringilla orci, ac viverra metus pulvinar at. Suspendisse non lectus eget justo dapibus scelerisque. Nullam nec venenatis lorem, in elementum sem. Cras sollicitudin ligula vitae nibh dignissim sagittis. Duis vitae finibus nibh. Maecenas ut orci a elit tristique porta quis in massa. Suspendisse id mattis mi, eu dapibus enim. Praesent sodales ante eget ligula euismod, vel pulvinar nibh tempor.";
//const char text[] = "abcde";
//int num_elements = (sizeof( text ) / sizeof( text[0] ))-1;

int main(int argc, char *argv[])
{
  //std::cout << num_elements << std::endl;
  SDL_Window* Main_Window;
  SDL_Renderer* Main_Renderer;
  SDL_Surface* Loading_Surf;
  SDL_Texture* Font_Tx;

  /* Rectangles for drawing which will specify source (inside the texture)
  and target (on the screen) for rendering our textures. */
  SDL_Rect SrcR;
  SDL_Rect DestR;

  SrcR.x = 0;
  SrcR.y = 0;
  SrcR.w = SHAPE_SIZE_W;
  SrcR.h = SHAPE_SIZE_H;

  DestR.x = 0;
  DestR.y = 0;
  DestR.w = SHAPE_SIZE_W * SCALE_FACTOR;
  DestR.h = SHAPE_SIZE_H * SCALE_FACTOR;

  for(int column = 0; column < 4; column++){
  	for(int row = 0; row < 32; row++){
  		SrcR.x = row*4;
  		SrcR.y = column*6;
  		DestR.x = row*4*SCALE_FACTOR;
  		DestR.y = column*6*SCALE_FACTOR;
  		srcRectList.push_back(SrcR);
  		destRectList.push_back(DestR);
  	}
  }
  
  auto myDict = std::map<const char, int>{ {' ', 32}, {'!', 33}, {'"', 34}, {'#', 35} ,{'$', 36} ,{'%', 37}, {'&', 38}, {'\'', 39},
					   { '(', 40 }, { ')', 41 }, { '*', 42 }, {'+', 43}, {',', 44}, {'-', 45}, {'.', 46}, {'/', 47},
					   { '0', 48 }, { '1', 49 }, { '2', 50 }, {'3', 51}, {'4', 52}, {'5', 53}, {'6', 54}, {'7', 55},
					   { '8', 56}, { '9', 57}, { ':', 58}, {';', 59}, {'<', 60}, {'=', 61}, {'>', 62}, {'?', 63},
					   { '@', 64}, { 'A', 65}, { 'B', 66}, {'C', 67}, {'D', 68}, {'E', 69}, {'F', 70}, {'G', 71},
					   { 'H', 72}, { 'I', 73}, { 'J', 74}, {'K', 75}, {'L', 76}, {'M', 77}, {'N', 78}, {'O', 79},
					   { 'P', 80}, { 'Q', 81}, { 'R', 82}, {'S', 83}, {'T', 84}, {'U', 85}, {'V', 86}, {'W', 87},
					   { 'X', 88}, { 'Y', 89}, { 'Z', 90}, {'[', 91}, {'\\', 92}, {']', 93}, {'^', 94}, {'_', 95},
					   { '`', 96}, { 'a', 97}, { 'b', 98}, {'c', 99}, {'d', 100}, {'e', 101}, {'f', 102}, {'g', 103},
					   { 'h', 104}, { 'i', 105}, { 'j', 106}, {'k', 107}, {'l', 108}, {'m', 109}, {'n', 110}, {'o', 111},
					   { 'p', 112}, { 'q', 113}, { 'r', 114}, {'s', 115}, {'t', 116}, {'u', 117}, {'v', 118}, {'w', 119},
					   { 'x', 120}, { 'y', 121}, { 'z', 122}, {'{', 123}, {'|', 124}, {'}', 125}, {'~', 126}, {'\0', 127} };
  //std::cout << myDict['$'] << std::endl;

  /*
  for(unsigned int i = 0; i < rectList.size(); ++i){
  std::cout << "x: " << rectList[i].x << std::endl;
  std::cout << "y: " << rectList[i].y << std::endl;
  std::cout << "w: " << rectList[i].w << std::endl;
  std::cout << "h: " << rectList[i].h << std::endl;
  }
  */

  /* Before we can render anything, we need a window and a renderer */
  Main_Window = SDL_CreateWindow("SDL_RenderCopy Example",
  SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, WINDOW_W, WINDOW_H, 0);
  Main_Renderer = SDL_CreateRenderer(Main_Window, -1, SDL_RENDERER_ACCELERATED);

  /* The loading of the background texture. Since SDL_LoadBMP() returns
  a surface, we convert it to a texture afterwards for fast accelerated
  blitting. */
  Loading_Surf = IMG_Load("tom-thumb-new.png");
  Font_Tx = SDL_CreateTextureFromSurface(Main_Renderer, Loading_Surf);
  SDL_FreeSurface(Loading_Surf); /* we got the texture now -> free surface */

  //Our event structure
  SDL_Event e;
  //For tracking if we want to quit
  bool quit = false;
  while (!quit){
  	//Read any events that occured, for now we'll just quit if any event occurs
  	while (SDL_PollEvent(&e)){
  		//If user closes the window
  		if (e.type == SDL_QUIT){
  			quit = true;
  		}
  		//If user presses any key
  		if (e.type == SDL_KEYDOWN){
  			quit = true;
  		}
  		//If user clicks the mouse
  		if (e.type == SDL_MOUSEBUTTONDOWN){
  			quit = true;
  		}
  	}

	SDL_RenderClear(Main_Renderer);	
	for(int i = 0; i < 128; ++i){
		SDL_RenderCopy(Main_Renderer, Font_Tx, &srcRectList[myDict[text[i]]], &destRectList[i] );
	}
	//SDL_RenderCopy(Main_Renderer, Font_Tx, &srcRectList[36], &destRectList[0] );

     	/* render the current animation step of our shape */
      	SDL_RenderPresent(Main_Renderer);
  }	

  /* The renderer works pretty much like a big canvas:
  when you RenderCopy() you are adding paint, each time adding it
  on top.
  You can change how it blends with the stuff that
  the new data goes over.
  When your 'picture' is complete, you show it
  by using SDL_RenderPresent(). */

  /* SDL 1.2 hint: If you're stuck on the whole renderer idea coming
  from 1.2 surfaces and blitting, think of the renderer as your
  main surface, and SDL_RenderCopy() as the blit function to that main
  surface, with SDL_RenderPresent() as the old SDL_Flip() function.*/

  SDL_DestroyTexture(Font_Tx);
  SDL_DestroyRenderer(Main_Renderer);
  SDL_DestroyWindow(Main_Window);
  SDL_Quit();

  return 0;
}
