import bge
from mathutils import Vector, Euler, Matrix
from operator import attrgetter
import datetime

scene = bge.logic.getCurrentScene()
obj = bge.logic.getCurrentController().owner

def deactivateSlide( s ):
    if 'pos' not in s:
        s['position'] = Vector( ( 0,0,0 ) )
        s['position_target'] = Vector( ( 0,0,0 ) )
        s['orientation'] = Vector( ( 0,0,0 ) )
        s['orientation_target'] = Vector( ( 0,0,0 ) )
    if 'video_path' in s:
        s['play'] = False

def activateSlide( s ):
    if 'video_path' in s:
        s['play'] = True

def slidePosition( obj ):
    
    for i in range( len( obj[ 'slides' ] ) ):
        s = obj[ 'slides' ][ i ]
        gap = abs( i - obj['current_slides'] )
        if ( i > obj['current_slides'] ):
            s['position_target'] = Vector( ( 1 + 0.1 * gap, 0, - (0.5 + 0.01 * gap) ) )
            s['orientation_target'] = Vector( ( -0.1, -( 1.3 + 0.03 * gap ) ,-0.1 ) )
        elif ( i < obj['current_slides'] ):
            s['position_target'] = Vector( ( -( 1 + 0.1 * gap ), 0, -(0.5 + 0.01 * gap) ) )
            s['orientation_target'] = Vector( ( -0.1, ( 1.3 + 0.03 * gap ) ,0.1 ) )
        else:
            s['position_target'] = Vector( ( 0, 0, 0.35 ) )
            s['orientation_target'] = Vector( ( 0, 0, 0 ) )

def nextSlide():
    deactivateSlide( obj['slides'][ obj['current_slides'] ] )
    obj['current_slides'] += 1
    if ( obj['current_slides'] >= len( obj['slides'] ) ):
        obj['current_slides'] = 0
    activateSlide( obj['slides'][ obj['current_slides'] ] )
    obj['target'] = Vector( ( obj['current_slides'] * 2, 0, obj.worldPosition.z ) )
    slidePosition( obj )
    obj['waituntil'] = obj['time'] + obj['slides'][ obj['current_slides'] ][ 'duration' ]

def previousSlide():
    deactivateSlide( obj['slides'][ obj['current_slides'] ] )
    obj['current_slides'] -= 1
    if ( obj['current_slides'] < 0 ):
        obj['current_slides'] = len( obj['slides'] ) - 1
    activateSlide( obj['slides'][ obj['current_slides'] ] )
    obj['target'] = Vector( ( obj['current_slides'] * 2, 0, obj.worldPosition.z ) )
    slidePosition( obj )
    obj['waituntil'] = obj['time'] + obj['slides'][ obj['current_slides'] ][ 'duration' ]

def goToSlide( sID ):
    if sID == obj['current_slides']:
        return
    deactivateSlide( obj['slides'][ obj['current_slides'] ] )
    obj['current_slides'] = sID
    activateSlide( obj['slides'][ obj['current_slides'] ] )
    obj['target'] = Vector( ( obj['current_slides'] * 2, 0, obj.worldPosition.z ) )
    slidePosition( obj )
    obj['waituntil'] = obj['time'] + obj['slides'][ obj['current_slides'] ][ 'duration' ]

if 'slides' not in obj:
    
    obj['slides'] = []
    
    for o in scene.objects:
        if o.name[0:6] == "slide_":
            obj['slides'].append( o )
            deactivateSlide( o )
    obj['slides'] = sorted( obj['slides'], key=attrgetter('name'))
    obj['current_slides'] = 0
    obj['keyn'] = False
    obj['keyp'] = False
    obj['target'] = Vector( ( 0, 0, obj.worldPosition.z ) )
    slidePosition( obj )
    # print( obj['slides'] )
    obj['waituntil'] = obj['slides'][ obj['current_slides'] ][ 'duration' ]
    obj['lastmx'] = 0.5
    bge.render.setMousePosition( int( bge.render.getWindowWidth() / 2 ), int( bge.render.getWindowHeight() / 2 ) )

if obj.sensors['key_N'].positive:
    if not obj['keyn']:
        nextSlide()
        obj['keyn'] = True
else:
    obj['keyn'] = False
    
if obj.sensors['key_P'].positive:
    if not obj['keyp']:
        previousSlide()
        obj['keyp'] = True
else:
    obj['keyp'] = False

if obj['lastmx'] != bge.logic.mouse.position[ 0 ]:
    sID = int( len( obj['slides'] ) * bge.logic.mouse.position[ 0 ] )
    if sID < 0:
        sID = 0
    elif sID >= len( obj['slides'] ):
        sID = len( obj['slides'] ) - 1
    goToSlide( sID )
    obj['lastmx'] = bge.logic.mouse.position[ 0 ]

if obj['time'] > obj['waituntil']:
    nextSlide()

for s in obj['slides']:
    s['position'] = Vector( ( 
                 s['position'].x + ( s['position_target'].x - s['position'].x ) * 0.1,
                 s['position'].y + ( s['position_target'].y - s['position'].y ) * 0.1,
                 s['position'].z + ( s['position_target'].z - s['position'].z ) * 0.1
                 ) )
    s.worldPosition = s['position']
    s['orientation'] = Vector( ( 
                 s['orientation'].x + ( s['orientation_target'].x - s['orientation'].x ) * 0.1,
                 s['orientation'].y + ( s['orientation_target'].y - s['orientation'].y ) * 0.1,
                 s['orientation'].z + ( s['orientation_target'].z - s['orientation'].z ) * 0.1
                 ) )
    s.worldOrientation = Euler( ( s['orientation'].x, s['orientation'].y, s['orientation'].z ), 'XYZ' ).to_matrix()

'''
obj.worldPosition = Vector( (
                             obj.worldPosition.x + ( obj['target'].x - obj.worldPosition.x ) * 0.1,
                             obj.worldPosition.y + ( obj['target'].y - obj.worldPosition.y ) * 0.1,
                             obj.worldPosition.z + ( obj['target'].z - obj.worldPosition.z ) * 0.1
                             ) )
'''