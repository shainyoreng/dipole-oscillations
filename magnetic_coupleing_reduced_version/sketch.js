let theta1, theta2, omega1, omega2;  // angular positions and velocities

let I = 2;                           // mass of the pendulum
let m = 1e-3;                           // Dipole moment
let D = 8e-3;                           // Distance between pendulums
let Dt = 0.02*Math.sqrt(D*D*D)*Math.sqrt(I)/m; //time diffrecial


let T = 0; //total time
let omega0bar = 0.3; //theta1 initial speed, without units.
// omega1 = omega0bar*m/(sqrt(I)*Math.sqrt(D*D*D))

let period_bar = 4*Math.PI/(Math.sqrt(11/8)+Math.sqrt(7/8));

let Period = period_bar*Math.sqrt(D*D*D)*Math.sqrt(I)/m;


let Yfactor=400;
let Xfactor=4;

let Scale=20000;


function estimate(t){
  let freq = TWO_PI/Period;
  let freqFactor = (sqrt(11)+sqrt(7))/(sqrt(11)-sqrt(7));
  return omega0bar*m/(sqrt(I)*Math.sqrt(D*D*D))*Math.sin(freq*t)*(Math.cos(freq*t/freqFactor))/freq;
}

function estimate2(t){
  let freq1 = sqrt(7/8)*m/(Math.sqrt(D*D*D)*Math.sqrt(I));
  let freq2 = sqrt(11/8)*m/(Math.sqrt(D*D*D)*Math.sqrt(I));
  return omega0bar*m/(sqrt(I)*Math.sqrt(D*D*D))/2 *(Math.sin(freq1*t)/freq1+Math.sin(freq2*t)/freq2);
}


function setup() {
  createCanvas(900, 700);
  theta1 = 0;   // initial angle for pendulum 1
  theta2 = 0;   // initial angle for pendulum 2
  omega1 = omega0bar*m/(sqrt(I)*Math.sqrt(D*D*D));        // initial angular velocity for pendulum 1
  omega2 = 0;        // initial angular velocity for pendulum 2
  
  
  fill(127);

  background(255);
  stroke(0);
  rect(-width/2,0,width,height/2);
  
  for (let i = 1; i<100;i++){
      line(i*Period/(2*Xfactor*Dt),height/2,i*Period/(2*Xfactor*Dt),height);

  }
  
  for (let t = 0; t<width*Dt*Xfactor;t+=Dt){
      point(t/(Xfactor*Dt),5*height/6- Yfactor*estimate2(t));
  }

}

function draw() {

  
  translate(width/2,height/3);
  noStroke();
  fill(255);
  rect(-width/2,-height/2,width,height/2);

  // Calculate angular accelerations based on the equations of motion
  let alpha1 = calculateAcceleration1(theta1, theta2, omega1, omega2);
  let alpha2 = calculateAcceleration2(theta1, theta2, omega1, omega2);

  // Update velocities using Euler's method
  omega1 += alpha1 * Dt;  // Dt = 0.01
  omega2 += alpha2 * Dt;

  // Update positions (angles)
  theta1 += omega1 * Dt;
  theta2 += omega2 * Dt;
  
  T += Dt;
  
  fill(117);

  stroke(0);
  rect(-width/2,0,width,height/5);

  
  // Draw the pendulums
  strokeWeight(2);
  
  ellipse(0,0, 20, 20);

  fill(color(220,20,30));
  ellipse(D * Scale, 0, 20, 20);
  
  fill(color(20,210,30));
  ellipse(-D * Scale, 0, 20, 20);
  
  stroke(color(20,20,170));
  
  // Draw moments
  line( D * Scale+sin(theta1)*100, -cos(theta1)*100, D * Scale, 0);
  line( -D * Scale-sin(theta2)*100, -cos(theta2)*100, -D * Scale, 0);
  line(0, 0, 0, -100);
  
  stroke(0);
  line(-width/2,height/2,width/2,height/2);
  
  // Draw data points
  
  stroke(color(220,20,30))
  point(T/(Xfactor*Dt)-width/2,height/2- Yfactor*theta1);
  stroke(color(20,210,30));
  point(T/(Xfactor*Dt)-width/2,height/2- Yfactor*theta2);
  
  strokeWeight(1);
  stroke(color(90,90,150));

  //line(-width/2,height/2-Yfactor*3*omega0bar/PI,width/2,height/2-Yfactor*3*omega0bar/PI);



}

// Function to calculate angular acceleration for pendulum 1
function calculateAcceleration1(theta1, theta2, omega1, omega2) {
  return -(1 / I) * ( (m * m / (8 * D * D * D)) * (8 * sin(theta1) + 2 * cos(theta1) * sin(theta2) + sin(theta1) * cos(theta2))  );
}

// Function to calculate angular acceleration for pendulum 2
function calculateAcceleration2(theta1, theta2, omega1, omega2) {
  return -(1 / I) * ( (m * m / (8 * D * D * D)) * (8 * sin(theta2) + 2 * sin(theta1) * cos(theta2) + cos(theta1) * sin(theta2)) );
}
