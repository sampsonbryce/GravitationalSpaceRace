/*
    Player object for controlling where other players are
*/

var Player = function(name, mesh){
    console.log('Player created');
    if(mesh === undefined){
       this.mesh = new THREE.Mesh(new THREE.SphereGeometry(50, 16, 16),new THREE.MeshLambertMaterial({
        color: 0xCC0000}));
    }else{
        this.mesh = mesh;
    }
    this.name = name;
    this.vectorUp = new THREE.Vector3(0, 1, 0);
    return this;
};

Player.prototype.updatePosition = function(position) {
    console.log('in update position', position.x, position.y, position.z);
    this.mesh.position.x = position.x;
    this.mesh.position.y = position.y;
    this.mesh.position.z = position.z;
};

Player.prototype.moveForward = function(distance, direction) {
    this.mesh.position.add(direction.normalize().multiplyScalar(distance));
};
Player.prototype.moveBackward = function(distance, direction) {
    this.mesh.position.add((direction.normalize().multiplyScalar(-distance)));
};
Player.prototype.moveLeft = function(distance, direction) {
    this.mesh.position.add(new THREE.Vector3().crossVectors(this.vectorUp, direction).normalize().multiplyScalar(distance));
    // camera.position.add(new THREE.Vector3().crossVectors(vectorUp, direction).normalize().multiplyScalar(distance));
};
Player.prototype.moveRight = function(distance, direction) {
    this.mesh.position.add(new THREE.Vector3().crossVectors(direction, this.vectorUp).normalize().multiplyScalar(distance));
    // camera.position.add(new THREE.Vector3().crossVectors(direction, vectorUp).normalize().multiplyScalar(moveDistance));
};
