/**
 * @author mrdoob / http://mrdoob.com/
 */

THREE.PointerLockOrbit = function ( camera, target) {

	var scope = this;
	scope.target = target;
    scope.vectorUp = new THREE.Vector3(0, 1, 0);
	scope.camera = camera;
	camera.rotation.set( 0, 0, 0 );

	var pitchObject = new THREE.Object3D();
	pitchObject.add( camera );

	var yawObject = new THREE.Object3D();
	yawObject.position.y = 10;
	yawObject.add( pitchObject );

	var PI_2 = Math.PI / 2;

	var onMouseMove = function ( event ) {
		if ( scope.enabled === false ) return;

		var movementX = event.movementX || event.mozMovementX || event.webkitMovementX || 0;
		var movementY = event.movementY || event.mozMovementY || event.webkitMovementY || 0;
		console.log('movement', movementX, movementY);

		// scope.target.rotation.x -= movementX * 0.002;
		scope.target.rotateX(-movementY * 0.002);
        scope.target.rotateY(-movementX * 0.002);
        // scope.target.rotation.y -= movementY * 0.002;

		var relativeCameraOffset = new THREE.Vector3(0,50,200);
        var cameraOffset = relativeCameraOffset.applyMatrix4( scope.target.matrixWorld );
        scope.camera.position.x = cameraOffset.x;
        scope.camera.position.y = cameraOffset.y;
        scope.camera.position.z = cameraOffset.z;
        scope.camera.lookAt( scope.target.position );
	};

	this.moveForward = function(distance, direction) {
    	this.target.position.add(direction.normalize().multiplyScalar(distance));
        this.camera.position.add(direction.normalize().multiplyScalar(distance));
    };
    this.moveBackward = function(distance, direction) {
        this.target.position.add((direction.normalize().multiplyScalar(-distance)));
        this.camera.position.add((direction.normalize().multiplyScalar(distance)));
    };
    this.moveLeft = function(distance, direction) {
        this.target.position.add(new THREE.Vector3().crossVectors(this.vectorUp, direction).normalize().multiplyScalar(distance));
        this.camera.position.add(new THREE.Vector3().crossVectors(vectorUp, direction).normalize().multiplyScalar(distance));
    };
    this.moveRight = function(distance, direction) {
        this.target.position.add(new THREE.Vector3().crossVectors(direction, this.vectorUp).normalize().multiplyScalar(distance));
        this.camera.position.add(new THREE.Vector3().crossVectors(direction, vectorUp).normalize().multiplyScalar(distance));
    };

	this.dispose = function() {

		document.removeEventListener( 'mousemove', onMouseMove, false );

	};

	document.addEventListener( 'mousemove', onMouseMove, false );

	this.enabled = false;
    this.target = null;

	this.getObject = function () {

		return yawObject;

	};

	this.getDirection = function() {

		// assumes the camera itself is not rotated

		var direction = new THREE.Vector3( 0, 0, - 1 );
		var rotation = new THREE.Euler( 0, 0, 0, "YXZ" );

		return function( v ) {

			rotation.set( pitchObject.rotation.x, yawObject.rotation.y, 0 );

			v.copy( direction ).applyEuler( rotation );

			return v;

		};

	}();

};
