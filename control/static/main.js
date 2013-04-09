// Generated by CoffeeScript 1.3.3
var Collection, ControlCanvas, Joystick, Vector2, Vector2Const, WEB_SOCKET_DEBUG, WEB_SOCKET_SWF_LOCATION;

window.requestAnimFrame = (function() {
  return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || function(callback) {
    return window.setTimeout(callback, 1000 / 60);
  };
})();

Collection = (function() {

  function Collection() {
    this.count = 0;
    this.collection = {};
  }

  Collection.prototype.add = function(key, item) {
    if (this.collection[key] !== void 0) {
      return void 0;
    }
    this.collection[key] = item;
    return ++this.count;
  };

  Collection.prototype.remove = function(key) {
    if (this.collection[key] === void 0) {
      return void 0;
    }
    delete this.collection[key];
    return --this.count;
  };

  Collection.prototype.item = function(key) {
    return this.collection[key];
  };

  Collection.prototype.forEach = function(block) {
    var key, _results;
    _results = [];
    for (key in this.collection) {
      if (this.collection.hasOwnProperty(key)) {
        _results.push(block(this.collection[key]));
      } else {
        _results.push(void 0);
      }
    }
    return _results;
  };

  return Collection;

})();

Joystick = (function() {

  Joystick.prototype.maxDistance = 60;

  Joystick.prototype.nubSize = 30;

  function Joystick(e, canvas, startPos, touchPos) {
    this.canvas = canvas;
    this.startPos = startPos;
    this.touchPos = touchPos;
    _.bindAll(this);
    this.vector = new Vector2;
    if (!this.canvas) {
      throw new Error('Joystick missing canvas element');
    }
    if (!this.startPos) {
      throw new Error('Joystick missing start position');
    }
    if (_.isArray(this.startPos)) {
      if (this.startPos.length !== 2) {
        throw new Error('Joystick has incorrect starting position array length');
      }
      this.startPos = new Vector2(this.startPos[0], this.startPos[1]);
    }
    this.id = e.identifier;
    if (!this.touchPos && this.startPos) {
      this.touchPos = new Vector2();
      this.touchPos.copyFrom(this.startPos);
    }
  }

  Joystick.prototype.updateTouchPos = function(x, y) {
    return this.touchPos.reset(x, y);
  };

  Joystick.prototype.getDriveFactor = function() {
    var dist, power;
    this.vector.copyFrom(this.touchPos);
    this.vector.minusEq(this.startPos);
    dist = this.startPos.dist(this.touchPos);
    power = (dist < this.maxDistance ? dist : this.maxDistance) / this.maxDistance;
    return [power.toFixed(2), this.vector.angle(true).toFixed(3)];
  };

  Joystick.prototype.draw = function() {
    this.canvas.beginPath();
    this.canvas.strokeStyle = "cyan";
    this.canvas.lineWidth = 6;
    this.canvas.arc(this.startPos.x, this.startPos.y, this.nubSize, 0, Math.PI * 2, true);
    this.canvas.stroke();
    this.canvas.beginPath();
    this.canvas.strokeStyle = "cyan";
    this.canvas.lineWidth = 2;
    this.canvas.arc(this.startPos.x, this.startPos.y, this.maxDistance, 0, Math.PI * 2, true);
    this.canvas.stroke();
    this.canvas.beginPath();
    this.canvas.strokeStyle = "cyan";
    this.canvas.arc(this.touchPos.x, this.touchPos.y, this.nubSize, 0, Math.PI * 2, true);
    return this.canvas.stroke();
  };

  return Joystick;

})();

document.ontouchmove = function(e) {
  return e.preventDefault();
};

WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";

WEB_SOCKET_DEBUG = true;

ControlCanvas = (function() {

  ControlCanvas.prototype.leftIdentifier = null;

  ControlCanvas.prototype.rightIdentifier = null;

  ControlCanvas.prototype.prevPositions = [[0, 0], [0, 0]];

  ControlCanvas.prototype.sent = 0;

  function ControlCanvas() {
    var canvas;
    _.bindAll(this);
    canvas = this.setupCanvas();
    this.joysticks = new Collection();
    this.canvas.addEventListener("pointerdown", this.onJoystickDown, false);
    this.canvas.addEventListener("pointermove", this.onJoystickMove, false);
    this.canvas.addEventListener("pointerup", this.onJoystickUp, false);
    this.canvas.addEventListener("pointerout", this.onJoystickUp, false);
    requestAnimFrame(this.draw);
    window.onorientationchange = this.resetCanvas;
    window.onresize = this.resetCanvas;
    this.socket = io.connect('/joysticks');
  }

  ControlCanvas.prototype.setupCanvas = function() {
    this.canvas = document.getElementById("joysticks");
    this.c2d = this.canvas.getContext("2d");
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.midpoint = this.canvas.width / 2;
    this.c2d.strokeStyle = "#ffffff";
    this.c2d.lineWidth = 2;
    return this.canvas;
  };

  ControlCanvas.prototype.resetCanvas = function(e) {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.midpoint = this.canvas.width / 2;
    return window.scrollTo(0, 0);
  };

  ControlCanvas.prototype.emitTrottle = _.throttle(function() {
    var left, leftjs, positons, right, rightjs;
    if (this.joysticks.count || !_.isEqual(this.prevPositions, [[0, 0], [0, 0]])) {
      left = (leftjs = this.joysticks.item(this.leftIdentifier)) ? leftjs.getDriveFactor() : [0, 0];
      right = (rightjs = this.joysticks.item(this.rightIdentifier)) ? rightjs.getDriveFactor() : [0, 0];
      positons = [left, right];
      if (!_.isEqual(this.prevPositions, positons)) {
        this.prevPositions = positons;
        return this.socket.emit('update', positons);
      }
    }
  }, 30);

  ControlCanvas.prototype.draw = function() {
    var _this = this;
    this.c2d.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.joysticks.forEach(function(joystick) {
      return joystick.draw();
    });
    this.emitTrottle();
    return requestAnimFrame(this.draw);
  };

  ControlCanvas.prototype.onJoystickDown = function(e) {
    try {
      if (e.clientX < this.midpoint && !this.leftIdentifier) {
        this.leftIdentifier = e.pointerId;
      } else if (e.clientX > this.midpoint && !this.rightIdentifier) {
        this.rightIdentifier = e.pointerId;
      } else {
        throw '';
      }
      return this.joysticks.add(e.pointerId, new Joystick(e, this.c2d, [e.clientX, e.clientY]));
    } catch (error) {

    }
  };

  ControlCanvas.prototype.onJoystickMove = function(e) {
    var js;
    if (js = this.joysticks.item(e.pointerId)) {
      return js.updateTouchPos(e.clientX, e.clientY);
    }
  };

  ControlCanvas.prototype.onJoystickUp = function(e) {
    this.joysticks.remove(e.pointerId);
    if (this.rightIdentifier === e.pointerId) {
      this.rightIdentifier = null;
    }
    if (this.leftIdentifier === e.pointerId) {
      return this.leftIdentifier = null;
    }
  };

  return ControlCanvas;

})();

document.addEventListener("DOMContentLoaded", function() {
  return new ControlCanvas();
});

Vector2 = (function() {

  function Vector2(x, y) {
    this.x = x != null ? x : 0;
    this.y = y != null ? y : 0;
  }

  Vector2.prototype.reset = function(x, y) {
    this.x = x;
    this.y = y;
    return this;
  };

  Vector2.prototype.toString = function(decPlaces) {
    var scalar;
    decPlaces = decPlaces || 3;
    scalar = Math.pow(10, decPlaces);
    return "[" + Math.round(this.x * scalar) / scalar + ", " + Math.round(this.y * scalar) / scalar + "]";
  };

  Vector2.prototype.toArray = function() {
    return [this.x, this.y];
  };

  Vector2.prototype.clone = function() {
    return new Vector2(this.x, this.y);
  };

  Vector2.prototype.copyTo = function(v) {
    v.x = this.x;
    return v.y = this.y;
  };

  Vector2.prototype.copyFrom = function(v) {
    this.x = v.x;
    return this.y = v.y;
  };

  Vector2.prototype.magnitude = function() {
    return Math.sqrt((this.x * this.x) + (this.y * this.y));
  };

  Vector2.prototype.magnitudeSquared = function() {
    return (this.x * this.x) + (this.y * this.y);
  };

  Vector2.prototype.normalise = function() {
    var m;
    m = this.magnitude();
    this.x = this.x / m;
    this.y = this.y / m;
    return this;
  };

  Vector2.prototype.reverse = function() {
    this.x = -this.x;
    this.y = -this.y;
    return this;
  };

  Vector2.prototype.plusEq = function(v) {
    this.x += v.x;
    this.y += v.y;
    return this;
  };

  Vector2.prototype.plusNew = function(v) {
    return new Vector2(this.x + v.x, this.y + v.y);
  };

  Vector2.prototype.minusEq = function(v) {
    this.x -= v.x;
    this.y -= v.y;
    return this;
  };

  Vector2.prototype.minusNew = function(v) {
    return new Vector2(this.x - v.x, this.y - v.y);
  };

  Vector2.prototype.multiplyEq = function(scalar) {
    this.x *= scalar;
    this.y *= scalar;
    return this;
  };

  Vector2.prototype.multiplyNew = function(scalar) {
    var returnvec;
    returnvec = this.clone();
    return returnvec.multiplyEq(scalar);
  };

  Vector2.prototype.divideEq = function(scalar) {
    this.x /= scalar;
    this.y /= scalar;
    return this;
  };

  Vector2.prototype.divideNew = function(scalar) {
    var returnvec;
    returnvec = this.clone();
    return returnvec.divideEq(scalar);
  };

  Vector2.prototype.dot = function(v) {
    return (this.x * v.x) + (this.y * v.y);
  };

  Vector2.prototype.dist = function(v) {
    return Math.sqrt(Math.pow(this.x - v.x, 2) + Math.pow(this.y - v.y, 2));
  };

  Vector2.prototype.angle = function(useRadians) {
    return Math.atan2(this.y, this.x) * (useRadians ? 1 : Vector2Const.TO_DEGREES);
  };

  Vector2.prototype.rotate = function(angle, useRadians) {
    var cosRY, sinRY;
    cosRY = Math.cos(angle * (useRadians ? 1 : Vector2Const.TO_RADIANS));
    sinRY = Math.sin(angle * (useRadians ? 1 : Vector2Const.TO_RADIANS));
    Vector2Const.temp.copyFrom(this);
    this.x = (Vector2Const.temp.x * cosRY) - (Vector2Const.temp.y * sinRY);
    this.y = (Vector2Const.temp.x * sinRY) + (Vector2Const.temp.y * cosRY);
    return this;
  };

  Vector2.prototype.equals = function(v) {
    return (this.x === v.x) && (this.y === v.x);
  };

  Vector2.prototype.isCloseTo = function(v, tolerance) {
    if (this.equals(v)) {
      return true;
    }
    Vector2Const.temp.copyFrom(this);
    Vector2Const.temp.minusEq(v);
    return Vector2Const.temp.magnitudeSquared() < tolerance * tolerance;
  };

  Vector2.prototype.rotateAroundPoint = function(point, angle, useRadians) {
    Vector2Const.temp.copyFrom(this);
    Vector2Const.temp.minusEq(point);
    Vector2Const.temp.rotate(angle, useRadians);
    Vector2Const.temp.plusEq(point);
    return this.copyFrom(Vector2Const.temp);
  };

  Vector2.prototype.isMagLessThan = function(distance) {
    return this.magnitudeSquared() < distance * distance;
  };

  Vector2.prototype.isMagGreaterThan = function(distance) {
    return this.magnitudeSquared() > distance * distance;
  };

  return Vector2;

})();

Vector2Const = {
  TO_DEGREES: 180 / Math.PI,
  TO_RADIANS: Math.PI / 180,
  temp: new Vector2()
};
