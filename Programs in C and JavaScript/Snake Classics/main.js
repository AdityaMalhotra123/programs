
var STATES =
{
	WELCOME:1, GAME:2, END:3
}


var GameManager = {

	canvas:null,
	ctx:null,
	frameRate:60,
	frameDelay:0,
	LEFT:0, TOP:1, RIGHT: 2, DOWN:3,
	Score:0,
	frames: 0,
	KEY_LEFT: 37, KEY_TOP: 38, KEY_RIGHT:39, KEY_DOWN: 40,
	rows:0,
	cols:0,
	state:null,

	Init: function()
	{
		this.canvas = document.getElementById("myCanvas");
		this.ctx = this.canvas.getContext('2d');
		this.frameDelay = 1000/this.frameRate;
		this.cols = this.canvas.width/20;
		this.rows = this.canvas.height/20;
		this.state = STATES.WELCOME;
		WelcomeState.Init();
		GameState.Init();

		document.addEventListener("click", GameManager.mouseDownHandler, false);
		document.addEventListener("keydown", GameManager.keyDownHandler, false);
	},

	Update: function()
	{
		switch(this.state)
		{
			case STATES.WELCOME:
			WelcomeState.Update();
			break;
			case STATES.GAME:
			GameState.Update();
			break;

			case STATES.END:
			break;
		}

	},

	mouseDownHandler:function(e)
	{
		if(GameManager.BtnClicked(WelcomeState.playbtn, e))
		{
			GameManager.state = STATES.GAME;
		}

	},

	BtnClicked:function(btn,mouse)
	{
var relativeX = mouse.clientX - this.canvas.offsetLeft;
var relativeY = mouse.clientY - this.canvas.offsetTop;

if (relativeX > btn.x && relativeX < btn.x + btn.width && relativeY > btn.y && relativeY < btn.y + btn.height)
	{
		return true;
	}

	return false;
	},

	keyDownHandler: function(e)
	{
       if(e.keyCode == GameManager.KEY_TOP &&
	   GameState.snake.direction != GameManager.DOWN)
       {
       	GameState.snake.direction = GameManager.TOP;
       }

        if(e.keyCode == GameManager.KEY_DOWN &&
	    GameState.snake.direction != GameManager.TOP)

       {
       	GameState.snake.direction = GameManager.DOWN;
       }

       if(e.keyCode == GameManager.KEY_LEFT &&
	    GameState.snake.direction != GameManager.RIGHT)

       {
       	GameState.snake.direction = GameManager.LEFT;
       }

       if(e.keyCode == GameManager.KEY_RIGHT &&
	    GameState.snake.direction != GameManager.LEFT)

       {
       	GameState.snake.direction = GameManager.RIGHT;
       }
	}

}


function Snake()
{
	this.body = [];
	this.direction = null;
	this.bodyImg = null;
	this.headImg = null;
	this.Init = function()

	{
		this.direction = GameManager.RIGHT;
		this.bodyImg = new Image();
		this.bodyImg.src = "images/body.png";
		this.headImg = new Image();
		this.headlist = ["head0.png", "head90.png", "head180.png"," head270.png"];



		this.body = [
		{x:40, y:40},
		{x:60, y:40},
		{x:80, y:40}
		];
	}

	this.add = function()
	{
		var tail = this.body[this.body.length-1];

		switch(this.direction)
		{
		case GameManager.LEFT:
		this.body.push({x:tail.x-20, y:tail.y})
		this.headImg.src = "images/head0.png";
		break;
		case GameManager.TOP:
		this.body.push({x:tail.x, y: tail.y - 20})
		this.headImg.src = "images/head90.png";
		break;
		case GameManager.RIGHT:
		this.body.push({x:tail.x + 20, y:tail.y})
		this.headImg.src = "images/head180.png";
		break;
		case GameManager.DOWN:
		this.body.push({x:tail.x, y:tail.y + 20})
		this.headImg.src = "images/head270.png";
		break;
	}
}


this.Update = function()
{
	GameManager.frames ++;
	if(GameManager.frames % 10 == 0)
{
	this.body.shift();
	this.add();
}
for (var i = 0; i < this.body.length; i++)
{
var b = this.body[i];
if(i == this.body.length - 1)
{
	GameManager.ctx.drawImage(this.headImg, b.x, b.y, 20, 20);
}
else
{
	GameManager.ctx.drawImage(this.bodyImg, b.x, b.y, 20, 20);

}

}

}
}


var GameState =
{
	snake: null,
	food:null,
	ground:null,

	Init:function()
	{
		this.snake = new Snake();
		this.food = new Food();
		this.snake.Init()
		this.food.Init();

		this.food.getRandomPos();
		this.ground = new Image();
		this.ground.src = "images/ground.jpg";

		GameManager.Score = 0;

	},

	Update: function()
	{
		GameManager.ctx.clearRect(0,0, GameManager.canvas.width, GameManager.canvas.height);
		GameManager.ctx.drawImage(this.ground, 0, 0, GameManager.canvas.width, GameManager.canvas.height)

		this.snake.Update();
		this.food.Update();


		var b = this.snake.body[this.snake.body.length - 1];

		if(b.x/20 == this.food.x && b.y/20 == this.food.y)
		{
			this.food.getRandomPos();
			this.snake.add();

			GameManager.Score += 1;
		}

		if(b.x < 0 || b.x > GameManager.canvas.width || b.y < 0
			|| b.y > GameManager.canvas.height)

		{
			return this.Init();
		}
for(var i = 0; i < this.snake.body.length; i++)
{
	var head = this.snake.body[this.snake.body.length - 1];
	if(i < this.snake.body.length - 1)
	{
		var b = this.snake.body[i];

		if(b.x == head.x && b.y == head.y)
		{
			return this.Init();
		}

	}
}




		GameManager.ctx.font = "bolder 18px Arial";
		GameManager.ctx.fillStyle = "#000";
		GameManager.ctx.fillText("SCORE: "+GameManager.Score, 10, 30);
	}
}


function Food()
{
	this.x = null;
	this.y = null;
	this.fruitlist = [];
	this.fruit = null;

	this.Init = function()
	{
		this.fruitlist = ["kiwi.png", "lychee.png", "pear.png", "pompgranate.png"];
	}

	this.getRandomPos = function()
	{


		this.x = Math.floor(Math.random() * GameManager.cols);
		this.y = Math.floor(Math.random() * GameManager.rows);

		this.fruit = new Image();
		this.fruit.src = "images/" + this.fruitlist[Math.floor(Math.random() * this.fruitlist.length)];




		console.log("cols" + this.x);
		console.log("rows" + this.y);
	}

	this.Update = function()
	{
		GameManager.ctx.drawImage(this.fruit, this.x * 20, this.y * 20, 20, 20);
	}


}

var WelcomeState =
{
	background: null,
	playbtn: null,

	Init:function()
	{
		this.background = new Image();
		this.background.src = "images/snakeTitle.jpg"
		this.playbtn = new Button(GameManager.canvas.width/2-60, GameManager.canvas.height/2-20,
		"Play", 120, 30, "#00ff00", "16px Times New Roman", "#000", -15, 0);

	},



	Update:function()
	{
		GameManager.ctx.drawImage(this.background,0,0, GameManager.canvas.width, GameManager.canvas.height);
		this.playbtn.draw();

	}



}

function Init()
{
	GameManager.Init();
}

function Update()
{
 	GameManager.Update();
}

function Button(posx, posy, text, width, height, textcolor, font, buttoncolor, offsetX, offsetY)

{
	this.x = posx;
	this.y = posy;
	this.text = text;
	this.width = width;
	this.height = height;
	this.textcolor = textcolor;
	this.font = font;
	this.buttoncolor = buttoncolor;

	this.draw = function()
	{
		GameManager.ctx.beginPath();
		GameManager.ctx.rect(this.x, this.y, this.width, this.height);
		GameManager.ctx.fillStyle = this.buttoncolor;
		GameManager.ctx.fill();
		GameManager.ctx.closePath();

		GameManager.ctx.font = this.font;
		GameManager.ctx.fillStyle = this.textcolor;
		GameManager.ctx.fillText(this.text, (this.x+this.width/2) - (this.width/this.text.length)-offsetX, this.y+this.height/2+this.text.length-offsetY);

	}

}

Init()

setInterval(function(){Update();}, GameManager.frameDelay);
