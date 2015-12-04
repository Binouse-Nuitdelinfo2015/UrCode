/*
The konami_code is easy to intall :
- Create a konami_code directory at the root of the site
- Put konami.js and xwing.png in this directory
- Add  this line in the head of your site :
<script src="konami_code/konami.js"></script>
- If your site doesn't use jQuery, add this line to the head of your site :
<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script>
*/

var scriptSrc = this.src.replace("konami.js", "");

// TODO Remove jQuery because I don't use it enough
// Replace it by JS

//Haut, haut, bas, bas, gauche, droite, gauche, droite, B, A
var k = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65],
n = 0;
$(document).keydown(function (e) {
    if (e.keyCode === k[n++]) {
        if (n === k.length) {
            konami();
            n = 0;
            return false;
        }
    } else {
        n = 0;
    }
});

/*
This is the function called when the konami code is done 
*/
function konami() {
	// canvas and 2D context initialization
	canvas = document.createElement("canvas");
	canvas.width = document.body.clientWidth; //document.width is obsolete
	canvas.height = document.body.clientHeight; //document.height is obsolete
	canvas.style = "position: fixed; top: 0px; left: 0px; z-index: 100;";
	document.body.appendChild(canvas);
	
	window.addEventListener("resize", function() {
		canvas.width = document.body.clientWidth; //document.width is obsolete
		canvas.height = document.body.clientHeight; //document.height is obsolete
	});
	
	context2D = canvas.getContext("2d");
	
	xwing = new XWing();
	
	document.addEventListener("click", function(evt) {
		var x = document.body.clientWidth / 2 + xwing.cursorX;
		var y = document.body.clientHeight / 2 + xwing.cursorY;
		
		createExplosion(x, y, "#525252");
		createExplosion(x, y, "#FFA318");
	});
	
	document.addEventListener("mousemove", function(evt) {
		xwing.mouseX = evt.clientX - (document.body.clientWidth / 2);
		xwing.mouseY = evt.clientY - (document.body.clientHeight / 2);
	});
	
	// starting the game loop at 60 frames per second
	var frameRate = 60.0;
	var frameDelay = 1000.0/frameRate;
	
	setInterval(function()
	{
		update(frameDelay);
		
	}, frameDelay);
}

/*
XWing constructor
*/
function XWing() {
	// The cursor is where the XWing will fire
	this.cursorX = 0, this.cursorY = 0;
	this.cursorCoef = 10; // If it is high, the cursor will be slower
	this.cursorRadius = 15; // Size of the cursor
	this.cursorColor = "#FF0000"; // Red
	this.mouseX = 0, this.mouseY = 0; // Real mouse position
	this.scale = 0.5; // Scale of the XWing compared to the source image
	this.img = document.createElement("img");
	this.img.src = scriptSrc + "xwing.png";
	
	// Function to move the cursor to the direction of the mouse
	this.moveCursor = function() {
		this.cursorX = (this.cursorX * this.cursorCoef + this.mouseX) / (this.cursorCoef + 1);
		this.cursorY = (this.cursorY * this.cursorCoef + this.mouseY) / (this.cursorCoef + 1);
	}
	
	// Function to draw the XWing and its cursor
	this.draw = function(context2D)
	{
		// Changing context2D
		context2D.save();
		context2D.translate(document.body.clientWidth / 2, document.body.clientHeight / 2);
		
		// Color the cursor
		context2D.strokeStyle = this.cursorColor;
		context2D.lineWidth = 3;
		
		// Draw the cursor
		context2D.beginPath();
		context2D.arc(this.cursorX, this.cursorY, this.cursorRadius, 0, Math.PI * 2, true);
		context2D.closePath();
		context2D.stroke();
		context2D.beginPath();
		context2D.arc(this.cursorX, this.cursorY, 1, 0, Math.PI * 2, true);
		context2D.closePath();
		context2D.stroke();
		
		// Draw the XWing
		context2D.scale(this.scale, this.scale);
		context2D.rotate(Math.PI * this.cursorX / document.body.clientWidth);
		context2D.drawImage(this.img, - this.img.width / 2, - this.img.height / 2);
		
		// Restore the saved context2D
		context2D.restore();
	};
}

var canvas;
var context2D;

var particles = [];

function randomFloat (min, max)
{
	return min + Math.random()*(max-min);
}

/*
 * A single explosion particle
 */
function Particle ()
{
	this.scale = 1.0;
	this.x = 0;
	this.y = 0;
	this.radius = 20;
	this.color = "#000";
	this.velocityX = 0;
	this.velocityY = 0;
	this.scaleSpeed = 0.5;
	
	this.update = function(ms)
	{
		// shrinking
		this.scale -= this.scaleSpeed * ms / 1000.0;
		
		if (this.scale <= 0)
		{
			this.scale = 0;
		}
		
		// moving away from explosion center
		this.x += this.velocityX * ms/1000.0;
		this.y += this.velocityY * ms/1000.0;
	};
	
	this.draw = function(context2D)
	{
		// translating the 2D context to the particle coordinates
		context2D.save();
		context2D.translate(this.x, this.y);
		context2D.scale(this.scale, this.scale);
		
		// drawing a filled circle in the particle's local space
		context2D.beginPath();
		context2D.arc(0, 0, this.radius, 0, Math.PI*2, true);
		context2D.closePath();
		
		context2D.fillStyle = this.color;
		context2D.fill();
		
		context2D.restore();
	};
}

/*
 * Basic Explosion, all particles move and shrink at the same speed.
 * 
 * Parameter : explosion center
 */
function createBasicExplosion(x, y)
{
	// creating 4 particles that scatter at 0, 90, 180 and 270 degrees
	for (var angle=0; angle<360; angle+=90)
	{
		var particle = new Particle();
		
		// particle will start at explosion center
		particle.x = x;
		particle.y = y;
		
		particle.color = "#FF0000";
		
		var speed = 50.0;
		
		// velocity is rotated by "angle"
		particle.velocityX = speed * Math.cos(angle * Math.PI / 180.0);
		particle.velocityY = speed * Math.sin(angle * Math.PI / 180.0);
		
		// adding the newly created particle to the "particles" array
		particles.push(particle);
	}
}

/*
 * Advanced Explosion effect
 * Each particle has a different size, move speed and scale speed.
 * 
 * Parameters:
 * 	x, y - explosion center
 * 	color - particles' color
 */
function createExplosion(x, y, color)
{
	var minSize = 10;
	var maxSize = 30;
	var count = 10;
	var minSpeed = 60.0;
	var maxSpeed = 200.0;
	var minScaleSpeed = 1.0;
	var maxScaleSpeed = 4.0;
	
	
	for (var angle=0; angle<360; angle += Math.round(360/count))
	{
		var particle = new Particle();
		
		particle.x = x;
		particle.y = y;
		
		particle.radius = randomFloat(minSize, maxSize);
		
		particle.color = color;
		
		particle.scaleSpeed = randomFloat(minScaleSpeed, maxScaleSpeed);
		
		var speed = randomFloat(minSpeed, maxSpeed);
		
		particle.velocityX = speed * Math.cos(angle * Math.PI / 180.0);
		particle.velocityY = speed * Math.sin(angle * Math.PI / 180.0);
		
		particles.push(particle);
	}
}

function update (frameDelay)
{
	// draw a white background to clear canvas
	//context2D.fillStyle = "rgba(0, 0, 0, 0)";
	context2D.clearRect(0, 0, context2D.canvas.width, context2D.canvas.height);
	
	// update and draw particles
	for (var i=0; i<particles.length; i++)
	{
		var particle = particles[i];
		
		particle.update(frameDelay);
		particle.draw(context2D);
	}
	
	xwing.draw(context2D);
	xwing.moveCursor();
}
