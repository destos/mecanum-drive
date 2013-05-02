# http://david.blob.core.windows.net/html5/touchjoystick/Touches.html
# http://seb.ly/2011/04/multi-touch-game-controller-in-javascripthtml5-for-ipad/
# https://github.com/sebleedelisle/JSTouchController/blob/master/TouchControl.html
# http://handjs.codeplex.com/documentation

# shim layer with setTimeout fallback
window.requestAnimFrame = ( ->
    return window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    (callback) ->
        window.setTimeout(callback, 1000 / 60)
)()



class Collection
    constructor: ->
        @count = 0
        @collection = {}

    add: (key, item) ->
        return undefined unless @collection[key] is undefined
        @collection[key] = item
        ++@count

    remove: (key) ->
        return undefined if @collection[key] is undefined
        delete @collection[key]
        --@count

    item: (key) ->
        @collection[key]

    forEach: (block) ->
        for key of @collection
            block @collection[key] if @collection.hasOwnProperty(key)


class Joystick
    maxDistance: 60
    nubSize: 30
    constructor: (e, @canvas, @startPos, @touchPos) ->
        _.bindAll @
        @vector = new Vector2
        if not @canvas
            throw new Error 'Joystick missing canvas element'
        if not @startPos
            throw new Error 'Joystick missing start position'
        if _.isArray @startPos
            if @startPos.length isnt 2
                throw new Error 'Joystick has incorrect starting position array length'
            @startPos = new Vector2(@startPos[0], @startPos[1])

        @id = e.identifier
        if not @touchPos and @startPos
            @touchPos = new Vector2()
            @touchPos.copyFrom(@startPos)

    updateTouchPos: (x, y) ->
        @touchPos.reset(x, y)
    
    # TODO: need to get the distance and angle and calculate the new point the joystick should reside at. ( doesn't move past limit)
    
    # retuns power and direction in radians
    getDriveFactor: ->
        @vector.copyFrom(@touchPos)
        @vector.minusEq(@startPos)
        dist = @startPos.dist(@touchPos)
        # angle = @vector.angle() + 180
        # radians = @vector.angle(true)
        power = (if dist < @maxDistance then dist else @maxDistance) / @maxDistance
        # 
        # y = Math.sin(radians) * power
        # x = Math.cos(radians) * power
        # factors = new Vector2(x,y).reverse().toArray()
        
        # console.log factors
        # return factors
        [power.toFixed(2), @vector.angle(true).toFixed(3)]

    draw: ->
        # TODO: make sure we don't move beyond our distance
        @canvas.beginPath()
        @canvas.strokeStyle = "cyan"
        @canvas.lineWidth = 6
        @canvas.arc(@startPos.x, @startPos.y, @nubSize,0,Math.PI*2,true)
        @canvas.stroke()
        
        @canvas.beginPath()
        @canvas.strokeStyle = "cyan"
        @canvas.lineWidth = 2
        @canvas.arc(@startPos.x, @startPos.y, @maxDistance,0,Math.PI*2,true)
        @canvas.stroke()
        
        # joystick nub
        @canvas.beginPath()
        @canvas.strokeStyle = "cyan"
        @canvas.arc(@touchPos.x, @touchPos.y, @nubSize, 0,Math.PI*2, true)
        @canvas.stroke() 
        
        
# no sliding in iOS
document.ontouchmove = (e) ->
    e.preventDefault()

# socket stuff
WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf"
WEB_SOCKET_DEBUG = true

class ControlCanvas

    leftIdentifier: null

    rightIdentifier: null

    prevPositions: [[0,0],[0,0]]
    
    sent: 0
    
    constructor: ->
        _.bindAll @

        canvas = @setupCanvas()
        @joysticks = new Collection()
        @canvas.addEventListener "pointerdown", @onJoystickDown, false
        @canvas.addEventListener "pointermove", @onJoystickMove, false
        @canvas.addEventListener "pointerup", @onJoystickUp, false
        @canvas.addEventListener "pointerout", @onJoystickUp, false

        # start loop
        requestAnimFrame @draw

        window.onorientationchange = @resetCanvas
        window.onresize = @resetCanvas

        @socket = io.connect('/joysticks')

        indicator = document.getElementById('connection')
        @socket.on 'connect', ->
            indicator.className = 'on'
            console.log 'connected'
        .on 'disconnect', ->
            indicator.className = 'off'
            console.log 'disconnected'

    setupCanvas: ->
        @canvas = document.getElementById("joysticks")
        @c2d = @canvas.getContext("2d")
        @canvas.width = window.innerWidth
        @canvas.height = window.innerHeight
        @midpoint = @canvas.width / 2
        @c2d.strokeStyle = "#ffffff"
        @c2d.lineWidth = 2
        return @canvas
         
    resetCanvas: (e) ->
        # resize the canvas - but remember - this clears the canvas too.
        @canvas.width = window.innerWidth
        @canvas.height = window.innerHeight
        @midpoint = @canvas.width / 2

        #make sure we scroll to the top left.
        window.scrollTo 0, 0

    emitTrottle: _.throttle ->
        if @joysticks.count or not _.isEqual(@prevPositions, [[0,0],[0,0]])
            left = if leftjs = @joysticks.item(@leftIdentifier) then leftjs.getDriveFactor() else [0,0]
            right = if rightjs = @joysticks.item(@rightIdentifier) then rightjs.getDriveFactor() else [0,0]
            positons = [left, right]
            if not _.isEqual(@prevPositions, positons)
                @prevPositions = positons
                @socket.emit('update', positons)
    , 30
    
    draw: ->
        @c2d.clearRect 0, 0, @canvas.width, @canvas.height
        @joysticks.forEach (joystick) =>
            joystick.draw()
            # joystick.getDriveFactor()
        @emitTrottle()
        requestAnimFrame @draw

    onJoystickDown: (e) ->
        try
            if e.clientX < @midpoint and not @leftIdentifier
                @leftIdentifier = e.pointerId
            else if e.clientX > @midpoint and not @rightIdentifier
                @rightIdentifier = e.pointerId
            else
                throw ''
            @joysticks.add e.pointerId, new Joystick(e, @c2d, [e.clientX, e.clientY])
        catch error

    onJoystickMove: (e) ->
        if js = @joysticks.item(e.pointerId)
            js.updateTouchPos(e.clientX, e.clientY)

    onJoystickUp: (e) ->
        @joysticks.remove e.pointerId
        @rightIdentifier = null if @rightIdentifier is e.pointerId
        @leftIdentifier = null if @leftIdentifier is e.pointerId


document.addEventListener "DOMContentLoaded", ->
    new ControlCanvas()


class Vector2
    constructor: (@x = 0, @y = 0) ->

    reset: (x, y) ->
        @x = x
        @y = y
        @

    toString: (decPlaces) ->
        decPlaces = decPlaces or 3
        scalar = Math.pow(10, decPlaces)
        "[" + Math.round(@x * scalar) / scalar + ", " + Math.round(@y * scalar) / scalar + "]"
    
    toArray: ->
        [@x, @y]

    clone: ->
        new Vector2(@x, @y)

    copyTo: (v) ->
        v.x = @x
        v.y = @y

    copyFrom: (v) ->
        @x = v.x
        @y = v.y

    magnitude: ->
        Math.sqrt (@x * @x) + (@y * @y)

    magnitudeSquared: ->
        (@x * @x) + (@y * @y)

    normalise: ->
        m = @magnitude()
        @x = @x / m
        @y = @y / m
        @

    reverse: ->
        @x = -@x
        @y = -@y
        @

    plusEq: (v) ->
        @x += v.x
        @y += v.y
        @

    plusNew: (v) ->
        new Vector2(@x + v.x, @y + v.y)

    minusEq: (v) ->
        @x -= v.x
        @y -= v.y
        @

    minusNew: (v) ->
        new Vector2(@x - v.x, @y - v.y)

    multiplyEq: (scalar) ->
        @x *= scalar
        @y *= scalar
        @

    multiplyNew: (scalar) ->
        returnvec = @clone()
        returnvec.multiplyEq scalar

    divideEq: (scalar) ->
        @x /= scalar
        @y /= scalar
        @

    divideNew: (scalar) ->
        returnvec = @clone()
        returnvec.divideEq scalar

    dot: (v) ->
        (@x * v.x) + (@y * v.y)

    dist: (v)->
        Math.sqrt(Math.pow((@x - v.x),2) + Math.pow((@y - v.y),2))

    angle: (useRadians) ->
        Math.atan2(@y, @x) * ((if useRadians then 1 else Vector2Const.TO_DEGREES))

    rotate: (angle, useRadians) ->
        cosRY = Math.cos(angle * ((if useRadians then 1 else Vector2Const.TO_RADIANS)))
        sinRY = Math.sin(angle * ((if useRadians then 1 else Vector2Const.TO_RADIANS)))
        Vector2Const.temp.copyFrom @
        @x = (Vector2Const.temp.x * cosRY) - (Vector2Const.temp.y * sinRY)
        @y = (Vector2Const.temp.x * sinRY) + (Vector2Const.temp.y * cosRY)
        @

    equals: (v) ->
        (@x is v.x) and (@y is v.x)

    isCloseTo: (v, tolerance) ->
        return true    if @equals(v)
        Vector2Const.temp.copyFrom @
        Vector2Const.temp.minusEq v
        Vector2Const.temp.magnitudeSquared() < tolerance * tolerance

    rotateAroundPoint: (point, angle, useRadians) ->
        Vector2Const.temp.copyFrom @
    
        #trace("rotate around point "+t+" "+point+" " +angle)
        Vector2Const.temp.minusEq point
    
        #trace("after subtract "+t)
        Vector2Const.temp.rotate angle, useRadians
    
        #trace("after rotate "+t)
        Vector2Const.temp.plusEq point
    
        #trace("after add "+t)
        @copyFrom Vector2Const.temp

    isMagLessThan: (distance) ->
        @magnitudeSquared() < distance * distance

    isMagGreaterThan: (distance) ->
        @magnitudeSquared() > distance * distance


# still AS3 to convert : 
# public function projectOnto(v:Vector2) : Vector2
# {
# 		var dp:Number = dot(v)
# 
# 		var f:Number = dp / ( v.x*v.x + v.y*v.y )
# 
# 		return new Vector2( f*v.x , f*v.y)
# 	}
# 
# 
# public function convertToNormal():void
# {
# 	var tempx:Number = x 
# 	x = -y 
# 	y = tempx 
# 	
# 	
# }		
# public function getNormal():Vector2
# {
# 	
# 	return new Vector2(-y,x) 
# 	
# }
# 
# 
# 
# public function getClosestPointOnLine ( vectorposition : Point, targetpoint : Point ) : Point
# {
# 	var m1 : Number = y / x 
# 	var m2 : Number = x / -y 
# 	
# 	var b1 : Number = vectorposition.y - ( m1 * vectorposition.x ) 
# 	var b2 : Number = targetpoint.y - ( m2 * targetpoint.x ) 
# 	
# 	var cx : Number = ( b2 - b1 ) / ( m1 - m2 ) 
# 	var cy : Number = m1 * cx + b1 
# 	
# 	return new Point ( cx, cy ) 
# }
# 
Vector2Const =
    TO_DEGREES: 180 / Math.PI
    TO_RADIANS: Math.PI / 180
    temp: new Vector2()