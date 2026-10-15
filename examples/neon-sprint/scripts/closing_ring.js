// Closing ring: dots gather in a circle around the player, then close in. One gap faces away from the
// centre of the screen, so there is always a way out. Written for the Neon Sprint example.
meta = {
  name: 'Closing ring',
  description: 'A ring of dots locks onto the player and closes in, leaving one gap.',
  category: 'Projectiles',
  length: 4,
  params: {
    dots: { type: 'int', label: 'Dots', default: 18, min: 6, max: 48 },
    radius: { type: 'number', label: 'Start radius', default: 320, min: 100, max: 800 },
    gap: { type: 'int', label: 'Gap (dots)', default: 3, min: 1, max: 12 },
    warnBeats: { type: 'beats', label: 'Warning', default: 1, min: 0.25, max: 4, step: 0.25 },
    closeBeats: { type: 'beats', label: 'Close in over', default: 2, min: 0.5, max: 8, step: 0.25 },
    size: { type: 'number', label: 'Dot size', default: 22, min: 6, max: 80 },
  },
};

function start(p) {
  // Lock onto where the player is when it appears.
  var t = nearestPlayer(this.x, this.y);
  this.cx = t ? t.x : this.x;
  this.cy = t ? t.y : this.y;
  // The gap points away from the screen centre: the safe side.
  this.gapAngle = angleTo(0, 0, this.cx, this.cy);
  if (this.cx === 0 && this.cy === 0) this.gapAngle = random(0, 360);
  this.spin = chance(0.5) ? 40 : -40;
}

function draw() {
  var warn = this.warnBeats * beatMs, close = this.closeBeats * beatMs;
  var r = this.radius, warning = this.age < warn;
  if (!warning) r = lerp(this.radius, 0, ease('inQuad', clamp((this.age - warn) / close, 0, 1)));
  if (r <= 4) return;
  var turn = this.spin * this.age / 1000;
  for (var i = 0; i < this.dots; i++) {
    var a = this.gapAngle + turn + (i + this.gap / 2 + 0.5) * 360 / (this.dots + this.gap);
    var v = vec(a, r);
    var s = warning ? this.size * ease('outBack', this.age / warn) : this.size;
    circle(this.cx + v.x, this.cy + v.y, s, { warning: warning });
  }
}
